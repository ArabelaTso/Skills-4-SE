# Symbolic Execution for Equivalence Checking

## Overview

Symbolic execution explores program paths using symbolic values instead of concrete inputs, enabling systematic discovery of behavioral differences between code artifacts.

## Core Concepts

### Symbolic Values

Replace concrete inputs with symbolic variables:
- Concrete: `x = 5` → compute with 5
- Symbolic: `x = α` → track constraints on α

### Path Conditions

Accumulate constraints along execution paths:
```
if (x > 0):
    y = x + 1      # Path condition: x > 0
else:
    y = x - 1      # Path condition: x <= 0
```

### Constraint Solving

Use SMT solvers to:
- Check path feasibility
- Generate concrete test inputs
- Find counterexamples to equivalence

## Equivalence Checking Workflow

### Step 1: Symbolic Execution of Both Artifacts

Execute both artifacts symbolically with same symbolic inputs:

```python
# Artifact A
def artifact_a(x):
    if x > 0:
        return x * 2
    else:
        return 0

# Artifact B
def artifact_b(x):
    if x > 0:
        return x + x
    else:
        return -x
```

**Symbolic execution:**
- Path 1 (x > 0): A returns 2x, B returns 2x → Equivalent
- Path 2 (x ≤ 0): A returns 0, B returns -x → Not equivalent when x < 0

### Step 2: Path Exploration Strategies

**Depth-First Search (DFS):**
- Explore one path completely before backtracking
- Memory efficient
- May miss shallow bugs

**Breadth-First Search (BFS):**
- Explore all paths at depth k before depth k+1
- Finds shallow bugs quickly
- Higher memory usage

**Heuristic-Guided:**
- Prioritize paths likely to reveal differences
- Use coverage metrics or complexity heuristics
- Balance exploration efficiency

### Step 3: Constraint Collection

For each path pair (path_A, path_B):
```
PC_A: path condition for Artifact A
PC_B: path condition for Artifact B
Output_A: symbolic output expression for A
Output_B: symbolic output expression for B

Check: PC_A ∧ PC_B ∧ (Output_A ≠ Output_B)
If satisfiable → Found counterexample
If unsatisfiable → Paths are equivalent
```

### Step 4: Counterexample Generation

When difference found:
1. Extract satisfying assignment from solver
2. Convert symbolic values to concrete test case
3. Verify difference with concrete execution
4. Report input demonstrating non-equivalence

## Tools and Frameworks

### KLEE

Symbolic execution engine for C/LLVM:

```c
#include <klee/klee.h>

int artifact_a(int x) {
    if (x > 0) return x * 2;
    return 0;
}

int artifact_b(int x) {
    if (x > 0) return x + x;
    return -x;
}

int main() {
    int x;
    klee_make_symbolic(&x, sizeof(x), "x");

    int result_a = artifact_a(x);
    int result_b = artifact_b(x);

    klee_assert(result_a == result_b);
    return 0;
}
```

Run: `klee --emit-all-errors program.bc`

### SymDiff

Differential symbolic execution tool:
- Compares two program versions
- Identifies semantic differences
- Generates difference summary

### Angr

Python framework for binary analysis:

```python
import angr

# Load both binaries
proj_a = angr.Project('artifact_a.bin')
proj_b = angr.Project('artifact_b.bin')

# Create symbolic state
state_a = proj_a.factory.entry_state()
state_b = proj_b.factory.entry_state()

# Add symbolic input
x = state_a.solver.BVS('x', 32)
state_a.memory.store(0x1000, x)
state_b.memory.store(0x1000, x)

# Explore paths
simgr_a = proj_a.factory.simulation_manager(state_a)
simgr_b = proj_b.factory.simulation_manager(state_b)

simgr_a.explore()
simgr_b.explore()

# Compare outputs
for state_a in simgr_a.deadended:
    for state_b in simgr_b.deadended:
        if state_a.solver.satisfiable(extra_constraints=[
            state_a.regs.rax != state_b.regs.rax
        ]):
            print("Found difference:", state_a.solver.eval(x))
```

### Java PathFinder (JPF)

Symbolic execution for Java:

```java
import gov.nasa.jpf.symbc.Debug;

public class Equivalence {
    public static int artifactA(int x) {
        if (x > 0) return x * 2;
        return 0;
    }

    public static int artifactB(int x) {
        if (x > 0) return x + x;
        return -x;
    }

    public static void main(String[] args) {
        int x = Debug.makeSymbolicInteger("x");
        int resultA = artifactA(x);
        int resultB = artifactB(x);
        assert resultA == resultB : "Not equivalent";
    }
}
```

## Handling Complexity

### Path Explosion

**Problem:** Exponential growth in number of paths

**Solutions:**
1. **Path merging**: Combine similar paths using disjunctions
2. **Loop bounds**: Limit loop iterations (k-bounded exploration)
3. **Function summaries**: Precompute summaries for called functions
4. **Compositional analysis**: Verify components separately

### Constraint Complexity

**Problem:** Complex constraints slow down solver

**Solutions:**
1. **Incremental solving**: Reuse solver state across paths
2. **Constraint simplification**: Apply algebraic simplifications
3. **Theory-specific optimizations**: Use specialized solvers
4. **Concretization**: Replace symbolic values with concrete ones when beneficial

### Memory Modeling

**Problem:** Symbolic pointers and heap operations

**Solutions:**
1. **Lazy initialization**: Create objects on-demand
2. **Address concretization**: Use concrete addresses when possible
3. **Shape analysis**: Abstract heap structure
4. **Bounded heap**: Limit heap size for analysis

## Differential Symbolic Execution

Optimize for equivalence checking:

**Key insight:** Only explore paths where artifacts diverge

**Algorithm:**
1. Execute both artifacts in lockstep
2. When control flow diverges, fork exploration
3. When control flow reconverges, check output equivalence
4. Prune equivalent paths early

**Benefits:**
- Fewer paths to explore
- Faster counterexample discovery
- Scales better than independent analysis

## Practical Guidelines

**When to use symbolic execution:**
- Moderate-sized functions (< 1000 LOC)
- Programs with complex branching logic
- When concrete test generation is difficult
- Security-critical code paths

**Limitations:**
- Path explosion for large programs
- Constraint solver timeouts
- External dependencies (I/O, network)
- Native code and system calls

**Best practices:**
- Set reasonable time/path bounds
- Focus on critical code sections
- Combine with concrete testing
- Use function summaries for libraries
- Monitor solver performance

## Example: Complete Workflow

```python
# Using Z3 for simple symbolic execution

from z3 import *

def symbolic_execute_equivalence(artifact_a, artifact_b, input_vars):
    """
    Check equivalence using symbolic execution

    Returns: (is_equivalent, counterexample)
    """
    solver = Solver()

    # Execute both artifacts symbolically
    result_a = artifact_a(*input_vars)
    result_b = artifact_b(*input_vars)

    # Check if outputs can differ
    solver.add(result_a != result_b)

    if solver.check() == sat:
        # Found counterexample
        model = solver.model()
        counterexample = {str(v): model[v] for v in input_vars}
        return False, counterexample
    else:
        # Proven equivalent
        return True, None

# Example usage
x = Int('x')
y = Int('y')

def artifact_a(x, y):
    return If(x > y, x - y, y - x)

def artifact_b(x, y):
    return If(x > y, x - y, x - y)  # Bug: should be y - x

is_equiv, counter = symbolic_execute_equivalence(artifact_a, artifact_b, [x, y])

if is_equiv:
    print("Artifacts are equivalent")
else:
    print(f"Not equivalent. Counterexample: {counter}")
```
