# Coq Proof Tactics and Patterns

## Table of Contents
1. Basic Proof Structure
2. Common Tactics
3. Proof Patterns by Type
4. Induction Patterns
5. Case Analysis Patterns

## 1. Basic Proof Structure

### Simple Proof
```coq
Theorem theorem_name : statement.
Proof.
  tactics.
Qed.
```

### Proof with Intermediate Steps
```coq
Theorem theorem_name : statement.
Proof.
  (* step 1 *)
  tactic1.
  (* step 2 *)
  tactic2.
  (* conclusion *)
  tactic3.
Qed.
```

### Proof with Hypotheses
```coq
Theorem theorem_name :
  hypothesis1 -> hypothesis2 -> conclusion.
Proof.
  intros H1 H2.
  (* proof body *)
Qed.
```

## 2. Common Tactics

### Introduction Tactics
- `intros` - Introduce hypotheses and variables
- `intro x` - Introduce with specific name
- `intros [patterns]` - Introduction with pattern matching

### Application Tactics
- `apply H` - Apply hypothesis or theorem
- `apply H in H'` - Apply to hypothesis
- `eapply` - Apply with existential variables
- `exact H` - Exact proof term

### Rewriting Tactics
- `rewrite H` - Rewrite using equality
- `rewrite <- H` - Rewrite right-to-left
- `rewrite H in H'` - Rewrite in hypothesis
- `reflexivity` - Prove by reflexivity
- `symmetry` - Swap sides of equality

### Simplification Tactics
- `simpl` - Simplify expressions
- `unfold def` - Unfold definition
- `fold def` - Fold definition
- `compute` - Full computation

### Logical Tactics
- `split` - Split conjunction
- `left` / `right` - Choose disjunction
- `exists witness` - Provide existential witness
- `destruct H` - Case analysis on hypothesis
- `inversion H` - Invert inductive definition

### Automation Tactics
- `auto` - Automatic proof search
- `trivial` - Solve trivial goals
- `easy` - Combination of simple tactics
- `intuition` - Propositional reasoning
- `omega` - Linear arithmetic (deprecated, use lia)
- `lia` - Linear integer arithmetic
- `nia` - Non-linear integer arithmetic

## 3. Proof Patterns by Type

### Equality Proofs
```coq
Theorem equality_example : f x = g x.
Proof.
  unfold f, g.
  simpl.
  reflexivity.
Qed.
```

### Implication Proofs
```coq
Theorem implication_example :
  P -> Q.
Proof.
  intro HP.
  (* prove Q using HP *)
  admit.
Admitted.
```

### Universal Quantification
```coq
Theorem forall_example :
  forall x, P x -> Q x.
Proof.
  intros x HP.
  (* prove Q x using HP *)
  admit.
Admitted.
```

### Existential Quantification
```coq
Theorem exists_example :
  exists x, P x.
Proof.
  exists witness.
  (* prove P witness *)
  admit.
Admitted.
```

### Conjunction Proofs
```coq
Theorem conjunction_example :
  P /\ Q.
Proof.
  split.
  - (* prove P *)
    admit.
  - (* prove Q *)
    admit.
Admitted.
```

### Disjunction Proofs
```coq
Theorem disjunction_example :
  P \/ Q.
Proof.
  left. (* or: right *)
  (* prove P (or Q) *)
  admit.
Admitted.
```

## 4. Induction Patterns

### List Induction
```coq
Theorem list_theorem :
  forall (l : list A), P l.
Proof.
  intros l.
  induction l as [| x xs IHxs].
  - (* Base case: P nil *)
    admit.
  - (* Inductive case: P xs -> P (x :: xs) *)
    (* IHxs : P xs *)
    admit.
Admitted.
```

### Natural Number Induction
```coq
Theorem nat_theorem :
  forall n, P n.
Proof.
  intros n.
  induction n as [| n' IHn'].
  - (* Base case: P 0 *)
    admit.
  - (* Inductive case: P n' -> P (S n') *)
    (* IHn' : P n' *)
    admit.
Admitted.
```

### Strong Induction
```coq
Theorem strong_induction :
  forall n, P n.
Proof.
  intros n.
  induction n as [n IH] using lt_wf_ind.
  (* IH : forall m, m < n -> P m *)
  admit.
Admitted.
```

### Structural Induction (Custom Types)
```coq
Theorem tree_theorem :
  forall (t : tree A), P t.
Proof.
  intros t.
  induction t as [| l IHl x r IHr].
  - (* Base case: P Leaf *)
    admit.
  - (* Inductive case *)
    (* IHl : P l *)
    (* IHr : P r *)
    admit.
Admitted.
```

## 5. Case Analysis Patterns

### Boolean Case Split
```coq
Theorem bool_cases :
  forall b, P b.
Proof.
  intros b.
  destruct b.
  - (* Case: b = true *)
    admit.
  - (* Case: b = false *)
    admit.
Admitted.
```

### Option Case Split
```coq
Theorem option_cases :
  forall (o : option A), P o.
Proof.
  intros o.
  destruct o as [x |].
  - (* Case: o = Some x *)
    admit.
  - (* Case: o = None *)
    admit.
Admitted.
```

### Custom Datatype Cases
```coq
Theorem datatype_cases :
  forall (x : datatype), P x.
Proof.
  intros x.
  destruct x as [| arg1 arg2].
  - (* Constructor1 *)
    admit.
  - (* Constructor2 arg1 arg2 *)
    admit.
Admitted.
```

### Case Analysis with Equations
```coq
Theorem cases_with_eq :
  forall x, P x.
Proof.
  intros x.
  destruct x eqn:Heq.
  - (* Use Heq : x = ... *)
    admit.
  - admit.
Admitted.
```

## Key Proof Strategies

### Forward Reasoning
Build up facts step by step:
```coq
Proof.
  intros.
  assert (H1 : fact1) by tactics.
  assert (H2 : fact2) by tactics.
  (* use H1, H2 to prove goal *)
Qed.
```

### Backward Reasoning
Apply rules to reduce goal:
```coq
Proof.
  intros.
  apply some_theorem.
  - (* subgoal 1 *)
    admit.
  - (* subgoal 2 *)
    admit.
Admitted.
```

### Using Hypotheses
```coq
Proof.
  intros H1 H2.
  apply H1 in H2.
  rewrite H2.
  reflexivity.
Qed.
```

### Proof by Contradiction
```coq
Proof.
  intros.
  destruct (classic P) as [HP | HnotP].
  - (* Case: P *)
    admit.
  - (* Case: ~P *)
    exfalso. (* prove False *)
    admit.
Admitted.
```
