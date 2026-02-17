# Common Semantic Bug Patterns

Catalog of semantic bugs where implementation doesn't match intent.

## Table of Contents
- [Off-by-One Errors](#off-by-one-errors)
- [Inverted Logic](#inverted-logic)
- [Boundary Mismatches](#boundary-mismatches)
- [Wrong Operator](#wrong-operator)
- [Missing Edge Cases](#missing-edge-cases)
- [Type Confusion](#type-confusion)

## Off-by-One Errors

### Pattern: Array/List Indexing

**Intent indicators**: "last N elements", "first N items", "range [a, b)"

**Bug**: Using `n+1` instead of `n`, or `<=` instead of `<`

**Example 1**:
```python
def get_last_n_elements(arr, n):
    """Returns the last n elements from the array."""
    return arr[-n-1:]  # BUG: Returns n+1 elements
```

**Correct**:
```python
def get_last_n_elements(arr, n):
    """Returns the last n elements from the array."""
    return arr[-n:]
```

**Example 2**:
```javascript
// Returns first n elements
function getFirstN(arr, n) {
    return arr.slice(0, n+1);  // BUG: Returns n+1 elements
}
```

**Correct**:
```javascript
function getFirstN(arr, n) {
    return arr.slice(0, n);
}
```

### Pattern: Loop Boundaries

**Intent indicators**: "iterate N times", "process all elements", "up to index i"

**Bug**: Using `<=` when should use `<`, or vice versa

**Example**:
```python
def sum_first_n(arr, n):
    """Sum the first n elements."""
    total = 0
    for i in range(n+1):  # BUG: Iterates n+1 times
        total += arr[i]
    return total
```

**Correct**:
```python
def sum_first_n(arr, n):
    """Sum the first n elements."""
    total = 0
    for i in range(n):
        total += arr[i]
    return total
```

## Inverted Logic

### Pattern: Boolean Predicates

**Intent indicators**: "is_even", "is_empty", "has_property"

**Bug**: Returning opposite boolean value

**Example 1**:
```python
def is_even(x):
    """Check if x is even."""
    return x % 2 == 1  # BUG: Returns True for odd numbers
```

**Correct**:
```python
def is_even(x):
    """Check if x is even."""
    return x % 2 == 0
```

**Example 2**:
```java
// Check if list is empty
public boolean isEmpty(List<T> list) {
    return list.size() > 0;  // BUG: Returns true when NOT empty
}
```

**Correct**:
```java
public boolean isEmpty(List<T> list) {
    return list.size() == 0;
}
```

### Pattern: Comparison Operators

**Intent indicators**: "greater than", "less than", "at least", "at most"

**Bug**: Using wrong comparison operator

**Example**:
```python
def is_positive(x):
    """Check if x is positive (greater than zero)."""
    return x >= 0  # BUG: Includes zero, which is not positive
```

**Correct**:
```python
def is_positive(x):
    """Check if x is positive (greater than zero)."""
    return x > 0
```

## Boundary Mismatches

### Pattern: Inclusive vs Exclusive Ranges

**Intent indicators**: "[a, b]", "[a, b)", "(a, b]", "(a, b)"

**Bug**: Using inclusive when should be exclusive, or vice versa

**Example 1**:
```python
def in_range(x, start, end):
    """Check if x is in range [start, end)."""
    return start <= x <= end  # BUG: Includes end
```

**Correct**:
```python
def in_range(x, start, end):
    """Check if x is in range [start, end)."""
    return start <= x < end
```

**Example 2**:
```javascript
// Returns elements in range [start, end)
function getRange(arr, start, end) {
    return arr.slice(start, end+1);  // BUG: Includes end
}
```

**Correct**:
```javascript
function getRange(arr, start, end) {
    return arr.slice(start, end);
}
```

### Pattern: String/Array Slicing

**Intent indicators**: "substring from i to j", "elements between indices"

**Bug**: Incorrect slice boundaries

**Example**:
```python
def get_middle_chars(s):
    """Get the middle character(s) of a string.
    For odd length, returns 1 char. For even length, returns 2 chars."""
    mid = len(s) // 2
    if len(s) % 2 == 1:
        return s[mid]
    else:
        return s[mid:mid+1]  # BUG: Returns only 1 char for even length
```

**Correct**:
```python
def get_middle_chars(s):
    """Get the middle character(s) of a string."""
    mid = len(s) // 2
    if len(s) % 2 == 1:
        return s[mid]
    else:
        return s[mid-1:mid+1]
```

## Wrong Operator

### Pattern: Arithmetic Operations

**Intent indicators**: "sum", "product", "difference", "average"

**Bug**: Using wrong arithmetic operator

**Example 1**:
```python
def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    return sum(numbers) * len(numbers)  # BUG: Should divide, not multiply
```

**Correct**:
```python
def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    return sum(numbers) / len(numbers)
```

**Example 2**:
```javascript
// Calculate product of array elements
function product(arr) {
    let result = 0;  // BUG: Should initialize to 1
    for (let x of arr) {
        result *= x;
    }
    return result;
}
```

**Correct**:
```javascript
function product(arr) {
    let result = 1;
    for (let x of arr) {
        result *= x;
    }
    return result;
}
```

### Pattern: Logical Operations

**Intent indicators**: "both conditions", "either condition", "not condition"

**Bug**: Using `or` instead of `and`, or vice versa

**Example**:
```python
def is_valid_age(age):
    """Check if age is valid (between 0 and 120 inclusive)."""
    return age >= 0 or age <= 120  # BUG: Should use 'and'
```

**Correct**:
```python
def is_valid_age(age):
    """Check if age is valid (between 0 and 120 inclusive)."""
    return age >= 0 and age <= 120
```

## Missing Edge Cases

### Pattern: Empty Input

**Intent indicators**: "process all elements", "find maximum", "calculate sum"

**Bug**: Not handling empty input

**Example**:
```python
def find_max(numbers):
    """Find the maximum number in the list."""
    max_val = numbers[0]  # BUG: Crashes on empty list
    for num in numbers[1:]:
        if num > max_val:
            max_val = num
    return max_val
```

**Correct**:
```python
def find_max(numbers):
    """Find the maximum number in the list."""
    if not numbers:
        raise ValueError("Cannot find max of empty list")
    max_val = numbers[0]
    for num in numbers[1:]:
        if num > max_val:
            max_val = num
    return max_val
```

### Pattern: Null/None Values

**Intent indicators**: "process data", "transform input"

**Bug**: Not checking for null/None

**Example**:
```javascript
// Get length of string
function getLength(str) {
    return str.length;  // BUG: Crashes if str is null/undefined
}
```

**Correct**:
```javascript
function getLength(str) {
    if (str == null) {
        return 0;
    }
    return str.length;
}
```

### Pattern: Division by Zero

**Intent indicators**: "divide", "calculate ratio", "average"

**Bug**: Not checking for zero divisor

**Example**:
```python
def calculate_ratio(a, b):
    """Calculate the ratio a/b."""
    return a / b  # BUG: Crashes when b is 0
```

**Correct**:
```python
def calculate_ratio(a, b):
    """Calculate the ratio a/b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

## Type Confusion

### Pattern: String vs Number

**Intent indicators**: "numeric value", "string representation"

**Bug**: Treating string as number or vice versa

**Example**:
```python
def increment_value(x):
    """Increment the numeric value by 1."""
    return x + "1"  # BUG: String concatenation instead of addition
```

**Correct**:
```python
def increment_value(x):
    """Increment the numeric value by 1."""
    return x + 1
```

### Pattern: List vs Single Element

**Intent indicators**: "process items", "handle element"

**Bug**: Treating single element as list or vice versa

**Example**:
```python
def process_items(items):
    """Process a list of items."""
    for item in items:
        print(item[0])  # BUG: Assumes each item is indexable
```

**Correct**:
```python
def process_items(items):
    """Process a list of items."""
    for item in items:
        print(item)
```

## Detection Strategies

### Strategy 1: Name-Behavior Mismatch

1. Extract function/variable name
2. Infer expected behavior from name
3. Analyze actual implementation
4. Compare expected vs actual

**Example**: Function named `is_even` should return `True` for even numbers

### Strategy 2: Comment-Code Mismatch

1. Parse comments and docstrings
2. Extract stated intent
3. Verify implementation matches intent
4. Flag discrepancies

**Example**: Comment says "returns first n elements" but code returns `n+1`

### Strategy 3: Boundary Analysis

1. Identify range specifications in docs
2. Check if implementation respects boundaries
3. Verify inclusive/exclusive semantics

**Example**: Doc says "[start, end)" but code uses `<=` for end

### Strategy 4: Operator Consistency

1. Identify operation from name/docs
2. Check if correct operator is used
3. Verify initialization values

**Example**: Function named `product` should use `*` not `+`, initialize to 1 not 0

### Strategy 5: Edge Case Coverage

1. Identify potential edge cases from context
2. Check if code handles them
3. Flag missing checks

**Example**: Function processing list should handle empty list
