# Test Update Strategies

## Overview

When program code changes, regression tests must be updated to maintain interval coverage and correctness.

## Update Strategies

### 1. Input Adjustment

Modify test inputs to cover new or changed intervals.

**Scenario: New interval added**

```python
# Old code
def process(x):
    if x < 10:
        return x * 2
    else:
        return x + 10

# Old test
assert process(5) == 10   # Covers [0, 10)
assert process(15) == 25  # Covers [10, ∞)

# New code (added negative handling)
def process(x):
    if x < 0:
        return -x
    elif x < 10:
        return x * 2
    else:
        return x + 10

# Updated test suite
assert process(-5) == 5   # NEW: Covers (-∞, 0)
assert process(5) == 10   # Covers [0, 10)
assert process(15) == 25  # Covers [10, ∞)
```

**Scenario: Interval boundary changed**

```python
# Old code: if x < 10
# New code: if x < 20

# Old test
assert process(5) == 10   # Was in [0, 10)
assert process(15) == 25  # Was in [10, ∞)

# Updated test
assert process(5) == 10   # Still in [0, 20)
assert process(15) == 30  # Now in [0, 20), behavior changed!
assert process(25) == 35  # NEW: Covers [20, ∞)
```

### 2. Assertion Adjustment

Update expected values when behavior changes.

**Scenario: Logic change**

```python
# Old code
def calculate_discount(price):
    if price < 100:
        return price * 0.9  # 10% discount
    else:
        return price * 0.8  # 20% discount

# Old test
assert calculate_discount(50) == 45   # 50 * 0.9
assert calculate_discount(150) == 120 # 150 * 0.8

# New code (changed discount rates)
def calculate_discount(price):
    if price < 100:
        return price * 0.95  # 5% discount
    else:
        return price * 0.85  # 15% discount

# Updated test
assert calculate_discount(50) == 47.5  # 50 * 0.95 (UPDATED)
assert calculate_discount(150) == 127.5 # 150 * 0.85 (UPDATED)
```

### 3. Test Removal

Remove redundant or obsolete tests.

**Scenario: Intervals merged**

```python
# Old code
def categorize(x):
    if x < 0:
        return "negative"
    elif x == 0:
        return "zero"
    elif x < 10:
        return "small"
    else:
        return "large"

# Old tests
assert categorize(-5) == "negative"
assert categorize(0) == "zero"
assert categorize(5) == "small"
assert categorize(15) == "large"

# New code (simplified)
def categorize(x):
    if x <= 0:
        return "non-positive"
    elif x < 10:
        return "small"
    else:
        return "large"

# Updated tests (removed redundant test)
assert categorize(-5) == "non-positive"  # Covers (-∞, 0]
# REMOVED: test for x=0 (now covered by x=-5)
assert categorize(5) == "small"
assert categorize(15) == "large"
```

### 4. Test Generation

Create new tests for uncovered intervals.

**Scenario: New feature added**

```python
# Old code
def validate_age(age):
    if age < 18:
        return "minor"
    else:
        return "adult"

# Old tests
assert validate_age(10) == "minor"
assert validate_age(25) == "adult"

# New code (added senior category)
def validate_age(age):
    if age < 18:
        return "minor"
    elif age < 65:
        return "adult"
    else:
        return "senior"

# Updated tests
assert validate_age(10) == "minor"
assert validate_age(25) == "adult"
assert validate_age(70) == "senior"  # NEW test
```

## Update Patterns

### Pattern 1: Boundary Shift

**Detection:**
- Interval boundary value changed
- Comparison operator changed

**Action:**
- Adjust test inputs near boundaries
- Update assertions if behavior changed

**Example:**
```python
# Old: if x < 10
# New: if x <= 10

# Update test at boundary
# Old: assert process(10) == result_for_large
# New: assert process(10) == result_for_small
```

### Pattern 2: Interval Split

**Detection:**
- Single interval divided into multiple intervals
- New conditional added

**Action:**
- Keep existing tests
- Add tests for new intervals

**Example:**
```python
# Old: if x < 100
# New: if x < 50 ... elif x < 100

# Keep: test for x < 50
# Keep: test for x >= 100
# Add: test for 50 <= x < 100
```

### Pattern 3: Interval Merge

**Detection:**
- Multiple intervals combined
- Conditional removed

**Action:**
- Keep one representative test
- Remove redundant tests

**Example:**
```python
# Old: if x < 0 ... elif x == 0 ... elif x > 0
# New: if x <= 0 ... else

# Keep: test for x < 0
# Remove: test for x == 0 (redundant)
# Keep: test for x > 0
```

### Pattern 4: Interval Inversion

**Detection:**
- Condition negated
- Branches swapped

**Action:**
- Swap expected results
- Verify all tests still valid

