"""
Concurrent Counter - Buggy Version

This implementation has a race condition in the increment method.
Multiple threads incrementing concurrently can cause lost updates.
"""

class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        """
        Increment the counter by 1.

        BUG: This operation is not atomic!
        The read-modify-write sequence can be interleaved by other threads.
        """
        # Read current value
        temp = self.value

        # Simulate some computation
        # In real code, this could be any operation between read and write
        temp = temp + 1

        # Write new value
        # Problem: Another thread might have modified self.value in between!
        self.value = temp

    def get(self):
        """Get the current counter value."""
        return self.value

    def reset(self):
        """Reset the counter to 0."""
        self.value = 0


# Example usage showing the bug
if __name__ == "__main__":
    import threading

    counter = Counter()

    def increment_many(n):
        for _ in range(n):
            counter.increment()

    # Create 10 threads, each incrementing 100 times
    threads = []
    for _ in range(10):
        t = threading.Thread(target=increment_many, args=(100,))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Expected: 10 * 100 = 1000
    # Actual: Usually less due to race condition
    print(f"Expected: 1000")
    print(f"Actual: {counter.get()}")
    print(f"Lost updates: {1000 - counter.get()}")
