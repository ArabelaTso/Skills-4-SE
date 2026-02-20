---
name: test-guided-bug-detector
description: Analyze failing tests to detect functional bugs in code. Takes repository and failing test output as input, analyzes execution behavior, assertions, and stack traces to identify suspicious code regions and root causes. Use when debugging test failures, investigating regression bugs, or understanding why tests fail. Explains the bug mechanism, identifies affected code, and suggests fixes based on test expectations vs actual behavior.
---

# Test-Guided Bug Detector

Analyze failing tests to detect and explain functional bugs in code.

## Overview

When tests fail, they provide valuable clues about bugs in the code. This skill analyzes:

1. **Test failure output** - Error messages, stack traces, assertion failures
2. **Test expectations** - What the test expects to happen
3. **Actual behavior** - What actually happened
4. **Code execution path** - Which code was executed
5. **Suspicious patterns** - Common bug patterns that match the failure

The goal is to identify the root cause bug and explain why the test exposes it.

## Bug Detection Workflow

```
Failing Test Output
    ↓
Parse Failure Information
    ↓
Identify Test Expectations
    ↓
Trace Execution Path
    ↓
Analyze Discrepancy
    ↓
Identify Suspicious Code
    ↓
Explain Bug Mechanism
    ↓
Suggest Fix
```

## Analysis Process

### Step 1: Parse Test Failure

Extract key information from test output:

**What to extract:**
- Test name and location
- Failure type (assertion, exception, timeout, etc.)
- Expected vs actual values
- Stack trace
- Error messages

**Example:**
```
FAILED tests/test_calculator.py::test_divide - AssertionError: assert 0 == 5
Expected: 5
Actual: 0

Stack trace:
  File "tests/test_calculator.py", line 15, in test_divide
    assert divide(10, 2) == 5
  File "src/calculator.py", line 8, in divide
    return a // b
```

### Step 2: Understand Test Intent

Determine what the test is trying to verify:

**Questions to answer:**
- What functionality is being tested?
- What are the inputs?
- What is the expected output?
- What properties should hold?

**Example:**
```python
def test_divide():
    # Intent: Verify division returns correct result
    result = divide(10, 2)
    assert result == 5  # Expects 10 / 2 = 5
```

### Step 3: Trace Execution Path

Follow the code path from test to failure:

**Trace elements:**
- Function calls in stack trace
- Control flow decisions
- Data transformations
- Return values

**Example trace:**
```
test_divide()
  → divide(10, 2)
    → return a // b  (integer division)
    → returns 5
  → assert 5 == 5  ✓ Should pass!
```

### Step 4: Identify Discrepancy

Find where expected and actual diverge:

