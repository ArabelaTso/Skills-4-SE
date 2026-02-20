---
name: interval-guided-regression-test-update
description: Automatically updates regression tests based on interval analysis to maintain coverage of key program intervals. Use when code changes affect value ranges, conditionals, or control flow, and existing tests need updating to maintain interval coverage. Analyzes interval information from updated code, identifies coverage gaps, adjusts test inputs and assertions, removes redundant tests, and generates new tests for uncovered intervals. Supports Python, Java, JavaScript, and C/C++ with various test frameworks (pytest, JUnit, Jest, Google Test).
---

# Interval-Guided Regression Test Update

Automatically update regression tests to maintain interval coverage when program code changes.

## Core Concept

**Intervals** represent ranges of values that variables can take during execution. When code changes, intervals may be added, removed, or modified. This skill ensures regression tests continue to cover all important intervals.

**Example:**
```python
# Old code
def process(x):
    if x < 10:
        return x * 2
    else:
        return x + 10

# Intervals: [0, 10), [10, ∞)

# New code (added negative handling)
def process(x):
    if x < 0:
        return -x
    elif x < 10:
        return x * 2
    else:
        return x + 10

# Intervals: (-∞, 0), [0, 10), [10, ∞)
# Need to add test for new interval: x < 0
```

## Workflow

### 1. Analyze Existing Tests

Parse the current regression test suite:
- Identify test inputs
- Determine which intervals each test covers
- Calculate current interval coverage

```python
# Example test analysis
test_process_small: input=5, covers [0, 10)
test_process_large: input=15, covers [10, ∞)
# Coverage: 2/2 intervals = 100%
```

### 2. Extract Interval Information

Obtain interval information from the updated program:

**From static analysis:**
- Parse conditionals (if, switch, etc.)
- Extract comparison operators
- Derive interval constraints

**From profiling:**
- Run existing tests
- Track observed value ranges
- Identify intervals exercised

**From symbolic execution:**
- Execute with symbolic values
- Collect path constraints
- Derive interval constraints

See [references/interval-analysis.md](references/interval-analysis.md) for detailed extraction methods.

### 3. Identify Coverage Gaps

Compare current coverage with new intervals:

```python
old_intervals = {[0, 10), [10, ∞)}
new_intervals = {(-∞, 0), [0, 10), [10, ∞)}

added_intervals = {(-∞, 0)}  # Need new test
removed_intervals = {}
modified_intervals = {}
```

### 4. Update Tests

Apply appropriate update strategies:

**Add tests for new intervals:**
```python
# New test for (-∞, 0)
def test_process_negative():
    assert process(-5) == 5
```

**Adjust inputs for modified intervals:**
```python
# If boundary changed from x < 10 to x < 20
# Old: test_process_large with input=15
# New: test_process_large with input=25
```

**Update assertions for changed behavior:**
```python
# If logic changed
# Old: assert process(5) == 10
# New: assert process(5) == 15
```

**Remove redundant tests:**
```python
# If intervals merged, remove duplicate coverage
```

See [references/test-update-strategies.md](references/test-update-strategies.md) for detailed strategies.

### 5. Validate Updated Tests

Run the updated test suite:
- Execute all tests
- Verify all pass
- Check interval coverage
- Identify any remaining gaps

### 6. Generate Coverage Report

Provide comprehensive summary:
- Before/after interval coverage
- Tests added, modified, removed
- Validation results
- Remaining gaps (if any)

## Quick Start Examples

### Example 1: New Interval Added

**Scenario:** Function adds handling for negative numbers

**Original code:**
```python
def abs_double(x):
    if x < 10:
        return x * 2
    else:
        return x + 10
```

**Original tests:**
```python
def test_small():
    assert abs_double(5) == 10

def test_large():
    assert abs_double(15) == 25
```

**Updated code:**
```python
def abs_double(x):
    if x < 0:
        return -x * 2
    elif x < 10:
        return x * 2
    else:
        return x + 10
```

**Updated tests:**
```python
def test_negative():  # NEW
    assert abs_double(-5) == 10

def test_small():
    assert abs_double(5) == 10

def test_large():
    assert abs_double(15) == 25
```

**Summary:**
- Added interval: (-∞, 0)
- Added test: test_negative
- Coverage: 2/2 → 3/3 (100%)

### Example 2: Interval Boundary Changed

**Scenario:** Threshold value modified

**Original code:**
```python
def categorize(score):
    if score < 60:
        return "fail"
    else:
        return "pass"
```

**Original tests:**
```python
def test_fail():
    assert categorize(50) == "fail"

def test_pass():
    assert categorize(70) == "pass"
```

**Updated code:**
```python
def categorize(score):
    if score < 50:  # Changed from 60
        return "fail"
    else:
        return "pass"
```

**Updated tests:**
```python
def test_fail():
    assert categorize(40) == "fail"  # Changed input from 50

def test_pass():
    assert categorize(60) == "pass"  # Changed input from 70
```

**Summary:**
- Modified interval: [0, 60) → [0, 50)
- Modified interval: [60, ∞) → [50, ∞)
- Updated 2 test inputs
- Coverage: 2/2 → 2/2 (100%)

