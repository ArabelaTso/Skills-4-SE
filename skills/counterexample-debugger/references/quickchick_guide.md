# QuickChick Counterexample Tool (Coq)

## Overview

QuickChick is a property-based testing tool for Coq that generates random test cases to find counterexamples. It's based on QuickCheck from Haskell and helps debug specifications before proving.

## Basic Usage

### Setting Up QuickChick

```coq
From QuickChick Require Import QuickChick.
Import QcDefaultNotation.
Open Scope qc_scope.
```

### Running QuickChick

```coq
Definition prop_example (x : nat) : bool :=
  x + 1 =? x.

QuickChick prop_example.
```

**Output:**
```
QuickChick prop_example
0
*** Failed after 1 tests and 0 shrinks. (0 discards)
```

## Interpreting Counterexamples

### Example 1: Simple Property

```coq
Definition prop_rev_eq (l : list nat) : bool :=
  list_eq_dec Nat.eq_dec l (rev l).

QuickChick prop_rev_eq.
```

**QuickChick output:**
```
[0; 1]
*** Failed after 2 tests and 1 shrinks. (0 discards)
```

**Interpretation:**
- Found counterexample: `[0; 1]`
- `rev [0; 1] = [1; 0] ≠ [0; 1]`
- Property fails for non-palindromic lists

### Example 2: Conditional Property

```coq
Definition prop_div (x y : nat) : bool :=
  (y =? 0) || (x / y * y <=? x).

QuickChick prop_div.
```

**QuickChick output:**
```
Success! Passed 10000 tests.
```

**Interpretation:**
- No counterexample found in 10000 tests
- Property likely correct (but not proven)

### Example 3: Shrinking

```coq
Definition prop_sorted_insert (x : nat) (l : list nat) : bool :=
  is_sorted (insert x l).

QuickChick prop_sorted_insert.
```

**QuickChick output:**
```
5 [3; 1]
*** Failed after 15 tests and 3 shrinks. (0 discards)
```

**Interpretation:**
- Original counterexample was larger
- Shrunk to minimal: `insert 5 [3; 1]`
- Result `[3; 1; 5]` is not sorted
- Issue: `insert` doesn't assume input is sorted

## Defining Testable Properties

### Boolean Properties

```coq
Definition prop_name (args : types) : bool :=
  (* boolean expression *).

QuickChick prop_name.
```

### Conditional Properties

```coq
Definition prop_conditional (x y : nat) : bool :=
  (precondition x y) ==> (postcondition x y).
```

The `==>` operator discards tests where precondition is false.

### Custom Generators

```coq
(* Generate sorted lists *)
Fixpoint genSortedList (size : nat) : G (list nat) :=
  match size with
  | 0 => ret []
  | S n =>
      l <- genSortedList n ;;
      x <- choose (0, 100) ;;
      ret (insert x l)
  end.

Sample (genSortedList 5).
```

## Common Counterexample Patterns

### Pattern 1: Empty Structures

```coq
Definition prop_head_in_list (l : list nat) : bool :=
  match l with
  | [] => true  (* Guard against empty *)
  | h :: _ => existsb (Nat.eqb h) l
  end.

QuickChick prop_head_in_list.
```

### Pattern 2: Boundary Values

```coq
Definition prop_div_correct (x y : nat) : bool :=
  (y =? 0) || (x / y * y + x mod y =? x).

QuickChick prop_div_correct.
(* Passes: handles y = 0 case *)
```

### Pattern 3: Type Constraints

```coq
Definition prop_positive (x : nat) : bool :=
  (x =? 0) ==> (x - 1 <? x).

QuickChick prop_positive.
(* Counterexample: x = 0 *)
(* Fix: change precondition to x > 0 *)
```

### Pattern 4: Quantifier Issues

```coq
(* Wrong: exists y such that for all x, P x y *)
Definition prop_wrong : Checker :=
  exists y, forAll arbitrary (fun x => P x y).

(* Right: for all x, exists y such that P x y *)
Definition prop_right : Checker :=
  forAll arbitrary (fun x => exists y, P x y).
```

## QuickChick Combinators

### Basic Combinators

