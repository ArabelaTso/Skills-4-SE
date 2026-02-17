# Reduction Algorithms

## Delta Debugging

Delta debugging is the most effective algorithm for test case reduction. It systematically removes chunks of the test case and validates each reduction.

### Algorithm

1. Start with the full test case divided into n chunks (typically n=2)
2. For each chunk:
   - Try removing the chunk
   - Run the test with the reduced version
   - If the test still fails, keep the reduction
   - If the test passes, restore the chunk
3. If any chunk was successfully removed, decrease granularity (n = n-1)
4. If no chunks could be removed, increase granularity (n = n*2)
5. Repeat until no further reduction is possible

### Complexity

- Best case: O(n) where n is the number of elements
- Worst case: O(n²)
- Typical case: O(n log n)

### Example

```
Original test (8 lines):
1. import module
2. setup_data()
3. x = compute()
4. y = process(x)
5. z = transform(y)
6. assert z > 0
7. cleanup()
8. print("done")

Iteration 1 (n=2, chunks of 4):
- Try removing lines 1-4: Test passes (failure not reproduced)
- Try removing lines 5-8: Test fails! Keep this reduction

Reduced to:
1. import module
2. setup_data()
3. x = compute()
4. y = process(x)

Iteration 2 (n=2, chunks of 2):
- Try removing lines 1-2: Test passes
- Try removing lines 3-4: Test fails! Keep this reduction

Reduced to:
1. import module
2. setup_data()

Final: 2 lines (75% reduction)
```

## Binary Search Reduction

Binary search reduction removes half of the test case at a time.

### Algorithm

1. Try removing the first half
2. If test still fails, keep first half and discard second half
3. If test passes, try removing the second half
4. If test still fails, keep second half and discard first half
5. If neither half alone reproduces the failure, stop
6. Repeat on the remaining half

### Complexity

- O(log n) iterations
- Very fast but may not find minimal reduction

### When to Use

- As a first pass before more thorough algorithms
- When test execution is very slow
- For aggressive reduction strategies

## Greedy Line-by-Line Reduction

Greedy reduction tries removing each line one at a time.

### Algorithm

1. Start at line 1
2. Try removing the current line
3. If test still fails, keep the removal and stay at same position
4. If test passes, restore the line and move to next line
5. Repeat until end of test case

### Complexity

- O(n²) in worst case
- O(n) in best case

### When to Use

- After delta debugging for final cleanup
- For conservative reduction strategies
- When test case structure is simple

## Hierarchical Reduction

Reduce at multiple levels: functions, statements, expressions.

### Algorithm

1. Identify structural elements (functions, blocks, statements)
2. Apply delta debugging at function level
3. Apply delta debugging at statement level within remaining functions
4. Apply delta debugging at expression level within remaining statements

### Example

```python
# Original
def test():
    x = expensive_setup()
    y = complex_computation(x)
    z = another_operation(y)
    assert z == expected

# After function-level reduction (if possible)
def test():
    z = another_operation(y)
    assert z == expected

# After statement-level reduction
def test():
    assert z == expected
```

## Syntax-Aware Reduction

Maintain syntactic validity during reduction.

### Strategies

**Preserve structure:**
- Keep matching braces, parentheses
- Maintain indentation
- Preserve imports for used symbols

**Smart removal:**
- Remove entire statements, not partial
- Remove unused variable definitions
- Remove unreachable code

**Example:**
```python
# Don't create invalid syntax
if condition:  # Keep this
    statement1  # Try removing
    statement2  # Try removing

# Not:
if condition:  # Partial removal creates syntax error
    statement2
```

## Reduction Strategies

### Aggressive

1. Binary search reduction (fast initial reduction)
2. Delta debugging (thorough reduction)
3. Greedy line-by-line (final cleanup)

**Pros:** Fastest, smallest result
**Cons:** May remove too much, less readable

### Balanced (Recommended)

1. Delta debugging with moderate granularity
2. Optional greedy cleanup

**Pros:** Good balance of speed and quality
**Cons:** May take longer than aggressive

### Conservative

1. Greedy line-by-line only
2. Preserve comments and structure

**Pros:** Most readable, safest
**Cons:** Slower, larger result

## Handling Different Test Types

### Unit Tests

Focus on:
- Test setup/teardown
- Assertions
- Test data

Preserve:
- Test framework imports
- Test function signature

### Integration Tests

Focus on:
- API calls
- Database operations
- External dependencies

Preserve:
- Connection setup
- Authentication

### Input Files

Focus on:
- Input data lines
- Configuration values

Preserve:
- File format structure
- Required headers

## Validation During Reduction

### Oracle Types

**Exit code:**
```python
# Test fails if exit code is non-zero
oracle = ExitCodeOracle(expected=1)
```

**Exception type:**
```python
# Test fails if specific exception is raised
oracle = ExceptionOracle(expected="ValueError")
```

**Output pattern:**
```python
# Test fails if output contains pattern
oracle = OutputOracle(expected="Error: division by zero")
```

**Assertion:**
```python
# Test fails if assertion fails
oracle = AssertionOracle(expected="AssertionError")
```

### Validation Best Practices

1. **Verify original failure:** Ensure original test exhibits expected failure
2. **Check each reduction:** Run test after each modification
3. **Timeout handling:** Set reasonable timeouts to avoid hanging
4. **Determinism:** Ensure test failure is deterministic
5. **Side effects:** Watch for tests that modify global state

## Optimization Techniques

### Caching

Cache test results for identical test cases:
```python
cache = {}
def run_test_cached(test_content):
    key = hash(test_content)
    if key in cache:
        return cache[key]
    result = run_test(test_content)
    cache[key] = result
    return result
```

### Parallel Execution

Run independent reduction attempts in parallel:
```python
# Try removing multiple chunks in parallel
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(try_remove_chunk, i)
               for i in range(n_chunks)]
    results = [f.result() for f in futures]
```

### Early Termination

Stop if reduction ratio is good enough:
```python
if (original_size - current_size) / original_size > 0.9:
    # 90% reduction achieved, stop
    break
```

## Common Pitfalls

1. **Non-deterministic tests:** Failures that occur randomly
   - Solution: Run test multiple times, require consistent failure

2. **Timeout too short:** Test needs more time
   - Solution: Increase timeout or optimize test

3. **Side effects:** Test modifies files/database
   - Solution: Clean up between runs or use isolated environment

4. **Syntax errors:** Reduction creates invalid code
   - Solution: Use syntax-aware reduction

5. **Over-reduction:** Removing too much context
   - Solution: Use conservative strategy or preserve key elements
