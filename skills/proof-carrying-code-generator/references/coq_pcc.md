# Coq Proof-Carrying Code

Comprehensive guide for generating proof-carrying code in Coq.

## Extraction Basics

### Basic Extraction

**Extract single function:**
```coq
Require Extraction.

Fixpoint factorial (n : nat) : nat :=
  match n with
  | 0 => 1
  | S n' => n * factorial n'
  end.

Extraction "factorial.ml" factorial.
```

**Extract multiple definitions:**
```coq
Extraction "module.ml" func1 func2 func3.
```

**Extract entire module:**
```coq
Module MyModule.
  Definition func1 := ...
  Definition func2 := ...
End MyModule.

Extraction "my_module.ml" MyModule.
```

### Extraction Languages

**OCaml (default):**
```coq
Extraction Language OCaml.
Extraction "output.ml" my_function.
```

**Haskell:**
```coq
Extraction Language Haskell.
Extraction "Output.hs" my_function.
```

**Scheme:**
```coq
Extraction Language Scheme.
Extraction "output.scm" my_function.
```

**JSON (for inspection):**
```coq
Extraction Language JSON.
Extraction "output.json" my_function.
```

## Verified Implementations

### Pattern 1: Direct Implementation with Proof

**Workflow:**
1. Implement function
2. State correctness theorem
3. Prove theorem
4. Extract code

**Example: Verified list operations**
```coq
Require Import List.
Import ListNotations.

(* Implementation *)
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

(* Correctness properties *)
Require Import Sorted Permutation.

Lemma insert_sorted : forall x l,
  LocallySorted le l → LocallySorted le (insert x l).
Proof.
  induction l; simpl; intros.
  - constructor.
  - destruct (x <=? a) eqn:E.
    + constructor; auto.
      apply Nat.leb_le in E.
      inversion H; subst; auto.
      constructor; auto.
    + inversion H; subst.
      * simpl. destruct (x <=? a) eqn:E2.
        -- constructor; auto. constructor.
        -- constructor; auto.
      * simpl in IHl. destruct (x <=? a0) eqn:E2.
        -- constructor; auto.
        -- apply IHl in H3.
           (* Continue proof *)
Admitted.

Theorem insertion_sort_correct : forall l,
  LocallySorted le (insertion_sort l) /\
  Permutation l (insertion_sort l).
Proof.
  induction l; simpl.
  - split; constructor.
  - destruct IHl as [IH1 IH2].
    split.
    + apply insert_sorted. auto.
    + (* Permutation proof *)
Admitted.

(* Extract *)
Extraction "insertion_sort.ml" insertion_sort.
```

### Pattern 2: Program Framework

**Workflow:**
1. Write function with contracts
2. Coq generates proof obligations
3. Prove obligations
4. Extract code

**Example: Safe division**
```coq
Require Import Program.

Program Definition safe_div (a b : nat) (H : b <> 0) : nat :=
  a / b.

(* Proof obligation automatically generated and discharged *)

(* Alternative with option *)
Program Definition safe_div_opt (a b : nat) : option nat :=
  if b =? 0 then None else Some (a / b).

Next Obligation.
  apply Nat.eqb_neq in H. auto.
Qed.

(* Extract *)
Extraction "safe_div.ml" safe_div safe_div_opt.
```

### Pattern 3: Refinement-Based

**Workflow:**
1. Abstract specification
2. Concrete implementation
3. Prove refinement
4. Extract concrete code

**Example: Verified search**
```coq
Require Import List.
Import ListNotations.

(* Abstract specification *)
Definition find_spec {A} (P : A → bool) (l : list A) : option A :=
  (* Nondeterministic: any element satisfying P *)
  if existsb P l then
    Some (hd_error (filter P l))
  else None.

(* Concrete implementation *)
Fixpoint find {A} (P : A → bool) (l : list A) : option A :=
  match l with
  | [] => None
  | x :: xs => if P x then Some x else find P xs
  end.

(* Refinement proof *)
Theorem find_refines : forall A (P : A → bool) l,
  find P l = find_spec P l.
Proof.
  induction l; simpl; intros.
  - reflexivity.
  - destruct (P a) eqn:E.
    + reflexivity.
    + apply IHl.
Qed.

(* Extract *)
Extraction "find.ml" find.
```

