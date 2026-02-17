---
name: behavior-preservation-checker
description: Compare runtime behavior between original and migrated repositories to detect behavioral differences, regressions, and semantic changes. Use when validating code migrations, refactorings, language ports, framework upgrades, or any transformation that should preserve behavior. Automatically compares test results, execution traces, API responses, and observable outputs between two repository versions. Provides actionable guidance for fixing deviations and ensuring behavioral equivalence.
---

# Behavior Preservation Checker

## Overview

Validate that a migrated or refactored codebase preserves the original behavior by automatically comparing runtime behavior, test results, execution traces, and observable outputs between two repository versions.

## Core Workflow

### 1. Setup Repositories

Prepare both repositories for comparison:

```bash
# Clone or locate repositories
ORIGINAL_REPO=/path/to/original
MIGRATED_REPO=/path/to/migrated

# Ensure both are at comparable states
cd $ORIGINAL_REPO && git checkout main
cd $MIGRATED_REPO && git checkout main
```

### 2. Run Behavior Comparison

Use the comparison script to analyze behavioral differences:

```bash
python scripts/behavior_checker.py \
    --original $ORIGINAL_REPO \
    --migrated $MIGRATED_REPO \
    --output behavior_report.json
```

### 3. Review Results

Examine the generated report for:
- Test result differences
- Execution trace divergences
- Output mismatches
- Performance regressions
- API contract violations

### 4. Fix Deviations

Follow actionable guidance to resolve behavioral differences.

## Comparison Methods

### Method 1: Test-Based Comparison

Run the same test suite on both repositories and compare results:

**Workflow**:
1. Identify common test suite (or create equivalent tests)
2. Run tests on original repository
3. Run tests on migrated repository
4. Compare pass/fail status, assertions, and outputs

**Example**:
```bash
# Run on original
cd $ORIGINAL_REPO
pytest tests/ --json-report --json-report-file=original_results.json

# Run on migrated
cd $MIGRATED_REPO
pytest tests/ --json-report --json-report-file=migrated_results.json

# Compare
python scripts/compare_test_results.py \
    original_results.json \
    migrated_results.json
```

### Method 2: Execution Trace Comparison

Capture and compare execution traces:

**Workflow**:
1. Instrument code to capture function calls, arguments, and return values
2. Run identical inputs through both versions
3. Compare execution traces for divergences

**Example**:
```python
# Trace original
python scripts/trace_execution.py \
    --repo $ORIGINAL_REPO \
    --input test_inputs.json \
    --output original_trace.json

# Trace migrated
python scripts/trace_execution.py \
    --repo $MIGRATED_REPO \
    --input test_inputs.json \
    --output migrated_trace.json

# Compare traces
python scripts/compare_traces.py \
    original_trace.json \
    migrated_trace.json
```

### Method 3: Observable Output Comparison

Compare program outputs for identical inputs:

**Workflow**:
1. Define test inputs (API requests, CLI commands, function calls)
2. Capture outputs from both versions (stdout, files, API responses)
3. Compare outputs for differences

**Example**:
```bash
# Test API endpoints
python scripts/compare_api_outputs.py \
    --original-url http://localhost:8000 \
    --migrated-url http://localhost:8001 \
    --test-cases api_test_cases.json
```

### Method 4: Property-Based Testing

Use property-based testing to find behavioral differences:

**Workflow**:
1. Define behavioral properties (invariants, contracts)
2. Generate random inputs
3. Verify properties hold for both versions
4. Report any property violations

**Example**:
```python
# Property: sorting should produce same result
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_equivalence(input_list):
    original_result = original_sort(input_list)
    migrated_result = migrated_sort(input_list)
    assert original_result == migrated_result
```

## Difference Detection

### Test Result Differences

**What to check**:
- Tests that pass in original but fail in migrated
- Tests that fail in original but pass in migrated
- New test failures
- Changed assertion messages

**Severity levels**:
- **Critical**: Core functionality tests fail
- **High**: Integration tests fail
- **Medium**: Edge case tests fail
- **Low**: Flaky tests or timing-dependent failures

### Execution Trace Differences

**What to check**:
- Different function call sequences
- Different argument values
- Different return values
- Missing or extra function calls

**Example divergence**:
```
Original trace:
  calculate(x=10) -> 20
  validate(20) -> True
  save(20) -> Success

Migrated trace:
  calculate(x=10) -> 21  # ← Difference!
  validate(21) -> True
  save(21) -> Success
```

