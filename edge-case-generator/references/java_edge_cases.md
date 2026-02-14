# Java Edge Cases and Testing Patterns

Java-specific edge cases, common pitfalls, and testing patterns using JUnit, TestNG, and other frameworks.

## Table of Contents

1. [Null Pointer Edge Cases](#null-pointer-edge-cases)
2. [Integer and Numeric Edge Cases](#integer-and-numeric-edge-cases)
3. [String Edge Cases](#string-edge-cases)
4. [Collection Edge Cases](#collection-edge-cases)
5. [Exception Handling](#exception-handling)
6. [Concurrency Edge Cases](#concurrency-edge-cases)
7. [Generics and Type Edge Cases](#generics-and-type-edge-cases)
8. [Testing Frameworks](#testing-frameworks)

## Null Pointer Edge Cases

### Common Null Pitfalls

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class NullEdgeCasesTest {
    @Test
    void testNullPointerExceptions() {
        String nullString = null;

        // Most common NPE source
        assertThrows(NullPointerException.class, () -> {
            int length = nullString.length();
        });

        // Method chaining with null
        assertThrows(NullPointerException.class, () -> {
            nullString.toUpperCase().trim();
        });

        // Array access with null
        String[] array = null;
        assertThrows(NullPointerException.class, () -> {
            int len = array.length;
        });
    }

    @Test
    void testNullSafeOperations() {
        String str = null;

        // Safe null check
        assertEquals(0, str == null ? 0 : str.length());

        // Objects.requireNonNull
        assertThrows(NullPointerException.class, () -> {
            Objects.requireNonNull(str, "String must not be null");
        });

        // Optional to avoid null
        Optional<String> optional = Optional.ofNullable(str);
        assertFalse(optional.isPresent());
        assertEquals("default", optional.orElse("default"));
    }

    @Test
    void testAutoboxingNullEdgeCases() {
        Integer nullInteger = null;

        // Unboxing null throws NPE!
        assertThrows(NullPointerException.class, () -> {
            int primitive = nullInteger; // Auto-unboxing NPE
        });

        // Safe unboxing
        int safe = nullInteger != null ? nullInteger : 0;
        assertEquals(0, safe);
    }
}
```

## Integer and Numeric Edge Cases

### Integer Overflow and Boundaries

```java
class IntegerEdgeCasesTest {
    @Test
    void testIntegerOverflow() {
        // Integer overflow wraps around
        assertEquals(Integer.MIN_VALUE, Integer.MAX_VALUE + 1);
        assertEquals(Integer.MAX_VALUE, Integer.MIN_VALUE - 1);

        // Silent overflow in arithmetic
        int max = Integer.MAX_VALUE;
        assertTrue(max + 1 < 0); // Wrapped to negative!

        // Safe arithmetic (Java 8+)
        assertThrows(ArithmeticException.class, () -> {
            Math.addExact(Integer.MAX_VALUE, 1);
        });

        assertThrows(ArithmeticException.class, () -> {
            Math.multiplyExact(Integer.MAX_VALUE, 2);
        });
    }

    @Test
    void testIntegerBoundaries() {
        assertEquals(2147483647, Integer.MAX_VALUE);
        assertEquals(-2147483648, Integer.MIN_VALUE);

        // Boundary arithmetic
        assertEquals(0, Integer.MAX_VALUE - Integer.MAX_VALUE);
        assertEquals(-1, Integer.MAX_VALUE - Integer.MIN_VALUE - 1);
    }

    @Test
    void testDivisionEdgeCases() {
        // Division by zero
        assertThrows(ArithmeticException.class, () -> {
            int result = 10 / 0;
        });

        // Integer division truncates
        assertEquals(3, 10 / 3);
        assertEquals(-3, -10 / 3); // Truncates toward zero

        // Modulo with negative numbers
        assertEquals(1, 10 % 3);
        assertEquals(-1, -10 % 3);
        assertEquals(1, 10 % -3);

        // Special case: MIN_VALUE / -1 overflows!
        assertEquals(Integer.MIN_VALUE, Integer.MIN_VALUE / -1); // Overflow
    }

    @Test
    void testFloatingPointEdgeCases() {
        // NaN comparisons
        double nan = Double.NaN;
        assertFalse(nan == nan);
        assertTrue(Double.isNaN(nan));

        // Infinity
        assertEquals(Double.POSITIVE_INFINITY, 1.0 / 0.0);
        assertEquals(Double.NEGATIVE_INFINITY, -1.0 / 0.0);
        assertTrue(Double.isNaN(0.0 / 0.0));

        // Floating point precision
        assertNotEquals(0.3, 0.1 + 0.2);
        assertEquals(0.3, 0.1 + 0.2, 0.00001); // With delta

        // Special comparisons
        assertTrue(Double.POSITIVE_INFINITY > Double.MAX_VALUE);
        assertTrue(Double.NEGATIVE_INFINITY < -Double.MAX_VALUE);
    }
}
```

## String Edge Cases

### String Operations

```java
class StringEdgeCasesTest {
    @Test
    void testEmptyString() {
        String empty = "";

        assertEquals(0, empty.length());
        assertEquals("", empty.trim());
        assertFalse(empty == null);
        assertTrue(empty.isEmpty());
    }

    @Test
    void testStringComparison() {
        String s1 = "hello";
        String s2 = "hello";
        String s3 = new String("hello");

        // == vs equals()
        assertTrue(s1 == s2);        // Same intern pool reference
        assertFalse(s1 == s3);       // Different objects
        assertTrue(s1.equals(s3));   // Same content

        // Case sensitivity
        assertFalse("Hello".equals("hello"));
        assertTrue("Hello".equalsIgnoreCase("hello"));

        // Null comparison
        String nullStr = null;
        assertThrows(NullPointerException.class, () -> {
            nullStr.equals("test"); // NPE!
        });

        // Safe comparison
        assertFalse("test".equals(nullStr)); // No NPE
    }

    @Test
    void testStringSubstring() {
        String str = "Hello";

        // Valid substrings
        assertEquals("ell", str.substring(1, 4));
        assertEquals("", str.substring(2, 2)); // Empty substring

        // Boundary conditions
        assertEquals("Hello", str.substring(0));
        assertEquals("", str.substring(5)); // Empty from end

        // Invalid indices
        assertThrows(StringIndexOutOfBoundsException.class, () -> {
            str.substring(-1);
        });

        assertThrows(StringIndexOutOfBoundsException.class, () -> {
            str.substring(0, 10); // Beyond length
        });
    }

    @Test
    void testStringSplit() {
        // Empty string
        assertArrayEquals(new String[] {""}, "".split(","));

        // No delimiter
        assertArrayEquals(new String[] {"hello"}, "hello".split(","));

        // Multiple delimiters
        assertArrayEquals(new String[] {"a", "b", "c"}, "a,b,c".split(","));

        // Trailing empty strings removed by default
        assertArrayEquals(new String[] {"a", "b"}, "a,b,,,".split(","));

        // Keep trailing empty strings with limit
        assertArrayEquals(new String[] {"a", "b", "", "", ""},
                         "a,b,,,".split(",", -1));

        // Regex special characters need escaping
        assertArrayEquals(new String[] {"a", "b"}, "a.b".split("\\."));
    }
}
```

## Collection Edge Cases

### List Edge Cases

```java
class CollectionEdgeCasesTest {
    @Test
    void testArrayListEdgeCases() {
        List<Integer> list = new ArrayList<>();

        // Empty list
        assertEquals(0, list.size());
        assertTrue(list.isEmpty());
        assertThrows(IndexOutOfBoundsException.class, () -> {
            list.get(0);
        });

        // Single element
        list.add(42);
        assertEquals(1, list.size());
        assertEquals(42, list.get(0));

        // Negative index
        assertThrows(IndexOutOfBoundsException.class, () -> {
            list.get(-1);
        });

        // Index out of bounds
        assertThrows(IndexOutOfBoundsException.class, () -> {
            list.get(10);
        });

        // Remove while iterating (ConcurrentModificationException)
        list.addAll(Arrays.asList(1, 2, 3, 4, 5));
        assertThrows(ConcurrentModificationException.class, () -> {
            for (Integer i : list) {
                if (i == 3) {
                    list.remove(i); // Concurrent modification!
                }
            }
        });

        // Safe removal with iterator
        Iterator<Integer> it = list.iterator();
        while (it.hasNext()) {
            if (it.next() == 3) {
                it.remove(); // Safe
            }
        }
        assertFalse(list.contains(3));
    }

    @Test
    void testNullInCollections() {
        List<String> list = new ArrayList<>();

        // ArrayList allows null
        list.add(null);
        assertTrue(list.contains(null));
        assertEquals(1, list.size());

        // Operations with null
        assertNull(list.get(0));

        // Sorting with null throws NPE (Comparator dependent)
        list.add("hello");
        assertThrows(NullPointerException.class, () -> {
            Collections.sort(list); // NPE with null elements
        });
    }

    @Test
    void testArraysAsListEdgeCases() {
        // Fixed-size list from array
        List<Integer> list = Arrays.asList(1, 2, 3);

        assertEquals(3, list.size());

        // Can modify elements
        list.set(0, 10);
        assertEquals(10, list.get(0));

        // Cannot add or remove
        assertThrows(UnsupportedOperationException.class, () -> {
            list.add(4);
        });

        assertThrows(UnsupportedOperationException.class, () -> {
            list.remove(0);
        });
    }

    @Test
    void testMapEdgeCases() {
        Map<String, Integer> map = new HashMap<>();

        // Get from empty map
        assertNull(map.get("missing"));

        // getOrDefault
        assertEquals(0, map.getOrDefault("missing", 0));

        // Null keys and values
        map.put(null, 100);  // HashMap allows null key
        assertEquals(100, map.get(null));

        map.put("key", null); // HashMap allows null value
        assertTrue(map.containsKey("key"));
        assertNull(map.get("key"));

        // computeIfAbsent edge case
        map.computeIfAbsent("new", k -> 42);
        assertEquals(42, map.get("new"));

        // putIfAbsent with null
        map.putIfAbsent("key", 10); // Won't replace null
        assertNull(map.get("key")); // Still null!
    }
}
```

## Exception Handling

### Exception Edge Cases

```java
class ExceptionEdgeCasesTest {
    @Test
    void testTryWithResourcesEdgeCases() throws Exception {
        // Null resource
        assertThrows(NullPointerException.class, () -> {
            try (BufferedReader br = null) {
                br.readLine(); // NPE on null
            }
        });

        // Exception in close()
        class FailingCloseable implements AutoCloseable {
            @Override
            public void close() throws Exception {
                throw new Exception("Close failed");
            }
        }

        assertThrows(Exception.class, () -> {
            try (FailingCloseable fc = new FailingCloseable()) {
                // Normal execution
            } // Exception thrown on close
        });
    }

    @Test
    void testExceptionInFinally() {
        // Exception in finally block suppresses try block exception
        assertThrows(RuntimeException.class, () -> {
            try {
                throw new IllegalStateException("try block");
            } finally {
                throw new RuntimeException("finally block"); // This one is thrown
            }
        });
    }

    @Test
    void testCatchingErrors() {
        // Catching Error (not recommended)
        try {
            throw new OutOfMemoryError("OOM");
        } catch (Error e) {
            assertTrue(e instanceof OutOfMemoryError);
        }

        // StackOverflowError
        assertThrows(StackOverflowError.class, this::infiniteRecursion);
    }

    private void infiniteRecursion() {
        infiniteRecursion(); // Stack overflow!
    }
}
```

## Concurrency Edge Cases

### Thread Safety

```java
class ConcurrencyEdgeCasesTest {
    @Test
    void testRaceCondition() throws InterruptedException {
        Counter counter = new Counter();

        // Start multiple threads incrementing counter
        int threadCount = 10;
        int incrementsPerThread = 1000;

        Thread[] threads = new Thread[threadCount];
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    counter.increment();
                }
            });
            threads[i].start();
        }

        for (Thread thread : threads) {
            thread.join();
        }

        // Race condition: final count is likely < expected
        int expectedCount = threadCount * incrementsPerThread;
        assertTrue(counter.getCount() <= expectedCount);
        // Often significantly less than expected!
    }

    @Test
    void testThreadSafeCounter() throws InterruptedException {
        ThreadSafeCounter counter = new ThreadSafeCounter();

        int threadCount = 10;
        int incrementsPerThread = 1000;

        Thread[] threads = new Thread[threadCount];
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    counter.increment();
                }
            });
            threads[i].start();
        }

        for (Thread thread : threads) {
            thread.join();
        }

        // With proper synchronization
        assertEquals(threadCount * incrementsPerThread, counter.getCount());
    }

    @Test
    void testDeadlock() {
        final Object lock1 = new Object();
        final Object lock2 = new Object();

        Thread t1 = new Thread(() -> {
            synchronized (lock1) {
                try { Thread.sleep(10); } catch (InterruptedException e) {}
                synchronized (lock2) {
                    // Work
                }
            }
        });

        Thread t2 = new Thread(() -> {
            synchronized (lock2) {
                try { Thread.sleep(10); } catch (InterruptedException e) {}
                synchronized (lock1) {
                    // Work
                }
            }
        });

        t1.start();
        t2.start();

        // Potential deadlock - test with timeout
        assertTimeout(Duration.ofSeconds(2), () -> {
            t1.join(1000);
            t2.join(1000);
        });
    }

    // Supporting classes
    static class Counter {
        private int count = 0;

        public void increment() {
            count++; // Not atomic!
        }

        public int getCount() {
            return count;
        }
    }

    static class ThreadSafeCounter {
        private final AtomicInteger count = new AtomicInteger(0);

        public void increment() {
            count.incrementAndGet(); // Atomic
        }

        public int getCount() {
            return count.get();
        }
    }
}
```

## Generics and Type Edge Cases

### Generic Type Edge Cases

```java
class GenericsEdgeCasesTest {
    @Test
    void testRawTypes() {
        // Raw type (no generics)
        List rawList = new ArrayList();
        rawList.add("string");
        rawList.add(42);
        rawList.add(new Object());

        // Type safety lost
        assertEquals(3, rawList.size());

        // Casting required, risk of ClassCastException
        String first = (String) rawList.get(0);
        assertEquals("string", first);

        assertThrows(ClassCastException.class, () -> {
            String second = (String) rawList.get(1); // Integer, not String!
        });
    }

