# Coq Lemma Discovery

Comprehensive guide for discovering and using lemmas in Coq.

## Searching for Lemmas

### Search Commands

**Search by pattern:**
```coq
Search (_ + _).
(* Finds all lemmas involving addition *)
```

**Search by name:**
```coq
Search "plus".
(* Finds all lemmas with "plus" in name *)
```

**SearchAbout (deprecated, use Search):**
```coq
Search nat.
(* Finds all lemmas about nat *)
```

**SearchPattern:**
```coq
SearchPattern (_ + 0).
(* Finds lemmas matching the pattern *)
```

**Search with constraints:**
```coq
Search (_ + _) inside Arith.
(* Search only in Arith module *)

Search (_ + _) -"_ * _".
(* Exclude multiplication *)
```

### Locate

Find where a name is defined:
```coq
Locate "++".
(* Shows: Notation "x ++ y" := app x y *)

Locate plus.
(* Shows: Constant Coq.Init.Nat.add *)
```

### Print

Display definition or theorem:
```coq
Print plus.
(* Shows definition of plus *)

Print Nat.add_comm.
(* Shows statement and proof of commutativity *)
```

## Automatic Proof Search

### Auto and Eauto

**auto:** Applies simple tactics automatically
```coq
Lemma example : forall n, n + 0 = n.
Proof.
  auto.
Qed.
```

**eauto:** More powerful, uses existential variables
```coq
Lemma example : exists n, n + 5 = 10.
Proof.
  eauto.
Qed.
```

**With depth limit:**
```coq
Proof.
  auto 10.  (* Search depth 10 *)
Qed.
```

**With hint database:**
```coq
Proof.
  auto with arith.
Qed.
```

### Intuition and Tauto

**intuition:** Propositional reasoning
```coq
Lemma example : forall P Q, P /\ Q -> Q /\ P.
Proof.
  intuition.
Qed.
```

**tauto:** Tautology checker
```coq
Lemma example : forall P Q, (P -> Q) -> ~Q -> ~P.
Proof.
  tauto.
Qed.
```

### Omega and Lia

**omega (deprecated):** Linear arithmetic
```coq
Require Import Omega.

Lemma example : forall n m, n < m -> n + 1 <= m.
Proof.
  intros. omega.
Qed.
```

**lia:** Modern linear integer arithmetic
```coq
Require Import Lia.

Lemma example : forall n m, n < m -> n + 1 <= m.
Proof.
  intros. lia.
Qed.
```

### Ring and Field

**ring:** Ring equations
```coq
Require Import Ring.

Lemma example : forall x y, (x + y) * (x + y) = x*x + 2*x*y + y*y.
Proof.
  intros. ring.
Qed.
```

**field:** Field equations
```coq
Require Import Field.

Lemma example : forall x, x <> 0 -> x / x = 1.
Proof.
  intros. field. auto.
Qed.
```

## Common Lemma Patterns

### List Lemmas

**Append properties:**
```coq
Lemma app_nil_l : forall A (l : list A), [] ++ l = l.
Lemma app_nil_r : forall A (l : list A), l ++ [] = l.
Lemma app_assoc : forall A (l m n : list A), l ++ m ++ n = (l ++ m) ++ n.
Lemma app_length : forall A (l l' : list A), length (l ++ l') = length l + length l'.
```

**Map properties:**
```coq
Lemma map_app : forall A B (f : A -> B) l l',
  map f (l ++ l') = map f l ++ map f l'.
Lemma map_map : forall A B C (f : A -> B) (g : B -> C) l,
  map g (map f l) = map (fun x => g (f x)) l.
Lemma map_length : forall A B (f : A -> B) l,
  length (map f l) = length l.
```

**Filter properties:**
```coq
Lemma filter_app : forall A (f : A -> bool) l l',
  filter f (l ++ l') = filter f l ++ filter f l'.
Lemma filter_length : forall A (f : A -> bool) l,
  length (filter f l) <= length l.
```

**Reverse properties:**
```coq
Lemma rev_app_distr : forall A (l l' : list A),
  rev (l ++ l') = rev l' ++ rev l.
Lemma rev_involutive : forall A (l : list A),
  rev (rev l) = l.
Lemma rev_length : forall A (l : list A),
  length (rev l) = length l.
```

