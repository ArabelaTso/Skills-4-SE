# Proof Skeleton Examples

This file contains complete examples of proof skeletons for common theorems in both Isabelle/HOL and Coq.

## Example 1: List Reversal Properties

### Theorem Statement
Prove that reversing a list twice yields the original list: `reverse (reverse xs) = xs`

### Isabelle/HOL Proof Skeleton

```isabelle
theory ReverseReverse
  imports Main
begin

(* Theorem: Reversing twice is identity *)
theorem reverse_reverse:
  "rev (rev xs) = xs"
proof (induction xs)
  case Nil
  (* Goal: rev (rev []) = [] *)
  (* Strategy: Simplify using definition of rev *)
  show ?case by simp
next
  case (Cons x xs)
  (* Goal: rev (rev (x # xs)) = x # xs *)
  (* IH: Cons.IH is "rev (rev xs) = xs" *)
  (* Strategy:
     1. Unfold rev (x # xs) = rev xs @ [x]
     2. Apply rev to get: rev (rev xs @ [x])
     3. Use lemma: rev (xs @ ys) = rev ys @ rev xs
     4. Simplify using IH
  *)
  show ?case
  proof -
    have "rev (rev (x # xs)) = rev (rev xs @ [x])" by simp
    also have "... = rev [x] @ rev (rev xs)" by simp
    also have "... = [x] @ xs" using Cons.IH by simp
    also have "... = x # xs" by simp
    finally show ?thesis .
  qed
qed

(* Helper lemma that might be needed *)
lemma rev_append:
  "rev (xs @ ys) = rev ys @ rev xs"
  by simp

end
```

### Coq Proof Skeleton

```coq
Require Import List.
Import ListNotations.

(* Theorem: Reversing twice is identity *)
Theorem reverse_reverse :
  forall (A : Type) (l : list A),
    rev (rev l) = l.
Proof.
  intros A l.
  induction l as [| x xs IHxs].
  - (* Base case: rev (rev []) = [] *)
    (* Strategy: Simplify using definition *)
    simpl.
    reflexivity.
  - (* Inductive case: rev (rev xs) = xs -> rev (rev (x :: xs)) = x :: xs *)
    (* IHxs : rev (rev xs) = xs *)
    (* Strategy:
       1. Simplify rev (x :: xs) = rev xs ++ [x]
       2. Apply rev to get: rev (rev xs ++ [x])
       3. Use lemma: rev (l1 ++ l2) = rev l2 ++ rev l1
       4. Simplify using IHxs
    *)
    simpl.
    rewrite rev_app_distr.
    simpl.
    rewrite IHxs.
    reflexivity.
Qed.

(* Helper lemma (already in standard library as rev_app_distr) *)
Lemma rev_append :
  forall (A : Type) (l1 l2 : list A),
    rev (l1 ++ l2) = rev l2 ++ rev l1.
Proof.
  (* Proof omitted - use standard library *)
  apply rev_app_distr.
Qed.
```

## Example 2: Insertion Sort Correctness

### Theorem Statement
Prove that insertion sort produces a sorted list.

### Isabelle/HOL Proof Skeleton

