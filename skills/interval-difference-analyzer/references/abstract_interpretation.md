# Abstract Interpretation

## Overview

Abstract interpretation is a theory of sound approximation of program semantics, providing a mathematical framework for static program analysis. It forms the theoretical foundation for interval analysis and many other static analysis techniques.

## Core Concepts

### Concrete Semantics

The **concrete semantics** describes the actual execution behavior of a program.

**Example**:
```python
x = 5
y = x + 3
# Concrete state: {x: 5, y: 8}
```

### Abstract Semantics

The **abstract semantics** describes an approximation of the concrete behavior.

**Example**:
```python
x = [0, 10]  # Abstract: x can be any value in [0, 10]
y = x + 3
# Abstract state: {x: [0, 10], y: [3, 13]}
```

### Soundness

An abstract interpretation is **sound** if it over-approximates all possible concrete behaviors.

**Property**: If the abstract analysis says "no error", then no error can occur in any concrete execution.

## Mathematical Framework

### Lattices

A **lattice** is a partially ordered set with:
- **Join (⊔)**: Least upper bound (union)
- **Meet (⊓)**: Greatest lower bound (intersection)
- **Bottom (⊥)**: Least element (no information)
- **Top (⊤)**: Greatest element (any value)

**Interval Lattice Example**:
```
        ⊤ ([-∞, ∞])
       / | \
      /  |  \
   [0,10] [5,15] ...
     |  \/  |
     | [5,10]|
     |  /\  |
     [5,5] ...
       |
       ⊥ (empty)
```

### Galois Connection

A **Galois connection** relates concrete and abstract domains:

```
Concrete Domain ←→ Abstract Domain
      α ↓           ↑ γ
   (abstraction) (concretization)
```

**Properties**:
- α(C) ⊑ A ⟺ C ⊆ γ(A)
- α ∘ γ ⊑ id (abstraction loses information)
- id ⊑ γ ∘ α (concretization is sound)

**Example**:
```python
# Concrete: {1, 2, 3, 4, 5}
# α (abstraction) → [1, 5]
# γ (concretization) → {1, 2, 3, 4, 5} (and more)
```

## Abstract Domains

### Interval Domain

Represents sets of values as intervals.

**Abstract values**: `[min, max]`

**Operations**:
- Join: `[a,b] ⊔ [c,d] = [min(a,c), max(b,d)]`
- Meet: `[a,b] ⊓ [c,d] = [max(a,c), min(b,d)]`
- Add: `[a,b] + [c,d] = [a+c, b+d]`

**Example**:
```python
[1, 5] ⊔ [3, 8] = [1, 8]  # Union
[1, 5] ⊓ [3, 8] = [3, 5]  # Intersection
```

### Sign Domain

Tracks the sign of values.

**Abstract values**: `{-, 0, +, ⊤, ⊥}`

**Operations**:
```
+ × + = +
+ × - = -
+ × 0 = 0
- × - = +
```

**Example**:
```python
x = +  # Positive
y = -  # Negative
z = x + y  # ⊤ (unknown sign)
```

### Parity Domain

Tracks whether values are even or odd.

**Abstract values**: `{even, odd, ⊤, ⊥}`

**Operations**:
```
even + even = even
even + odd = odd
odd + odd = even
even × even = even
odd × odd = odd
```

### Octagon Domain

Tracks relationships of the form: `±x ± y ≤ c`

**Example constraints**:
```
x - y ≤ 5
x + y ≤ 10
-x + y ≤ 3
```

**More precise than intervals**:
```python
# Intervals: x ∈ [0, 10], y ∈ [0, 10]
# Octagon: x ∈ [0, 10], y ∈ [0, 10], x + y ≤ 10
# Octagon is more precise!
```

### Polyhedra Domain

Tracks arbitrary linear constraints: `a₁x₁ + a₂x₂ + ... ≤ c`

**Most precise but expensive**:
```python
# Constraints:
# x + y ≤ 10
# 2x - y ≥ 0
# x ≥ 0, y ≥ 0
```

## Fixed Point Computation

### Iterative Analysis

Compute fixed point by iteration:

```python
def analyze_loop():
    state = ⊥  # Initial state

    while not converged:
        new_state = transfer(state)
        state = state ⊔ new_state

    return state
```

### Widening

Accelerate convergence for loops:

**Widening operator (▽)**:
```python
[0, 10] ▽ [0, 20] = [0, ∞]
```

**Purpose**: Force convergence in finite steps

**Example**:
```python
x = 0
while x < 100:
    x = x + 1

# Without widening: [0,0] → [0,1] → [0,2] → ... (100 iterations)
# With widening: [0,0] → [0,1] → [0,∞] (converged!)
```

### Narrowing

Refine after widening:

