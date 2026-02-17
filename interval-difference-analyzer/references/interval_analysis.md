# Interval Analysis Techniques

## Overview

Interval analysis is a static program analysis technique that computes safe approximations of the possible values that variables can take during program execution.

## Fundamental Concepts

### What is an Interval?

An **interval** is a continuous range of values represented as `[min, max]` where:
- `min`: Lower bound (inclusive)
- `max`: Upper bound (inclusive)

**Examples**:
- `[0, 10]`: Values from 0 to 10
- `[-5, 5]`: Values from -5 to 5
- `[3.14, 3.14]`: Single value (constant)
- `[-∞, ∞]`: Any value (unknown)

### Interval Arithmetic

Operations on intervals produce result intervals:

**Addition**: `[a, b] + [c, d] = [a+c, b+d]`
```
[1, 3] + [2, 4] = [3, 7]
```

**Subtraction**: `[a, b] - [c, d] = [a-d, b-c]`
```
[5, 10] - [1, 3] = [2, 9]
```

**Multiplication**: `[a, b] × [c, d] = [min(ac,ad,bc,bd), max(ac,ad,bc,bd)]`
```
[2, 3] × [4, 5] = [8, 15]
[-1, 2] × [3, 4] = [-4, 8]
```

**Division**: `[a, b] / [c, d]` (if 0 ∉ [c, d])
```
[6, 12] / [2, 3] = [2, 6]
```

## Analysis Methods

### 1. Static Interval Analysis

Compute intervals without executing the program.

**Approach**:
1. Parse program into AST
2. Initialize intervals for inputs
3. Propagate intervals through operations
4. Handle control flow (branches, loops)
5. Compute fixed points for loops

**Example**:
```python
def analyze(x):
    # x: [0, 10] (given)
    y = x + 5
    # y: [0, 10] + [5, 5] = [5, 15]
    z = y * 2
    # z: [5, 15] × [2, 2] = [10, 30]
    return z
```

**Advantages**:
- No execution needed
- Sound over-approximation
- Complete coverage

**Limitations**:
- May be imprecise
- Conservative estimates
- Difficult for complex code

### 2. Dynamic Interval Analysis

Observe actual value ranges during execution.

**Approach**:
1. Instrument program to log values
2. Run with test inputs
3. Track min/max observed values
4. Build interval database

**Example**:
```python
# Instrumented code
def process(x):
    log_value('x', x)  # Log x
    y = x * 2
    log_value('y', y)  # Log y
    return y

# After running tests with x ∈ {1, 5, 10}:
# x: [1, 10] (observed)
# y: [2, 20] (observed)
```

**Advantages**:
- Precise for tested paths
- Easy to implement
- Reflects actual behavior

**Limitations**:
- Requires test suite
- Incomplete coverage
- Only observes tested values

### 3. Hybrid Analysis

Combine static and dynamic analysis.

**Approach**:
1. Run dynamic analysis to get concrete intervals
2. Use static analysis to extend coverage
3. Refine static intervals with dynamic observations
4. Validate static results with dynamic tests

**Benefits**:
- Better precision than pure static
- Better coverage than pure dynamic
- Validates static analysis results

## Handling Control Flow

### Conditional Branches

Refine intervals based on conditions:

```python
x = [0, 100]  # Initial interval

if x > 50:
    # In this branch: x ∈ [51, 100]
    y = x - 50
    # y ∈ [1, 50]
else:
    # In this branch: x ∈ [0, 50]
    y = x + 50
    # y ∈ [50, 100]

# After merge: y ∈ [1, 100]
```

### Loops

Compute fixed points for loop variables:

```python
x = 0  # x: [0, 0]

while x < 10:
    # Iteration 1: x ∈ [0, 0]
    # Iteration 2: x ∈ [0, 1]
    # Iteration 3: x ∈ [0, 2]
    # ...
    # Fixed point: x ∈ [0, 10]
    x = x + 1

# After loop: x ∈ [10, 10]
```

**Widening**: Accelerate convergence for complex loops:
```
If interval grows, widen to ∞:
[0, 10] → [0, 20] → [0, ∞]
```

**Narrowing**: Refine after fixed point:
```
Use loop condition to narrow:
[0, ∞] with condition x < 100 → [0, 99]
```

## Advanced Techniques

### Relational Analysis

Track relationships between variables:

