# Nitpick Counterexample Tool (Isabelle/HOL)

## Overview

Nitpick is a counterexample finder for Isabelle/HOL that searches for finite models that violate a theorem. It's invaluable for debugging incorrect specifications before attempting proofs.

## Basic Usage

### Running Nitpick

```isabelle
lemma "statement"
  nitpick
  (* Nitpick will search for counterexamples *)
```

### Nitpick with Options

```isabelle
lemma "statement"
  nitpick [timeout = 60, card = 1-10]
  (* timeout: seconds to search *)
  (* card: cardinality bounds for types *)
```

## Interpreting Counterexamples

### Example 1: Simple Counterexample

```isabelle
lemma "∀xs. rev xs = xs"
  nitpick
```

**Nitpick output:**
```
Nitpick found a counterexample:
  Free variables:
    xs = [a₁, a₂]
  where
    a₁ ≠ a₂
```

**Interpretation:**
- Nitpick found a list with two distinct elements
- `rev [a₁, a₂] = [a₂, a₁] ≠ [a₁, a₂]`
- The theorem is false for non-palindromic lists

### Example 2: Type-Specific Counterexample

```isabelle
lemma "∀(x::nat) y. x + y = y + x + 1"
  nitpick
```

**Nitpick output:**
```
Nitpick found a counterexample:
  Free variables:
    x = 0
    y = 0
```

**Interpretation:**
- For x=0, y=0: `0 + 0 = 0` but `0 + 0 + 1 = 1`
- The theorem adds an extra 1 incorrectly

### Example 3: Missing Precondition

```isabelle
lemma "∀xs. length xs > 0 ⟶ hd xs ∈ set xs"
  nitpick
```

**Nitpick output:**
```
Nitpick found no counterexample.
```

**Interpretation:**
- The theorem is likely correct (within tested bounds)
- Nitpick couldn't find a violation
- This doesn't guarantee correctness, but increases confidence

## Common Counterexample Patterns

### Pattern 1: Empty List/Set

Many theorems fail on empty structures:

```isabelle
lemma "∀xs. hd xs ∈ set xs"
  nitpick
(* Counterexample: xs = [] *)
```

**Fix:** Add precondition `xs ≠ []`

### Pattern 2: Boundary Values

Theorems often fail at boundaries:

```isabelle
lemma "∀n. n div 2 * 2 = n"
  nitpick
(* Counterexample: n = 1 *)
```

**Fix:** Theorem only holds for even numbers

### Pattern 3: Type Cardinality

Theorems may fail for small types:

```isabelle
lemma "∀(x::nat) y z. x ≠ y ⟶ x ≠ z ⟶ y ≠ z"
  nitpick [card nat = 2]
(* Counterexample: x = 0, y = 1, z = 0 *)
```

**Fix:** Theorem is false; x can equal z

### Pattern 4: Quantifier Order

Wrong quantifier order leads to counterexamples:

```isabelle
lemma "∃y. ∀x. x < y"
  nitpick
(* Counterexample found for finite domains *)
```

**Fix:** Should be `∀x. ∃y. x < y`

## Nitpick Options

### Cardinality Control

```isabelle
nitpick [card 'a = 3]        (* Type 'a has 3 elements *)
nitpick [card nat = 5]       (* Natural numbers up to 4 *)
nitpick [card = 1-8]         (* Try cardinalities 1 to 8 *)
```

### Timeout and Limits

```isabelle
nitpick [timeout = 120]      (* 2 minutes *)
nitpick [max_potential = 10] (* Limit potential models *)
nitpick [max_genuine = 5]    (* Limit genuine counterexamples *)
```

### Scope Control

```isabelle
nitpick [show_all]           (* Show all details *)
nitpick [verbose]            (* Verbose output *)
nitpick [debug]              (* Debug information *)
```

## Debugging Workflow with Nitpick

### Step 1: Run Nitpick First

Before attempting a proof, run Nitpick:

```isabelle
lemma my_theorem: "statement"
  nitpick
  (* If no counterexample, proceed with proof *)
  sorry
```

### Step 2: Analyze Counterexample

If Nitpick finds a counterexample:
1. Identify which values violate the theorem
2. Determine if the theorem is wrong or needs preconditions
3. Check if the specification matches the intent

### Step 3: Fix and Retest

```isabelle
(* Original (incorrect) *)
lemma "∀xs. length (rev xs) = length xs + 1"
  nitpick
  (* Counterexample: xs = [] gives 0 ≠ 1 *)

(* Fixed *)
lemma "∀xs. length (rev xs) = length xs"
  nitpick
  (* No counterexample *)
  by simp
```

## Limitations

### What Nitpick Can Find

- Finite counterexamples within cardinality bounds
- Violations in small models
- Type errors and inconsistencies

### What Nitpick Cannot Find

- Counterexamples requiring infinite structures
- Counterexamples beyond cardinality bounds
- Subtle errors in large models

### When Nitpick Says "No Counterexample"

This means:
- No counterexample found within the search bounds
- The theorem might still be false for larger models
- Proceed with caution; not a proof of correctness

## Common Fixes Based on Counterexamples

### Add Preconditions

```isabelle
(* Before *)
lemma "hd xs = last xs"
  nitpick (* Counterexample: xs = [a, b] *)

(* After *)
lemma "length xs = 1 ⟹ hd xs = last xs"
  by (cases xs) auto
```

### Strengthen Postconditions

```isabelle
(* Before *)
lemma "sorted (sort xs)"
  nitpick (* May find issues with sort definition *)

(* After *)
lemma "sorted (sort xs) ∧ set (sort xs) = set xs"
  sorry
```

### Fix Quantifier Order

```isabelle
(* Before *)
lemma "∃y. ∀x. P x y"
  nitpick (* Counterexample likely *)

(* After *)
lemma "∀x. ∃y. P x y"
  sorry
```

### Adjust Type Constraints

```isabelle
(* Before *)
lemma "∀(x::nat). x - 1 < x"
  nitpick (* Counterexample: x = 0 *)

(* After *)
lemma "∀(x::nat). x > 0 ⟹ x - 1 < x"
  by simp
```
