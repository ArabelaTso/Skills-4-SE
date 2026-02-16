# Counterexample Debugging Examples

This file contains complete examples of debugging proofs using counterexamples from Nitpick and QuickChick.

## Example 1: Incorrect Sortedness Definition

### Problem

User attempts to prove insertion sort correctness but the proof fails.

### Isabelle/HOL Version

```isabelle
theory SortBug
  imports Main
begin

(* Buggy sortedness definition *)
fun is_sorted :: "nat list ⇒ bool" where
  "is_sorted [] = True" |
  "is_sorted [x] = True" |
  "is_sorted (x # y # ys) = (x < y ∧ is_sorted (y # ys))"
  (* BUG: uses < instead of ≤ *)

fun insert :: "nat ⇒ nat list ⇒ nat list" where
  "insert x [] = [x]" |
  "insert x (y # ys) = (if x ≤ y then x # y # ys else y # insert x ys)"

fun insertion_sort :: "nat list ⇒ nat list" where
  "insertion_sort [] = []" |
  "insertion_sort (x # xs) = insert x (insertion_sort xs)"

(* Attempt to prove *)
lemma insertion_sort_sorted:
  "is_sorted (insertion_sort xs)"
  nitpick
  (* Nitpick finds counterexample *)
end
```

**Nitpick Output:**
```
Nitpick found a counterexample:
  Free variables:
    xs = [0, 0]
```

**Analysis:**
1. Input: `[0, 0]`
2. `insertion_sort [0, 0] = [0, 0]`
3. `is_sorted [0, 0]` checks if `0 < 0`, which is false
4. **Root cause**: Definition uses `<` instead of `≤`
5. **Fix**: Change to `x ≤ y` in `is_sorted`

**Corrected Version:**
```isabelle
fun is_sorted_fixed :: "nat list ⇒ bool" where
  "is_sorted_fixed [] = True" |
  "is_sorted_fixed [x] = True" |
  "is_sorted_fixed (x # y # ys) = (x ≤ y ∧ is_sorted_fixed (y # ys))"

lemma insertion_sort_sorted_fixed:
  "is_sorted_fixed (insertion_sort xs)"
  nitpick
  (* No counterexample found *)
  sorry (* Now ready to prove *)
```

### Coq Version

```coq
Require Import List Arith.
From QuickChick Require Import QuickChick.
Import ListNotations.

(* Buggy sortedness definition *)
Fixpoint is_sorted (l : list nat) : bool :=
  match l with
  | [] => true
  | [x] => true
  | x :: y :: ys => (x <? y) && is_sorted (y :: ys)
  end.
(* BUG: uses <? instead of <=? *)

Fixpoint insert (x : nat) (l : list nat) : list nat :=
  match l with
  | [] => [x]
  | y :: ys => if x <=? y then x :: y :: ys else y :: insert x ys
  end.

Fixpoint insertion_sort (l : list nat) : list nat :=
  match l with
  | [] => []
  | x :: xs => insert x (insertion_sort xs)
  end.

(* Test property *)
Definition prop_insertion_sort_sorted (l : list nat) : bool :=
  is_sorted (insertion_sort l).

QuickChick prop_insertion_sort_sorted.
```

**QuickChick Output:**
```
[0; 0]
*** Failed after 3 tests and 1 shrinks. (0 discards)
```

**Analysis:**
1. Counterexample: `[0; 0]`
2. `insertion_sort [0; 0] = [0; 0]`
3. `is_sorted [0; 0]` checks `0 <? 0 = false`
4. **Root cause**: Uses strict inequality
5. **Fix**: Change to `<=?`

**Corrected Version:**
```coq
Fixpoint is_sorted_fixed (l : list nat) : bool :=
  match l with
  | [] => true
  | [x] => true
  | x :: y :: ys => (x <=? y) && is_sorted_fixed (y :: ys)
  end.

Definition prop_fixed (l : list nat) : bool :=
  is_sorted_fixed (insertion_sort l).

QuickChick prop_fixed.
(* Success! Passed 10000 tests. *)
```