```python
x = [0, 10]
y = x + 5
# Relation: y = x + 5
# If x = 3, then y = 8 (not just y ∈ [5, 15])
```

### Symbolic Intervals

Use symbolic bounds:

```python
def process(n):
    # n: [0, N] where N is symbolic
    x = [0, n]
    # x: [0, N]
    y = x * 2
    # y: [0, 2N]
```

### Modular Intervals

Track values modulo some number:

```python
x = [0, 100]
y = x % 10
# y: [0, 9] (modular arithmetic)
```

## Precision vs. Performance

### Precision Techniques

**Narrower intervals** (more precise):
- Path-sensitive analysis
- Relational analysis
- Symbolic execution
- SMT solvers

**Cost**: Higher computational complexity

### Performance Techniques

**Wider intervals** (less precise):
- Flow-insensitive analysis
- Widening operators
- Abstract interpretation
- Simple interval arithmetic

**Benefit**: Faster analysis

## Practical Applications

### 1. Overflow Detection

Check if intervals exceed type bounds:

```python
# int32 range: [-2147483648, 2147483647]
x = [1000000, 2000000]
y = [1000000, 2000000]
z = x * y
# z: [1000000000000, 4000000000000]
# Overflow! Exceeds int32 max
```

### 2. Array Bounds Checking

Verify array indices are valid:

```python
arr = [0] * 100  # Length 100
index = [0, 150]  # Potential out of bounds!
# WARNING: index may exceed array length
```

### 3. Division by Zero

Detect potential division by zero:

```python
x = [1, 10]
y = [-5, 5]  # Contains 0!
z = x / y
# ERROR: Division by zero possible
```

### 4. Test Case Generation

Generate boundary test cases:

```python
# Interval: x ∈ [0, 100]
# Test cases: 0, 1, 50, 99, 100
```

## Implementation Considerations

### Representation

**Concrete intervals**: `[3, 7]`
- Exact bounds
- Efficient operations

**Symbolic intervals**: `[0, N]`
- Parametric bounds
- More expressive

**Floating-point intervals**: `[3.14, 3.15]`
- Rounding considerations
- Precision issues

### Soundness

**Sound analysis**: Never underestimates possible values
- May report false positives
- Safe for verification

**Unsound analysis**: May miss some values
- Fewer false positives
- Not safe for verification

### Completeness

**Complete analysis**: Finds all possible values
- May be imprecise
- Conservative approximation

**Incomplete analysis**: May miss some values
- More precise
- Requires validation

## Tools and Libraries

### Python

- **PyInterval**: Interval arithmetic library
- **Z3**: SMT solver with interval support
- **Pyta**: Static analysis with intervals

### C/C++

- **APRON**: Numerical abstract domains
- **Frama-C**: Static analyzer with value analysis
- **CBMC**: Bounded model checker

### Java

- **Soot**: Program analysis framework
- **WALA**: Static analysis library
- **Checker Framework**: Pluggable type systems

## Best Practices

1. **Start with dynamic analysis**: Get concrete intervals from tests
2. **Use static analysis for coverage**: Extend to untested paths
3. **Validate results**: Check intervals against expected behavior
4. **Focus on critical variables**: Prioritize safety-critical code
5. **Document assumptions**: Record input interval assumptions
6. **Iterate and refine**: Improve precision incrementally
7. **Automate analysis**: Integrate into CI/CD pipeline

## Common Pitfalls

### Over-approximation

**Problem**: Intervals too wide to be useful
```python
x = [0, ∞]  # Too imprecise!
```

**Solution**: Use more precise analysis or add constraints

### Under-approximation

**Problem**: Missing possible values
```python
# Actual: x ∈ [0, 100]
# Computed: x ∈ [0, 50]  # Missing values!
```

**Solution**: Use sound analysis techniques

### Ignoring Overflow

**Problem**: Not checking type bounds
```python
x = [1000000, 2000000]
y = x * x  # Overflow not detected!
```

**Solution**: Always check against type limits

### Imprecise Loop Analysis

**Problem**: Widening too aggressively
```python
# Loop: for i in range(10)
# Computed: i ∈ [0, ∞]  # Too wide!
```

**Solution**: Use narrowing or better loop analysis

## References

- Cousot, P., & Cousot, R. (1977). "Abstract interpretation: a unified lattice model"
- Miné, A. (2006). "The octagon abstract domain"
- Blanchet, B., et al. (2003). "A static analyzer for large safety-critical software"