### Arithmetic Lemmas

**Addition:**
```coq
Lemma plus_0_l : forall n, 0 + n = n.
Lemma plus_0_r : forall n, n + 0 = n.
Lemma plus_comm : forall n m, n + m = m + n.
Lemma plus_assoc : forall n m p, n + (m + p) = (n + m) + p.
Lemma plus_reg_l : forall n m p, p + n = p + m -> n = m.
```

**Multiplication:**
```coq
Lemma mult_0_l : forall n, 0 * n = 0.
Lemma mult_1_l : forall n, 1 * n = n.
Lemma mult_comm : forall n m, n * m = m * n.
Lemma mult_assoc : forall n m p, n * (m * p) = (n * m) * p.
Lemma mult_plus_distr_r : forall n m p, (n + m) * p = n * p + m * p.
```

**Ordering:**
```coq
Lemma le_refl : forall n, n <= n.
Lemma le_trans : forall n m p, n <= m -> m <= p -> n <= p.
Lemma le_antisym : forall n m, n <= m -> m <= n -> n = m.
Lemma plus_le_compat : forall n m p q, n <= m -> p <= q -> n + p <= m + q.
```

### Boolean Lemmas

**Basic properties:**
```coq
Lemma andb_true_iff : forall b1 b2, b1 && b2 = true <-> b1 = true /\ b2 = true.
Lemma orb_true_iff : forall b1 b2, b1 || b2 = true <-> b1 = true \/ b2 = true.
Lemma negb_involutive : forall b, negb (negb b) = b.
```

## Induction Lemmas

### Strengthening Induction

**Problem:** Induction hypothesis too weak.

**Pattern:** Generalize with additional parameter.

**Example:**
```coq
(* Too specific *)
Fixpoint sum_n (n : nat) : nat :=
  match n with
  | 0 => 0
  | S n' => n + sum_n n'
  end.

Lemma sum_n_formula : forall n,
  2 * sum_n n = n * (n + 1).
Proof.
  induction n.
  - reflexivity.
  - simpl. (* Stuck: induction hypothesis not strong enough *)
Abort.

(* Generalized version *)
Lemma sum_n_formula_gen : forall n acc,
  2 * (acc + sum_n n) = 2 * acc + n * (n + 1).
Proof.
  induction n; intros; simpl.
  - lia.
  - rewrite IHn. lia.
Qed.
```

### Mutual Induction

**Pattern:** Define mutually recursive predicates.

**Example:**
```coq
Fixpoint even (n : nat) : bool :=
  match n with
  | 0 => true
  | S n' => odd n'
  end
with odd (n : nat) : bool :=
  match n with
  | 0 => false
  | S n' => even n'
  end.

Lemma even_odd_correct : forall n,
  (even n = true <-> exists k, n = 2 * k) /\
  (odd n = true <-> exists k, n = 2 * k + 1).
Proof.
  induction n.
  - split; split; intros.
    + exists 0. reflexivity.
    + reflexivity.
    + discriminate.
    + destruct H as [k H]. discriminate.
  - destruct IHn as [[IH1 IH2] [IH3 IH4]].
    split; split; intros.
    + (* Use IH3 for odd case *)
    + (* Use IH4 for odd case *)
    + (* Use IH1 for even case *)
    + (* Use IH2 for even case *)
Qed.
```

### Well-Founded Induction

**Pattern:** Induction on well-founded relation.

**Example:**
```coq
Require Import Wellfounded.

Lemma lt_wf_ind : forall P : nat -> Prop,
  (forall n, (forall m, m < n -> P m) -> P n) ->
  forall n, P n.
Proof.
  intros P H n.
  apply (well_founded_ind lt_wf P H n).
Qed.
```

## Rewriting Lemmas

### Basic Rewriting

**rewrite:** Apply equation left-to-right
```coq
Lemma example : forall n, n + 0 = n.
Proof.
  intros. rewrite plus_0_r. reflexivity.
Qed.
```

**rewrite <-:** Apply equation right-to-left
```coq
Lemma example : forall n, n = n + 0.
Proof.
  intros. rewrite <- plus_0_r. reflexivity.
Qed.
```