## Example 2: Missing Precondition

### Problem

Theorem about list head fails without proper precondition.

### Isabelle/HOL Version

```isabelle
theory HeadBug
  imports Main
begin

(* Incorrect theorem: missing precondition *)
lemma head_in_list:
  "hd xs ∈ set xs"
  nitpick
end
```

**Nitpick Output:**
```
Nitpick found a counterexample:
  Free variables:
    xs = []
```

**Analysis:**
1. Counterexample: empty list `[]`
2. `hd []` is undefined (returns arbitrary value)
3. Empty set has no elements
4. **Root cause**: Missing non-empty precondition
5. **Fix**: Add `xs ≠ []` assumption

**Corrected Version:**
```isabelle
lemma head_in_list_fixed:
  assumes "xs ≠ []"
  shows "hd xs ∈ set xs"
  using assms by (cases xs) auto
```

### Coq Version

```coq
Require Import List.
From QuickChick Require Import QuickChick.
Import ListNotations.

(* Test property without precondition *)
Definition prop_head_in_list (l : list nat) : bool :=
  match l with
  | [] => true  (* Vacuously true for empty *)
  | h :: _ => existsb (Nat.eqb h) l
  end.

QuickChick prop_head_in_list.
(* Success - but only because we handled empty case *)

(* What if we forget to handle it? *)
Definition prop_head_in_list_buggy (l : list nat) : bool :=
  existsb (Nat.eqb (hd 0 l)) l.

QuickChick prop_head_in_list_buggy.
```

**QuickChick Output:**
```
[]
*** Failed after 1 tests and 0 shrinks. (0 discards)
```

**Analysis:**
1. Counterexample: `[]`
2. `hd 0 [] = 0` (default value)
3. `existsb (Nat.eqb 0) [] = false`
4. **Root cause**: Doesn't handle empty list
5. **Fix**: Add precondition or handle empty case

**Corrected Version:**
```coq
Definition prop_head_in_list_fixed (l : list nat) : bool :=
  (length l =? 0) || existsb (Nat.eqb (hd 0 l)) l.

QuickChick prop_head_in_list_fixed.
(* Success! *)
```

## Example 3: Wrong Quantifier Order

### Problem

Existential and universal quantifiers in wrong order.

### Isabelle/HOL Version

```isabelle
theory QuantifierBug
  imports Main
begin

(* Incorrect: claims there exists one y that works for all x *)
lemma wrong_order:
  "∃y. ∀x. x < (y::nat)"
  nitpick [card nat = 5]
end
```

**Nitpick Output:**
```
Nitpick found a counterexample:
  Skolem constants:
    y = 4
  Free variables:
    x = 4
```

**Analysis:**
1. Nitpick tries y = 4 (largest in domain)
2. But x = 4 violates `4 < 4`
3. **Root cause**: No single y works for all x
4. **Fix**: Swap quantifiers

**Corrected Version:**
```isabelle
lemma correct_order:
  "∀x. ∃y. x < (y::nat)"
  by auto
```

### Coq Version

```coq
From QuickChick Require Import QuickChick.

(* Wrong order: exists y such that for all x, x < y *)
Definition prop_wrong_order : Checker :=
  exists (y : nat),
    forAll arbitrary (fun x => x <? y).

QuickChick prop_wrong_order.
```

**QuickChick Output:**
```
Counterexample found (for some y, there exists x >= y)
```

**Analysis:**
1. For any fixed y, can find x ≥ y
2. **Root cause**: Quantifier order
3. **Fix**: For each x, find y > x

**Corrected Version:**
```coq
Definition prop_correct_order : Checker :=
  forAll arbitrary (fun x =>
    exists (y : nat), x <? y).

QuickChick prop_correct_order.
(* Success! *)
```

## Example 4: Off-by-One Error

### Problem

Specification has subtle off-by-one error.

### Isabelle/HOL Version

```isabelle
theory OffByOne
  imports Main
begin

(* Buggy: claims reverse adds one element *)
lemma reverse_length_bug:
  "length (rev xs) = length xs + 1"
  nitpick
end
```

