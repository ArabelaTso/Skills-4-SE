# Abstract Interpretation Concepts

## Overview

Abstract interpretation is a theory of sound approximation of program semantics. It provides a framework for analyzing program behavior by computing over-approximations of the set of possible runtime states.

## Core Concepts

### Abstract Domains

Abstract domains represent sets of concrete values in a simplified form:

**Numerical Domains:**
- **Intervals**: `[a, b]` represents all values between a and b
- **Signs**: {-, 0, +, ⊤} represents negative, zero, positive, or unknown
- **Octagons**: Linear constraints of form ±x ±y ≤ c
- **Polyhedra**: Arbitrary linear constraints

**Non-Numerical Domains:**
- **Constant propagation**: Tracks known constant values
- **Parity**: {even, odd, ⊤} for integer values
- **Nullness**: {null, non-null, ⊤} for pointers/references
- **Type domains**: Tracks possible types of values

### Lattice Operations

**Join (∪)**: Combines information from multiple paths
- Example: `[1,5] ∪ [3,8] = [1,8]`
- Represents union of possible values

**Meet (∩)**: Refines information from constraints
- Example: `[1,10] ∩ [5,15] = [5,10]`
- Represents intersection of possible values

**Widening (∇)**: Ensures termination by accelerating convergence
- Example: `[0,n] ∇ [0,n+1] = [0,+∞]`
- Used at loop heads to guarantee fixpoint

**Narrowing (△)**: Refines widened results
- Example: `[0,+∞] △ [0,100] = [0,100]`
- Used after widening to improve precision

### Transfer Functions

Transfer functions model how statements affect abstract states:

**Assignment**: `x = e`
- Evaluate expression e in abstract domain
- Update abstract state for variable x

**Conditional**: `if (condition)`
- Refine abstract state based on condition
- Different states for true/false branches

**Loop**: `while (condition)`
- Compute fixpoint using widening
- Optionally refine with narrowing

## Control Flow Analysis

### Control Flow Graph (CFG)

Represents program structure as directed graph:
- **Nodes**: Program points (statements, basic blocks)
- **Edges**: Control flow transitions
- **Entry**: Program start
- **Exit**: Program termination points

### Path Sensitivity

**Path-insensitive**: Single abstract state per program point
- Merges all paths reaching a point
- More efficient, less precise

**Path-sensitive**: Separate states for different paths
- Tracks conditions along paths
- More precise, more expensive

**Trace partitioning**: Hybrid approach
- Partition based on key predicates
- Balance precision and cost

## Variable Relationships

### Relational Domains

Track relationships between variables:

**Equality domain**: Tracks which variables have equal values
- Example: `x = y` implies `x == y`

**Interval congruences**: Combines intervals with modular arithmetic
- Example: `x ∈ [0,100] ∧ x ≡ 0 (mod 4)`

**Octagons**: Constraints of form `±x ±y ≤ c`
- Example: `x - y ≤ 5 ∧ x + y ≤ 10`

**Polyhedra**: General linear constraints
- Example: `2x + 3y ≤ 10 ∧ x - y ≥ 0`

### Dependency Analysis

**Data dependencies**: Which variables affect which computations
- **Def-use chains**: Where variables are defined and used
- **Use-def chains**: Which definitions reach each use

**Control dependencies**: Which conditions affect execution
- **Dominance**: Which nodes must execute before others
- **Post-dominance**: Which nodes must execute after others

## Runtime State Abstraction

### Memory Abstraction

**Stack abstraction**:
- Abstract stack frames
- Track local variable states
- Model call/return behavior

**Heap abstraction**:
- **Allocation-site**: Group objects by allocation location
- **Type-based**: Group objects by type
- **Shape analysis**: Track heap structure (lists, trees)

**Pointer abstraction**:
- **Points-to sets**: Which objects a pointer may reference
- **Must-alias**: Pointers that definitely point to same object
- **May-alias**: Pointers that might point to same object

### Exception Handling

**Exception flow**:
- Track which exceptions may be thrown
- Model try-catch-finally blocks
- Propagate exceptional states

**Resource management**:
- Track resource acquisition/release
- Detect leaks and double-frees
- Model cleanup in finally blocks

## Trace Summarization Techniques

### Loop Summarization

**Loop invariants**: Properties that hold at loop head
- Computed via fixpoint iteration
- Refined with narrowing

**Loop bounds**: Iteration count estimates
- Constant bounds: `for i in range(10)`
- Symbolic bounds: `for i in range(n)`
- Unbounded: `while condition`

**Loop effects**: How loop modifies state
- Which variables are modified
- Relationships between iterations
- Accumulated effects

### Function Summarization

**Preconditions**: Required input states
- Parameter constraints
- Global state requirements

**Postconditions**: Guaranteed output states
- Return value properties
- Side effects on parameters
- Global state modifications

**Frame conditions**: What remains unchanged
- Unmodified variables
- Preserved invariants

### Path Summarization

**Symbolic execution**: Track symbolic values along paths
- Path conditions (constraints)
- Symbolic expressions for variables
- Feasibility checking

