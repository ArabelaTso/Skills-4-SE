# Abstract Domains Reference

This reference provides comprehensive information about abstract interpretation and various abstract domains used for static program analysis.

## Table of Contents

1. [Abstract Interpretation Fundamentals](#abstract-interpretation-fundamentals)
2. [Interval Domain](#interval-domain)
3. [Octagon Domain](#octagon-domain)
4. [Polyhedra Domain](#polyhedra-domain)
5. [Sign Domain](#sign-domain)
6. [Congruence Domain](#congruence-domain)
7. [Reduced Product Domains](#reduced-product-domains)
8. [Widening and Narrowing](#widening-and-narrowing)
9. [Domain Operations](#domain-operations)
10. [Analysis Examples](#analysis-examples)

## Abstract Interpretation Fundamentals

### Core Concepts

**Abstract Interpretation:**
A theory of sound approximation of program semantics. It computes over-approximations of all possible program behaviors using abstract domains.

**Concrete Domain:**
The actual set of all possible program states (typically infinite or very large).

**Abstract Domain:**
A finite representation that approximates the concrete domain, trading precision for computability.

**Galois Connection:**
A pair of functions (α, γ) connecting concrete and abstract domains:
- α: Concrete → Abstract (abstraction function)
- γ: Abstract → Concrete (concretization function)

**Soundness:**
An analysis is sound if it never misses any possible behavior. Over-approximation ensures soundness.

### Lattice Structure

Abstract domains form a complete lattice with:
- **⊥ (bottom)**: Empty set, no values
- **⊤ (top)**: All possible values, unknown
- **⊔ (join)**: Least upper bound, union of information
- **⊓ (meet)**: Greatest lower bound, intersection of information
- **⊑ (ordering)**: Partial order, precision relation

## Interval Domain

### Definition

The interval domain represents each variable as an interval [l, u] where l is the lower bound and u is the upper bound.

**Representation:**
- x ∈ [a, b] means a ≤ x ≤ b
- [a, a] represents a single value
- [-∞, +∞] represents ⊤ (unknown)
- Empty interval represents ⊥ (unreachable)

### Operations

**Addition:**
[a, b] + [c, d] = [a + c, b + d]

**Subtraction:**
[a, b] - [c, d] = [a - d, b - c]

**Multiplication:**
[a, b] × [c, d] = [min(ac, ad, bc, bd), max(ac, ad, bc, bd)]

**Division:**
[a, b] / [c, d] = [a, b] × [1/d, 1/c] (if 0 ∉ [c, d])

**Join (Union):**
[a, b] ⊔ [c, d] = [min(a, c), max(b, d)]

**Meet (Intersection):**
[a, b] ⊓ [c, d] = [max(a, c), min(b, d)] (if max(a, c) ≤ min(b, d), else ⊥)

### Example Analysis

```c
int x = 0;        // x ∈ [0, 0]
int y = 10;       // y ∈ [10, 10]
int z = x + y;    // z ∈ [10, 10]
if (x < 5) {
    x = x + 1;    // x ∈ [1, 1]
}
// After join: x ∈ [0, 1]
```

### Strengths and Limitations

**Strengths:**
- Simple and efficient
- Good for range analysis
- Low memory overhead

**Limitations:**
- Cannot express relationships between variables
- Loses precision on joins
- Cannot represent x = y or x + y = 10

## Octagon Domain

### Definition

The octagon domain represents constraints of the form:
- ±x ± y ≤ c (where c is a constant)

This includes:
- x - y ≤ c
- x + y ≤ c
- -x - y ≤ c
- -x + y ≤ c

**Representation:**
Stored as a Difference Bound Matrix (DBM) with 2n dimensions for n variables.

### Expressiveness

**Can represent:**
- Intervals: x ≤ 5 (as x - 0 ≤ 5)
- Relationships: x ≤ y + 3
- Sums: x + y ≤ 10
- Differences: x - y ≤ 2

**Cannot represent:**
- General linear inequalities: 2x + 3y ≤ 10
- Non-octagonal constraints

### Example Analysis

```c
int x = 0;        // x ∈ [0, 0]
int y = 0;        // y ∈ [0, 0], x = y
while (x < 10) {
    x = x + 1;    // x ∈ [1, 10]
    y = y + 1;    // y ∈ [1, 10], x = y
}
// Octagon infers: x = y, x ∈ [10, 10], y ∈ [10, 10]
```

**Invariant discovered:** x - y = 0 (maintained throughout loop)

### Operations

**Join:**
Compute convex hull of two octagons (may lose precision).

**Meet:**
Intersection of constraints.

**Widening:**
Extrapolate constraints to ensure termination:
- Remove unstable bounds
- Widen to ±∞ for diverging constraints

### Strengths and Limitations

**Strengths:**
- Captures relationships between pairs of variables
- More precise than intervals
- Efficient representation (O(n²) space)
- Good for loop invariants

**Limitations:**
- Cannot express general linear constraints
- More expensive than intervals (O(n³) operations)
- Limited to octagonal constraints

## Polyhedra Domain

### Definition

The polyhedra domain represents arbitrary linear constraints:
- a₁x₁ + a₂x₂ + ... + aₙxₙ ≤ c

**Representation:**
- Constraint representation: Set of linear inequalities
- Generator representation: Convex hull of vertices and rays

### Expressiveness

**Can represent:**
- All interval constraints
- All octagon constraints
- General linear relationships: 2x + 3y ≤ 10
- Complex invariants: x + y = z, 3x - 2y ≤ 5z + 7

**Cannot represent:**
- Non-linear constraints: x × y ≤ 10
- Disjunctions: x < 0 ∨ x > 10

### Example Analysis

```c
int x = 0, y = 0, z = 0;
while (x < 10) {
    x = x + 1;
    y = y + 2;
    z = x + y;
}
// Polyhedra infers:
// x ∈ [10, 10]
// y ∈ [20, 20]
// z ∈ [30, 30]
// Invariant: z = x + y, y = 2x
```

### Operations

**Join:**
Compute convex hull (exact but expensive).

**Meet:**
Intersection of polyhedra.

**Projection:**
Eliminate variables using Fourier-Motzkin elimination.

**Widening:**
Standard widening: remove constraints not satisfied by both operands.

### Strengths and Limitations

**Strengths:**
- Most expressive numerical domain
- Can capture complex linear relationships
- Exact operations (no precision loss except widening)

**Limitations:**
- Expensive: exponential worst-case complexity
- High memory usage
- Slow convergence on complex programs
- Not suitable for large-scale analysis

## Sign Domain

### Definition

The sign domain tracks the sign of integer variables.

**Lattice:**
```
        ⊤ (unknown)
       /  |  \
      /   |   \
    <0   =0   >0
      \   |   /
       \  |  /
        ⊥ (empty)
```

**Values:**
- ⊥: Empty (unreachable)
- <0: Negative
- =0: Zero
- >0: Positive
- ≤0: Non-positive
- ≥0: Non-negative
- ≠0: Non-zero
- ⊤: Unknown

### Operations

**Addition:**
- <0 + <0 = <0
- >0 + >0 = >0
- <0 + >0 = ⊤
- =0 + x = x

**Multiplication:**
- <0 × <0 = >0
- <0 × >0 = <0
- >0 × >0 = >0
- =0 × x = =0

**Join:**
Least upper bound in the lattice.

### Example Analysis

```c
int x = -5;       // x: <0
int y = 10;       // y: >0
int z = x + y;    // z: ⊤ (unknown sign)
if (z > 0) {
    // z: >0
} else {
    // z: ≤0
}
```

### Strengths and Limitations

**Strengths:**
- Very efficient (constant time operations)
- Useful for detecting sign errors
- Good for division by zero detection

**Limitations:**
- Very imprecise
- No information about magnitudes
- Loses information quickly

## Congruence Domain

### Definition

The congruence domain represents values modulo a constant:
- x ≡ a (mod b) means x = a + kb for some integer k

**Representation:**
- (a, b): x ≡ a (mod b)
- (a, 0): x = a (single value)
- (0, 1): x ≡ 0 (mod 1) = ⊤ (all integers)

### Operations

**Addition:**
(a, b) + (c, d) = (a + c, gcd(b, d))

**Multiplication by constant k:**
k × (a, b) = (ka, kb)

**Join:**
(a, b) ⊔ (c, d) = (a, gcd(b, d, |a - c|))

### Example Analysis

```c
int x = 0;        // x: (0, 0)
while (x < 100) {
    x = x + 2;    // x: (0, 2) - always even
}
// Invariant: x ≡ 0 (mod 2)
```

```c
int i = 0;        // i: (0, 0)
int sum = 0;      // sum: (0, 0)
while (i < 10) {
    sum = sum + 3;  // sum: (0, 3)
    i = i + 1;
}
// Invariant: sum ≡ 0 (mod 3)
```

### Strengths and Limitations

**Strengths:**
- Detects modular patterns
- Useful for array indexing analysis
- Complements interval domain well

**Limitations:**
- No information about ranges
- Limited expressiveness
- Best used in combination with other domains

## Reduced Product Domains

### Definition

A reduced product combines multiple abstract domains to gain precision from both.

**Product Domain:**
(D₁ × D₂) represents elements as pairs (d₁, d₂).

**Reduced Product:**
Applies reduction functions to exchange information between domains and eliminate inconsistencies.

### Common Combinations

**Interval × Congruence:**
```c
int x = 0;
while (x < 100) {
    x = x + 2;
}
// Interval: x ∈ [0, 100]
// Congruence: x ≡ 0 (mod 2)
// Reduced: x ∈ {0, 2, 4, ..., 100}
```

**Interval × Sign:**
```c
int x = 5;        // Interval: [5, 5], Sign: >0
x = x - 10;       // Interval: [-5, -5], Sign: <0
// Reduction confirms consistency
```

### Reduction Operations

**Interval → Congruence:**
If x ∈ [a, a], then x ≡ a (mod n) for any n.

**Congruence → Interval:**
If x ≡ a (mod b) and x ∈ [l, u], refine bounds to match congruence.

**Example:**
- x ∈ [10, 20] and x ≡ 1 (mod 3)
- Reduced: x ∈ {10, 13, 16, 19}
- Tighter interval: x ∈ [10, 19]

### Strengths and Limitations

**Strengths:**
- Combines strengths of multiple domains
- More precise than individual domains
- Can detect inconsistencies

**Limitations:**
- Higher computational cost
- More complex implementation
- Reduction may be incomplete

## Widening and Narrowing

### Widening

**Purpose:**
Ensure termination of fixpoint computation by accelerating convergence.

**Principle:**
When iterating, extrapolate to a stable upper bound instead of computing exact join.

**Interval Widening:**
```
[a, b] ∇ [c, d] = [if c < a then -∞ else a, if d > b then +∞ else b]
```

**Example:**
```c
int x = 0;
while (x < 100) {
    x = x + 1;
}
```

Iterations without widening:
- Iteration 0: x ∈ [0, 0]
- Iteration 1: x ∈ [0, 1]
- Iteration 2: x ∈ [0, 2]
- ... (100 iterations)

With widening (applied at iteration 2):
- Iteration 0: x ∈ [0, 0]
- Iteration 1: x ∈ [0, 1]
- Iteration 2: x ∈ [0, 0] ∇ [0, 1] = [0, +∞]
- Converged!

**Widening with Thresholds:**
Use a set of thresholds T = {0, 1, 10, 100, 1000, ...} to improve precision:
```
[a, b] ∇_T [c, d] = [if c < a then max{t ∈ T | t ≤ c} else a,
                      if d > b then min{t ∈ T | t ≥ d} else b]
```

### Narrowing

**Purpose:**
Refine over-approximations obtained by widening.

**Principle:**
Iteratively improve the result by computing meets with loop body semantics.

**Interval Narrowing:**
```
[a, b] △ [c, d] = [if a = -∞ then c else a, if b = +∞ then d else b]
```

**Example:**
After widening: x ∈ [0, +∞]
After narrowing with condition x < 100: x ∈ [0, 99]

### Widening/Narrowing Strategy

1. **Ascending phase (widening):**
   - Compute fixpoint with widening
   - Ensures termination
   - May be imprecise

2. **Descending phase (narrowing):**
   - Refine result with narrowing
   - Improves precision
   - Limited iterations (typically 1-3)

## Domain Operations

### Transfer Functions

Transfer functions define how abstract values change through program statements.

**Assignment: x = e**
- Evaluate expression e in abstract domain
- Update abstract state for x

**Condition: assume(c)**
- Refine abstract state based on condition c
- Intersection with constraint

**Join: merge control flow**
- Compute least upper bound of incoming states
- Used at merge points (after if-else, loops)

### Example Transfer Functions (Intervals)

**x = y + 5:**
If y ∈ [a, b], then x ∈ [a + 5, b + 5]

**x = y * 2:**
If y ∈ [a, b], then x ∈ [2a, 2b]

**assume(x > 5):**
If x ∈ [a, b], then x ∈ [max(a, 6), b]

**assume(x < 10):**
If x ∈ [a, b], then x ∈ [a, min(b, 9)]

### Fixpoint Computation

**Forward Analysis:**
```
1. Initialize: entry state = initial abstract value
2. Repeat until convergence:
   - For each program point:
     - Compute abstract state by applying transfer functions
     - Join with previous state (with widening if needed)
3. Apply narrowing if desired
```

**Loop Analysis:**
```
while (condition) {
    body
}
```

1. Before loop: state₀
2. Iteration 1: state₁ = transfer(body, state₀)
3. Iteration 2: state₂ = transfer(body, state₁)
4. Apply widening: state_w = state₁ ∇ state₂
5. Check convergence
6. Apply narrowing if needed

## Analysis Examples

### Example 1: Simple Loop (Intervals)

```c
int x = 0;
int y = 100;
while (x < 10) {
    x = x + 1;
    y = y - 1;
}
```

**Analysis:**
- Entry: x ∈ [0, 0], y ∈ [100, 100]
- Iteration 1: x ∈ [1, 1], y ∈ [99, 99]
- Iteration 2: x ∈ [0, 2], y ∈ [98, 100]
- Widening: x ∈ [0, +∞], y ∈ [-∞, 100]
- Refine with condition x < 10: x ∈ [0, 9], y ∈ [-∞, 100]
- Narrowing: x ∈ [0, 9], y ∈ [91, 100]
- Exit: x ∈ [10, 10], y ∈ [90, 90]

**Invariant:** x + y = 100

### Example 2: Nested Loops (Octagons)

```c
int i = 0, j = 0;
while (i < 10) {
    j = 0;
    while (j < i) {
        j = j + 1;
    }
    i = i + 1;
}
```

**Analysis:**
- Outer loop: i ∈ [0, 10]
- Inner loop: j ∈ [0, i], j ≤ i
- Exit: i ∈ [10, 10], j ∈ [9, 9]

**Invariants:**
- j ≤ i (octagon captures this)
- i ∈ [0, 10]
- j ∈ [0, 9]

### Example 3: Linear Relationships (Polyhedra)

```c
int x = 0, y = 0, z = 0;
while (x < 10) {
    x = x + 1;
    y = y + 2;
    z = x + y;
}
```

**Analysis:**
- Polyhedra infers: y = 2x, z = 3x
- Exit: x = 10, y = 20, z = 30

**Invariants:**
- y = 2x
- z = x + y
- z = 3x

### Example 4: Modular Arithmetic (Congruence)

```c
int sum = 0;
for (int i = 0; i < 100; i++) {
    sum = sum + 3;
}
```

**Analysis:**
- Congruence: sum ≡ 0 (mod 3)
- Interval: sum ∈ [0, 300]
- Combined: sum ∈ {0, 3, 6, ..., 297, 300}

**Invariant:** sum ≡ 0 (mod 3)

### Example 5: Sign Analysis

```c
int balance = 1000;
int withdrawal = read_input();
balance = balance - withdrawal;
if (balance < 0) {
    error("Insufficient funds");
}
```

**Analysis:**
- balance: [1000, 1000], >0
- withdrawal: [-∞, +∞], ⊤
- balance after: [-∞, +∞], ⊤
- In error branch: balance: [-∞, -1], <0

**Detects:** Possible negative balance

### Example 6: Array Bounds (Intervals + Congruence)

```c
int arr[10];
int i = 0;
while (i < 10) {
    arr[i] = 0;
    i = i + 1;
}
```

**Analysis:**
- Interval: i ∈ [0, 9] in loop body
- Congruence: i ≡ 0 (mod 1) (all integers)
- Array access: arr[i] where i ∈ [0, 9]

**Proves:** No array bounds violation

### Example 7: Division by Zero (Sign + Intervals)

```c
int x = read_input();
int y = x * x;
int z = 100 / y;
```

**Analysis:**
- x: [-∞, +∞], ⊤
- y = x * x: [0, +∞], ≥0
- Problem: y could be 0 if x = 0
- Division 100 / y: potential division by zero

**Detects:** Possible division by zero when x = 0