**Nitpick Output:**
```
Nitpick found a counterexample:
  Free variables:
    xs = []
```

**Analysis:**
1. Counterexample: `[]`
2. `length (rev []) = 0`
3. `length [] + 1 = 1`
4. `0 ≠ 1`
5. **Root cause**: Incorrect specification
6. **Fix**: Remove the `+ 1`

**Corrected Version:**
```isabelle
lemma reverse_length_correct:
  "length (rev xs) = length xs"
  by simp
```

### Coq Version

```coq
Require Import List.
From QuickChick Require Import QuickChick.
Import ListNotations.

(* Buggy specification *)
Definition prop_rev_length_bug (l : list nat) : bool :=
  (length (rev l) =? length l + 1).

QuickChick prop_rev_length_bug.
```

**QuickChick Output:**
```
[]
*** Failed after 1 tests and 0 shrinks. (0 discards)
```

**Analysis:**
1. Counterexample: `[]`
2. `length (rev []) = 0`
3. `length [] + 1 = 1`
4. **Root cause**: Wrong specification
5. **Fix**: Remove `+ 1`

**Corrected Version:**
```coq
Definition prop_rev_length_correct (l : list nat) : bool :=
  (length (rev l) =? length l).

QuickChick prop_rev_length_correct.
(* Success! Passed 10000 tests. *)
```

## Example 5: Incomplete Specification

### Problem

Specification is too weak and doesn't capture full requirements.

### Isabelle/HOL Version

```isabelle
theory IncompleteSpec
  imports Main
begin

fun my_sort :: "nat list ⇒ nat list" where
  "my_sort xs = xs"  (* Buggy: doesn't actually sort *)

(* Weak specification: only checks sortedness *)
lemma my_sort_sorted:
  "is_sorted (my_sort xs)"
  nitpick
  (* May not find issue if is_sorted is weak *)
end
```

**Better Specification:**
```isabelle
lemma my_sort_correct:
  "is_sorted (my_sort xs) ∧ set (my_sort xs) = set xs"
  nitpick
  (* Nitpick finds: my_sort [1, 0] = [1, 0] which is not sorted *)
end
```

**Analysis:**
1. Original spec only checked sortedness
2. Didn't verify that elements are preserved
3. **Root cause**: Incomplete specification
4. **Fix**: Add permutation/set equality requirement

### Coq Version

```coq
Require Import List.
From QuickChick Require Import QuickChick.
Import ListNotations.

(* Buggy sort: returns input unchanged *)
Definition my_sort (l : list nat) : list nat := l.

(* Weak specification *)
Definition prop_weak (l : list nat) : bool :=
  is_sorted (my_sort l).

QuickChick prop_weak.
(* May fail on unsorted inputs *)
```

**QuickChick Output:**
```
[1; 0]
*** Failed after 2 tests and 1 shrinks. (0 discards)
```

**Analysis:**
1. Input: `[1; 0]`
2. `my_sort [1; 0] = [1; 0]` (unchanged)
3. `is_sorted [1; 0] = false`
4. **Root cause**: Implementation doesn't sort
5. **Fix**: Implement actual sorting

**Complete Specification:**
```coq
Definition prop_complete (l : list nat) : bool :=
  let sorted := my_sort l in
  is_sorted sorted && (length sorted =? length l).
  (* Should also check permutation *)

QuickChick prop_complete.
```

## Debugging Checklist

When counterexample is found:

1. **Verify the counterexample manually**
   - Compute the result for the counterexample
   - Check if it actually violates the theorem

2. **Identify the root cause**
   - Missing precondition?
   - Wrong specification?
   - Implementation bug?
   - Quantifier order issue?

3. **Determine the fix**
   - Add/strengthen preconditions
   - Correct the specification
   - Fix the implementation
   - Reorder quantifiers

4. **Retest after fixing**
   - Run Nitpick/QuickChick again
   - Verify no counterexample found
   - Attempt the proof

5. **Consider edge cases**
   - Empty structures
   - Boundary values
   - Type limits
   - Special cases
