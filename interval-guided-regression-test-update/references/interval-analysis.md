# Interval Analysis Concepts

## What are Intervals?

Intervals represent ranges of values that variables can take during program execution. They are used for:
- **Static analysis**: Determining possible value ranges without execution
- **Test coverage**: Ensuring tests exercise different value ranges
- **Regression testing**: Maintaining coverage when code changes

### Types of Intervals

**Numeric intervals:**
```
x ∈ [0, 10]      # x is between 0 and 10
y ∈ (-∞, 5]      # y is at most 5
z ∈ [1, ∞)       # z is at least 1
```

**Symbolic intervals:**
```
x ∈ [min, max]   # x bounded by symbolic values
y ∈ [0, n-1]     # y is array index
```

**Conditional intervals:**
```
if (x > 0):
    x ∈ (0, ∞)   # x is positive in this branch
else:
    x ∈ (-∞, 0]  # x is non-positive in this branch
```

## Extracting Interval Information

### Static Analysis

**Abstract interpretation:**
```python
def analyze_intervals(code):
    intervals = {}

    # Example: x = input(); if x > 0: ...
    # Before if: x ∈ (-∞, ∞)
    # True branch: x ∈ (0, ∞)
    # False branch: x ∈ (-∞, 0]

    return intervals
```

**Constraint solving:**
```python
# From code: if (x > 5 and x < 10)
# Derive: x ∈ (5, 10)
```

### Dynamic Analysis

**Profiling:**
```python
def profile_intervals(program, test_inputs):
    observed_ranges = {}

    for test_input in test_inputs:
        values = execute_and_track(program, test_input)
        update_ranges(observed_ranges, values)

    return observed_ranges
```

**Symbolic execution:**
```python
def symbolic_intervals(program):
    # Execute with symbolic values
    # Track constraints on variables
    # Derive interval constraints
    return interval_constraints
```

## Interval Coverage

### Coverage Metrics

**Interval coverage:**
```
Coverage = (Covered intervals) / (Total intervals)
```

**Example:**
```python
def process(x):
    if x < 0:      # Interval: (-∞, 0)
        return -x
    elif x < 10:   # Interval: [0, 10)
        return x * 2
    else:          # Interval: [10, ∞)
        return x + 10

# Test with x=5 covers [0, 10)
# Test with x=15 covers [10, ∞)
# Test with x=-3 covers (-∞, 0)
# Total coverage: 3/3 = 100%
```

### Interval Partitioning

**Equivalence partitioning:**
```
Function: sqrt(x)
Intervals:
- x < 0: Invalid (error)
- x = 0: Boundary
- 0 < x < 1: Small positive
- x ≥ 1: Large positive

Tests needed: One per interval
```

**Boundary value analysis:**
```
For interval [a, b]:
Test values: a-1, a, a+1, b-1, b, b+1
```

## Interval Changes in Updated Code

### New Intervals

**Code change:**
```python
# Old version
def process(x):
    if x < 10:
        return x * 2
    else:
        return x + 10

# New version (added interval)
def process(x):
    if x < 0:      # NEW interval
        return -x
    elif x < 10:
        return x * 2
    else:
        return x + 10
```

**Impact:** Need test for x < 0

### Modified Intervals

**Code change:**
```python
# Old: if x < 10
# New: if x < 20

# Old interval: [0, 10)
# New interval: [0, 20)
```

**Impact:** Existing tests may need adjustment

### Removed Intervals

**Code change:**
```python
# Old version
def process(x):
    if x < 0:
        return -x
    elif x < 10:
        return x * 2
    else:
        return x + 10

# New version (removed interval)
def process(x):
    if x < 10:     # Merged x < 0 case
        return x * 2
    else:
        return x + 10
```

**Impact:** Tests for x < 0 may be redundant

## Interval-Based Test Generation

### Input Selection