    @Test
    void testGenericArrayEdgeCases() {
        // Cannot create generic array directly
        // List<String>[] array = new List<String>[10]; // Compile error

        // Workaround with unchecked cast
        @SuppressWarnings("unchecked")
        List<String>[] array = (List<String>[]) new List[10];

        array[0] = new ArrayList<>();
        array[0].add("test");

        assertEquals("test", array[0].get(0));
    }

    @Test
    void testWildcardEdgeCases() {
        List<Integer> integers = Arrays.asList(1, 2, 3);
        List<? extends Number> numbers = integers;

        // Can read
        Number first = numbers.get(0);
        assertEquals(1, first);

        // Cannot add (except null)
        // numbers.add(1); // Compile error
        numbers.add(null); // Only null allowed
    }

    @Test
    void testTypeErasure() {
        List<String> strings = new ArrayList<>();
        List<Integer> integers = new ArrayList<>();

        // Type erasure: same class at runtime
        assertEquals(strings.getClass(), integers.getClass());

        // Cannot distinguish generic types at runtime
        assertTrue(strings instanceof List);
        // assertTrue(strings instanceof List<String>); // Compile error
    }
}
```

## Testing Frameworks

### JUnit 5 Patterns

```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;

class JUnitEdgeCasePatterns {
    // Parameterized tests for edge cases
    @ParameterizedTest
    @ValueSource(ints = {Integer.MIN_VALUE, -1, 0, 1, Integer.MAX_VALUE})
    void testIntegerBoundaries(int value) {
        assertDoesNotThrow(() -> process(value));
    }

