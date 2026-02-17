---
name: regression-consistency-checker
description: Checks whether a new version of a repository preserves the behavior observed by tests on the old version. Use this skill when comparing two versions of code to detect regressions, verify refactoring safety, validate bug fixes don't break existing functionality, or ensure backward compatibility. Detects differences in function outputs, exceptions, observable states, and performance between versions. Generates reports highlighting potential regressions (critical, high, medium, low severity), improvements, and areas requiring verification. Triggers when users ask to check for regressions between versions, compare test behavior across versions, verify behavior preservation, or validate that changes don't break existing tests.
---

# Regression Consistency Checker

Check whether a new version of a repository preserves the behavior observed by tests on the old version.

## Workflow

### 1. Prepare Versions

**Set up old version**:
```bash
# Tag or note the old version
git tag old-version

# Or checkout specific commit
git checkout <old-commit-hash>
```

**Set up new version**:
```bash
# Tag the new version
git tag new-version

# Or checkout new commit
git checkout <new-commit-hash>
```

**Ensure clean environment**:
- Same dependencies installed
- Same test configuration
- Same environment variables
- Deterministic test execution (fix random seeds, mock time)

### 2. Run Tests on Old Version

**Capture baseline results**:
```bash
# Python (pytest with JSON report)
git checkout old-version
pytest --json-report --json-report-file=old_results.json

# JavaScript (Jest with JSON report)
git checkout old-version
npm test -- --json --outputFile=old_results.json

# Run multiple times to check stability
pytest --json-report --json-report-file=old_results_1.json
pytest --json-report --json-report-file=old_results_2.json
# Compare to ensure deterministic
```

**Verify baseline stability**:
- All tests should pass (or document known failures)
- Results should be consistent across runs
- No flaky tests

### 3. Run Tests on New Version

**Capture new results**:
```bash
# Python
git checkout new-version
pytest --json-report --json-report-file=new_results.json

# JavaScript
git checkout new-version
npm test -- --json --outputFile=new_results.json
```

**Note any immediate failures**:
- Tests that now fail
- New errors or exceptions
- Changed behavior

### 4. Compare Results

**Use comparison script**:
```bash
python scripts/compare_results.py old_results.json new_results.json

# With custom tolerance for floats
python scripts/compare_results.py old_results.json new_results.json --tolerance 0.001

# Save detailed report
python scripts/compare_results.py old_results.json new_results.json --output regression_report.json
```

**Script detects**:
- 🔴 **Critical**: Tests that passed now fail, missing tests
- 🟠 **High**: Different outputs for same inputs
- 🟡 **Medium**: Different exception types
- 🔵 **Low**: Changed error messages
- ✅ **Improvements**: Tests that now pass, bug fixes

### 5. Analyze Regressions

For each regression, determine:

**Is it a true regression?**
- Unintended behavior change
- Bug introduced
- Performance degradation
- Breaking change

**Or is it expected?**
- Intentional behavior change
- Bug fix that changes output
- Improved error handling
- Refactoring with equivalent behavior

**Review strategies** in [detection_strategies.md](references/detection_strategies.md).

### 6. Investigate Root Causes

**For critical regressions**:
```bash
# Find commits that caused regression
git bisect start
git bisect bad new-version
git bisect good old-version
# Test each commit
git bisect run pytest path/to/failing_test.py
```

**For output differences**:
- Compare function inputs/outputs
- Check for changed algorithms
- Verify data transformations
- Review calculation logic

**For exception changes**:
- Check error handling code
- Verify exception types
- Review validation logic

### 7. Document Findings