### Output Differences

**What to check**:
- Different stdout/stderr
- Different file contents
- Different API response bodies
- Different status codes
- Different error messages

**Tolerance levels**:
```python
# Exact match required
assert original_output == migrated_output

# Numerical tolerance
assert abs(original_value - migrated_value) < 0.001

# Structural equivalence (ignore formatting)
assert json.loads(original) == json.loads(migrated)
```

## Actionable Guidance

### Pattern 1: Logic Error

**Symptom**: Different outputs for same inputs

**Diagnosis**:
```bash
python scripts/isolate_difference.py \
    --original $ORIGINAL_REPO \
    --migrated $MIGRATED_REPO \
    --failing-test test_calculation
```

**Guidance**:
1. Identify the diverging function
2. Compare implementations side-by-side
3. Check for off-by-one errors, operator changes, or logic inversions
4. Add unit test for the specific case

### Pattern 2: Missing Functionality

**Symptom**: Tests pass in original but fail in migrated with "not implemented" or "attribute error"

**Diagnosis**:
```bash
python scripts/find_missing_functions.py \
    --original $ORIGINAL_REPO \
    --migrated $MIGRATED_REPO
```

**Guidance**:
1. List all missing functions/methods
2. Implement missing functionality
3. Verify with targeted tests

### Pattern 3: API Contract Violation

**Symptom**: Different response structure or status codes

**Diagnosis**:
```bash
python scripts/compare_api_contracts.py \
    --original-spec openapi_original.yaml \
    --migrated-spec openapi_migrated.yaml
```

**Guidance**:
1. Document API contract differences
2. Update migrated API to match original contract
3. Add contract tests to prevent future violations

### Pattern 4: Performance Regression

**Symptom**: Migrated version is significantly slower

**Diagnosis**:
```bash
python scripts/benchmark_comparison.py \
    --original $ORIGINAL_REPO \
    --migrated $MIGRATED_REPO \
    --iterations 100
```

**Guidance**:
1. Profile both versions to identify bottlenecks
2. Check for algorithmic changes (O(n) → O(n²))
3. Look for missing optimizations or caching
4. Verify database query efficiency

### Pattern 5: State Management Issues

**Symptom**: Tests fail intermittently or depend on execution order

**Diagnosis**:
```bash
python scripts/detect_state_issues.py \
    --repo $MIGRATED_REPO \
    --test-suite tests/
```

**Guidance**:
1. Identify shared state between tests
2. Add proper setup/teardown
3. Ensure test isolation
4. Check for global variable usage

## Report Format

The behavior checker generates a comprehensive JSON report:

```json
{
  "summary": {
    "total_tests": 150,
    "passed_both": 140,
    "failed_both": 2,
    "passed_original_failed_migrated": 5,
    "failed_original_passed_migrated": 3,
    "behavioral_equivalence": "92.7%"
  },
  "differences": [
    {
      "type": "test_failure",
      "test_name": "test_user_authentication",
      "severity": "critical",
      "original_result": "passed",
      "migrated_result": "failed",
      "error_message": "AssertionError: Expected 200, got 401",
      "guidance": "Check authentication logic in migrated version",
      "affected_files": ["auth/login.py"]
    }
  ],
  "recommendations": [
    "Fix 5 critical test failures before deployment",
    "Review 3 output differences for correctness"
  ]
}
```

## Best Practices

1. **Start with tests**: Ensure comprehensive test coverage before migration
2. **Incremental validation**: Check behavior after each migration step
3. **Document intentional changes**: Mark expected behavioral differences
4. **Use multiple comparison methods**: Combine tests, traces, and outputs
5. **Automate the process**: Integrate into CI/CD pipeline
6. **Set tolerance thresholds**: Define acceptable differences (e.g., timing, formatting)

## Resources

- **[references/comparison_techniques.md](references/comparison_techniques.md)**: Detailed comparison methodologies
- **[references/difference_patterns.md](references/difference_patterns.md)**: Common behavioral difference patterns
- **scripts/behavior_checker.py**: Main comparison orchestrator
- **scripts/compare_test_results.py**: Test result comparison
- **scripts/trace_execution.py**: Execution trace capture
- **scripts/compare_traces.py**: Trace comparison and analysis