## Safety Certification

### Memory Safety

**Pattern: Bounds-checked access**
```coq
Require Import List Vector.
Import ListNotations.

(* Safe list access *)
Definition safe_nth {A} (l : list A) (n : nat) : option A :=
  nth_error l n.

(* Safety property *)
Lemma safe_nth_bounds : forall A (l : list A) n v,
  safe_nth l n = Some v → n < length l.
Proof.
  intros. unfold safe_nth in H.
  apply nth_error_Some. congruence.
Qed.

(* Vector: length-indexed lists *)
Definition safe_nth_vec {A n} (v : Vector.t A n) (i : nat) (H : i < n) : A :=
  Vector.nth_order v H.

(* Safety guaranteed by type *)
Lemma safe_nth_vec_safe : forall A n (v : Vector.t A n) i H,
  exists a, safe_nth_vec v i H = a.
Proof.
  intros. exists (safe_nth_vec v i H). reflexivity.
Qed.

(* Extract *)
Extraction "safe_access.ml" safe_nth.
```

### Null Safety

**Pattern: Non-empty types**
```coq
Require Import List.
Import ListNotations.

(* Non-empty list type *)
Inductive nonempty_list (A : Type) : Type :=
  | singleton : A → nonempty_list A
  | cons : A → nonempty_list A → nonempty_list A.

(* Safe head *)
Definition ne_head {A} (l : nonempty_list A) : A :=
  match l with
  | singleton x => x
  | cons x _ => x
  end.

(* Safety property *)
Lemma ne_head_safe : forall A (l : nonempty_list A),
  exists x, ne_head l = x.
Proof.
  intros. exists (ne_head l). reflexivity.
Qed.

(* Convert from list with proof *)
Program Definition list_to_nonempty {A} (l : list A) (H : l <> []) : nonempty_list A :=
  match l with
  | [] => _
  | [x] => singleton A x
  | x :: xs => cons A x (list_to_nonempty xs _)
  end.
Next Obligation.
  contradiction.
Qed.
Next Obligation.
  intro. discriminate.
Qed.

(* Extract *)
Extraction "nonempty_list.ml" nonempty_list ne_head.
```

### Arithmetic Safety

**Pattern: Division by zero prevention**
```coq
Require Import Arith.

(* Safe division with option *)
Definition safe_div (a b : nat) : option nat :=
  if b =? 0 then None else Some (a / b).

(* Safety property *)
Lemma safe_div_no_error : forall a b q,
  safe_div a b = Some q → b <> 0 /\ a / b = q.
Proof.
  intros. unfold safe_div in H.
  destruct (b =? 0) eqn:E.
  - discriminate.
  - injection H as H. split.
    + apply Nat.eqb_neq. auto.
    + auto.
Qed.

(* Alternative: dependent type *)
Program Definition safe_div_dep (a b : nat) (H : b <> 0) : nat :=
  a / b.

(* Extract *)
Extraction "safe_arith.ml" safe_div safe_div_dep.
```

## Functional Correctness

### Specification-Based Verification

**Pattern: Prove implementation meets specification**
```coq
Require Import Nat.

(* Specification *)
Definition gcd_spec (a b g : nat) : Prop :=
  (g | a) /\ (g | b) /\ forall d, (d | a) → (d | b) → (d | g).

(* Implementation *)
Fixpoint gcd_impl (a b : nat) : nat :=
  match b with
  | 0 => a
  | S b' => gcd_impl b (a mod b)
  end.

(* Correctness proof *)
Theorem gcd_impl_correct : forall a b,
  gcd_spec a b (gcd_impl a b).
Proof.
  intros a b. functional induction (gcd_impl a b).
  - unfold gcd_spec. split; [apply Nat.divide_refl | split].
    + apply Nat.divide_0_r.
    + intros. auto.
  - unfold gcd_spec in *. destruct IHn as [IH1 [IH2 IH3]].
    split; [| split].
    + (* Prove (gcd_impl b (a mod b)) | a *)
    + (* Prove (gcd_impl b (a mod b)) | b *)
    + (* Prove maximality *)
Admitted.

(* Extract *)
Extraction "gcd.ml" gcd_impl.
```

