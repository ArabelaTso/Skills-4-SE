# Python Edge Cases and Testing Patterns

Python-specific edge cases, common pitfalls, and testing patterns using pytest, unittest, and Hypothesis.

## Table of Contents

1. [None and Truthiness](#none-and-truthiness)
2. [Mutable Default Arguments](#mutable-default-arguments)
3. [List and Dictionary Edge Cases](#list-and-dictionary-edge-cases)
4. [String and Unicode](#string-and-unicode)
5. [Numeric Types](#numeric-types)
6. [Exception Handling](#exception-handling)
7. [Iterator and Generator Edge Cases](#iterator-and-generator-edge-cases)
8. [Concurrency](#concurrency)
9. [Testing Frameworks](#testing-frameworks)

## None and Truthiness

### Common Pitfalls

```python
def test_none_vs_false():
    """Python's None, False, 0, [], {} are all falsy"""

    # Dangerous: Treats 0 and False as None
    def bad_example(value=None):
        if not value:  # Wrong! Treats 0, False, [] as None
            return "default"

    # Correct: Explicitly check for None
    def good_example(value=None):
        if value is None:  # Only treats None as None
            return "default"

    # Edge case tests
    assert bad_example(0) == "default"  # Unintended!
    assert bad_example(False) == "default"  # Unintended!
    assert good_example(0) != "default"  # Correct
    assert good_example(False) != "default"  # Correct
```

### Edge Case Tests

```python
import pytest

def test_none_edge_cases():
    """Test None handling"""

    # None vs empty string
    assert "" is not None
    assert not ""  # Empty string is falsy
    assert "" == ""

    # None vs empty list
    assert [] is not None
    assert not []  # Empty list is falsy

    # None vs zero
    assert 0 is not None
    assert not 0  # Zero is falsy

    # None vs False
    assert False is not None
    assert None is not False
    assert not False
    assert not None
```

## Mutable Default Arguments

### Common Pitfall

```python
def test_mutable_defaults():
    """Mutable default arguments are shared across calls"""

    # DANGEROUS: Mutable default argument
    def append_to_list_bad(item, lst=[]):
        lst.append(item)
        return lst

    # Edge case: List is shared across calls!
    result1 = append_to_list_bad(1)
    result2 = append_to_list_bad(2)
    assert result1 == [1, 2]  # Unexpected!
    assert result2 == [1, 2]  # Same object!

    # CORRECT: Use None and create new list
    def append_to_list_good(item, lst=None):
        if lst is None:
            lst = []
        lst.append(item)
        return lst

    result3 = append_to_list_good(1)
    result4 = append_to_list_good(2)
    assert result3 == [1]  # Expected
    assert result4 == [2]  # Expected
```

## List and Dictionary Edge Cases

### List Slicing

```python
def test_list_slicing_edge_cases():
    """Python list slicing has many edge cases"""
    lst = [1, 2, 3, 4, 5]

    # Out of bounds indices don't raise errors
    assert lst[10:20] == []  # Empty, not error
    assert lst[-100:2] == [1, 2]  # Clamps to start

    # Negative indices
    assert lst[-1] == 5  # Last element
    assert lst[-2:] == [4, 5]  # Last two

    # Empty slices
    assert lst[2:2] == []  # Empty slice
    assert lst[5:10] == []  # Past end

    # Reverse slicing
    assert lst[::-1] == [5, 4, 3, 2, 1]  # Reverse
    assert lst[4:1:-1] == [5, 4, 3]  # Reverse slice

    # Step values
    assert lst[::2] == [1, 3, 5]  # Every other
    assert lst[1::2] == [2, 4]  # Every other from index 1
```

### Dictionary Edge Cases

```python
def test_dict_edge_cases():
    """Dictionary edge cases"""

    # Missing key
    d = {"a": 1}
    with pytest.raises(KeyError):
        _ = d["b"]

    # get() with default
    assert d.get("b") is None
    assert d.get("b", "default") == "default"

    # setdefault()
    d.setdefault("b", []).append(1)
    assert d["b"] == [1]

    # Update with duplicate keys (last wins)
    d.update({"a": 2, "a": 3})
    assert d["a"] == 3

    # Iteration during modification
    d = {"a": 1, "b": 2, "c": 3}
    # Don't modify dict during iteration
    # Use list(d.keys()) to avoid RuntimeError
    for key in list(d.keys()):
        if key == "b":
            del d[key]
    assert "b" not in d
```

## String and Unicode

### Unicode Edge Cases

```python
def test_string_unicode_edge_cases():
    """Unicode and string edge cases"""

    # Empty string
    assert "" == ""
    assert len("") == 0
    assert not ""  # Falsy

    # Whitespace
    assert "   ".strip() == ""
    assert " ".isspace()
    assert not "".isspace()  # Empty is not whitespace

    # Unicode characters
    assert len("café") == 4  # 4 characters
    assert len("🎉") == 1  # 1 emoji character
    assert len("👨‍👩‍👧‍👦") == 7  # Family emoji is 7 code points!

    # Encoding edge cases
    text = "café"
    assert text.encode("utf-8") == b'caf\xc3\xa9'
    assert text.encode("ascii", errors="ignore") == b'caf'

    # Case transformations
    assert "straße".upper() == "STRASSE"  # German ß
    assert "İstanbul".lower() == "i̇stanbul"  # Turkish İ

    # Normalization
    import unicodedata
    assert unicodedata.normalize("NFC", "café") == \
           unicodedata.normalize("NFD", "café")  # False! Different forms
```

### String Comparison Edge Cases

```python
def test_string_comparison_edge_cases():
    """String comparison edge cases"""

    # Case sensitivity
    assert "Hello" != "hello"
    assert "Hello".lower() == "hello"

    # Whitespace
    assert "hello" != " hello"
    assert "hello" != "hello "
    assert " hello ".strip() == "hello"

    # None vs empty string
    assert "" != None
    assert not "" and not None  # Both falsy

    # Numeric strings
    assert "10" < "9"  # Lexicographic ordering!
    assert int("10") > int("9")  # Numeric ordering

    # Special characters
    assert "\n" != "\\n"  # Newline vs escaped
    assert r"\n" == "\\n"  # Raw string
```

## Numeric Types

### Integer Edge Cases

```python
def test_integer_edge_cases():
    """Python 3 integers have unlimited precision"""

    # No overflow in Python 3!
    big_num = 10**100
    assert big_num * big_num == 10**200

    # Division types
    assert 5 / 2 == 2.5  # Float division
    assert 5 // 2 == 2  # Integer division
    assert 5 % 2 == 1  # Modulo

    # Negative division
    assert -5 // 2 == -3  # Floors toward negative infinity
    assert -5 % 2 == 1  # Sign matches divisor

    # Zero division
    with pytest.raises(ZeroDivisionError):
        _ = 1 / 0
    with pytest.raises(ZeroDivisionError):
        _ = 1 // 0
```

### Float Edge Cases

```python
import math
import pytest

def test_float_edge_cases():
    """Floating point edge cases"""

    # Precision loss
    assert 0.1 + 0.2 != 0.3  # Famous floating point issue
    assert abs((0.1 + 0.2) - 0.3) < 1e-10  # Use epsilon comparison

    # Special values
    assert math.isnan(float('nan'))
    assert math.isinf(float('inf'))
    assert math.isinf(float('-inf'))

    # NaN comparisons
    nan = float('nan')
    assert nan != nan  # NaN != NaN!
    assert not (nan == nan)
    assert math.isnan(nan)  # Correct way to check

    # Infinity arithmetic
    inf = float('inf')
    assert inf + 1 == inf
    assert inf * 2 == inf
    assert inf > 10**100
    assert -inf < -10**100

    # Division by zero for floats
    assert 1.0 / 0.0 == inf  # No exception! Returns inf
    assert -1.0 / 0.0 == -inf
    assert math.isnan(0.0 / 0.0)  # 0/0 is NaN
```

## Exception Handling

### Testing Exceptions

```python
def test_exception_edge_cases():
    """Exception handling edge cases"""

    # Basic exception testing
    with pytest.raises(ValueError):
        int("not a number")

    # Check exception message
    with pytest.raises(ValueError, match="invalid literal"):
        int("not a number")

    # Multiple exceptions
    with pytest.raises((TypeError, ValueError)):
        int(None)  # Raises TypeError

    # Exception not raised
    def safe_divide(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return None

    assert safe_divide(1, 0) is None  # No exception raised
    assert safe_divide(4, 2) == 2.0

    # Catching wrong exception
    with pytest.raises(ZeroDivisionError):
        with pytest.raises(ValueError):
            _ = 1 / 0  # Raises ZeroDivisionError, not ValueError
```

## Iterator and Generator Edge Cases

### Iterator Exhaustion

```python
def test_iterator_edge_cases():
    """Iterator edge cases"""

    # Iterator exhaustion
    it = iter([1, 2, 3])
    assert list(it) == [1, 2, 3]
    assert list(it) == []  # Exhausted!

    # StopIteration
    it = iter([1])
    assert next(it) == 1
    with pytest.raises(StopIteration):
        next(it)

    # next() with default
    it = iter([])
    assert next(it, "default") == "default"

    # Generator exhaustion
    def gen():
        yield 1
        yield 2

    g = gen()
    assert next(g) == 1
    assert next(g) == 2
    with pytest.raises(StopIteration):
        next(g)
```

### Generator Edge Cases

```python
def test_generator_edge_cases():
    """Generator-specific edge cases"""

    # Empty generator
    def empty_gen():
        return
        yield  # Never reached

    assert list(empty_gen()) == []

    # Generator with exception
    def error_gen():
        yield 1
        raise ValueError("error")
        yield 2  # Never reached

    g = error_gen()
    assert next(g) == 1
    with pytest.raises(ValueError):
        next(g)

    # Generator cleanup
    def cleanup_gen():
        try:
            yield 1
            yield 2
        finally:
            print("Cleanup")

    g = cleanup_gen()
    next(g)
    # g.close() triggers finally block
```

## Concurrency

### Threading Edge Cases

```python
import threading
import time

def test_threading_edge_cases():
    """Threading edge cases"""

    # Race condition
    counter = 0

    def increment():
        nonlocal counter
        for _ in range(10000):
            counter += 1  # Not atomic!

    threads = [threading.Thread(target=increment) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Counter likely < 100000 due to race condition
    assert counter <= 100000

    # With lock (correct)
    counter = 0
    lock = threading.Lock()

    def increment_safe():
        nonlocal counter
        for _ in range(10000):
            with lock:
                counter += 1

    threads = [threading.Thread(target=increment_safe) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert counter == 100000  # Correct
```

## Testing Frameworks

### Pytest Patterns

```python
import pytest

# Parametrized tests for edge cases
@pytest.mark.parametrize("input,expected", [
    (0, 0),  # Zero
    (1, 1),  # One
    (-1, 1),  # Negative
    (10, 10),  # Positive
    (2**31 - 1, 2**31 - 1),  # Max int32
])
def test_abs_edge_cases(input, expected):
    assert abs(input) == expected

# Fixtures for setup/teardown
@pytest.fixture
def temp_file(tmp_path):
    """Create temporary file for testing"""
    file = tmp_path / "test.txt"
    file.write_text("test content")
    yield file
    # Cleanup happens automatically

def test_file_operations(temp_file):
    assert temp_file.read_text() == "test content"

# Mocking for edge cases
from unittest.mock import Mock, patch

def test_network_failure():
    """Test behavior when network fails"""
    with patch('requests.get', side_effect=ConnectionError("Network down")):
        with pytest.raises(ConnectionError):
            import requests
            requests.get("http://example.com")
```

### Hypothesis Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_reverse_property(lst):
    """Reversing twice returns original"""
    assert list(reversed(list(reversed(lst)))) == lst

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Addition is commutative"""
    assert a + b == b + a

@given(st.text())
def test_uppercase_length(s):
    """Uppercase preserves length"""
    assert len(s.upper()) == len(s)

# Constrained strategies for edge cases
@given(st.integers(min_value=0, max_value=100))
def test_percentage(pct):
    """Test with valid percentage range"""
    assert 0 <= pct <= 100
```

## Common Python Testing Anti-Patterns

### Anti-Pattern: Testing Implementation Details

```python
# BAD: Testing private methods
def test_private_method():
    obj = MyClass()
    assert obj._private_method() == "result"  # Fragile!

# GOOD: Test public interface
def test_public_behavior():
    obj = MyClass()
    assert obj.public_method() == "expected"  # Tests behavior
```

### Anti-Pattern: Assertions Without Messages

```python
# BAD: No context on failure
def test_calculation():
    assert calculate(5, 3) == 8

# GOOD: Helpful failure message
def test_calculation():
    result = calculate(5, 3)
    assert result == 8, f"Expected 8, got {result}"
```

### Anti-Pattern: Testing Multiple Things

```python
# BAD: Multiple unrelated assertions
def test_everything():
    assert len([]) == 0
    assert 1 + 1 == 2
    assert "hello".upper() == "HELLO"

# GOOD: Separate focused tests
def test_empty_list_length():
    assert len([]) == 0

def test_addition():
    assert 1 + 1 == 2

def test_string_uppercase():
    assert "hello".upper() == "HELLO"
```