```isabelle
theory InsertionSortCorrect
  imports Main
begin

(* Definitions from formal-spec-generator *)
fun insert :: "nat ⇒ nat list ⇒ nat list" where
  "insert x [] = [x]" |
  "insert x (y # ys) = (if x ≤ y then x # y # ys else y # insert x ys)"

fun insertion_sort :: "nat list ⇒ nat list" where
  "insertion_sort [] = []" |
  "insertion_sort (x # xs) = insert x (insertion_sort xs)"

fun is_sorted :: "nat list ⇒ bool" where
  "is_sorted [] = True" |
  "is_sorted [x] = True" |
  "is_sorted (x # y # ys) = (x ≤ y ∧ is_sorted (y # ys))"

(* Key lemma: insert preserves sortedness *)
lemma insert_sorted:
  assumes "is_sorted xs"
  shows "is_sorted (insert x xs)"
proof (induction xs)
  case Nil
  (* Goal: is_sorted (insert x []) *)
  (* Strategy: Simplify definition *)
  show ?case by simp
next
  case (Cons y ys)
  (* Goal: is_sorted ys ⟹ is_sorted (insert x (y # ys)) *)
  (* IH: Cons.IH is "is_sorted ys ⟹ is_sorted (insert x ys)" *)
  (* Strategy: Case split on x ≤ y *)
  show ?case
  proof (cases "x ≤ y")
    case True
    (* x ≤ y, so insert x (y # ys) = x # y # ys *)
    (* Need to show: is_sorted (x # y # ys) *)
    then show ?thesis sorry
  next
    case False
    (* x > y, so insert x (y # ys) = y # insert x ys *)
    (* Need to show: is_sorted (y # insert x ys) *)
    (* Use IH and properties of is_sorted *)
    then show ?thesis sorry
  qed
qed

(* Main theorem: insertion_sort produces sorted list *)
theorem insertion_sort_sorted:
  "is_sorted (insertion_sort xs)"
proof (induction xs)
  case Nil
  (* Goal: is_sorted (insertion_sort []) *)
  show ?case by simp
next
  case (Cons x xs)
  (* Goal: is_sorted (insertion_sort (x # xs)) *)
  (* IH: Cons.IH is "is_sorted (insertion_sort xs)" *)
  (* Strategy:
     1. Unfold: insertion_sort (x # xs) = insert x (insertion_sort xs)
     2. Apply insert_sorted lemma with IH
  *)
  show ?case
  proof -
    have "insertion_sort (x # xs) = insert x (insertion_sort xs)" by simp
    moreover have "is_sorted (insertion_sort xs)" using Cons.IH by simp
    ultimately show ?thesis using insert_sorted by simp
  qed
qed

end
```

### Coq Proof Skeleton

```coq
Require Import List Arith.
Import ListNotations.

(* Definitions from formal-spec-generator *)
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

Fixpoint is_sorted (l : list nat) : Prop :=
  match l with
  | [] => True
  | [x] => True
  | x :: y :: ys => x <= y /\ is_sorted (y :: ys)
  end.

(* Key lemma: insert preserves sortedness *)
Lemma insert_sorted :
  forall x l,
    is_sorted l ->
    is_sorted (insert x l).
Proof.
  intros x l Hsorted.
  induction l as [| y ys IHys].
  - (* Base case: insert x [] *)
    simpl.
    trivial.
  - (* Inductive case: insert x (y :: ys) *)
    simpl.
    destruct (x <=? y) eqn:Hcmp.
    + (* Case: x <= y *)
      (* insert x (y :: ys) = x :: y :: ys *)
      (* Need: is_sorted (x :: y :: ys) *)
      admit.
    + (* Case: x > y *)
      (* insert x (y :: ys) = y :: insert x ys *)
      (* Need: is_sorted (y :: insert x ys) *)
      (* Use IH *)
      admit.
Admitted.

(* Main theorem: insertion_sort produces sorted list *)
Theorem insertion_sort_sorted :
  forall l,
    is_sorted (insertion_sort l).
Proof.
  intros l.
  induction l as [| x xs IHxs].
  - (* Base case: insertion_sort [] *)
    simpl.
    trivial.
  - (* Inductive case: insertion_sort (x :: xs) *)
    (* IHxs : is_sorted (insertion_sort xs) *)
    (* Strategy:
       1. Simplify: insertion_sort (x :: xs) = insert x (insertion_sort xs)
       2. Apply insert_sorted with IHxs
    *)
    simpl.
    apply insert_sorted.
    exact IHxs.
Qed.
```

## Example 3: Binary Search Correctness

### Theorem Statement
Prove that binary search returns the correct index when the element is found.

### Isabelle/HOL Proof Skeleton

