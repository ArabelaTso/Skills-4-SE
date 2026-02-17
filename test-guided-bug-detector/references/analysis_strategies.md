# Analysis Strategies by Language and Framework

Language and framework-specific strategies for analyzing test failures.

## Python

### pytest

**Failure output format:**
```
FAILED tests/test_module.py::test_function - AssertionError: assert X == Y
```

**Analysis strategy:**
1. Parse test location: `tests/test_module.py::test_function`
2. Extract failure type: `AssertionError`
3. Extract comparison: `assert X == Y`
4. Read test code to understand intent
5. Trace execution in implementation

**Common patterns:**
```python
# Assertion with message
assert result == expected, f"Expected {expected}, got {result}"

# Exception testing
with pytest.raises(ValueError):
    function_call()

# Approximate comparison
assert result == pytest.approx(3.14, rel=1e-2)

# Parametrized tests
@pytest.mark.parametrize("input,expected", [...])
```

**Stack trace analysis:**
```
tests/test_module.py:15: in test_function
    assert divide(10, 2) == 5
src/module.py:8: in divide
    return a // b
```
- Start at test (line 15)
- Follow to implementation (line 8)
- Check implementation logic

### unittest

**Failure output format:**
```
FAIL: test_function (tests.test_module.TestClass)
AssertionError: 3 != 5
```

**Analysis strategy:**
1. Identify test class and method
2. Extract assertion type
3. Check assertion methods used
4. Trace to implementation

**Common assertions:**
```python
self.assertEqual(a, b)
self.assertTrue(condition)
self.assertRaises(Exception, func)
self.assertIn(item, collection)
```

## JavaScript

### Jest

**Failure output format:**
```
FAIL tests/module.test.js
  ● test function
    expect(received).toBe(expected)
    Expected: 5
    Received: 3
```

**Analysis strategy:**
1. Parse test file and test name
2. Extract matcher used (toBe, toEqual, etc.)
3. Compare expected vs received
4. Check implementation

**Common matchers:**
```javascript
expect(value).toBe(5)              // Strict equality
expect(value).toEqual({a: 1})      // Deep equality
expect(fn).toThrow(Error)          // Exception
expect(value).toBeNull()           // Null check
expect(array).toContain(item)      // Membership
```

**Async test failures:**
```javascript
// Timeout
"Timeout - Async callback was not invoked"

// Unhandled promise rejection
"UnhandledPromiseRejectionWarning"
```

### Mocha

**Failure output format:**
```
1) test function:
   AssertionError: expected 3 to equal 5
```

**Analysis strategy:**
1. Parse test description
2. Extract assertion library used (chai, assert)
3. Analyze expectation
4. Trace to implementation

**Common patterns:**
```javascript
// Chai expect
expect(value).to.equal(5)
expect(array).to.have.lengthOf(3)
expect(fn).to.throw(Error)

// Chai assert
assert.equal(actual, expected)
assert.isTrue(condition)
```

## Java

### JUnit

**Failure output format:**
```
org.junit.ComparisonFailure: expected:<5> but was:<3>
    at TestClass.testMethod(TestClass.java:15)
    at Module.method(Module.java:42)
```

**Analysis strategy:**
1. Parse exception type (ComparisonFailure, AssertionError)
2. Extract expected and actual values
3. Follow stack trace
4. Check implementation at indicated line

**Common assertions:**
```java
assertEquals(expected, actual)
assertTrue(condition)
assertThrows(Exception.class, () -> method())
assertNull(value)
assertArrayEquals(expected, actual)
```

**Hamcrest matchers:**
```java
assertThat(value, is(5))
assertThat(list, hasSize(3))
assertThat(string, containsString("text"))
```

## C/C++

### Google Test

**Failure output format:**
```
test_module.cpp:15: Failure
Expected equality of these values:
  result
    Which is: 3
  5
```

**Analysis strategy:**
1. Parse file and line number
2. Extract compared values
3. Check test macro used
4. Trace to implementation

**Common macros:**
```cpp
EXPECT_EQ(expected, actual)
EXPECT_TRUE(condition)
EXPECT_THROW(statement, exception)
EXPECT_NEAR(val1, val2, abs_error)
ASSERT_EQ(expected, actual)  // Fatal
```

**Death tests:**
```cpp
EXPECT_DEATH(statement, regex)
// Tests that code terminates
```

## Go

### testing package

**Failure output format:**
```
--- FAIL: TestFunction (0.00s)
    module_test.go:15: Expected 5, got 3
```

**Analysis strategy:**
1. Parse test function name
2. Extract file and line
3. Read error message
4. Check implementation

**Common patterns:**
```go
if result != expected {
    t.Errorf("Expected %v, got %v", expected, result)
}

if err != nil {
    t.Fatalf("Unexpected error: %v", err)
}
```

**Table-driven tests:**
```go
tests := []struct {
    input    int
    expected int
}{
    {1, 2},
    {2, 4},
}
for _, tt := range tests {
    result := function(tt.input)
    if result != tt.expected {
        t.Errorf("...")
    }
}
```

## Analysis Workflow

### Step 1: Parse Test Output

**Extract:**
- Test name and location
- Failure type
- Expected vs actual values
- Stack trace
- Error messages

### Step 2: Understand Test Intent

**Questions:**
- What is being tested?
- What are the inputs?
- What is the expected behavior?
- What assertions are made?

### Step 3: Trace Execution

**Follow:**
- Test setup
- Function calls
- Implementation logic
- Return path

### Step 4: Identify Discrepancy

**Compare:**
- Expected behavior
- Actual behavior
- Where they diverge

### Step 5: Locate Bug

**Check:**
- Implementation at divergence point
- Related functions
- State management
- Edge case handling

### Step 6: Explain and Fix

**Provide:**
- Bug description
- Why test exposes it
- Proposed fix
- Verification steps

## Framework-Specific Tips

### pytest
- Use `-v` for verbose output
- Use `--tb=short` for concise tracebacks
- Use `-x` to stop at first failure
- Use `--pdb` to drop into debugger

### Jest
- Use `--verbose` for detailed output
- Use `--no-coverage` to speed up
- Use `.only` to run single test
- Check for async/await issues

### JUnit
- Check for test isolation issues
- Verify @Before/@After methods
- Look for static state
- Check exception handling

### Google Test
- Use `--gtest_filter` to run specific tests
- Check for memory leaks with valgrind
- Verify pointer handling
- Check for undefined behavior

## Common Pitfalls

### All Languages

1. **Floating point comparison** - Use approximate equality
2. **Async timing** - Proper synchronization needed
3. **Test isolation** - Clean up state between tests
4. **Mocking issues** - Verify mocks match real behavior
5. **Environment dependencies** - File system, network, time

### Language-Specific

**Python:**
- Mutable default arguments
- Reference vs copy
- Integer division (Python 2 vs 3)

**JavaScript:**
- Callback hell
- Promise rejection handling
- `this` binding issues

**Java:**
- Null pointer exceptions
- Autoboxing issues
- Concurrent modification

**C/C++:**
- Memory leaks
- Buffer overflows
- Undefined behavior

**Go:**
- Goroutine leaks
- Channel deadlocks
- Nil pointer dereference
