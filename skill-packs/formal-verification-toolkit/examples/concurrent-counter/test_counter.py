"""
Test suite for Concurrent Counter

These tests were generated from the counterexample found during formal verification.
They verify that the race condition is fixed.
"""

import pytest
import threading
import time
from counter_buggy import Counter as BuggyCounter
from counter_fixed import Counter as FixedCounter


class TestBuggyCounter:
    """Tests demonstrating the race condition in the buggy implementation."""

    def test_single_thread_increment(self):
        """Single-threaded increment should work correctly."""
        counter = BuggyCounter()
        counter.increment()
        assert counter.get() == 1

    def test_concurrent_increment_shows_race_condition(self):
        """
        This test demonstrates the race condition.
        With multiple threads, we expect lost updates.

        Note: This test might occasionally pass due to timing,
        but it will fail most of the time.
        """
        counter = BuggyCounter()
        num_threads = 10
        increments_per_thread = 100

        def increment_many():
            for _ in range(increments_per_thread):
                counter.increment()

        threads = [threading.Thread(target=increment_many) for _ in range(num_threads)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        expected = num_threads * increments_per_thread
        actual = counter.get()

        # We expect lost updates, so actual < expected
        print(f"Expected: {expected}, Actual: {actual}, Lost: {expected - actual}")
        # This assertion documents the bug
        assert actual < expected, "Race condition should cause lost updates"

    def test_counterexample_scenario(self):
        """
        Reproduce the exact counterexample from model checking.

        Scenario:
        - Thread 1 reads value (0)
        - Thread 2 reads value (0)
        - Thread 1 writes value (1)
        - Thread 2 writes value (1)
        - Result: value = 1 (should be 2)
        """
        counter = BuggyCounter()

        # Shared state to control thread execution order
        barrier1 = threading.Barrier(2)
        barrier2 = threading.Barrier(2)

        def thread1():
            # Read
            temp = counter.value
            barrier1.wait()  # Wait for thread2 to also read

            # Compute
            temp = temp + 1
            barrier2.wait()  # Wait for thread2 to compute

            # Write
            counter.value = temp

        def thread2():
            # Read
            temp = counter.value
            barrier1.wait()  # Both threads have read

            # Compute
            temp = temp + 1
            barrier2.wait()  # Both threads have computed

            # Write (this will overwrite thread1's write!)
            time.sleep(0.001)  # Ensure thread1 writes first
            counter.value = temp

        t1 = threading.Thread(target=thread1)
        t2 = threading.Thread(target=thread2)

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Lost update: value is 1 instead of 2
        assert counter.get() == 1, "Counterexample: lost update occurred"


class TestFixedCounter:
    """Tests verifying that the fixed implementation is thread-safe."""

    def test_single_thread_increment(self):
        """Single-threaded increment should work correctly."""
        counter = FixedCounter()
        counter.increment()
        assert counter.get() == 1

    def test_concurrent_increment_no_race_condition(self):
        """
        With the fix, concurrent increments should be safe.
        No lost updates should occur.
        """
        counter = FixedCounter()
        num_threads = 10
        increments_per_thread = 100

        def increment_many():
            for _ in range(increments_per_thread):
                counter.increment()

        threads = [threading.Thread(target=increment_many) for _ in range(num_threads)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        expected = num_threads * increments_per_thread
        actual = counter.get()

        print(f"Expected: {expected}, Actual: {actual}")
        assert actual == expected, "No lost updates should occur"

    def test_high_contention(self):
        """Test with high contention (many threads, many increments)."""
        counter = FixedCounter()
        num_threads = 50
        increments_per_thread = 1000

        def increment_many():
            for _ in range(increments_per_thread):
                counter.increment()

        threads = [threading.Thread(target=increment_many) for _ in range(num_threads)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        expected = num_threads * increments_per_thread
        assert counter.get() == expected

    def test_concurrent_read_write(self):
        """Test concurrent reads and writes."""
        counter = FixedCounter()
        num_writers = 10
        num_readers = 10
        increments_per_writer = 100

        results = []

        def writer():
            for _ in range(increments_per_writer):
                counter.increment()

        def reader():
            for _ in range(increments_per_writer):
                results.append(counter.get())

        threads = []
        threads.extend([threading.Thread(target=writer) for _ in range(num_writers)])
        threads.extend([threading.Thread(target=reader) for _ in range(num_readers)])

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        expected = num_writers * increments_per_writer
        assert counter.get() == expected

        # All reads should return valid values (0 to expected)
        for value in results:
            assert 0 <= value <= expected

    def test_reset_is_thread_safe(self):
        """Test that reset is also thread-safe."""
        counter = FixedCounter()

        def increment_and_reset():
            for _ in range(100):
                counter.increment()
                if counter.get() > 50:
                    counter.reset()

        threads = [threading.Thread(target=increment_and_reset) for _ in range(5)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should not crash or have inconsistent state
        final_value = counter.get()
        assert 0 <= final_value <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
