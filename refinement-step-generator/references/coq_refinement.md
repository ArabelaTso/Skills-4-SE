# Coq Refinement Techniques

Comprehensive guide for refinement in Coq using Program, Equations, and refinement types.

## Basic Refinement in Coq

### Refinement with Subset Types

Use subset types `{x : A | P x}` to refine types with predicates.

```coq
Require Import List Arith.

(* Refined type: non-empty lists *)
Definition NonEmptyList (A : Type) := {l : list A | l <> nil}.

(* Head function with refinement *)
Program Definition head {A : Type} (l : NonEmptyList A) : A :=
  match l with
  | nil => _
  | x :: _ => x
  end.
Next Obligation.
  destruct l as [l Hl]. simpl in *. contradiction.
Qed.

(* Tail function *)
Program Definition tail {A : Type} (l : NonEmptyList A) : list A :=
  match l with
  | nil => nil
  | _ :: xs => xs
  end.
```

### Refinement with Dependent Types

```coq
Require Import Vector.

(* Vector: length-indexed list *)
Definition Vec (A : Type) (n : nat) := Vector.t A n.

(* Safe indexing *)
Definition vec_nth {A : Type} {n : nat} (v : Vec A n) (i : nat) (H : i < n) : A :=
  Vector.nth_order v H.

(* Append with length proof *)
Definition vec_append {A : Type} {m n : nat}
  (v1 : Vec A m) (v2 : Vec A n) : Vec A (m + n) :=
  Vector.append v1 v2.
```

## Program Framework

The Program framework allows writing programs with obligations that are proven separately.

### Basic Program Usage

```coq
Require Import Program.

(* Division with proof obligation *)
Program Definition safe_div (a b : nat) (H : b <> 0) : nat :=
  a / b.

(* Factorial with decreasing argument *)
Program Fixpoint factorial (n : nat) : nat :=
  match n with
  | 0 => 1
  | S n' => n * factorial n'
  end.
```

### Program with Specifications

```coq
(* Specification as type *)
Program Definition find_index {A : Type} (P : A -> bool) (l : list A) :
  {n : nat | n < length l /\ P (nth n l) = true} + {forall x, In x l -> P x = false} :=
  fix find_aux l n :=
    match l with
    | nil => inright _
    | x :: xs =>
      if P x then inleft (exist _ n _)
      else find_aux xs (S n)
    end l 0.
Next Obligation.
  (* Prove obligations *)
Qed.
```

### Program with Refinement

```coq
(* Abstract specification *)
Definition sort_spec {A : Type} (R : A -> A -> Prop) (l l' : list A) : Prop :=
  Permutation l l' /\ StronglySorted R l'.

(* Concrete implementation with Program *)
Program Fixpoint insertion_sort (l : list nat) :
  {l' : list nat | sort_spec le l l'} :=
  match l with
  | nil => nil
  | x :: xs =>
    let (sorted_xs, _) := insertion_sort xs in
    insert x sorted_xs
  end.
Next Obligation.
  (* Prove sort_spec holds *)
Qed.
```

## Equations Plugin

Equations provides better support for dependent pattern matching and well-founded recursion.

### Basic Equations Usage

```coq
Require Import Equations.Equations.

(* Simple recursion *)
Equations factorial (n : nat) : nat :=
  factorial 0 := 1;
  factorial (S n) := S n * factorial n.

(* Pattern matching *)
Equations filter {A : Type} (P : A -> bool) (l : list A) : list A :=
  filter P nil := nil;
  filter P (cons x xs) with P x := {
    | true := cons x (filter P xs);
    | false := filter P xs
  }.
```

### Well-Founded Recursion

```coq
(* Ackermann function *)
Equations ackermann (m n : nat) : nat by wf (m, n) (Nat.lt ×ₗ Nat.lt) :=
  ackermann 0 n := S n;
  ackermann (S m) 0 := ackermann m 1;
  ackermann (S m) (S n) := ackermann m (ackermann (S m) n).

(* Quicksort with well-founded recursion *)
Equations quicksort (l : list nat) : list nat by wf (length l) lt :=
  quicksort nil := nil;
  quicksort (cons pivot xs) :=
    let (smaller, larger) := partition (fun x => x <=? pivot) xs in
    quicksort smaller ++ [pivot] ++ quicksort larger.
```

### Dependent Equations

