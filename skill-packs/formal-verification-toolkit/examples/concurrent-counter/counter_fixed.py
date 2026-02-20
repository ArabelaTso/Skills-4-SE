"""
Concurrent Counter - Fixed Version

This implementation uses a lock to ensure atomic increments.
Multiple threads can safely increment concurrently without lost updates.
"""

import threading


class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()  # Added: Lock for synchronization

    def increment(self):
        """
        Increment the counter by 1.

        FIXED: Now uses a lock to ensure atomicity.
        The entire read-modify-write sequence is protected.
        """
        with self.lock:  # Added: Acquire lock before accessing shared state
            # Read current value
            temp = self.value

            # Simulate some computation
            temp = temp + 1

            # Write new value
            self.value = temp
        # Lock automatically released here

    def get(self):
        """
        Get the current counter value.

        Note: For consistency, we also protect reads.
        """
        with self.lock:
            return self.value

    def reset(self):
        """Reset the counter to 0."""
        with self.lock:
            self.value = 0


# Example usage showing the fix works
if __name__ == "__main__":
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
    # Actual: Now always 1000!
    print(f"Expected: 1000")
    print(f"Actual: {counter.get()}")
    print(f"Lost updates: {1000 - counter.get()}")

    if counter.get() == 1000:
        print("✅ Counter is thread-safe!")
    else:
        print("❌ Still has race conditions")
