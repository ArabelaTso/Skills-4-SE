# Formal Specification Examples

This file contains complete examples of formalizing algorithms in both Isabelle/HOL and Coq.

## Example 1: Insertion Sort

### Informal Specification
```
Function: insertion_sort
Input: A list of natural numbers
Output: A sorted list containing the same elements as the input
Properties:
  - The output is sorted in ascending order
  - The output is a permutation of the input
```

### Isabelle/HOL Specification

```isabelle
theory InsertionSort
  imports Main
begin

(* Insert an element into a sorted list *)
fun insert :: "nat ⇒ nat list ⇒ nat list" where
  "insert x [] = [x]" |
  "insert x (y # ys) = (if x ≤ y then x # y # ys else y # insert x ys)"

(* Insertion sort *)
fun insertion_sort :: "nat list ⇒ nat list" where
  "insertion_sort [] = []" |
  "insertion_sort (x # xs) = insert x (insertion_sort xs)"

(* Predicate: list is sorted *)
fun is_sorted :: "nat list ⇒ bool" where
  "is_sorted [] = True" |
  "is_sorted [x] = True" |
  "is_sorted (x # y # ys) = (x ≤ y ∧ is_sorted (y # ys))"

(* Correctness specification *)
definition insertion_sort_correct :: "nat list ⇒ bool" where
  "insertion_sort_correct xs ≡
    let ys = insertion_sort xs in
      is_sorted ys ∧
      set xs = set ys ∧
      length xs = length ys"

(* Correctness theorem (statement only) *)
theorem insertion_sort_correctness:
  "insertion_sort_correct xs"
  sorry

end
```

### Coq Specification

```coq
Require Import List.
Require Import Arith.
Require Import Permutation.
Import ListNotations.

(* Insert an element into a sorted list *)
Fixpoint insert (x : nat) (l : list nat) : list nat :=
  match l with
  | [] => [x]
  | y :: ys => if x <=? y then x :: y :: ys else y :: insert x ys
  end.

(* Insertion sort *)
Fixpoint insertion_sort (l : list nat) : list nat :=
  match l with
  | [] => []
  | x :: xs => insert x (insertion_sort xs)
  end.

(* Predicate: list is sorted *)
Fixpoint is_sorted (l : list nat) : Prop :=
  match l with
  | [] => True
  | [x] => True
  | x :: y :: ys => x <= y /\ is_sorted (y :: ys)
  end.

(* Correctness specification *)
Definition insertion_sort_correct (input : list nat) : Prop :=
  let output := insertion_sort input in
    is_sorted output /\
    Permutation input output.

(* Correctness theorem (statement only) *)
Theorem insertion_sort_correctness :
  forall l, insertion_sort_correct l.
Proof.
  (* Proof omitted *)
Admitted.
```

## Example 2: Binary Search

### Informal Specification
```
Function: binary_search
Input: A sorted array of integers, a target value
Output: Optional index where the target is found
Precondition: The input array is sorted
Postcondition: If Some(i) is returned, then array[i] = target
               If None is returned, then target is not in the array
```

### Isabelle/HOL Specification

```isabelle
theory BinarySearch
  imports Main
begin

(* Binary search on a sorted list *)
fun binary_search :: "nat list ⇒ nat ⇒ nat option" where
  "binary_search xs target = binary_search_aux xs target 0 (length xs - 1)"

fun binary_search_aux :: "nat list ⇒ nat ⇒ nat ⇒ nat ⇒ nat option" where
  "binary_search_aux xs target low high =
    (if low > high then None
     else let mid = (low + high) div 2 in
          if xs ! mid = target then Some mid
          else if xs ! mid < target then binary_search_aux xs target (mid + 1) high
          else binary_search_aux xs target low (mid - 1))"

(* Precondition: list is sorted *)
definition is_sorted :: "nat list ⇒ bool" where
  "is_sorted xs ≡ (∀i j. i < j ∧ j < length xs ⟶ xs ! i ≤ xs ! j)"

(* Postcondition specification *)
definition binary_search_spec :: "nat list ⇒ nat ⇒ nat option ⇒ bool" where
  "binary_search_spec xs target result ≡
    is_sorted xs ⟶
      (case result of
        None ⇒ target ∉ set xs |
        Some i ⇒ i < length xs ∧ xs ! i = target)"

(* Correctness theorem *)
theorem binary_search_correct:
  "binary_search_spec xs target (binary_search xs target)"
  sorry

end
```

