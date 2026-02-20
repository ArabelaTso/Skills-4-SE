# Regression Detection Strategies

This document outlines strategies for detecting behavioral regressions between code versions.

## Types of Regressions

### 1. Output Regressions

**Description**: Function returns different values for same inputs.

**Examples**:
- Calculation changes: `sum([1,2,3])` returns `6` → `7`
- Format changes: Returns `"2024-01-01"` → `"01/01/2024"`
- Type changes: Returns `42` → `"42"`
- Precision changes: Returns `3.14` → `3.14159`

**Detection**:
- Capture function outputs on old version
- Run same inputs on new version
- Compare outputs with appropriate tolerance

### 2. Exception Regressions

**Description**: Different exceptions raised or exception behavior changes.

**Examples**:
- New exception: Code that succeeded now raises exception
- Missing exception: Code that raised exception now succeeds
- Different exception type: `ValueError` → `TypeError`
- Different exception message: `"Invalid input"` → `"Bad value"`

**Detection**:
- Record which tests raise exceptions on old version
- Check if same tests raise same exceptions on new version
- Compare exception types and messages

### 3. State Regressions

**Description**: Observable state changes differ between versions.

**Examples**:
- Database state: Different records created/updated
- File system: Different files written
- External API calls: Different requests made
- Side effects: Different logs, metrics, events

**Detection**:
- Capture state snapshots before/after operations
- Compare state changes between versions
- Check side effects (logs, DB queries, API calls)

### 4. Performance Regressions

**Description**: Significant performance degradation.

**Examples**:
- Execution time: 100ms → 5000ms
- Memory usage: 10MB → 500MB
- Database queries: 1 query → N+1 queries
- API calls: 1 call → 10 calls

**Detection**:
- Measure execution time on both versions
- Track resource usage (memory, CPU, I/O)
- Count external calls (DB, API, file system)
- Flag significant increases (>50% slower)

### 5. Behavioral Regressions

**Description**: Subtle behavior changes not caught by assertions.

**Examples**:
- Order changes: List returned in different order
- Timing changes: Async operations complete in different order
- Randomness: Different random values (if not seeded)
- Caching: Different cache hit/miss patterns

**Detection**:
- Normalize outputs (sort lists, fix random seeds)
- Check invariants beyond exact equality
- Verify logical properties hold

## Detection Approaches

### Approach 1: Test Output Comparison

**Method**: Run tests on both versions, compare outputs.

**Steps**:
1. Run test suite on old version, capture outputs
2. Run test suite on new version, capture outputs
3. Compare outputs test by test
4. Flag differences as potential regressions

**Pros**:
- Simple to implement
- Works with existing tests
- No code modification needed

**Cons**:
- Only detects what tests observe
- May have false positives (intentional changes)
- Requires deterministic tests

**Implementation**:
```python
# Run on old version
old_results = run_tests(old_version)

# Run on new version
new_results = run_tests(new_version)

# Compare
for test_name in old_results:
    if old_results[test_name] != new_results[test_name]:
        report_regression(test_name, old_results[test_name], new_results[test_name])
```

### Approach 2: Differential Testing

**Method**: Run same inputs through both versions simultaneously.

**Steps**:
1. Extract test inputs from test suite
2. Run inputs through old version, record outputs
3. Run inputs through new version, record outputs
4. Compare outputs for each input

**Pros**:
- Precise comparison
- Can test at function level
- Isolates specific changes

**Cons**:
- Requires extracting test inputs
- May need to handle side effects
- More complex setup

**Implementation**:
```python
# Extract inputs from tests
inputs = extract_test_inputs(test_suite)

# Run through both versions
for test_input in inputs:
    old_output = run_on_old_version(test_input)
    new_output = run_on_new_version(test_input)

    if not outputs_match(old_output, new_output):
        report_regression(test_input, old_output, new_output)
```

### Approach 3: Snapshot Testing

**Method**: Capture snapshots of outputs/state, compare against new version.

**Steps**:
1. Run tests on old version, save snapshots
2. Run tests on new version
3. Compare new outputs against saved snapshots
4. Flag mismatches

**Pros**:
- Comprehensive state capture
- Good for complex outputs
- Easy to review changes

**Cons**:
- Large snapshot files
- Brittle to formatting changes
- Requires snapshot management

**Implementation**:
```python
# Generate snapshots from old version
snapshots = {}
for test in test_suite:
    output = run_test(test, old_version)
    snapshots[test.name] = serialize(output)
save_snapshots(snapshots)

# Compare against new version
for test in test_suite:
    output = run_test(test, new_version)
    expected = load_snapshot(test.name)
    if serialize(output) != expected:
        report_regression(test.name, expected, output)
```

### Approach 4: Property-Based Comparison

**Method**: Check that properties/invariants hold across versions.

**Steps**:
1. Define properties that should be preserved
2. Verify properties on old version
3. Verify same properties on new version
4. Flag property violations

**Pros**:
- Catches semantic changes
- Less brittle than exact comparison
- Focuses on important properties

**Cons**:
- Requires defining properties
- May miss some regressions
- More complex to implement

**Implementation**:
```python
# Define properties
properties = [
    lambda result: len(result) > 0,  # Non-empty result
    lambda result: all(x > 0 for x in result),  # All positive
    lambda result: result == sorted(result),  # Sorted
]

# Check properties on both versions
for test in test_suite:
    old_output = run_test(test, old_version)
    new_output = run_test(test, new_version)

    for prop in properties:
        old_holds = prop(old_output)
        new_holds = prop(new_output)

        if old_holds != new_holds:
            report_property_violation(test, prop, old_holds, new_holds)
```

