# Abstract Domains

## Overview

Abstract domains are mathematical structures that represent sets of concrete values in a compact way. They enable efficient static analysis by trading precision for tractability.

## Core Abstract Domains

### 1. Interval Domain

**Purpose**: Track numeric ranges

**Lattice Elements**: `[a, b]` where a, b ∈ ℤ ∪ {-∞, +∞}

**Operations**:
```
[a, b] + [c, d] = [a+c, b+d]
[a, b] - [c, d] = [a-d, b-c]
[a, b] * [c, d] = [min(ac,ad,bc,bd), max(ac,ad,bc,bd)]
[a, b] / [c, d] = [a, b] * [1/d, 1/c]  (if 0 ∉ [c,d])

[a, b] ⊔ [c, d] = [min(a,c), max(b,d)]  (join)
[a, b] ⊓ [c, d] = [max(a,c), min(b,d)]  (meet)
```

**Example**:
```python
x = 5           # x: [5, 5]
y = x + 3       # y: [8, 8]
if y > 10:
    z = y - 2   # z: [9, ∞] (since y: [11, ∞])
else:
    z = y + 1   # z: [-∞, 11] (since y: [-∞, 10])
# After join: z: [-∞, ∞]
```

**Widening** (for loop convergence):
```
[a, b] ∇ [c, d] = [if c < a then -∞ else a, if d > b then +∞ else b]
```

### 2. Sign Domain

**Purpose**: Track sign of numeric values

**Lattice**:
```
        ⊤
    /   |   \
   +    0    -
    \   |   /
        ⊥
```

**Elements**: {⊥, +, 0, -, ⊤}
- ⊥: No value (unreachable)
- +: Positive
- 0: Zero
- -: Negative
- ⊤: Unknown

**Operations**:
```
+ + + = +
+ + 0 = +
+ + - = ⊤
0 + 0 = 0
- + - = -

+ * + = +
+ * 0 = 0
+ * - = -
0 * _ = 0
- * - = +

+ / + = +
+ / - = -
_ / 0 = ⊥ (error)
```

**Example**:
```python
x = 5           # x: +
y = -3          # y: -
z = x + y       # z: ⊤ (could be +, 0, or -)
if z > 0:
    w = 10 / z  # w: + (safe, z: +)
else:
    w = 10 / z  # w: - or ⊥ (z could be 0!)
```

### 3. Null Domain

**Purpose**: Track null/non-null status of pointers/references

**Lattice**:
```
        ⊤
    /       \
  null   not-null
    \       /
        ⊥
```

**Elements**: {⊥, null, not-null, ⊤}
- ⊥: No value (unreachable)
- null: Definitely null
- not-null: Definitely not null
- ⊤: Unknown (maybe null)

**Operations**:
```
Dereference:
  not-null → safe
  null → error
  ⊤ → potential error

Null check (x == null):
  True branch: x = null
  False branch: x = not-null

Assignment:
  x = new Object() → x: not-null
  x = null → x: null
  x = y → x: abstract_value(y)
```

**Example**:
```python
def process(obj):
    # obj: ⊤ (unknown)
    if obj is None:
        # obj: null
        return
    # obj: not-null
    obj.method()  # Safe!
```

### 4. Type Domain

**Purpose**: Track possible types of variables (for dynamic languages)

**Elements**: Sets of types, e.g., {int}, {str}, {int, str}, ⊤

**Operations**:
```
typeof(x) ∈ T → x: T
x = 5 → x: {int}
x = "hello" → x: {str}

Union: {int} ⊔ {str} = {int, str}
Meet: {int, str} ⊓ {int} = {int}
```

**Example**:
```python
def process(x):
    # x: ⊤ (any type)
    if isinstance(x, int):
        # x: {int}
        y = x + 1  # Safe
    else:
        # x: ⊤ \ {int}
        y = x + 1  # Potential type error
```

### 5. Constant Propagation Domain

**Purpose**: Track exact constant values

**Elements**: Concrete values ∪ {⊤, ⊥}

**Operations**:
```
5 + 3 = 8
5 + ⊤ = ⊤
⊤ + ⊤ = ⊤
```

**Example**:
```python
x = 5           # x: 5
y = 3           # y: 3
z = x + y       # z: 8
arr[z]          # arr[8] - exact index known
```

### 6. Parity Domain

**Purpose**: Track even/odd property

**Lattice**:
```
        ⊤
    /       \
  even     odd
    \       /
        ⊥
```

**Operations**:
```
even + even = even
even + odd = odd
odd + odd = even

even * _ = even
odd * odd = odd
```

## Relational Domains

### Octagon Domain

**Purpose**: Track relationships between variables

**Form**: ±x ± y ≤ c

**Example**:
```python
x = 0
y = 0
while x < 10:
    x += 1
    y += 1
# Octagon: x - y = 0, x ≤ 10, y ≤ 10
```

**Advantages**: More precise than intervals
**Disadvantages**: More expensive

### Polyhedra Domain

**Purpose**: Track linear relationships

**Form**: a₁x₁ + a₂x₂ + ... + aₙxₙ ≤ c

**Example**:
```python
x = 0
y = 0
while x + y < 100:
    if random():
        x += 1
    else:
        y += 1
# Polyhedra: x + y ≤ 100, x ≥ 0, y ≥ 0
```

**Advantages**: Very precise
**Disadvantages**: Expensive (exponential worst case)

## Product Domains

Combine multiple domains for more precision:

**Example**: Interval × Null Domain
```python
def access(arr, index):
    # arr: (not-null, _)
    # index: (_, [0, ∞])
    if index < len(arr):
        # index: (_, [0, len(arr)-1])
        return arr[index]  # Safe!
```

## Reduced Product

Domains can exchange information:

**Example**: Sign × Parity
```python
x = 5  # x: (+, odd)
y = 2  # y: (+, even)
z = x + y  # z: (+, odd)
# Sign domain: + + + = +
# Parity domain: odd + even = odd
# Reduced: (+, odd) is more precise than (⊤, odd) or (+, ⊤)
```

## Domain Selection Guidelines

**For array bounds checking**: Interval domain
**For division by zero**: Sign domain or interval domain
**For null dereferences**: Null domain
**For type errors**: Type domain
**For precise numeric analysis**: Polyhedra or octagon domain
**For efficiency**: Sign or parity domain
**For general purpose**: Interval × Null product domain

## Precision vs. Cost Trade-off

```
Cost:     Low ←―――――――――――――――――――――――――――――――→ High
Precision: Low ←―――――――――――――――――――――――――――――――→ High

Sign < Interval < Octagon < Polyhedra
Parity < Constant Propagation
```

Choose based on:
- Analysis goals (what errors to detect)
- Code complexity (loops, conditionals)
- Performance requirements
- Desired precision