```coq
(* Vector operations *)
Equations vec_map {A B : Type} {n : nat} (f : A -> B) (v : Vec A n) : Vec B n :=
  vec_map f (Vector.nil _) := Vector.nil _;
  vec_map f (Vector.cons _ x _ xs) := Vector.cons _ (f x) _ (vec_map f xs).

(* Safe head *)
Equations vec_head {A : Type} {n : nat} (v : Vec A (S n)) : A :=
  vec_head (Vector.cons _ x _ _) := x.
```

## Refinement Types

### Option Refinement

```coq
(* Refine partial functions *)
Definition find_opt {A : Type} (P : A -> bool) (l : list A) : option A :=
  find P l.

(* Specification *)
Definition find_spec {A : Type} (P : A -> bool) (l : list A) (r : option A) : Prop :=
  match r with
  | None => forall x, In x l -> P x = false
  | Some x => In x l /\ P x = true
  end.

(* Correctness *)
Lemma find_correct : forall A P l,
  find_spec P l (@find_opt A P l).
Proof.
  (* Proof by induction *)
Qed.
```

### Result Type Refinement

```coq
Inductive Result (E A : Type) : Type :=
  | Ok : A -> Result E A
  | Error : E -> Result E A.

Arguments Ok {E A}.
Arguments Error {E A}.

(* Safe division *)
Definition safe_div_result (a b : nat) : Result string nat :=
  if b =? 0 then Error "Division by zero"
  else Ok (a / b).

(* Bind operation *)
Definition bind {E A B : Type} (r : Result E A) (f : A -> Result E B) : Result E B :=
  match r with
  | Ok x => f x
  | Error e => Error e
  end.

(* Example usage *)
Definition compute (x y z : nat) : Result string nat :=
  bind (safe_div_result x y) (fun r1 =>
  bind (safe_div_result r1 z) (fun r2 =>
  Ok r2)).
```

## Data Refinement Patterns

### Set to List Refinement

```coq
Require Import MSets.

(* Abstract: Set interface *)
Module Type SET.
  Parameter t : Type -> Type.
  Parameter empty : forall A, t A.
  Parameter add : forall A, A -> t A -> t A.
  Parameter mem : forall A, A -> t A -> bool.
End SET.

(* Concrete: List implementation *)
Module ListSet : SET.
  Definition t (A : Type) := list A.
  Definition empty {A} : t A := nil.
  Definition add {A} (x : A) (s : t A) : t A := x :: s.
  Definition mem {A} := @List.existsb A.
End ListSet.

(* Abstraction relation *)
Definition abs_list {A : Type} (l : list A) : list A -> Prop :=
  fun s => Permutation l s.

(* Refinement proofs *)
Lemma add_refines : forall A (x : A) l,
  abs_list (ListSet.add x l) (x :: l).
Proof.
  intros. unfold abs_list, ListSet.add. apply Permutation_refl.
Qed.
```

### Map to Association List

```coq
Require Import FMaps.

(* Association list *)
Definition alist (K V : Type) := list (K * V).

(* Operations *)
Fixpoint alist_lookup {K V : Type} (eq_dec : forall x y : K, {x = y} + {x <> y})
  (k : K) (al : alist K V) : option V :=
  match al with
  | nil => None
  | (k', v) :: rest =>
    if eq_dec k k' then Some v
    else alist_lookup eq_dec k rest
  end.

Definition alist_insert {K V : Type} (k : K) (v : V) (al : alist K V) : alist K V :=
  (k, v) :: al.

(* Abstraction to functional map *)
Fixpoint alist_to_map {K V : Type} (eq_dec : forall x y : K, {x = y} + {x <> y})
  (al : alist K V) : K -> option V :=
  fun k => alist_lookup eq_dec k al.

(* Refinement lemma *)
Lemma alist_insert_refines : forall K V eq_dec k v al,
  alist_to_map eq_dec (@alist_insert K V k v al) k = Some v.
Proof.
  intros. unfold alist_to_map, alist_insert. simpl.
  destruct (eq_dec k k); [reflexivity | contradiction].
Qed.
```

## Algorithmic Refinement

### Specification to Algorithm