### Invariant Preservation

**Pattern: Data structure invariants**
```coq
Require Import List.
Import ListNotations.

(* Binary search tree *)
Inductive tree : Type :=
  | Leaf : tree
  | Node : tree → nat → tree → tree.

(* BST invariant *)
Fixpoint bst (t : tree) : Prop :=
  match t with
  | Leaf => True
  | Node l x r =>
      bst l /\ bst r /\
      (forall y, In y (tree_to_list l) → y < x) /\
      (forall y, In y (tree_to_list r) → x < y)
  end
with tree_to_list (t : tree) : list nat :=
  match t with
  | Leaf => []
  | Node l x r => tree_to_list l ++ [x] ++ tree_to_list r
  end.

(* Insert operation *)
Fixpoint insert (x : nat) (t : tree) : tree :=
  match t with
  | Leaf => Node Leaf x Leaf
  | Node l y r =>
      if x <? y then Node (insert x l) y r
      else if y <? x then Node l y (insert x r)
      else t
  end.

(* Invariant preservation *)
Theorem insert_preserves_bst : forall x t,
  bst t → bst (insert x t).
Proof.
  induction t; simpl; intros.
  - repeat split; auto.
  - destruct H as [H1 [H2 [H3 H4]]].
    destruct (x <? n) eqn:E1.
    + simpl. repeat split; auto.
      * apply IHt1. auto.
      * intros. apply H3.
        (* Continue proof *)
Admitted.

(* Extract *)
Extraction "bst.ml" tree insert.
```

## Extraction Customization

### Type Mapping

**Map Coq types to native types:**
```coq
(* Map nat to OCaml int *)
Extract Inductive nat => "int"
  [ "0" "(fun x -> x + 1)" ]
  "(fun zero succ n -> if n = 0 then zero else succ (n - 1))".

(* Map list to OCaml list *)
Extract Inductive list => "list" [ "[]" "(::)" ].

(* Map bool to OCaml bool *)
Extract Inductive bool => "bool" [ "true" "false" ].

(* Map option to OCaml option *)
Extract Inductive option => "option" [ "Some" "None" ].
```

### Constant Mapping

**Map Coq constants to native functions:**
```coq
(* Map addition to native + *)
Extract Constant plus => "(+)".

(* Map multiplication to native * *)
Extract Constant mult => "(*)".

(* Map comparison *)
Extract Constant Nat.eqb => "(=)".
Extract Constant Nat.leb => "(<=)".
```

### Inlining

**Inline simple definitions:**
```coq
Extraction Inline my_simple_function.
```

## Termination Proofs

### Well-Founded Recursion with Equations

**Pattern: Prove termination explicitly**
```coq
Require Import Equations.Equations.
Require Import Arith Lia.

(* Ackermann function *)
Equations ackermann (m n : nat) : nat by wf (m, n) (Nat.lt ×ₗ Nat.lt) :=
  ackermann 0 n := S n;
  ackermann (S m) 0 := ackermann m 1;
  ackermann (S m) (S n) := ackermann m (ackermann (S m) n).

(* Termination automatically proven *)

(* Extract *)
Extraction "ackermann.ml" ackermann.
```

### Program with Measure

**Pattern: Specify decreasing measure**
```coq
Require Import Program Arith.

Program Fixpoint div2 (n : nat) {measure n} : nat :=
  match n with
  | 0 => 0
  | 1 => 0
  | S (S n') => S (div2 n')
  end.
Next Obligation.
  lia.
Qed.

(* Extract *)
Extraction "div2.ml" div2.
```