## Comparison Strategies

### Exact Comparison

**When to use**: Deterministic outputs, no floating point.

```python
def exact_match(old, new):
    return old == new
```

### Approximate Comparison

**When to use**: Floating point numbers, timing-dependent values.

```python
def approx_match(old, new, tolerance=1e-6):
    if isinstance(old, float) and isinstance(new, float):
        return abs(old - new) < tolerance
    return old == new
```

### Structural Comparison

**When to use**: Complex objects, ignore certain fields.

```python
def structural_match(old, new, ignore_fields=None):
    if ignore_fields is None:
        ignore_fields = ['timestamp', 'id']

    old_filtered = {k: v for k, v in old.items() if k not in ignore_fields}
    new_filtered = {k: v for k, v in new.items() if k not in ignore_fields}

    return old_filtered == new_filtered
```

### Semantic Comparison

**When to use**: Order-independent collections, equivalent representations.

```python
def semantic_match(old, new):
    # Lists: compare as sets (ignore order)
    if isinstance(old, list) and isinstance(new, list):
        return set(old) == set(new)

    # Dicts: compare keys and values
    if isinstance(old, dict) and isinstance(new, dict):
        return old.keys() == new.keys() and all(
            semantic_match(old[k], new[k]) for k in old.keys()
        )

    return old == new
```

## Handling Non-Determinism

### Random Values

**Problem**: Tests use random values, outputs differ each run.

**Solution**: Fix random seed.

```python
# Old version
import random
random.seed(42)
run_tests()

# New version
import random
random.seed(42)
run_tests()
```

### Timestamps

**Problem**: Outputs include current time.

**Solution**: Mock time or ignore timestamp fields.

```python
# Mock time
from unittest.mock import patch
with patch('datetime.datetime') as mock_datetime:
    mock_datetime.now.return_value = datetime(2024, 1, 1)
    run_tests()

# Or ignore timestamps in comparison
def compare_ignoring_timestamps(old, new):
    return structural_match(old, new, ignore_fields=['timestamp', 'created_at'])
```

### Async Operations

**Problem**: Async operations complete in different order.

**Solution**: Sort results or use deterministic execution.

```python
# Sort results before comparison
old_results = sorted(run_async_test(old_version), key=lambda x: x.id)
new_results = sorted(run_async_test(new_version), key=lambda x: x.id)
compare(old_results, new_results)
```

### External Dependencies

**Problem**: External APIs, databases return different data.

**Solution**: Mock external dependencies.

```python
# Mock external API
with patch('requests.get') as mock_get:
    mock_get.return_value.json.return_value = {'data': 'fixed'}
    run_tests()
```

## Regression Severity Classification

### Critical Regressions

**Indicators**:
- Test that passed now fails
- Exception raised where none before
- Data corruption or loss
- Security vulnerability introduced

**Action**: Block release, fix immediately.

### High Severity Regressions

**Indicators**:
- Incorrect output for valid input
- Wrong exception type raised
- Significant performance degradation (>2x slower)
- Breaking API changes

**Action**: Fix before release.

### Medium Severity Regressions

**Indicators**:
- Minor output format changes
- Performance degradation (50-100% slower)
- Changed error messages
- Deprecated API usage

**Action**: Review and fix if time permits.

### Low Severity Regressions

**Indicators**:
- Cosmetic changes (whitespace, formatting)
- Minor performance changes (<50%)
- Log message changes
- Internal refactoring

**Action**: Document, fix in future release.

### False Positives

**Indicators**:
- Intentional behavior changes
- Bug fixes that change output
- Improved error handling
- Performance improvements

**Action**: Mark as expected, update baseline.

## Best Practices

### 1. Establish Baseline

Run tests on old version multiple times to ensure stability:
```bash
# Run 3 times to check for flaky tests
for i in {1..3}; do
  run_tests old_version > baseline_$i.txt
done

# Compare baselines
diff baseline_1.txt baseline_2.txt
```

### 2. Isolate Changes

Test one change at a time when possible:
- Single commit
- Single feature
- Single bug fix

### 3. Use Version Control

Tag versions for comparison:
```bash
git tag old-version v1.0.0
git tag new-version v1.1.0
```

### 4. Automate Comparison

Create automated regression check:
```bash
#!/bin/bash
# Run tests on both versions
git checkout old-version
pytest --json-report > old_results.json

git checkout new-version
pytest --json-report > new_results.json

# Compare results
python compare_results.py old_results.json new_results.json
```

### 5. Document Expected Changes

Maintain changelog of intentional behavior changes:
```markdown
# v1.1.0 Changes

## Intentional Behavior Changes
- Function `foo()` now returns list instead of tuple
- Error messages now include more context
- Performance optimization: 2x faster

## Bug Fixes
- Fixed off-by-one error in `bar()`
```

### 6. Review All Differences

Don't automatically assume all differences are bugs:
- Some may be intentional improvements
- Some may be bug fixes
- Some may be acceptable trade-offs

### 7. Maintain Test Stability

Ensure tests are deterministic:
- Fix random seeds
- Mock external dependencies
- Use fixed timestamps
- Sort non-deterministic outputs