**Cover each interval:**
```python
def generate_test_inputs(intervals):
    test_inputs = []

    for interval in intervals:
        # Pick representative value from interval
        if interval.is_bounded():
            value = interval.midpoint()
        else:
            value = interval.representative_value()

        test_inputs.append(value)

    return test_inputs
```

**Example:**
```python
# Intervals: (-∞, 0), [0, 10), [10, ∞)
# Test inputs: -5, 5, 15
```

### Assertion Generation

**Expected behavior per interval:**
```python
def generate_assertions(function, intervals):
    assertions = []

    for interval, test_input in zip(intervals, test_inputs):
        expected = compute_expected(function, interval, test_input)
        assertions.append(f"assert {function}({test_input}) == {expected}")

    return assertions
```

## Interval Coverage Analysis

### Computing Coverage

```python
def compute_interval_coverage(tests, program_intervals):
    covered_intervals = set()

    for test in tests:
        # Execute test and track which intervals are covered
        intervals = execute_and_track_intervals(test)
        covered_intervals.update(intervals)

    coverage = len(covered_intervals) / len(program_intervals)
    return coverage, covered_intervals
```

### Identifying Gaps

```python
def find_coverage_gaps(program_intervals, covered_intervals):
    uncovered = program_intervals - covered_intervals
    under_covered = find_under_covered(program_intervals, covered_intervals)

    return {
        'uncovered': uncovered,
        'under_covered': under_covered
    }
```

## Practical Examples

### Example 1: Numeric Function

```python
def classify_number(x):
    if x < 0:
        return "negative"
    elif x == 0:
        return "zero"
    elif x < 100:
        return "small positive"
    else:
        return "large positive"

# Intervals:
# 1. (-∞, 0)
# 2. {0}
# 3. (0, 100)
# 4. [100, ∞)

# Test suite:
assert classify_number(-5) == "negative"    # Covers interval 1
assert classify_number(0) == "zero"         # Covers interval 2
assert classify_number(50) == "small positive"  # Covers interval 3
assert classify_number(150) == "large positive" # Covers interval 4
```

### Example 2: Array Index

```python
def get_element(arr, index):
    if index < 0:
        raise IndexError("negative index")
    elif index >= len(arr):
        raise IndexError("index out of bounds")
    else:
        return arr[index]

# Intervals (for arr of length n):
# 1. (-∞, 0)
# 2. [0, n)
# 3. [n, ∞)

# Test suite:
arr = [1, 2, 3, 4, 5]
# Test interval 1
with pytest.raises(IndexError):
    get_element(arr, -1)

# Test interval 2
assert get_element(arr, 2) == 3

# Test interval 3
with pytest.raises(IndexError):
    get_element(arr, 10)
```

### Example 3: String Length

```python
def validate_password(password):
    if len(password) < 8:
        return "too short"
    elif len(password) > 20:
        return "too long"
    else:
        return "valid"

# Intervals:
# 1. [0, 8)
# 2. [8, 20]
# 3. (20, ∞)

# Test suite:
assert validate_password("abc") == "too short"      # Interval 1
assert validate_password("password123") == "valid"  # Interval 2
assert validate_password("a" * 25) == "too long"    # Interval 3
```

## Tools for Interval Analysis

### Static Analysis Tools

- **KLEE**: Symbolic execution for C/C++
- **Pex**: Symbolic execution for .NET
- **Infer**: Static analyzer with interval analysis
- **Frama-C**: Value analysis for C

### Dynamic Analysis Tools

- **Daikon**: Invariant detection from execution traces
- **Valgrind**: Memory and value tracking
- **Coverage.py**: Python coverage with value tracking

### Custom Analysis

```python
import ast

class IntervalAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.intervals = {}

    def visit_If(self, node):
        # Extract condition
        # Derive intervals for true/false branches
        pass

    def visit_Compare(self, node):
        # Extract comparison: x < 10
        # Derive interval: x ∈ (-∞, 10)
        pass
```