    @ParameterizedTest
    @NullSource
    @EmptySource
    @ValueSource(strings = {" ", "  ", "\t", "\n"})
    void testStringEdgeCases(String input) {
        assertTrue(input == null || input.trim().isEmpty());
    }

    @ParameterizedTest
    @CsvSource({
        "0, 0",
        "1, 1",
        "-1, 1",
        "2147483647, 2147483647", // MAX_VALUE
        "-2147483648, 2147483648" // MIN_VALUE (overflow!)
    })
    void testAbsoluteValue(int input, long expected) {
        // Note: Math.abs(Integer.MIN_VALUE) overflows!
        assertEquals(expected, Math.abs((long) input));
    }

    // Timeout tests
    @Test
    @Timeout(value = 100, unit = TimeUnit.MILLISECONDS)
    void testTimeout() {
        // Must complete within 100ms
        performQuickOperation();
    }

    // Repeated tests for flaky edge cases
    @RepeatedTest(100)
    void testConcurrentAccess() {
        // Run 100 times to catch rare race conditions
        concurrentOperation();
    }

    // Assumptions for conditional edge cases
    @Test
    void testOnlyOnLinux() {
        assumeTrue(System.getProperty("os.name").toLowerCase().contains("linux"));
        // Test only runs on Linux
    }

