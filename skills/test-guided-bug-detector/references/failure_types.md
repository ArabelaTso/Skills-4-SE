# Test Failure Types

Guide for analyzing different types of test failures.

## Assertion Failures

### Simple Assertion

**Pattern:** Direct value comparison fails.

**Example:**
```python
assert result == 5
# AssertionError: assert 3 == 5
```

**Analysis:**
- Expected: 5
- Actual: 3
- Discrepancy: Result is 2 less than expected
- Check: Calculation error, missing operation, wrong formula

### Collection Assertion

**Pattern:** List/array comparison fails.

**Example:**
```python
assert result == [1, 2, 3]
# AssertionError: assert [1, 2] == [1, 2, 3]
```

**Analysis:**
- Expected: [1, 2, 3]
- Actual: [1, 2]
- Discrepancy: Missing element
- Check: Loop termination, collection building, filtering

### Floating Point Assertion

**Pattern:** Float comparison with precision issues.

**Example:**
```python
assert result == 0.3
# AssertionError: assert 0.30000000000000004 == 0.3
```

**Analysis:**
- Issue: Floating point precision
- Check: Use approximate comparison (pytest.approx, assertAlmostEqual)
- Not a bug: Expected behavior of floating point arithmetic

## Exception Failures

### Unexpected Exception

**Pattern:** Code raises exception when it shouldn't.

**Example:**
```python
def test_divide():
    result = divide(10, 2)
# ZeroDivisionError: division by zero
```

**Analysis:**
- Expected: Normal execution
- Actual: Exception raised
- Check: Input validation, edge cases, error handling

### Wrong Exception Type

**Pattern:** Different exception than expected.

**Example:**
```python
with pytest.raises(ValueError):
    process(invalid_input)
# Failed: DID NOT RAISE ValueError (raised TypeError instead)
```

**Analysis:**
- Expected: ValueError
- Actual: TypeError
- Check: Exception handling logic, validation code

### Missing Exception

**Pattern:** Code doesn't raise expected exception.

**Example:**
```python
with pytest.raises(ValueError):
    process(invalid_input)
# Failed: DID NOT RAISE ValueError
```

**Analysis:**
- Expected: ValueError raised
- Actual: No exception
- Check: Validation logic, error conditions

## Timeout Failures

### Infinite Loop

**Pattern:** Test times out due to non-terminating loop.

**Example:**
```python
def test_process():
    result = process_data(input)
# TIMEOUT after 5 seconds
```

**Analysis:**
- Check: Loop termination conditions
- Look for: Missing increment, wrong condition, infinite recursion

### Performance Regression

**Pattern:** Code too slow, exceeds timeout.

**Example:**
```python
def test_sort_performance():
    result = sort(large_list)
# TIMEOUT: Expected < 1s, took > 5s
```

**Analysis:**
- Check: Algorithm complexity, inefficient operations
- Look for: Nested loops, repeated work, missing optimization

## Unexpected Behavior

### Wrong Output Format

**Pattern:** Output structure doesn't match expected.

**Example:**
```python
assert isinstance(result, list)
# AssertionError: assert False (result is dict)
```

**Analysis:**
- Expected: list
- Actual: dict
- Check: Return type, data structure conversion

### Side Effect Failure

**Pattern:** Expected side effect doesn't occur.

**Example:**
```python
def test_save_user():
    save_user(user)
    assert user_exists(user.id)
# AssertionError: assert False
```

**Analysis:**
- Expected: User saved to database
- Actual: User not found
- Check: Persistence logic, transaction commit, error handling

### State Pollution

**Pattern:** Test fails due to previous test's state.

**Example:**
```python
def test_counter():
    counter = get_counter()
    assert counter == 0
# AssertionError: assert 5 == 0 (from previous test)
```

**Analysis:**
- Issue: Shared state between tests
- Check: Test isolation, setup/teardown, global variables

## Flaky Tests

### Timing-Dependent

**Pattern:** Test passes/fails based on timing.

**Example:**
```python
def test_async_operation():
    start_operation()
    time.sleep(0.1)  # Hope it's done
    assert is_complete()
# Sometimes passes, sometimes fails
```

**Analysis:**
- Issue: Race condition, insufficient wait
- Check: Async handling, proper synchronization

### Order-Dependent

**Pattern:** Test result depends on execution order.

**Example:**
```python
def test_a():
    global_state = 1

def test_b():
    assert global_state == 0  # Fails if test_a runs first
```

**Analysis:**
- Issue: Test interdependence
- Check: Shared state, test isolation

## Analysis Workflow by Failure Type

### For Assertion Failures:
1. Extract expected and actual values
2. Identify discrepancy type (value, type, structure)
3. Trace code path to assertion
4. Find where actual value is computed
5. Check computation logic

### For Exception Failures:
1. Identify exception type and message
2. Extract stack trace
3. Find where exception raised
4. Check if exception expected or bug
5. Analyze error handling

### For Timeout Failures:
1. Identify timeout duration
2. Check for infinite loops
3. Analyze algorithm complexity
4. Look for blocking operations
5. Profile performance

### For Unexpected Behavior:
1. Define expected behavior clearly
2. Observe actual behavior
3. Identify divergence point
4. Trace execution to divergence
5. Analyze logic at divergence

## Failure Message Patterns

### Pytest Patterns

```python
# Value mismatch
"AssertionError: assert 3 == 5"

# Collection mismatch
"AssertionError: assert [1, 2] == [1, 2, 3]"

# Exception mismatch
"Failed: DID NOT RAISE ValueError"

# Timeout
"TIMEOUT after 5.0 seconds"
```

### JUnit Patterns

```java
// Assertion failure
"expected:<5> but was:<3>"

// Exception failure
"Expected exception: java.lang.IllegalArgumentException"

// Null pointer
"java.lang.NullPointerException at line 42"
```

### Jest Patterns

```javascript
// Matcher failure
"Expected: 5, Received: 3"

// Undefined
"TypeError: Cannot read property 'x' of undefined"

// Async timeout
"Timeout - Async callback was not invoked within 5000ms"
```

## Quick Reference

| Failure Type | Key Indicator | First Check |
|--------------|---------------|-------------|
| Assertion | "assert X == Y" | Compare X and Y |
| Exception | Exception name | Stack trace |
| Timeout | "TIMEOUT" | Loop conditions |
| Wrong type | "isinstance" | Type conversions |
| Missing value | "None" | Return statements |
| Side effect | State check fails | Mutation operations |
| Flaky | Intermittent | Timing, state |