```coq
(* Implication *)
precondition ==> postcondition

(* Conjunction *)
prop1 .&&. prop2

(* Disjunction *)
prop1 .||. prop2

(* Negation *)
negb prop
```

### Quantifiers

```coq
(* Universal quantification *)
forAll gen (fun x => property x)

(* Existential quantification *)
exists x, property x

(* Conditional quantification *)
forAll gen (fun x => precondition x ==> property x)
```

## Debugging Workflow with QuickChick

### Step 1: Define Property

```coq
Definition prop_insertion_sort_correct (l : list nat) : bool :=
  let sorted := insertion_sort l in
  is_sorted sorted && permutation_check l sorted.
```

### Step 2: Run QuickChick

```coq
QuickChick prop_insertion_sort_correct.
```

### Step 3: Analyze Counterexample

If counterexample found:
```
[3; 1; 2]
*** Failed after 5 tests and 2 shrinks.
```

Analyze:
- Input: `[3; 1; 2]`
- Check `insertion_sort [3; 1; 2]`
- Verify which part fails: sortedness or permutation

### Step 4: Fix and Retest

```coq
(* Debug: check intermediate steps *)
Compute insertion_sort [3; 1; 2].
(* Result: [1; 2; 3] *)

Compute is_sorted [1; 2; 3].
(* Result: true *)

Compute permutation_check [3; 1; 2] [1; 2; 3].
(* Result: false - bug in permutation_check! *)
```

## Shrinking

QuickChick automatically shrinks counterexamples to minimal failing cases.

### How Shrinking Works

```coq
(* Original counterexample: [10; 25; 3; 17; 8] *)
(* Shrunk to: [3; 1] *)
```

Shrinking tries:
1. Smaller lists
2. Smaller values
3. Simpler structures

### Custom Shrinking

```coq
Instance shrinkMyType : Shrink MyType :=
  {| shrink x := (* custom shrinking logic *) |}.
```

## Common Fixes Based on Counterexamples

### Add Preconditions

```coq
(* Before *)
Definition prop_head (l : list nat) : bool :=
  hd 0 l =? last l 0.

QuickChick prop_head.
(* Counterexample: [1; 2] *)

(* After *)
Definition prop_head_fixed (l : list nat) : bool :=
  (length l =? 1) ==> (hd 0 l =? last l 0).

QuickChick prop_head_fixed.
```

### Fix Specification

```coq
(* Before: incorrect spec *)
Definition prop_sort_wrong (l : list nat) : bool :=
  is_sorted (sort l).

QuickChick prop_sort_wrong.
(* May pass but incomplete *)

(* After: complete spec *)
Definition prop_sort_correct (l : list nat) : bool :=
  let sorted := sort l in
  is_sorted sorted && (length sorted =? length l).

QuickChick prop_sort_correct.
```

### Adjust Generators

```coq
(* Before: generates any list *)
QuickChick (forAll arbitrary prop_on_sorted).
(* Many discards if prop needs sorted input *)

(* After: generate sorted lists *)
QuickChick (forAll genSortedList prop_on_sorted).
(* More efficient testing *)
```

## Limitations

### What QuickChick Can Find

- Counterexamples in randomly generated test cases
- Bugs in specifications and implementations
- Edge cases and boundary conditions

### What QuickChick Cannot Find

- Rare counterexamples (low probability)
- Counterexamples requiring specific structure
- Proof that property holds (only testing)

### When QuickChick Says "Success"

This means:
- No counterexample found in N tests
- Property likely correct but not proven
- Increases confidence but doesn't guarantee correctness

## Integration with Proofs

### Test Before Proving

```coq
Definition prop_theorem (x : nat) : bool :=
  (* property *).

QuickChick prop_theorem.
(* If passes, attempt proof *)

Theorem theorem_name :
  forall x, (* property *).
Proof.
  (* proof *)
Qed.
```

### Extract Lemmas from Counterexamples

```coq
QuickChick prop_main.
(* Counterexample: specific case *)

(* Prove the specific case first *)
Lemma specific_case :
  (* counterexample case *).
Proof.
  (* understand why it fails *)
Admitted.
```