**Example:**
```python
# Old: if x < 10: return "small" else: return "large"
# New: if x >= 10: return "large" else: return "small"

# Tests remain same (behavior unchanged)
# But verify assertions match new logic
```

## Test Update Workflow

### Step 1: Analyze Changes

```python
def analyze_code_changes(old_code, new_code):
    old_intervals = extract_intervals(old_code)
    new_intervals = extract_intervals(new_code)

    return {
        'added': new_intervals - old_intervals,
        'removed': old_intervals - new_intervals,
        'modified': find_modified_intervals(old_intervals, new_intervals)
    }
```

### Step 2: Assess Test Coverage

```python
def assess_coverage(tests, intervals):
    covered = set()

    for test in tests:
        interval = determine_interval(test.input, intervals)
        covered.add(interval)

    uncovered = intervals - covered
    return covered, uncovered
```

### Step 3: Update Tests

```python
def update_tests(tests, changes, intervals):
    updated_tests = []

    for test in tests:
        if test_needs_update(test, changes):
            updated_test = update_test(test, changes)
            updated_tests.append(updated_test)
        elif test_is_redundant(test, changes):
            # Skip redundant test
            continue
        else:
            updated_tests.append(test)

    # Add new tests for uncovered intervals
    for interval in find_uncovered(intervals, updated_tests):
        new_test = generate_test(interval)
        updated_tests.append(new_test)

    return updated_tests
```

### Step 4: Validate Tests

```python
def validate_tests(tests, program):
    results = []

    for test in tests:
        try:
            result = execute_test(test, program)
            results.append({
                'test': test,
                'status': 'pass' if result else 'fail',
                'output': result
            })
        except Exception as e:
            results.append({
                'test': test,
                'status': 'error',
                'error': str(e)
            })

    return results
```

## Language-Specific Strategies

### Python

**Test framework: pytest**

```python
# Update test inputs
def test_process_negative():
    assert process(-5) == 5  # NEW

def test_process_small():
    assert process(5) == 10  # EXISTING

def test_process_large():
    assert process(15) == 25  # EXISTING

# Update assertions
def test_calculate_discount():
    assert calculate_discount(50) == 47.5  # UPDATED from 45
```

### Java

**Test framework: JUnit**

```java
// Update test inputs
@Test
public void testProcessNegative() {
    assertEquals(5, process(-5));  // NEW
}

@Test
public void testProcessSmall() {
    assertEquals(10, process(5));  // EXISTING
}

// Update assertions
@Test
public void testCalculateDiscount() {
    assertEquals(47.5, calculateDiscount(50), 0.01);  // UPDATED
}
```

### JavaScript

**Test framework: Jest**

```javascript
// Update test inputs
test('process negative numbers', () => {
    expect(process(-5)).toBe(5);  // NEW
});

test('process small numbers', () => {
    expect(process(5)).toBe(10);  // EXISTING
});

// Update assertions
test('calculate discount', () => {
    expect(calculateDiscount(50)).toBe(47.5);  // UPDATED
});
```

## Handling Complex Changes

### Multiple Intervals Changed

```python
# Old code
def grade(score):
    if score < 60:
        return 'F'
    elif score < 70:
        return 'D'
    elif score < 80:
        return 'C'
    elif score < 90:
        return 'B'
    else:
        return 'A'

# New code (changed boundaries)
def grade(score):
    if score < 50:
        return 'F'
    elif score < 65:
        return 'D'
    elif score < 75:
        return 'C'
    elif score < 85:
        return 'B'
    else:
        return 'A'

# Update strategy:
# 1. Identify all changed boundaries: 60→50, 70→65, 80→75, 90→85
# 2. Update tests near boundaries
# 3. Verify coverage of all intervals
```

### Nested Conditions

```python
# Old code
def process(x, y):
    if x < 10:
        if y < 5:
            return "small-small"
        else:
            return "small-large"
    else:
        return "large"

# New code (added case)
def process(x, y):
    if x < 10:
        if y < 5:
            return "small-small"
        else:
            return "small-large"
    else:
        if y < 5:
            return "large-small"  # NEW
        else:
            return "large-large"

# Update strategy:
# 1. Identify new interval: x >= 10 and y < 5
# 2. Add test: assert process(15, 3) == "large-small"
# 3. Update existing test: assert process(15, 7) == "large-large"
```

## Best Practices

### Minimize Test Changes

- Only update tests that are affected by code changes
- Preserve tests that still provide value
- Avoid unnecessary test rewrites

### Maintain Test Quality

- Keep tests readable and maintainable
- Use descriptive test names
- Document why tests were updated

### Validate Thoroughly

- Run all tests after updates
- Check coverage metrics
- Verify no regressions introduced

### Document Changes

- Record what was changed and why
- Note any manual adjustments needed
- Track coverage improvements