**Common discrepancies:**
- Wrong operator (// vs /)
- Off-by-one errors
- Null/None handling
- Type mismatches
- Logic errors

**Example:**
```python
# Expected: 10 / 2 = 5.0
# Actual: 10 // 2 = 5 (but test got 0?)
# Discrepancy: Something else is wrong!
```

### Step 5: Analyze Suspicious Code

Examine code for bug patterns:

**Bug patterns to check:**
- Uninitialized variables
- Wrong operators
- Missing return statements
- Incorrect conditions
- Edge case handling

**Example analysis:**
```python
def divide(a, b):
    result = 0  # BUG: Initialized but never updated!
    return a // b  # This line is unreachable? No, wait...
    # Actually, this returns correctly, but...
```

### Step 6: Explain Bug Mechanism

Describe how the bug causes the failure:

**Explanation structure:**
1. What the code does
2. What it should do
3. Why there's a mismatch
4. How the test exposes it

### Step 7: Suggest Fix

Propose concrete fix with explanation:

**Fix components:**
- Code change
- Why it fixes the bug
- How to verify the fix

## Common Bug Patterns

For detailed bug patterns and detection strategies, see [references/bug_patterns.md](references/bug_patterns.md).

Categories include:
- Logic errors (wrong operators, conditions)
- State management (uninitialized, stale state)
- Boundary conditions (off-by-one, edge cases)
- Type errors (implicit conversions, null handling)
- Concurrency bugs (race conditions, deadlocks)

## Failure Type Analysis

For analyzing different types of test failures, see [references/failure_types.md](references/failure_types.md).

Failure types:
- Assertion failures
- Exceptions and errors
- Timeouts
- Unexpected behavior
- Flaky tests

## Example Analysis

**Input: Failing test**

```python
# Test file: tests/test_list_utils.py
def test_remove_duplicates():
    input_list = [1, 2, 2, 3, 3, 3, 4]
    result = remove_duplicates(input_list)
    assert result == [1, 2, 3, 4]
    assert input_list == [1, 2, 2, 3, 3, 3, 4]  # Original unchanged

# Test output:
# FAILED - AssertionError: assert [1, 2, 3, 4] == [1, 2, 2, 3, 3, 3, 4]
# The second assertion failed!

# Implementation: src/list_utils.py
def remove_duplicates(lst):
    seen = set()
    i = 0
    while i < len(lst):
        if lst[i] in seen:
            lst.pop(i)  # BUG: Modifies input list!
        else:
            seen.add(lst[i])
            i += 1
    return lst
```

**Output: Bug analysis**

```markdown
# Bug Analysis Report

## Test Failure Summary

**Test:** test_remove_duplicates
**Location:** tests/test_list_utils.py:2
**Failure Type:** Assertion failure
**Failed Assertion:** `assert input_list == [1, 2, 2, 3, 3, 3, 4]`

## Expected vs Actual

**Expected:** Original list unchanged: `[1, 2, 2, 3, 3, 3, 4]`
**Actual:** Original list modified: `[1, 2, 3, 4]`

## Root Cause

**Bug Location:** src/list_utils.py:7
**Bug Type:** Unintended side effect (input mutation)

**Problematic Code:**
```python
lst.pop(i)  # Modifies the input list directly
```

## Bug Mechanism

1. **What happens:** The function modifies the input list in-place using `lst.pop(i)`
2. **Why it's wrong:** The test expects the original list to remain unchanged
3. **How test exposes it:** Second assertion checks that input_list is unmodified
4. **Why it fails:** Since Python passes lists by reference, modifications to `lst`
   affect the original `input_list`

## Execution Trace

```
test_remove_duplicates()
  input_list = [1, 2, 2, 3, 3, 3, 4]
  ↓
  remove_duplicates(input_list)  # lst points to same list as input_list
    i=0: lst[0]=1, not in seen, add to seen, i=1
    i=1: lst[1]=2, not in seen, add to seen, i=2
    i=2: lst[2]=2, in seen, lst.pop(2)  # Removes from input_list!
    # Now lst = input_list = [1, 2, 3, 3, 3, 4]
    i=2: lst[2]=3, not in seen, add to seen, i=3
    i=3: lst[3]=3, in seen, lst.pop(3)  # Removes from input_list!
    # Now lst = input_list = [1, 2, 3, 3, 4]
    i=3: lst[3]=3, in seen, lst.pop(3)  # Removes from input_list!
    # Now lst = input_list = [1, 2, 3, 4]
    i=3: lst[3]=4, not in seen, add to seen, i=4
    return lst  # Returns [1, 2, 3, 4]
  ↓
  result = [1, 2, 3, 4]  ✓ First assertion passes
  input_list = [1, 2, 3, 4]  ✗ Second assertion fails!
```

## Suspicious Code Regions

### Primary Suspect: src/list_utils.py:7
```python
lst.pop(i)  # Direct mutation of input
```
**Suspicion Level:** HIGH
**Reason:** Modifies input list, violating immutability expectation

### Secondary Suspect: src/list_utils.py:11
```python
return lst  # Returns reference to modified input
```
**Suspicion Level:** MEDIUM
**Reason:** Returns same object as input, not a new list

## Recommended Fix

**Option 1: Create a copy (Recommended)**
```python
def remove_duplicates(lst):
    result = []  # Create new list
    seen = set()
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```

**Why this fixes it:**
- Creates new list instead of modifying input
- Original list remains unchanged
- Clearer intent

**Option 2: Explicit copy**
```python
def remove_duplicates(lst):
    lst = lst.copy()  # Work on a copy
    seen = set()
    i = 0
    while i < len(lst):
        if lst[i] in seen:
            lst.pop(i)
        else:
            seen.add(lst[i])
            i += 1
    return lst
```

**Why this fixes it:**
- `lst.copy()` creates a shallow copy
- Modifications don't affect original
- Preserves original algorithm structure

## Verification

To verify the fix:
1. Run the failing test: `pytest tests/test_list_utils.py::test_remove_duplicates`
2. Both assertions should pass
3. Add additional test for immutability:
```python
def test_remove_duplicates_immutable():
    original = [1, 2, 2, 3]
    original_copy = original.copy()
    result = remove_duplicates(original)
    assert original == original_copy  # Verify no mutation
```

## Related Issues

This bug could affect:
- Any code that assumes `remove_duplicates` doesn't modify input
- Functions that reuse the input list after calling `remove_duplicates`
- Concurrent code where multiple threads access the same list
```

## Analysis Strategies

For detailed analysis strategies by language and framework, see [references/analysis_strategies.md](references/analysis_strategies.md).

Strategies include:
- Python (pytest, unittest)
- JavaScript (Jest, Mocha)
- Java (JUnit)
- C/C++ (Google Test)
- Go (testing package)

## Best Practices

1. **Start with the failure message** - It often points directly to the bug
2. **Understand test intent** - Know what should happen
3. **Trace execution carefully** - Follow the actual code path
4. **Look for common patterns** - Many bugs follow known patterns
5. **Consider edge cases** - Bugs often hide at boundaries
6. **Check assumptions** - Verify what the code assumes
7. **Explain clearly** - Make the bug mechanism understandable

## Red Flags

Watch for these suspicious patterns:

**High-priority red flags:**
- Uninitialized variables
- Missing return statements
- Wrong operators (==  vs =, // vs /)
- Off-by-one errors (< vs <=)
- Null/None without checks
- Mutable default arguments
- Side effects in pure functions

**Medium-priority warnings:**
- Complex conditionals
- Nested loops with breaks
- Exception swallowing
- Type conversions
- Global state access

## Report Template

```markdown
# Bug Analysis Report

## Test Failure Summary
- Test name and location
- Failure type
- Failed assertion/error

## Expected vs Actual
- What should happen
- What actually happened

## Root Cause
- Bug location (file:line)
- Bug type
- Problematic code snippet

## Bug Mechanism
- Step-by-step explanation
- Why it's wrong
- How test exposes it

## Execution Trace
- Detailed trace from test to failure
- Variable values at key points

## Suspicious Code Regions
- Primary suspects with evidence
- Secondary suspects

## Recommended Fix
- Proposed code change
- Explanation of why it fixes the bug
- How to verify

## Related Issues
- Other code that might be affected
```

## Additional Resources

For detailed guidance:
- [Bug Patterns](references/bug_patterns.md) - Common bug patterns and detection
- [Failure Types](references/failure_types.md) - Analyzing different failure types
- [Analysis Strategies](references/analysis_strategies.md) - Language-specific strategies
