---
name: verified-pseudocode-extractor
description: "Extract language-agnostic pseudocode from formally verified programs (Isabelle/HOL, Coq) while preserving verified control flow, data dependencies, and algorithmic logic. Use when: (1) Users have verified code and need readable pseudocode, (2) Documenting verified algorithms for broader audiences, (3) Translating verified implementations to other languages, (4) Creating algorithm specifications from verified code, (5) Preserving verification guarantees in pseudocode form, or (6) Abstracting proof-heavy code to essential logic. Maintains semantic faithfulness to verified implementation."
---

# Verified Pseudocode Extractor

Extract language-agnostic pseudocode from formally verified programs while preserving verified properties and algorithmic structure.

## Core Principles

### Semantic Faithfulness
- Preserve exact control flow from verified code
- Maintain all data dependencies
- Keep algorithmic logic intact
- Do not introduce new behavior
- Do not omit verified steps

### Verification Preservation
- Mark verified properties explicitly
- Retain preconditions and postconditions
- Include loop invariants
- Note termination arguments
- Distinguish verified from unverified components

### Abstraction Without Loss
- Remove language-specific syntax
- Remove proof-specific code
- Keep essential algorithmic structure
- Maintain readability
- Preserve correctness guarantees

## Workflow

### 1. Identify Verified Components

Scan the input code for:
- **Function definitions**: `fun`, `Fixpoint`, `Definition`
- **Theorems**: `lemma`, `theorem`, `Theorem`, `Lemma`
- **Specifications**: `assumes`/`shows`, preconditions/postconditions
- **Invariants**: Loop invariants, inductive invariants
- **Helper lemmas**: Supporting correctness proofs

### 2. Extract Core Algorithm

For each verified function:

**Preserve**:
- Function signature (name, parameters, return type)
- Control flow (if/then/else, pattern matching, recursion)
- Data flow (variable assignments, computations)
- Termination structure (base cases, recursive calls)

**Remove**:
- Proof tactics (`by simp`, `auto`, `lia`, `Proof...Qed`)
- Type system details (type classes, implicit arguments)
- Language-specific syntax (`#` vs `::`, `@` vs `++`)
- Proof-only lemmas
- Module qualifications

### 3. Extract Verification Annotations

Identify and mark:

**Preconditions**:
```
PRECONDITION: condition  [VERIFIED: lemma_name]
```

**Postconditions**:
```
POSTCONDITION: property  [VERIFIED: theorem_name]
```

**Invariants**:
```
INVARIANT: property  [VERIFIED]
```

**Termination**:
```
TERMINATION: argument  [VERIFIED: termination_proof]
```

**Unverified components**:
```
[ASSUMED: assumption]
[UNVERIFIED: property]
```

### 4. Structure the Pseudocode

Use clear, structured format:

```
ALGORITHM: Name
VERIFIED IN: System (theory/module name)

FUNCTION name(params: Types) -> ReturnType
  DESCRIPTION: Brief description

  PRECONDITION: conditions  [VERIFIED: source]
  POSTCONDITION: guarantees  [VERIFIED: source]

  [Algorithm body in structured pseudocode]

  TERMINATION: argument  [VERIFIED]
  INVARIANT: properties  [VERIFIED]

VERIFIED PROPERTIES:
  1. Property 1  [VERIFIED: theorem]
  2. Property 2  [VERIFIED: lemma]
```

### 5. Verify Semantic Equivalence

Check that pseudocode:
- Has same control flow as original
- Performs same computations
- Maintains same data dependencies
- Preserves all verified properties
- Contains no new behavior
- Omits no essential steps

## Extraction Patterns

### Pattern Matching

**From** (Isabelle):
```isabelle
case xs of [] ⇒ base | (x # xs) ⇒ recursive
```

**From** (Coq):
```coq
match l with | [] => base | x :: xs => recursive end
```

**To** (Pseudocode):
```
MATCH list WITH
  CASE []: base
  CASE x :: xs: recursive
```

### Recursion

**From**:
```isabelle
fun f :: "nat ⇒ nat" where
  "f 0 = 0" |
  "f (Suc n) = f n + 1"
```

**To**:
```
FUNCTION f(n: Nat) -> Nat
  IF n = 0 THEN
    RETURN 0
  ELSE
    RETURN f(n - 1) + 1
  [VERIFIED: terminates (decreasing n)]
```

