---
name: semantic-equivalence-verifier
description: Analyzes and verifies semantic equivalence between two functions, classes, or modules by examining control flow, data flow, and observable behavior. Use when comparing code implementations (refactored vs original, different implementations of same functionality, migration verification), determining if two code artifacts produce identical behavior, identifying behavioral differences between code versions, or validating that code changes preserve semantics. Supports formal reasoning and symbolic execution approaches.
---

# Semantic Equivalence Verifier

## Overview

This skill enables rigorous analysis of semantic equivalence between two code artifacts (functions, classes, or modules). It systematically compares control flow, data flow, and observable behavior to determine if implementations are functionally identical, and provides actionable guidance for achieving equivalence when differences exist.

## Verification Workflow

### Step 1: Input Specification

Clearly identify the two code artifacts to compare:

```
Artifact A: [function/class/module name and location]
Artifact B: [function/class/module name and location]
```

Specify the equivalence scope:
- **Strict equivalence**: Identical behavior for all possible inputs
- **Partial equivalence**: Identical behavior for a specific input domain
- **Observable equivalence**: Identical externally visible behavior (may differ internally)

### Step 2: Static Analysis

Perform systematic static analysis on both artifacts:

**Control Flow Analysis:**
- Extract control flow graphs (CFG) for both artifacts
- Identify branching conditions, loops, and exit points
- Compare CFG structure and reachability
- Note: Different CFG structures don't necessarily mean non-equivalence

**Data Flow Analysis:**
- Trace variable definitions and uses
- Identify data dependencies
- Compare computation sequences
- Check for equivalent transformations (e.g., `x*2` vs `x+x`)

**Signature Analysis:**
- Compare function signatures (parameters, return types)
- Check preconditions and postconditions
- Verify exception handling behavior

### Step 3: Behavioral Analysis

Analyze runtime behavior and observable effects:

**Input-Output Mapping:**
- Identify representative test inputs covering edge cases
- Compare outputs for identical inputs
- Check boundary conditions and error cases

**Side Effects:**
- File I/O operations
- Network calls
- Database modifications
- Global state changes
- Memory allocations

**Performance Characteristics:**
- Time complexity (O-notation)
- Space complexity
- Note: Performance differences don't affect semantic equivalence unless specified

### Step 4: Advanced Verification (Optional)

For rigorous verification, apply formal methods:

**Symbolic Execution:**
- Generate symbolic constraints for both artifacts
- Use SMT solvers to check constraint equivalence
- Identify input conditions where behaviors diverge

**Formal Proof:**
- Define formal specifications for expected behavior
- Prove both artifacts satisfy the same specification
- Use proof assistants (Coq, Isabelle) for complex cases

**Equivalence Checking:**
- Apply program equivalence algorithms
- Use translation validation techniques
- Leverage existing verification tools (KLEE, SymDiff, SeaHorn)

### Step 5: Report Generation

Generate a comprehensive equivalence report using the template in `assets/equivalence_report_template.md`:

**If Equivalent:**
- State equivalence type (strict/partial/observable)
- Summarize analysis evidence
- Note any performance or style differences

**If Not Equivalent:**
- Identify specific divergence points
- Provide concrete input examples demonstrating differences
- Explain root causes of non-equivalence
- Suggest modifications to achieve equivalence

## Analysis Techniques by Language

Different languages require adapted analysis approaches:

**Statically Typed (Java, C++, Rust):**
- Leverage type system for stronger guarantees
- Use compiler-level analysis tools
- Check type-level equivalence first

**Dynamically Typed (Python, JavaScript):**
- Require more extensive runtime analysis
- Consider duck typing and dynamic dispatch
- Test broader input ranges

**Functional (Haskell, OCaml):**
- Exploit referential transparency
- Use equational reasoning
- Apply denotational semantics

## Common Equivalence Patterns

**Refactoring Patterns:**
- Extract method: Original function ≡ New function + extracted helper
- Inline variable: `temp=x; return temp` ≡ `return x`
- Rename: Identifier changes don't affect semantics

**Optimization Patterns:**
- Loop unrolling: Semantically equivalent, different performance
- Constant folding: `x*0` ≡ `0`
- Dead code elimination: Removing unreachable code preserves semantics

**Algorithm Substitution:**
- Different sorting algorithms with same comparison function
- Alternative data structures with same interface
- Mathematical identities: `pow(x,2)` ≡ `x*x`

## Practical Examples

**Example 1: Simple Function Comparison**

```python
# Artifact A
def sum_squares(n):
    total = 0
    for i in range(1, n+1):
        total += i * i
    return total

# Artifact B
def sum_squares(n):
    return n * (n + 1) * (2*n + 1) // 6
```

Analysis: Mathematically equivalent for all non-negative integers. Different algorithms, same result.

**Example 2: Class Refactoring**

```java
// Artifact A
class Calculator {
    int add(int a, int b) { return a + b; }
    int multiply(int a, int b) { return a * b; }
}

// Artifact B
class Calculator {
    int add(int a, int b) { return a + b; }
    int multiply(int a, int b) {
        int result = 0;
        for(int i = 0; i < b; i++) result += a;
        return result;
    }
}
```

Analysis: Not strictly equivalent - Artifact B fails for negative `b`. Partial equivalence for `b >= 0`.

## References

For detailed guidance on specific analysis techniques:
- **Formal methods**: See `references/formal_verification.md`
- **Symbolic execution**: See `references/symbolic_execution.md`
- **Language-specific patterns**: See `references/language_patterns.md`