### Coq Specification

```coq
Require Import List.
Require Import Arith.
Import ListNotations.

(* Precondition: list is sorted *)
Definition is_sorted (l : list nat) : Prop :=
  forall i j, i < j < length l -> nth i l 0 <= nth j l 0.

(* Binary search specification *)
Definition binary_search_spec (l : list nat) (target : nat) (result : option nat) : Prop :=
  is_sorted l ->
    match result with
    | None => ~ In target l
    | Some i => i < length l /\ nth i l 0 = target
    end.

(* Binary search function (simplified version) *)
Fixpoint binary_search_aux (l : list nat) (target low high : nat) : option nat :=
  match high - low with
  | 0 => if nth low l 0 =? target then Some low else None
  | S _ =>
      let mid := (low + high) / 2 in
      let mid_val := nth mid l 0 in
      if mid_val =? target then Some mid
      else if mid_val <? target then binary_search_aux l target (mid + 1) high
      else binary_search_aux l target low (mid - 1)
  end.

Definition binary_search (l : list nat) (target : nat) : option nat :=
  match l with
  | [] => None
  | _ => binary_search_aux l target 0 (length l - 1)
  end.

(* Correctness theorem *)
Theorem binary_search_correct :
  forall l target,
    binary_search_spec l target (binary_search l target).
Proof.
  (* Proof omitted *)
Admitted.
```

## Example 3: Stack Data Structure

### Informal Specification
```
Data Structure: Stack
Operations:
  - empty: Create an empty stack
  - push: Add an element to the top
  - pop: Remove and return the top element
  - is_empty: Check if stack is empty
Invariants:
  - pop(push(s, x)) = (x, s)
  - is_empty(empty) = true
  - is_empty(push(s, x)) = false
```

### Isabelle/HOL Specification

```isabelle
theory Stack
  imports Main
begin

(* Stack represented as a list *)
type_synonym 'a stack = "'a list"

definition empty :: "'a stack" where
  "empty ≡ []"

definition push :: "'a ⇒ 'a stack ⇒ 'a stack" where
  "push x s ≡ x # s"

definition pop :: "'a stack ⇒ ('a × 'a stack) option" where
  "pop s ≡ case s of [] ⇒ None | (x # xs) ⇒ Some (x, xs)"

definition is_empty :: "'a stack ⇒ bool" where
  "is_empty s ≡ (s = [])"

(* Stack invariants *)
lemma pop_push:
  "pop (push x s) = Some (x, s)"
  unfolding push_def pop_def by simp

lemma empty_is_empty:
  "is_empty empty"
  unfolding is_empty_def empty_def by simp

lemma push_not_empty:
  "¬ is_empty (push x s)"
  unfolding is_empty_def push_def by simp

end
```

### Coq Specification

```coq
Require Import List.
Import ListNotations.

(* Stack represented as a list *)
Definition stack (A : Type) := list A.

Definition empty {A : Type} : stack A := [].

Definition push {A : Type} (x : A) (s : stack A) : stack A := x :: s.

Definition pop {A : Type} (s : stack A) : option (A * stack A) :=
  match s with
  | [] => None
  | x :: xs => Some (x, xs)
  end.

Definition is_empty {A : Type} (s : stack A) : bool :=
  match s with
  | [] => true
  | _ => false
  end.

(* Stack invariants *)
Lemma pop_push : forall A (x : A) (s : stack A),
  pop (push x s) = Some (x, s).
Proof.
  intros. reflexivity.
Qed.

Lemma empty_is_empty : forall A,
  is_empty (@empty A) = true.
Proof.
  intros. reflexivity.
Qed.

Lemma push_not_empty : forall A (x : A) (s : stack A),
  is_empty (push x s) = false.
Proof.
  intros. reflexivity.
Qed.
```
