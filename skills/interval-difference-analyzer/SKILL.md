---
name: interval-difference-analyzer
description: Analyze differences in program intervals between two versions of a program (old and new) to identify added, removed, or modified intervals. Use when comparing program versions, analyzing variable ranges, detecting behavioral changes in numeric computations, validating refactorings, or assessing migration impacts. Supports optional test suite integration to validate interval changes. Generates comprehensive reports highlighting intervals requiring further testing or verification.
---

# Interval Difference Analyzer

## Overview

Analyze differences in program intervals (variable value ranges) between two versions of a program to detect behavioral changes, identify potential bugs, and guide testing efforts.

## Core Workflow

### 1. Setup Program Versions

Prepare both program versions for analysis:

```bash
OLD_VERSION=/path/to/old/program
NEW_VERSION=/path/to/new/program
TEST_SUITE=/path/to/tests  # Optional
```

### 2. Extract Intervals

Extract interval information from both versions:

```bash
python scripts/interval_analyzer.py \
    --program $OLD_VERSION \
    --output old_intervals.json

python scripts/interval_analyzer.py \
    --program $NEW_VERSION \
    --output new_intervals.json
```

### 3. Compare Intervals

Compare intervals and identify differences:

```bash
python scripts/compare_intervals.py \
    --old old_intervals.json \
    --new new_intervals.json \
    --output interval_diff_report.json
```

### 4. Review Report

Examine the generated report for:
- Added intervals (new variables or wider ranges)
- Removed intervals (deleted variables or narrower ranges)
- Modified intervals (changed bounds)
- Behavioral implications
- Testing recommendations

## What Are Program Intervals?

**Program intervals** represent the possible ranges of values that variables can take during program execution.

**Example**:
```python
def calculate_discount(price, discount_rate):
    # Intervals:
    # price: [0, 10000]
    # discount_rate: [0.0, 1.0]
    # discount: [0, 10000]
    discount = price * discount_rate
    return discount
```

**Why intervals matter**:
- Detect overflow/underflow risks
- Identify boundary condition changes
- Validate numeric computation correctness
- Guide test case generation

## Interval Extraction Methods

### Method 1: Static Analysis

Analyze code to infer possible value ranges without execution.

### Method 2: Dynamic Analysis

Execute program with test inputs and observe actual ranges.

### Method 3: Abstract Interpretation

Use abstract domains to compute sound interval approximations.

## Interval Comparison

### Identifying Added Intervals

**Pattern**: New variables or wider ranges in new version

**Implications**:
- New computation paths
- Potential new bugs
- Requires new tests

### Identifying Removed Intervals

**Pattern**: Deleted variables or narrower ranges in new version

**Implications**:
- Simplified computation
- Reduced intermediate state
- May affect debugging

### Identifying Modified Intervals

**Pattern**: Changed bounds for existing variables

**Example**:
```python
# Old version: age: [0, 120]
# New version: age: [0, 150]  # Widened!
```

**Implications**:
- Relaxed constraints
- May accept invalid inputs
- Requires validation testing

## Behavioral Change Detection

### Overflow/Underflow Detection

Check if new intervals exceed type bounds.

**Example**:
```python
# Old: result: [0, 1000000] ✓ Safe (int32)
# New: result: [0, 10000000000] ✗ Overflow risk!
```

### Precision Loss Detection

Check if new intervals lose precision.

**Example**:
```python
# Old: result: [0.0, 100.0] (float)
# New: result: [0, 100] (int) - precision loss!
```

### Boundary Condition Changes

Check if interval boundaries change critically.

**Example**:
```python
# Old: index: [0, 99]
# New: index: [-1, 99]  # Negative index possible!
```

## Testing Recommendations

### Priority Levels

**Critical**: Test immediately
- Overflow/underflow risks
- Negative indices
- Division by zero
- Type mismatches

**High**: Test soon
- Widened intervals
- Boundary changes
- Precision loss

**Medium**: Test when convenient
- Narrowed intervals (safer)
- Removed intermediate variables

**Low**: Optional testing
- Cosmetic changes
- Unchanged intervals

### Test Case Generation

Generate test cases targeting interval boundaries:

```python
# Interval: x: [0, 100]
test_cases = [0, 1, 50, 99, 100]

# For modified interval: [0, 100] → [0, 150]
additional_tests = [101, 125, 149, 150]
```

## Report Format

The analyzer generates a comprehensive JSON report:

```json
{
  "summary": {
    "total_intervals_old": 45,
    "total_intervals_new": 48,
    "added_intervals": 5,
    "removed_intervals": 2,
    "modified_intervals": 8
  },
  "differences": [
    {
      "type": "modified",
      "variable": "age",
      "old_interval": "[0, 120]",
      "new_interval": "[0, 150]",
      "severity": "high",
      "implications": ["Accepts wider range"],
      "testing_priority": "high",
      "suggested_tests": [121, 135, 149, 150]
    }
  ],
  "recommendations": [
    "Test modified intervals with boundary values",
    "Verify no overflow in calculations"
  ]
}
```

## Integration with Test Suites

### Validate Intervals with Tests

Run existing tests and verify intervals:

```bash
python scripts/validate_intervals.py \
    --program $NEW_VERSION \
    --intervals new_intervals.json \
    --test-suite $TEST_SUITE
```

### Generate Tests from Intervals

Automatically generate tests for interval boundaries:

```bash
python scripts/generate_interval_tests.py \
    --intervals interval_diff_report.json \
    --output generated_tests.py
```

## Best Practices

1. **Use both static and dynamic analysis**: Combine for better coverage
2. **Focus on critical intervals**: Prioritize safety-critical variables
3. **Test boundary values**: Always test interval bounds
4. **Document intentional changes**: Mark expected interval modifications
5. **Automate analysis**: Integrate into CI/CD pipeline

## Resources

- **[references/interval_analysis.md](references/interval_analysis.md)**: Detailed interval analysis techniques
- **[references/abstract_interpretation.md](references/abstract_interpretation.md)**: Abstract interpretation theory
- **scripts/interval_analyzer.py**: Main interval extraction tool
- **scripts/compare_intervals.py**: Interval comparison engine
- **scripts/validate_intervals.py**: Test suite validation
- **scripts/generate_interval_tests.py**: Test case generator
