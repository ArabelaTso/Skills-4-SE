# Path Exploration Strategies

Techniques for exploring execution paths during symbolic execution.

## Table of Contents

1. [Building Path Trees](#building-path-trees)
2. [Exploration Strategies](#exploration-strategies)
3. [Path Prioritization](#path-prioritization)
4. [Handling Loops](#handling-loops)
5. [State Management](#state-management)

---

## Building Path Trees

### Basic Path Tree Structure

```
                  [Initial State]
                   x = α, y = β
                        |
          +-------------+-------------+
          |                           |
    condition true            condition false
          |                           |
    [State 1]                    [State 2]
    PC: cond                    PC: ¬cond
          |                           |
    +-----+-----+               +-----+-----+
    |           |               |           |
 [S1.1]      [S1.2]         [S2.1]      [S2.2]
```

**Path Constraint (PC)**: Conjunction of all branch conditions along path.

### Manual Path Tree Construction

**Example Function:**

```python
def abs_value(x):
    if x < 0:
        result = -x
    else:
        result = x
    return result
```

**Path Tree:**

```
State 0: { x: α }
PC: (none)
  |
  +------ x < 0? ------+
  |                    |
  YES                  NO
  |                    |
State 1:           State 2:
{ result: -α }     { result: α }
PC: α < 0          PC: α ≥ 0
  |                    |
return -α          return α
```

**Paths:**
- Path 1: α < 0 → returns -α
- Path 2: α ≥ 0 → returns α

### Complex Example with Nested Branches

```python
def classify(x, y):
    if x > 0:
        if y > 0:
            return "Q1"  # First quadrant
        else:
            return "Q4"  # Fourth quadrant
    else:
        if y > 0:
            return "Q2"  # Second quadrant
        else:
            return "Q3"  # Third quadrant
```

**Path Tree:**

```
                State 0: { x: α, y: β }
                      PC: (none)
                          |
              +-----------+-----------+
              |                       |
           x > 0                   x ≤ 0
              |                       |
         PC: α > 0                PC: α ≤ 0
              |                       |
        +-----+-----+           +-----+-----+
        |           |           |           |
     y > 0       y ≤ 0       y > 0       y ≤ 0
        |           |           |           |
  PC: α>0∧β>0  PC: α>0∧β≤0  PC: α≤0∧β>0  PC: α≤0∧β≤0
        |           |           |           |
    "Q1"        "Q4"        "Q2"        "Q3"
    Path 1      Path 2      Path 3      Path 4
```

---

## Exploration Strategies

### 1. Depth-First Search (DFS)

Explore one path completely before backtracking.

**Algorithm:**
```
1. Start at root state
2. When encountering branch:
   - Push one branch to stack
   - Explore other branch immediately
3. When path terminates, pop from stack
4. Continue until stack empty
```

**Pros:**
- Memory efficient (only stores one path)
- Finds deep bugs quickly

**Cons:**
- May miss shallow bugs
- Can get stuck in deep paths

**Example:**
```
Order: Path 1 → Path 2 → Path 3 → Path 4
(Complete left subtree, then right subtree)
```

### 2. Breadth-First Search (BFS)

Explore all paths at depth n before depth n+1.

**Algorithm:**
```
1. Start with queue containing root state
2. Dequeue state, explore all immediate branches
3. Enqueue all child states
4. Repeat until queue empty
```

**Pros:**
- Finds shallow bugs first
- Systematic coverage

**Cons:**
- High memory usage
- Exponential growth with depth

**Example:**
```
Depth 0: Initial state
Depth 1: State after first branch
Depth 2: States after second branches
(All states at depth 1 before any at depth 2)
```

### 3. Random Path Selection

Randomly choose which branch to explore.

**Algorithm:**
```
1. At each branch, flip coin to decide direction
2. Continue until path terminates
3. Repeat with different random seeds
```

**Pros:**
- Good for finding rare bugs
- Avoids systematic biases

**Cons:**
- No coverage guarantee
- May revisit paths

### 4. Coverage-Guided Exploration

Prioritize paths that cover new code.

**Algorithm:**
```
1. Track covered lines/branches
2. Score each path by uncovered code it reaches
3. Explore highest-scoring paths first
```

**Pros:**
- Efficient coverage
- Finds bugs in unexplored code

**Cons:**
- Requires instrumentation
- May miss bugs in covered code

---

## Path Prioritization

### Bug-Distance Heuristic

Prioritize paths closer to potential bugs.

**Example: Prioritize paths leading to division**

```python
def compute(x, y):
    if x > 0:
        temp = x / y  # Potential div by zero
        return temp * 2
    else:
        return 0
```

**Prioritization:**
- Path with `x > 0`: HIGH priority (reaches division)
- Path with `x ≤ 0`: LOW priority (no division)

### Error-Prone Code Patterns

Prioritize paths containing:
- Pointer dereferences
- Array accesses
- Division operations
- Type casts
- External calls

### User-Specified Targets

Allow user to specify code locations to reach.

```python
# Target: Reach line 15
priority = distance_to_line(path, 15)
```

---

## Handling Loops

Loops cause path explosion. Mitigation strategies:

### 1. Loop Unrolling (Bounded)

Limit loop iterations to fixed bound.

**Example:**

```python
# Original
for i in range(n):
    process(i)

# Unrolled (k=3)
if n >= 1:
    process(0)
if n >= 2:
    process(1)
if n >= 3:
    process(2)
# Stop after k iterations
```

**Configuration:**
```python
MAX_LOOP_ITERATIONS = 10
```

### 2. Loop Summarization

Compute effect of entire loop symbolically.

**Example:**

```python
# Original
total = 0
for i in range(n):
    total += arr[i]

# Summary
total = sum(arr[0:n])
```

### 3. Loop Invariants

Define properties that hold at loop entry/exit.

**Example:**

```python
# Invariant: i ≤ n
i = 0
while i < n:
    process(i)
    i += 1
# After loop: i = n
```

### 4. Selective Loop Exploration

Explore only interesting iterations.

**Strategy:**
- First iteration (initialization)
- Last iteration (boundary)
- Middle iteration (typical case)
- Zero iterations (empty case)

---

## State Management

### State Representation

**State includes:**
```python
{
    'variables': {'x': α, 'y': β},
    'path_constraint': [α > 0, β < 10],
    'program_counter': 15,
    'memory': {...},
    'depth': 3
}
```

### State Merging

Combine states to reduce path explosion.

**When to merge:**
- States at same program location
- With compatible constraints
- After if-else rejoins

**Example:**

```python
# Two paths merge here:
if condition:
    x = 10
else:
    x = 20
# Merged state: x ∈ {10, 20}
y = x + 5  # y ∈ {15, 25}
```

**Implementation:**
```python
def merge_states(state1, state2):
    if state1.pc != state2.pc:
        return None  # Can't merge

    merged = State()
    merged.pc = state1.pc

    # Merge variables
    for var in state1.variables:
        if state1.variables[var] == state2.variables[var]:
            merged.variables[var] = state1.variables[var]
        else:
            # Create symbolic value representing both
            merged.variables[var] = ite(state1.path_constraint,
                                        state1.variables[var],
                                        state2.variables[var])

    return merged
```

### State Pruning

Eliminate infeasible states early.

**Pruning Conditions:**
- Unsatisfiable path constraint
- Exceeds resource limits (depth, time)
- Duplicates existing state

**Example:**

```python
def should_prune(state):
    # Check satisfiability
    solver = Solver()
    solver.add(state.path_constraint)
    if solver.check() == unsat:
        return True  # Infeasible path

    # Check depth limit
    if state.depth > MAX_DEPTH:
        return True

    return False
```

---

## Complete Example

**Function:**

```python
def search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

**Path Exploration (bounded unrolling, k=3):**

```
State 0: { arr: [α₁, α₂, α₃, ...], target: β, i: 0 }
PC: (none)

Iteration 0:
  Branch: arr[0] == target?
    YES: PC = (α₁ = β)
         Return 0
    NO:  PC = (α₁ ≠ β)
         Continue to i=1

Iteration 1 (given α₁ ≠ β):
  Branch: arr[1] == target?
    YES: PC = (α₁ ≠ β ∧ α₂ = β)
         Return 1
    NO:  PC = (α₁ ≠ β ∧ α₂ ≠ β)
         Continue to i=2

Iteration 2 (given α₁ ≠ β ∧ α₂ ≠ β):
  Branch: arr[2] == target?
    YES: PC = (α₁ ≠ β ∧ α₂ ≠ β ∧ α₃ = β)
         Return 2
    NO:  PC = (α₁ ≠ β ∧ α₂ ≠ β ∧ α₃ ≠ β)
         Exit loop, return -1
```

**Paths:**
1. Find at index 0: α₁ = β → return 0
2. Find at index 1: α₁ ≠ β ∧ α₂ = β → return 1
3. Find at index 2: α₁ ≠ β ∧ α₂ ≠ β ∧ α₃ = β → return 2
4. Not found: α₁ ≠ β ∧ α₂ ≠ β ∧ α₃ ≠ β → return -1

**Test Inputs (from constraint solving):**
```python
# Path 1
arr = [5, ...], target = 5  # α₁ = β

# Path 2
arr = [3, 5, ...], target = 5  # α₁ ≠ β ∧ α₂ = β

# Path 3
arr = [3, 7, 5, ...], target = 5  # α₁ ≠ β ∧ α₂ ≠ β ∧ α₃ = β

# Path 4
arr = [3, 7, 9], target = 5  # Not found
```

---

## Summary

**Strategy Selection:**

| Scenario | Recommended Strategy |
|----------|---------------------|
| Deep bugs | DFS |
| Shallow bugs | BFS |
| Rare bugs | Random |
| Maximum coverage | Coverage-guided |
| Specific targets | Bug-distance heuristic |

**Loop Handling:**

| Loop Type | Strategy |
|-----------|----------|
| Bounded loops | Full unrolling |
| Unbounded loops | Bounded unrolling (k iterations) |
| Simple loops | Summarization |
| Complex loops | Selective exploration |