### Example 3: Intervals Merged

**Scenario:** Simplified logic combines cases

**Original code:**
```python
def classify(x):
    if x < 0:
        return "negative"
    elif x == 0:
        return "zero"
    else:
        return "positive"
```

**Original tests:**
```python
def test_negative():
    assert classify(-5) == "negative"

def test_zero():
    assert classify(0) == "zero"

def test_positive():
    assert classify(5) == "positive"
```

**Updated code:**
```python
def classify(x):
    if x <= 0:
        return "non-positive"
    else:
        return "positive"
```

**Updated tests:**
```python
def test_non_positive():  # Merged
    assert classify(-5) == "non-positive"
    assert classify(0) == "non-positive"

def test_positive():
    assert classify(5) == "positive"
```

**Summary:**
- Merged intervals: (-∞, 0) and {0} → (-∞, 0]
- Removed test: test_zero (redundant)
- Updated test: test_negative → test_non_positive
- Coverage: 3/3 → 2/2 (100%)

## Update Strategies

### Strategy 1: Input Adjustment

Modify test inputs to cover new or changed intervals.

**When to use:**
- New interval added
- Interval boundary changed
- Need to cover previously uncovered interval

**How:**
1. Identify target interval
2. Select representative value from interval
3. Update test input
4. Verify test still valid

### Strategy 2: Assertion Update

Modify expected values when behavior changes.

**When to use:**
- Logic changed within interval
- Return value modified
- Side effects changed

**How:**
1. Execute test with new code
2. Observe actual output
3. Verify output is correct
4. Update assertion

### Strategy 3: Test Removal

Remove redundant or obsolete tests.

**When to use:**
- Intervals merged
- Multiple tests cover same interval
- Interval no longer exists

**How:**
1. Identify redundant tests
2. Keep most representative test
3. Remove others
4. Verify coverage maintained

### Strategy 4: Test Generation

Create new tests for uncovered intervals.

**When to use:**
- New interval added
- Coverage gap identified
- No existing test covers interval

**How:**
1. Identify uncovered interval
2. Generate representative input
3. Determine expected output
4. Create new test

## Coverage Analysis

### Computing Coverage

```
Interval Coverage = (Covered Intervals) / (Total Intervals) × 100%
```

**Example:**
```
Total intervals: 4
Covered by tests: 3
Coverage: 75%
```

### Coverage Report Format

```
Interval Coverage Report
========================

Before Update:
- Total intervals: 2
- Covered intervals: 2
- Coverage: 100%

After Update:
- Total intervals: 3
- Covered intervals: 3
- Coverage: 100%

Changes:
- Added intervals: 1
- Removed intervals: 0
- Modified intervals: 0

Test Changes:
- Added tests: 1
- Modified tests: 0
- Removed tests: 0
```

## Best Practices

### Minimize Changes

- Only update tests affected by code changes
- Preserve tests that still provide value
- Avoid unnecessary rewrites

### Maintain Test Quality

- Use descriptive test names
- Keep tests simple and focused
- Document why tests were updated

### Validate Thoroughly

- Run all tests after updates
- Check coverage metrics
- Verify no regressions

### Document Changes

- Record what changed and why
- Note any manual adjustments
- Track coverage improvements

## Common Scenarios

### Scenario 1: Refactoring with Logic Change

**Problem:** Code refactored, some logic changed

**Solution:**
1. Extract intervals from new code
2. Compare with old intervals
3. Update tests for changed intervals
4. Verify all tests pass

### Scenario 2: Feature Addition

**Problem:** New feature adds new code paths

**Solution:**
1. Identify new intervals
2. Generate tests for new intervals
3. Ensure existing tests still valid
4. Verify complete coverage

### Scenario 3: Bug Fix

**Problem:** Bug fix changes behavior in specific interval

**Solution:**
1. Identify affected interval
2. Update test for that interval
3. Add regression test if needed
4. Verify fix doesn't break other intervals

## Troubleshooting

### Tests Fail After Update

**Check:**
- Assertions match new behavior
- Inputs are valid for new code
- Expected values are correct

**Solution:**
- Review code changes carefully
- Execute tests manually
- Update assertions as needed

### Coverage Decreased

**Check:**
- New intervals added
- Tests removed incorrectly
- Intervals not properly identified

**Solution:**
- Identify uncovered intervals
- Generate missing tests
- Verify interval extraction

### Redundant Tests

**Check:**
- Multiple tests cover same interval
- Intervals merged in new code

**Solution:**
- Identify redundant tests
- Keep most representative
- Remove duplicates

## References

- **[interval-analysis.md](references/interval-analysis.md)**: Comprehensive guide to interval concepts, extraction methods, and coverage analysis
- **[test-update-strategies.md](references/test-update-strategies.md)**: Detailed strategies for updating tests including input adjustment, assertion updates, and test generation

## Tips

- **Start with coverage analysis**: Understand current coverage before making changes
- **Use interval extraction tools**: Leverage static analysis or profiling tools
- **Update incrementally**: Make one change at a time and validate
- **Preserve test intent**: Keep the purpose of each test clear
- **Document assumptions**: Note any assumptions about intervals
- **Validate coverage**: Always verify coverage after updates
