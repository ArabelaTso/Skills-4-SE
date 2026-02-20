# Assertion Guide

Framework-specific assertion reference and best practices for Python and Java testing frameworks.

## Table of Contents

1. [Python - pytest](#python-pytest)
2. [Python - unittest](#python-unittest)
3. [Java - JUnit 4](#java-junit-4)
4. [Java - JUnit 5](#java-junit-5)
5. [Best Practices](#best-practices)

---

## Python - pytest

### Basic Assertions

```python
# Equality
assert result == expected
assert result != unexpected

# Truthiness
assert result
assert not result

# Comparisons
assert x > 5
assert x >= 5
assert x < 10
assert x <= 10

# Containment
assert item in collection
assert item not in collection
assert "substring" in string

# Type checking
assert isinstance(obj, ExpectedType)
assert type(obj) == ExpectedType
```

### Floating Point Comparisons

```python
import pytest

# Approximate equality
assert result == pytest.approx(3.14159, abs=0.001)
assert result == pytest.approx(expected)  # Default tolerance

# Relative tolerance
assert result == pytest.approx(expected, rel=0.01)  # 1% tolerance

# For lists/tuples of floats
assert results == pytest.approx([1.0, 2.0, 3.0])
```

### Exception Testing

```python
import pytest

# Test that exception is raised
with pytest.raises(ValueError):
    function_that_raises()

# Test exception message
with pytest.raises(ValueError, match="specific error"):
    function_that_raises()

# Test exception message with regex
with pytest.raises(ValueError, match=r"error: \d+"):
    function_that_raises()

# Capture exception for further inspection
with pytest.raises(ValueError) as exc_info:
    function_that_raises()
assert "details" in str(exc_info.value)
```

### Collection Assertions

```python
# List/tuple equality (order matters)
assert result_list == expected_list

# Set equality (order doesn't matter)
assert set(result_list) == set(expected_list)

# Length
assert len(collection) == expected_length

# Empty/non-empty
assert collection  # Non-empty
assert not collection  # Empty

# All/any
assert all(x > 0 for x in numbers)
assert any(x > 100 for x in numbers)
```

### String Assertions

```python
# Exact match
assert text == "expected"

# Contains
assert "substring" in text

# Starts/ends with
assert text.startswith("prefix")
assert text.endswith("suffix")

# Regex match
import re
assert re.match(r"pattern", text)
assert re.search(r"pattern", text)
```

### Custom Failure Messages

```python
# Add message to assertion
assert result == expected, f"Expected {expected}, got {result}"
assert len(items) > 0, "List should not be empty"
```

---

## Python - unittest

### Basic Assertions

```python
import unittest

class TestExample(unittest.TestCase):

    # Equality
    def test_equality(self):
        self.assertEqual(result, expected)
        self.assertNotEqual(result, unexpected)

    # Truthiness
    def test_truthiness(self):
        self.assertTrue(condition)
        self.assertFalse(condition)

    # None
    def test_none(self):
        self.assertIsNone(value)
        self.assertIsNotNone(value)

    # Containment
    def test_containment(self):
        self.assertIn(item, collection)
        self.assertNotIn(item, collection)

    # Type checking
    def test_type(self):
        self.assertIsInstance(obj, ExpectedType)
        self.assertNotIsInstance(obj, WrongType)
```

### Numeric Assertions

```python
# Approximate equality
self.assertAlmostEqual(3.14159, 3.14, places=2)
self.assertNotAlmostEqual(3.14, 2.71, places=1)

# Greater/less than
self.assertGreater(10, 5)
self.assertGreaterEqual(10, 10)
self.assertLess(5, 10)
self.assertLessEqual(5, 5)
```

### Exception Testing

```python
# Test that exception is raised
with self.assertRaises(ValueError):
    function_that_raises()

# Test exception message
with self.assertRaises(ValueError) as context:
    function_that_raises()
self.assertIn("error message", str(context.exception))

# Test specific exception type
with self.assertRaises(SpecificException):
    function_that_raises()
```

### Collection Assertions

```python
# Sequence equality
self.assertSequenceEqual(list1, list2)
self.assertListEqual(list1, list2)
self.assertTupleEqual(tuple1, tuple2)

# Set equality
self.assertSetEqual(set1, set2)

# Dict equality
self.assertDictEqual(dict1, dict2)

# Count occurrences
self.assertCountEqual([1, 2, 2], [2, 1, 2])  # Order-independent
```

### String Assertions

```python
# Regex
self.assertRegex(text, r"pattern")
self.assertNotRegex(text, r"pattern")

# Multi-line strings
self.assertMultiLineEqual(text1, text2)
```

---

## Java - JUnit 4

### Basic Assertions

```java
import static org.junit.Assert.*;

// Equality
assertEquals(expected, actual);
assertNotEquals(unexpected, actual);

// Boolean
assertTrue(condition);
assertFalse(condition);

// Null
assertNull(object);
assertNotNull(object);

// Same object (reference equality)
assertSame(expected, actual);
assertNotSame(expected, actual);

// Custom message
assertEquals("Custom error message", expected, actual);
```

### Numeric Assertions

```java
// Exact equality
assertEquals(42, result);

// Floating point with delta
assertEquals(3.14159, result, 0.001);
assertEquals(3.14, result, 0.01);

// Not equal with delta
assertNotEquals(3.14, 2.71, 0.01);
```

### Exception Testing

```java
// Expected exception (annotation)
@Test(expected = IllegalArgumentException.class)
public void testExceptionThrown() {
    methodThatThrows();
}

// Manual exception testing
try {
    methodThatThrows();
    fail("Expected exception was not thrown");
} catch (IllegalArgumentException e) {
    // Expected
    assertTrue(e.getMessage().contains("error"));
}
```

### Array Assertions

```java
// Array equality
assertArrayEquals(expectedArray, actualArray);

// Array equality with delta (for floats/doubles)
assertArrayEquals(expectedDoubles, actualDoubles, 0.001);
```

### Collection Assertions (with Hamcrest)

```java
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

// Contains
assertThat(list, hasItem("item"));
assertThat(list, hasItems("item1", "item2"));

// Size
assertThat(list, hasSize(3));

// Empty
assertThat(list, empty());

// Contains in order
assertThat(list, contains("a", "b", "c"));

// Contains in any order
assertThat(list, containsInAnyOrder("c", "a", "b"));
```

### String Assertions (with Hamcrest)

```java
// String equality
assertThat(text, equalTo("expected"));

// Contains
assertThat(text, containsString("substring"));

// Starts/ends with
assertThat(text, startsWith("prefix"));
assertThat(text, endsWith("suffix"));

// Regex
assertThat(text, matchesPattern("\\d{3}-\\d{4}"));
```

---

## Java - JUnit 5

### Basic Assertions

```java
import static org.junit.jupiter.api.Assertions.*;

// Equality
assertEquals(expected, actual);
assertNotEquals(unexpected, actual);

// Boolean
assertTrue(condition);
assertFalse(condition);

// Null
assertNull(object);
assertNotNull(object);

// Same reference
assertSame(expected, actual);
assertNotSame(expected, actual);

// Custom message
assertEquals(expected, actual, "Custom error message");

// Lazy message (computed only on failure)
assertEquals(expected, actual, () -> "Computed: " + computeMessage());
```

### Exception Testing

```java
// Test exception is thrown
Exception exception = assertThrows(IllegalArgumentException.class, () -> {
    methodThatThrows();
});

// Test exception message
Exception exception = assertThrows(IllegalArgumentException.class, () -> {
    methodThatThrows();
});
assertTrue(exception.getMessage().contains("expected error"));

// Shorter form
assertThrows(IllegalArgumentException.class, () -> methodThatThrows());
```

### Grouped Assertions

```java
// Execute all assertions even if some fail
assertAll(
    () -> assertEquals(expected1, actual1),
    () -> assertEquals(expected2, actual2),
    () -> assertEquals(expected3, actual3)
);

// With heading
assertAll("User properties",
    () -> assertEquals("Alice", user.getName()),
    () -> assertEquals(25, user.getAge()),
    () -> assertEquals("alice@example.com", user.getEmail())
);
```

### Timeout Assertions

```java
// Assertion must complete within timeout
assertTimeout(Duration.ofSeconds(2), () -> {
    // Code that should complete within 2 seconds
    performOperation();
});

// Preemptive timeout (aborts if exceeded)
assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
    performOperation();
});
```

### Array and Collection Assertions

```java
// Array equality
assertArrayEquals(expectedArray, actualArray);

// Iterable contains
assertIterableEquals(expectedList, actualList);

// With message
assertArrayEquals(expected, actual, "Arrays should match");
```

### Advanced Assertions

```java
// Lines (for multi-line strings)
assertLinesMatch(expectedLines, actualLines);

// Custom assertion
assertTrue(complexCondition(), "Complex condition failed");

// Fail with message
fail("Test not implemented yet");

// Assume (skip test if assumption fails)
assumeTrue(System.getProperty("os.name").contains("Linux"));
```

---

## Best Practices

### 1. Use Descriptive Assertion Messages

```python
# Bad
assert result == 10

# Good
assert result == 10, f"Expected sum to be 10, got {result}"
```

```java
// Bad
assertEquals(10, result);

// Good
assertEquals(10, result, "Expected sum of [5, 5] to be 10");
```

### 2. One Logical Assertion Per Test

```python
# Acceptable - testing one concept
def test_user_creation():
    user = create_user("Alice", "alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.id is not None

# Better - use assertAll in Java or separate tests
def test_user_has_correct_name():
    user = create_user("Alice", "alice@example.com")
    assert user.name == "Alice"

def test_user_has_correct_email():
    user = create_user("Alice", "alice@example.com")
    assert user.email == "alice@example.com"
```

### 3. Test Behavior, Not Implementation

```python
# Bad - tests implementation detail
def test_uses_quicksort():
    sorter = Sorter()
    assert sorter.algorithm == "quicksort"

# Good - tests behavior
def test_sorts_list_in_ascending_order():
    sorter = Sorter()
    result = sorter.sort([3, 1, 2])
    assert result == [1, 2, 3]
```

### 4. Use Appropriate Assertion Methods

```python
# Less clear
assert len(items) == 0

# More clear
assert not items  # or
assert items == []

# Best (unittest)
self.assertEqual([], items)
```

```java
// Less clear
assertTrue(list.size() == 0);

// More clear
assertEquals(0, list.size());

// Best (Hamcrest)
assertThat(list, empty());
```

### 5. Be Specific with Exception Testing

```python
# Too general
with pytest.raises(Exception):
    risky_operation()

# Better
with pytest.raises(ValueError):
    risky_operation()

# Best
with pytest.raises(ValueError, match="Invalid input"):
    risky_operation()
```

### 6. Use Fixtures for Test Data

```python
# Bad - duplicated setup
def test_user_name():
    user = User("Alice", "alice@example.com")
    assert user.name == "Alice"

def test_user_email():
    user = User("Alice", "alice@example.com")
    assert user.email == "alice@example.com"

# Good - shared fixture
@pytest.fixture
def user():
    return User("Alice", "alice@example.com")

def test_user_name(user):
    assert user.name == "Alice"

def test_user_email(user):
    assert user.email == "alice@example.com"
```

### 7. Prefer Equality Over Truth

```python
# Less informative on failure
assert user.is_active()

# More informative on failure
assert user.is_active() == True  # Shows expected vs actual

# Or be explicit
assert user.is_active() is True
```

### 8. Test Edge Cases Explicitly

```python
def test_handles_empty_list():
    result = process([])
    assert result == expected_for_empty

def test_handles_single_item():
    result = process([item])
    assert result == expected_for_single

def test_handles_large_list():
    result = process([item] * 10000)
    assert result == expected_for_large
```

### 9. Use Parameterized Tests for Similar Cases

```python
# Instead of:
def test_discount_10_percent():
    assert calculate_discount(100, 10) == 90

def test_discount_20_percent():
    assert calculate_discount(100, 20) == 80

# Use:
@pytest.mark.parametrize("price,discount,expected", [
    (100, 10, 90),
    (100, 20, 80),
    (100, 50, 50),
])
def test_discount_calculation(price, discount, expected):
    assert calculate_discount(price, discount) == expected
```

### 10. Keep Assertions Simple

```python
# Too complex
assert all(
    user.age > 18 and user.email.endswith("@company.com")
    for user in users
    if user.is_active
)

# Better - break down or add helper
def test_all_active_users_are_adults_with_company_email():
    active_users = [u for u in users if u.is_active]
    assert all(u.age > 18 for u in active_users)
    assert all(u.email.endswith("@company.com") for u in active_users)
```