    // Helper methods
    private void process(int value) {
        // Implementation
    }

    private void performQuickOperation() {
        // Fast operation
    }

    private void concurrentOperation() {
        // Concurrent operation
    }
}
```

### AssertJ Fluent Assertions

```java
import static org.assertj.core.api.Assertions.*;

class AssertJEdgeCasePatterns {
    @Test
    void testCollectionEdgeCases() {
        List<Integer> list = Arrays.asList(1, 2, 3);

        assertThat(list)
            .isNotNull()
            .isNotEmpty()
            .hasSize(3)
            .contains(1, 2, 3)
            .doesNotContain(4)
            .containsExactly(1, 2, 3)
            .containsExactlyInAnyOrder(3, 1, 2);

        // Empty collection
        assertThat(Collections.emptyList())
            .isEmpty()
            .hasSize(0);

        // Null checks
        List<String> nullList = null;
        assertThat(nullList).isNull();
    }

    @Test
    void testExceptionEdgeCases() {
        assertThatThrownBy(() -> {
            throw new IllegalArgumentException("Invalid argument");
        })
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessage("Invalid argument")
            .hasMessageContaining("Invalid")
            .hasNoCause();

        // Multiple exception assertions
        assertThatExceptionOfType(NullPointerException.class)
            .isThrownBy(() -> {
                String s = null;
                s.length();
            });
    }
}
```