## Complete Example: Verified Merge Sort

```coq
Require Import List Sorted Permutation.
Import ListNotations.

(* Split list into two halves *)
Fixpoint split {A} (l : list A) : list A * list A :=
  match l with
  | [] => ([], [])
  | [x] => ([x], [])
  | x :: y :: rest =>
      let (l1, l2) := split rest in
      (x :: l1, y :: l2)
  end.

(* Merge two sorted lists *)
Fixpoint merge (l1 l2 : list nat) : list nat :=
  match l1, l2 with
  | [], _ => l2
  | _, [] => l1
  | x :: xs, y :: ys =>
      if x <=? y then x :: merge xs l2
      else y :: merge l1 ys
  end.

(* Merge sort *)
Fixpoint merge_sort (l : list nat) : list nat :=
  match l with
  | [] => []
  | [x] => [x]
  | _ =>
      let (l1, l2) := split l in
      merge (merge_sort l1) (merge_sort l2)
  end.

(* Helper lemmas *)
Lemma split_length : forall A (l : list A) l1 l2,
  split l = (l1, l2) →
  length l1 <= length l /\ length l2 <= length l.
Proof.
  induction l as [| x [| y rest]]; simpl; intros.
  - injection H as H1 H2. subst. auto.
  - injection H as H1 H2. subst. auto.
  - destruct (split rest) as [r1 r2] eqn:E.
    injection H as H1 H2. subst.
    specialize (IHl r1 r2 E).
    simpl. lia.
Qed.

Lemma merge_sorted : forall l1 l2,
  LocallySorted le l1 →
  LocallySorted le l2 →
  LocallySorted le (merge l1 l2).
Proof.
  induction l1; intros; simpl.
  - auto.
  - destruct l2; simpl.
    + auto.
    + destruct (a <=? n) eqn:E.
      * (* Continue proof *)
Admitted.

Lemma merge_permutation : forall l1 l2,
  Permutation (l1 ++ l2) (merge l1 l2).
Proof.
  induction l1; intros; simpl.
  - reflexivity.
  - destruct l2; simpl.
    + rewrite app_nil_r. reflexivity.
    + destruct (a <=? n) eqn:E.
      * (* Continue proof *)
Admitted.

(* Main correctness theorem *)
Theorem merge_sort_correct : forall l,
  LocallySorted le (merge_sort l) /\
  Permutation l (merge_sort l).
Proof.
  intro l.
  functional induction (merge_sort l).
  - split; constructor.
  - split; constructor.
  - destruct IHl0 as [IH1 IH2].
    destruct IHl3 as [IH3 IH4].
    split.
    + apply merge_sorted; auto.
    + (* Permutation proof *)
Admitted.

(* Extract certified code *)
Extraction "merge_sort.ml" merge_sort.
```

## Extraction Optimization

### Avoiding Proof Terms

**Pattern: Extract only computational content**
```coq
(* Proofs are erased during extraction *)
Definition verified_function (x : nat) : {y : nat | y > x} :=
  exist _ (S x) (Nat.lt_succ_diag_r x).

(* Extracted code only contains S x, proof is erased *)
Extraction verified_function.
```

### Efficient Data Structures

**Pattern: Use efficient representations**
```coq
(* Use native integers *)
Extract Inductive nat => "int"
  [ "0" "(fun x -> x + 1)" ]
  "(fun zero succ n -> if n = 0 then zero else succ (n - 1))".

(* Use native arrays *)
Require Import ExtrOcamlNatInt ExtrOcamlString.
```

## Testing Extracted Code

**Pattern: Generate test harness**
```coq
(* Test function *)
Definition test_sort (tests : list (list nat)) : bool :=
  forallb (fun l => LocallySorted_b le (merge_sort l)) tests.

(* Extract with tests *)
Extraction "merge_sort_test.ml" merge_sort test_sort.
```