**Create regression report**:
```
REGRESSION ANALYSIS REPORT
==========================

Version Comparison: v1.0.0 → v1.1.0
Date: 2024-01-15
Tests Run: 156

SUMMARY
-------
Critical Regressions: 2
High Severity: 5
Medium Severity: 3
Low Severity: 8
Improvements: 4
Unchanged: 134

CRITICAL REGRESSIONS
--------------------
1. test_user_authentication
   - Status: PASS → FAIL
   - Error: KeyError: 'user_id'
   - Root Cause: Removed field from response
   - Action: Restore field or update API contract

2. test_payment_processing
   - Status: PASS → FAIL
   - Error: AssertionError: expected 100.00, got 100.01
   - Root Cause: Rounding change in calculation
   - Action: Fix rounding logic

HIGH SEVERITY REGRESSIONS
--------------------------
1. test_data_export
   - Output changed: CSV format → JSON format
   - Impact: Breaking change for consumers
   - Action: Maintain backward compatibility

[... continue for all regressions ...]

EXPECTED CHANGES
----------------
1. test_error_messages
   - Error messages now include more context
   - Intentional improvement
   - Action: Update baseline

RECOMMENDATIONS
---------------
1. Fix critical regressions before release
2. Review high severity changes with team
3. Document breaking changes in changelog
4. Update tests for intentional changes
```

### 8. Fix or Accept Changes

**Fix true regressions**:
```bash
# Fix the code
git checkout new-version
# Make fixes
git commit -m "Fix: regression in user authentication"

# Re-run tests
pytest --json-report --json-report-file=fixed_results.json

# Verify fix
python scripts/compare_results.py old_results.json fixed_results.json
```

**Accept intentional changes**:
```bash
# Update baseline
cp new_results.json baseline_results.json

# Document in changelog
echo "- Changed: CSV export now returns JSON" >> CHANGELOG.md
```

## Quick Reference

### Regression Types

**Output Regressions**:
- Function returns different values
- Data format changes
- Calculation differences

**Exception Regressions**:
- New exceptions raised
- Different exception types
- Changed error messages

**State Regressions**:
- Different database state
- Different files created
- Different side effects

**Performance Regressions**:
- Slower execution
- Higher memory usage
- More API calls

### Severity Levels

**Critical** (block release):
- Test passed → failed
- Data corruption
- Security issues
- Crashes

**High** (fix before release):
- Wrong outputs
- Breaking API changes
- Major performance degradation (>2x)

**Medium** (review and decide):
- Minor output changes
- Moderate performance degradation (50-100%)
- Changed error messages

**Low** (document):
- Cosmetic changes
- Minor performance changes (<50%)
- Log message changes

### Comparison Strategies

**Exact comparison**:
```python
old_output == new_output
```

**Approximate comparison** (floats):
```python
abs(old_output - new_output) < tolerance
```

**Structural comparison** (ignore fields):
```python
# Ignore timestamps, IDs
compare_ignoring_fields(old, new, ['timestamp', 'id'])
```

**Semantic comparison** (order-independent):
```python
# Compare as sets
set(old_list) == set(new_list)
```

## Helper Script

The `compare_results.py` script automates comparison:

```bash
# Basic comparison
python scripts/compare_results.py old_results.json new_results.json

# Custom float tolerance
python scripts/compare_results.py old_results.json new_results.json --tolerance 0.001

# Save detailed report
python scripts/compare_results.py old_results.json new_results.json --output report.json
```

**Supported formats**:
- pytest JSON report
- Jest JSON report
- Generic JSON format

**Output includes**:
- Categorized regressions by severity
- Specific test failures
- Output diffs
- Exception changes
- Improvements

## Best Practices

**Ensure deterministic tests**:
- Fix random seeds
- Mock current time
- Mock external APIs
- Sort non-deterministic outputs

**Run multiple times**:
- Verify baseline stability
- Catch flaky tests
- Ensure reproducibility

**Isolate changes**:
- Test one change at a time
- Use git bisect for root cause
- Compare specific commits

**Document expectations**:
- Maintain changelog
- Note intentional changes
- Update test baselines

**Automate checks**:
- Run in CI/CD pipeline
- Block on critical regressions
- Generate reports automatically