```coq
(* Abstract specification: maximum element *)
Definition max_spec (l : list nat) (m : nat) : Prop :=
  In m l /\ forall x, In x l -> x <= m.

(* Concrete algorithm *)
Fixpoint find_max (l : list nat) : option nat :=
  match l with
  | nil => None
  | x :: xs =>
    match find_max xs with
    | None => Some x
    | Some m => Some (max x m)
    end
  end.

(* Correctness proof *)
Lemma find_max_correct : forall l m,
  find_max l = Some m -> max_spec l m.
Proof.
  induction l; intros.
  - discriminate.
  - simpl in H. destruct (find_max l) eqn:E.
    + injection H as H. subst.
      destruct (IHl n E) as [H1 H2].
      split.
      * apply Max.max_case_strong; auto.
      * intros. simpl in H. destruct H.
        -- subst. apply Nat.le_max_l.
        -- transitivity n; auto. apply Nat.le_max_r.
    + injection H as H. subst. split; simpl; auto.
      intros. destruct H; auto. contradiction.
Qed.
```

### Nondeterministic to Deterministic

```coq
(* Nondeterministic specification *)
Inductive find_any {A : Type} (P : A -> Prop) : list A -> A -> Prop :=
  | find_here : forall x xs, P x -> find_any P (x :: xs) x
  | find_later : forall x y xs, find_any P xs y -> find_any P (x :: xs) y.

(* Deterministic implementation *)
Fixpoint find_first {A : Type} (P : A -> bool) (l : list A) : option A :=
  match l with
  | nil => None
  | x :: xs => if P x then Some x else find_first P xs
  end.

(* Refinement: find_first refines find_any *)
Lemma find_first_refines : forall A P l x,
  find_first P l = Some x ->
  find_any (fun y => P y = true) l x.
Proof.
  induction l; intros.
  - discriminate.
  - simpl in H. destruct (P a) eqn:E.
    + injection H as H. subst. constructor. auto.
    + constructor. apply IHl. auto.
Qed.
```

## Extraction

Extract verified Coq code to OCaml, Haskell, or Scheme.

### Basic Extraction

```coq
Require Extraction.

(* Define function *)
Fixpoint fibonacci (n : nat) : nat :=
  match n with
  | 0 => 0
  | S 0 => 1
  | S (S n' as n'') => fibonacci n' + fibonacci n''
  end.

(* Extract to OCaml *)
Extraction Language OCaml.
Extraction "fibonacci.ml" fibonacci.

(* Extract to Haskell *)
Extraction Language Haskell.
Extraction "Fibonacci.hs" fibonacci.
```

### Extraction with Custom Types

```coq
(* Custom extraction for nat *)
Extract Inductive nat => "int"
  [ "0" "(fun x -> x + 1)" ]
  "(fun zero succ n -> if n = 0 then zero else succ (n - 1))".

(* Custom extraction for list *)
Extract Inductive list => "list" [ "[]" "(::)" ].

(* Custom extraction for bool *)
Extract Inductive bool => "bool" [ "true" "false" ].
```

## Complete Refinement Example

```coq
Require Import List Arith Program Permutation.
Import ListNotations.

(* Abstract specification: sorting *)
Definition sorted (l : list nat) : Prop :=
  forall i j, i < j < length l -> nth i l 0 <= nth j l 0.

Definition sort_spec (input output : list nat) : Prop :=
  sorted output /\ Permutation input output.

(* Refinement 1: Insertion sort specification *)
Fixpoint insert (x : nat) (l : list nat) : list nat :=
  match l with
  | [] => [x]
  | h :: t => if x <=? h then x :: l else h :: insert x t
  end.

Fixpoint insertion_sort (l : list nat) : list nat :=
  match l with
  | [] => []
  | h :: t => insert h (insertion_sort t)
  end.

(* Helper lemmas *)
Lemma insert_sorted : forall x l,
  sorted l -> sorted (insert x l).
Proof.
  (* Proof by induction *)
Admitted.

Lemma insert_perm : forall x l,
  Permutation (x :: l) (insert x l).
Proof.
  (* Proof by induction *)
Admitted.

(* Main correctness theorem *)
Theorem insertion_sort_correct : forall l,
  sort_spec l (insertion_sort l).
Proof.
  intros l. split.
  - induction l; simpl.
    + unfold sorted. intros. omega.
    + apply insert_sorted. apply IHl.
  - induction l; simpl.
    + apply Permutation_refl.
    + transitivity (a :: insertion_sort l).
      * apply perm_skip. apply IHl.
      * apply insert_perm.
Qed.

(* Extract to OCaml *)
Extraction "insertion_sort.ml" insertion_sort.
```