**Multiple rewrites:**
```coq
Lemma example : forall n m, n + m + 0 = m + n.
Proof.
  intros. rewrite plus_0_r, plus_comm. reflexivity.
Qed.
```

### Conditional Rewriting

**Pattern:** Rewrite under conditions.

**Example:**
```coq
Lemma example : forall n m,
  n < m -> n + 1 <= m.
Proof.
  intros n m H.
  rewrite <- (Nat.succ_pred m).
  - apply le_n_S. apply H.
  - (* Prove m <> 0 *)
    destruct m.
    + inversion H.
    + discriminate.
Qed.
```

## Case Analysis Lemmas

### Destruct and Case

**destruct:** Case analysis on term
```coq
Lemma example : forall n, n = 0 \/ n > 0.
Proof.
  intros. destruct n.
  - left. reflexivity.
  - right. apply Nat.lt_0_succ.
Qed.
```

**case_eq:** Case analysis with equation
```coq
Lemma example : forall b, b = true \/ b = false.
Proof.
  intros. case_eq b; intros.
  - left. auto.
  - right. auto.
Qed.
```

### Inversion

**Pattern:** Analyze constructor equations.

**Example:**
```coq
Inductive even : nat -> Prop :=
  | even_0 : even 0
  | even_SS : forall n, even n -> even (S (S n)).

Lemma even_not_odd : forall n,
  even n -> ~ even (S n).
Proof.
  intros n H. induction H.
  - intro H'. inversion H'.
  - intro H'. inversion H'. contradiction.
Qed.
```

## Proof Automation with Ltac

### Custom Tactics

**Simple tactic:**
```coq
Ltac solve_by_inversion :=
  match goal with
  | H : _ |- _ => inversion H; subst; auto
  end.
```

**Recursive tactic:**
```coq
Ltac crush :=
  repeat (simpl; auto; try discriminate; try contradiction; try congruence).
```

**Pattern matching tactic:**
```coq
Ltac destruct_match :=
  match goal with
  | |- context[match ?x with _ => _ end] => destruct x
  | H : context[match ?x with _ => _ end] |- _ => destruct x
  end.
```

### Hint Databases

**Create hint database:**
```coq
Create HintDb my_hints.
```

**Add hints:**
```coq
Hint Resolve my_lemma : my_hints.
Hint Rewrite my_eq : my_hints.
Hint Constructors my_inductive : my_hints.
```

**Use hints:**
```coq
Proof.
  auto with my_hints.
Qed.
```

## Lemma Discovery Workflow

### Step 1: Try Automatic Tactics

```coq
Lemma goal : ...
Proof.
  auto.
  (* or *)
  intuition.
  (* or *)
  lia.
Qed.
```

### Step 2: Search for Lemmas

```coq
Search (_ + _).
SearchPattern (_ + 0).
```

### Step 3: Manual Proof

```coq
Lemma goal : ...
Proof.
  intros.
  rewrite lemma1.
  apply lemma2.
  reflexivity.
Qed.
```

### Step 4: Identify Missing Lemmas

If proof fails, propose new lemma.

## Example: Complete Discovery

**Goal:**
```coq
Lemma filter_map_length : forall A B (f : A -> B) (P : B -> bool) l,
  length (filter P (map f l)) <= length l.
```

**Attempt 1:**
```coq
Proof.
  induction l; simpl.
  - reflexivity.
  - (* Stuck: need to case on P (f a) *)
Abort.
```

**Search for lemmas:**
```coq
Search (length (filter _ _)).
(* Finds: filter_length *)
```

**Attempt 2:**
```coq
Proof.
  induction l; simpl.
  - reflexivity.
  - destruct (P (f a)).
    + simpl. apply le_n_S. apply IHl.
    + (* Stuck: need lemma about <= and S *)
Abort.
```

**Search for lemmas:**
```coq
Search (_ <= S _).
(* Finds: le_S *)
```

**Final proof:**
```coq
Proof.
  induction l; simpl.
  - reflexivity.
  - destruct (P (f a)).
    + simpl. apply le_n_S. apply IHl.
    + apply le_S. apply IHl.
Qed.
```

**Alternative with automation:**
```coq
Proof.
  induction l; simpl; auto.
  destruct (P (f a)); simpl; auto.
Qed.
```