```isabelle
theory BinarySearchCorrect
  imports Main
begin

(* Simplified binary search *)
fun binary_search :: "nat list ⇒ nat ⇒ nat ⇒ nat ⇒ nat option" where
  "binary_search xs target low high =
    (if low > high then None
     else let mid = (low + high) div 2 in
          if xs ! mid = target then Some mid
          else if xs ! mid < target
               then binary_search xs target (mid + 1) high
               else binary_search xs target low (mid - 1))"

definition is_sorted :: "nat list ⇒ bool" where
  "is_sorted xs ≡ (∀i j. i < j ∧ j < length xs ⟶ xs ! i ≤ xs ! j)"

(* Correctness theorem *)
theorem binary_search_correct:
  assumes sorted: "is_sorted xs"
      and bounds: "low ≤ high" "high < length xs"
      and result: "binary_search xs target low high = Some idx"
  shows "idx < length xs ∧ xs ! idx = target"
proof -
  (* Strategy: Proof by induction on (high - low)
     - Termination measure: high - low decreases
     - Key invariant: if target in xs[low..high], then found
     - Use sortedness to justify binary search logic
  *)
  sorry
qed

(* Helper lemma: binary search maintains bounds *)
lemma binary_search_bounds:
  assumes "binary_search xs target low high = Some idx"
      and "low ≤ high"
  shows "low ≤ idx ∧ idx ≤ high"
  sorry

end
```

### Coq Proof Skeleton

```coq
Require Import List Arith Lia.
Import ListNotations.

(* Simplified binary search specification *)
Definition is_sorted (l : list nat) : Prop :=
  forall i j, i < j < length l -> nth i l 0 <= nth j l 0.

(* Correctness specification *)
Definition binary_search_spec
  (l : list nat) (target : nat) (low high : nat) (result : option nat) : Prop :=
  is_sorted l ->
  low <= high ->
  high < length l ->
  match result with
  | None => forall i, low <= i <= high -> nth i l 0 <> target
  | Some idx => low <= idx <= high /\ nth idx l 0 = target
  end.

(* Main correctness theorem *)
Theorem binary_search_correct :
  forall l target low high result,
    binary_search_spec l target low high result.
Proof.
  intros l target low high result.
  unfold binary_search_spec.
  intros Hsorted Hlow Hhigh.
  (* Strategy:
     - Proof by strong induction on (high - low)
     - Case analysis on result (None vs Some idx)
     - Use sortedness to justify correctness of binary search logic
     - Key insight: sorted array allows eliminating half the search space
  *)
  admit.
Admitted.
```

## Example 4: Arithmetic Property

### Theorem Statement
Prove that `n + m = m + n` (commutativity of addition).

### Isabelle/HOL Proof Skeleton

```isabelle
theory AddComm
  imports Main
begin

theorem add_comm:
  "n + m = (m + n :: nat)"
proof (induction n)
  case 0
  (* Goal: 0 + m = m + 0 *)
  (* Strategy: Use 0 + m = m and m + 0 = m *)
  show ?case by simp
next
  case (Suc n)
  (* Goal: Suc n + m = m + Suc n *)
  (* IH: Suc.IH is "n + m = m + n" *)
  (* Strategy:
     1. Suc n + m = Suc (n + m) by definition
     2. = Suc (m + n) by IH
     3. = m + Suc n by lemma
  *)
  show ?case
  proof -
    have "Suc n + m = Suc (n + m)" by simp
    also have "... = Suc (m + n)" using Suc.IH by simp
    also have "... = m + Suc n" by simp
    finally show ?thesis .
  qed
qed

end
```

### Coq Proof Skeleton

```coq
Require Import Arith.

Theorem add_comm :
  forall n m : nat,
    n + m = m + n.
Proof.
  intros n m.
  induction n as [| n' IHn'].
  - (* Base case: 0 + m = m + 0 *)
    simpl.
    rewrite <- plus_n_O.
    reflexivity.
  - (* Inductive case: S n' + m = m + S n' *)
    (* IHn' : n' + m = m + n' *)
    simpl.
    rewrite IHn'.
    rewrite <- plus_n_Sm.
    reflexivity.
Qed.
```