### Preconditions/Postconditions

**From** (Isabelle):
```isabelle
lemma function_correct:
  assumes "precondition x"
  shows "postcondition (function x)"
```

**To**:
```
FUNCTION function(x: Type) -> Type
  PRECONDITION: precondition(x)  [VERIFIED: function_correct]
  POSTCONDITION: postcondition(result)  [VERIFIED: function_correct]
```

### Dependent Types

**From** (Coq):
```coq
Definition safe_head (l : list A) (H : l <> []) : A
```

**To**:
```
FUNCTION safe_head(l: List<A>) -> A
  PRECONDITION: l ≠ []  [VERIFIED: type system]
```

## Verification Annotations

### Verified Components

Mark with `[VERIFIED]` or `[VERIFIED: source]`:

```
PRECONDITION: is_sorted(list)  [VERIFIED: sort_correct theorem]
POSTCONDITION: result ≤ all elements  [VERIFIED: max_correct lemma]
TERMINATION: list size decreases  [VERIFIED: structural recursion]
```

### Unverified Components

Mark clearly:

```
[ASSUMED: input is well-formed]
[UNVERIFIED: time complexity O(n log n)]
[UNVERIFIED: space complexity]
```

### Partial Verification

Be specific:

```
[VERIFIED: correctness]
[UNVERIFIED: termination]
```

### Unreachable Code

Mark when preconditions make cases impossible:

```
CASE []:
  UNREACHABLE  [precondition ensures list is non-empty]
```

## What to Preserve vs. Remove

### Always Preserve

✓ Function names and signatures
✓ Control flow structure
✓ Data dependencies
✓ Algorithmic steps
✓ Verified properties
✓ Preconditions and postconditions
✓ Loop invariants
✓ Termination arguments

### Always Remove

✗ Proof tactics and commands
✗ Proof scripts (`proof...qed`, `Proof...Qed`)
✗ Type class constraints (unless essential)
✗ Proof-only helper lemmas
✗ Language-specific syntax sugar
✗ Module system details
✗ Proof annotations
✗ Type inference hints

### Context-Dependent

? Type annotations: Keep if essential for understanding
? Helper functions: Keep if used in algorithm, remove if proof-only
? Definitions: Keep if part of algorithm, remove if proof infrastructure

## Output Format

Use structured, readable format:

```
ALGORITHM: [Name]
VERIFIED IN: [System] ([Module/Theory])

═══════════════════════════════════════════════════════════

FUNCTION name(params: Types) -> ReturnType
  DESCRIPTION: [Brief description]

  PRECONDITION: [conditions]  [VERIFIED: source]
  POSTCONDITION: [guarantees]  [VERIFIED: source]

  [Pseudocode body with clear structure]

  TERMINATION: [argument]  [VERIFIED]
  INVARIANT: [properties]  [VERIFIED]

═══════════════════════════════════════════════════════════

VERIFIED PROPERTIES:
  1. [Property]  [VERIFIED: theorem]
  2. [Property]  [VERIFIED: lemma]
  ...
```

## Quality Checks

Before finalizing pseudocode:

1. **Completeness**: All algorithmic steps included?
2. **Correctness**: Control flow matches original?
3. **Clarity**: Readable and understandable?
4. **Verification**: All verified properties marked?
5. **Faithfulness**: Semantically equivalent to original?
6. **No additions**: No new behavior introduced?
7. **No omissions**: No essential steps removed?

## Examples

For complete extraction examples including:
- Insertion sort (Isabelle/HOL)
- Binary search (Coq)
- Safe array access (Coq with dependent types)
- GCD algorithm (Isabelle/HOL)

See [examples.md](references/examples.md)

For detailed extraction patterns and rules:
See [extraction_patterns.md](references/extraction_patterns.md)

## Tips

- **Read proofs carefully**: Understand what's verified before extracting
- **Preserve structure**: Keep control flow exactly as in original
- **Mark everything**: Be explicit about verification status
- **Stay faithful**: Don't simplify away essential complexity
- **Remove proofs**: But keep what they prove
- **Use clear syntax**: Make pseudocode readable
- **Add comments**: Explain non-obvious logic
- **Check equivalence**: Verify semantic faithfulness
- **Distinguish verified/unverified**: Be honest about what's proven
- **Keep it language-agnostic**: Avoid source language idioms