**Abstract execution**: Track abstract values along paths
- Abstract path conditions
- Abstract expressions
- Over-approximation of reachable states

## Precision vs Performance Trade-offs

### Precision Techniques

**More precise (slower)**:
- Path-sensitive analysis
- Relational domains (polyhedra)
- Context-sensitive function analysis
- Flow-sensitive analysis

**Less precise (faster)**:
- Path-insensitive analysis
- Non-relational domains (intervals)
- Context-insensitive function analysis
- Flow-insensitive analysis

### Scalability Strategies

**Modular analysis**: Analyze functions separately
- Compute function summaries
- Reuse summaries at call sites
- Compositional reasoning

**Incremental analysis**: Reuse previous results
- Only re-analyze changed code
- Propagate changes efficiently

**Selective precision**: Apply precision where needed
- Use cheap analysis by default
- Refine critical regions
- Guided by queries or alarms

## Common Abstract Interpretation Patterns

### Interval Analysis Pattern

```
State: Map from variables to intervals

transfer(x = e, state):
    interval = eval_interval(e, state)
    return state[x := interval]

transfer(if x < c, state):
    true_state = state ∩ {x < c}
    false_state = state ∩ {x ≥ c}
    return (true_state, false_state)

fixpoint(loop_head, initial_state):
    state = initial_state
    repeat:
        old_state = state
        body_state = analyze_loop_body(state)
        state = state ∇ body_state
    until state = old_state
    return state
```

### Sign Analysis Pattern

```
Signs: {-, 0, +, ⊤}

abstract_add(s1, s2):
    if s1 = + and s2 = +: return +
    if s1 = - and s2 = -: return -
    if s1 = 0: return s2
    if s2 = 0: return s1
    return ⊤

abstract_mult(s1, s2):
    if s1 = 0 or s2 = 0: return 0
    if s1 = + and s2 = +: return +
    if s1 = - and s2 = -: return +
    if s1 = + and s2 = -: return -
    if s1 = - and s2 = +: return -
    return ⊤
```

### Nullness Analysis Pattern

```
Nullness: {null, non-null, ⊤}

transfer(x = new Object(), state):
    return state[x := non-null]

transfer(x = null, state):
    return state[x := null]

transfer(if x == null, state):
    true_state = state[x := null]
    false_state = state[x := non-null]
    return (true_state, false_state)

transfer(x.method(), state):
    if state[x] = null:
        report_error("Null pointer dereference")
    return state
```

## Trace Representation Formats

### Textual Representation

**Linear trace**:
```
L1: x = 0, y = 10
L2: x ∈ [0,10], y ∈ [0,10]
L3: x ∈ [0,10], y ∈ [0,10], x + y ≤ 20
```

**Tree representation**:
```
Entry: x = ⊤, y = ⊤
├─ if x > 0:
│  └─ x ∈ [1,+∞], y = ⊤
└─ else:
   └─ x ∈ [-∞,0], y = ⊤
```

### Graphical Representation

**State transition diagram**:
- Nodes: Abstract states
- Edges: Transitions with conditions
- Labels: Program locations

**Abstract reachability graph**:
- Nodes: (location, abstract state) pairs
- Edges: Statement executions
- Paths: Possible execution traces

### Symbolic Representation

**Constraints**:
```
Path 1: x > 0 ∧ y < 10 ∧ x + y = z
Path 2: x ≤ 0 ∧ y ≥ 10 ∧ x - y = z
```

**Formulas**:
```
∀ paths: x ∈ [-100, 100] ∧ y ∈ [0, 50]
∃ path: x = 0 ∧ y = 0
```

## Analysis Soundness and Completeness

### Soundness

**Over-approximation**: Abstract analysis includes all concrete behaviors
- No false negatives (all bugs are reported or covered)
- May have false positives (spurious warnings)

**Under-approximation**: Abstract analysis is subset of concrete behaviors
- No false positives (all warnings are real bugs)
- May have false negatives (miss some bugs)

### Completeness

**Complete analysis**: Finds all instances of a property
- Often undecidable for interesting properties
- Requires sound over-approximation

**Incomplete analysis**: May miss some instances
- More practical and scalable
- Trade precision for performance

## Practical Considerations

### Handling Language Features

**Dynamic dispatch**: Virtual method calls
- Type analysis to resolve targets
- Conservative over-approximation

**Reflection**: Runtime code generation
- Static analysis limitations
- Require annotations or assumptions

**Concurrency**: Multi-threaded execution
- Thread interleaving
- Synchronization primitives
- Data races and deadlocks

### Tool Integration

**Static analyzers**: Integrate abstract interpretation
- Coverity, Polyspace, Astrée
- Custom analyses for specific properties

**Verification tools**: Use abstract interpretation
- Frama-C (value analysis)
- SLAM/SDV (predicate abstraction)

**Compiler optimizations**: Apply abstract interpretation
- Constant propagation
- Dead code elimination
- Range analysis for bounds checking