**Narrowing operator (△)**:
```python
[0, ∞] △ [0, 100] = [0, 100]
```

**Purpose**: Improve precision after widening

**Example**:
```python
# After widening: x ∈ [0, ∞]
# Loop condition: x < 100
# After narrowing: x ∈ [0, 99]
```

## Transfer Functions

### Assignment

```python
# x = e
abstract_state[x] = eval(e, abstract_state)
```

**Example**:
```python
# x = [1, 5]
# y = x + 3
# Result: y = [4, 8]
```

### Conditional

```python
# if (condition)
true_state = filter(condition, abstract_state)
false_state = filter(not condition, abstract_state)
```

**Example**:
```python
# x = [0, 10]
# if x > 5:
#   true_branch: x ∈ [6, 10]
#   false_branch: x ∈ [0, 5]
```

### Join

```python
# Merge branches
result_state = true_state ⊔ false_state
```

**Example**:
```python
# if x > 5:
#   y = [10, 20]
# else:
#   y = [0, 5]
# After merge: y = [0, 20]
```

## Precision vs. Cost Trade-off

### Abstract Domain Hierarchy

```
Polyhedra (most precise, most expensive)
    ↑
Octagons
    ↑
Intervals
    ↑
Signs (least precise, least expensive)
```

### Choosing a Domain

**Intervals**: Good balance for most programs
- Moderate precision
- Efficient operations
- Widely applicable

**Octagons**: For relational properties
- Better precision
- Higher cost
- Good for array bounds

**Polyhedra**: For complex constraints
- Best precision
- Highest cost
- Use selectively

## Practical Applications

### 1. Buffer Overflow Detection

```python
arr = [0] * 100
index = [0, 150]  # Abstract interval

if index.max >= len(arr):
    report_error("Potential buffer overflow")
```

### 2. Division by Zero

```python
x = [1, 10]
y = [-5, 5]  # Contains 0!

if 0 in y:
    report_error("Potential division by zero")
```

### 3. Null Pointer Dereference

```python
ptr = {null, not_null}  # Abstract domain

if ptr == null:
    report_error("Potential null dereference")
```

### 4. Integer Overflow

```python
x = [1000000, 2000000]
y = x * x

if y.max > INT_MAX:
    report_error("Potential integer overflow")
```

## Implementation Strategies

### Worklist Algorithm

```python
def analyze(program):
    worklist = [entry_point]
    states = {entry_point: initial_state}

    while worklist:
        node = worklist.pop()
        old_state = states[node]
        new_state = transfer(node, old_state)

        if new_state != old_state:
            states[node] = new_state
            worklist.extend(successors(node))

    return states
```

### Modular Analysis

Analyze functions separately:

```python
def analyze_function(func):
    # Analyze function with abstract inputs
    abstract_inputs = get_input_intervals(func)
    abstract_outputs = analyze(func, abstract_inputs)
    return abstract_outputs
```

### Incremental Analysis

Reuse previous results:

```python
def incremental_analyze(program, changes):
    # Only re-analyze affected parts
    affected = compute_affected(changes)
    for node in affected:
        reanalyze(node)
```

## Limitations

### Imprecision

Abstract interpretation may report false positives:

```python
x = [0, 10]
if x == 5:
    y = 1 / (x - 5)  # Actually safe!
# But analysis reports: potential division by zero
```

### Scalability

Complex domains are expensive:

- Polyhedra: Exponential complexity
- Octagons: Cubic complexity
- Intervals: Linear complexity

### Incompleteness

Cannot prove all properties:

```python
# Halting problem: undecidable
while complex_condition():
    do_something()
# Cannot determine if loop terminates
```

## Best Practices

1. **Choose appropriate domain**: Balance precision and cost
2. **Use widening carefully**: Avoid losing too much precision
3. **Apply narrowing**: Refine results after widening
4. **Modular analysis**: Analyze functions separately
5. **Incremental updates**: Reuse previous results
6. **Validate results**: Check against test cases
7. **Document assumptions**: Record input constraints

## Tools Using Abstract Interpretation

### Research Tools

- **ASTRÉE**: Aerospace software verification
- **Frama-C**: C program analysis
- **APRON**: Numerical abstract domains library

### Commercial Tools

- **Polyspace**: MATLAB/C/C++ verification
- **CodeSonar**: Static analysis tool
- **Coverity**: Bug finding tool

## References

- Cousot, P., & Cousot, R. (1977). "Abstract interpretation: a unified lattice model for static analysis"
- Cousot, P., & Halbwachs, N. (1978). "Automatic discovery of linear restraints among variables"
- Miné, A. (2006). "The octagon abstract domain"
- Blanchet, B., et al. (2003). "A static analyzer for large safety-critical software"
