# Coq Tactics Reference

Comprehensive reference for Coq tactics organized by proof situation.

## Table of Contents
- [Structural Tactics](#structural-tactics)
- [Simplification](#simplification)
- [Induction and Cases](#induction-and-cases)
- [Rewriting](#rewriting)
- [Automation](#automation)
- [Logical Reasoning](#logical-reasoning)
- [Arithmetic](#arithmetic)

## Structural Tactics

### `intro` / `intros`
Introduce variables or hypotheses.
```coq
intro x.
intros x y H.
intros.  (* introduce all *)
```

### `apply <term>`
Apply a theorem or hypothesis.
```coq
apply H.
apply plus_comm.
apply IHn.
```

### `exact <term>`
Provide exact proof term.
```coq
exact H.
```

### `assumption`
Solve goal with an existing hypothesis.
```coq
assumption.
```

### `assert (<name>: <prop>)`
Prove intermediate lemma.
```coq
assert (H: n + 0 = n).
{ reflexivity. }
```

### `pose proof <term> as <name>`
Add a fact to context.
```coq
pose proof (plus_comm n m) as H.
```

## Simplification

### `simpl`
Simplify by computation.
```coq
simpl.
simpl in H.
simpl in *.
```

### `unfold <def>`
Unfold a definition.
```coq
unfold my_func.
unfold my_func in H.
```

### `fold <def>`
Fold a definition (reverse of unfold).
```coq
fold my_func.
```

### `cbv` / `lazy` / `compute`
Reduction strategies.
```coq
cbv.      (* call-by-value *)
lazy.     (* lazy evaluation *)
compute.  (* full computation *)
```

### `cbn`
Call-by-name normalization (recommended over simpl).
```coq
cbn.
cbn in H.
```

## Induction and Cases

### `induction <var>`
Proof by induction.
```coq
induction n.
- (* Base case: n = 0 *)
  reflexivity.
- (* Inductive case: n = S n' *)
  (* IHn: induction hypothesis *)
  simpl. rewrite IHn. reflexivity.
```

**Variants:**
- `induction n as [|n' IH]` - Name the induction hypothesis
- `induction n using custom_ind` - Use custom induction principle

### `destruct <var>`
Case analysis.
```coq
destruct n.
- (* Case: n = 0 *)
  reflexivity.
- (* Case: n = S n' *)
  simpl. reflexivity.
```

**Variants:**
- `destruct n as [|n']` - Name the cases
- `destruct n eqn:E` - Remember the equation
- `destruct H` - Destruct a hypothesis

### `case <var>`
Similar to destruct but less aggressive.
```coq
case n.
```

### `elim <var>`
Apply elimination principle.
```coq
elim n.
```

## Rewriting

### `rewrite <term>`
Rewrite using an equation (left-to-right).
```coq
rewrite H.
rewrite plus_comm.
rewrite <- H.  (* right-to-left *)
```

**Variants:**
- `rewrite H in H2` - Rewrite in hypothesis
- `rewrite H in *` - Rewrite everywhere
- `rewrite H1, H2, H3` - Multiple rewrites

### `replace <term1> with <term2>`
Replace one term with another.
```coq
replace (n + 0) with n.
- (* Prove n + 0 = n *)
  apply plus_n_O.
- (* Continue with n *)
```

### `subst`
Substitute all equations of form `x = t`.
```coq
subst.
subst x.
```

### `reflexivity`
Prove equality by computation.
```coq
reflexivity.
```

### `symmetry`
Swap sides of equality.
```coq
symmetry.
symmetry in H.
```

### `transitivity <term>`
Prove equality by transitivity.
```coq
transitivity (n + m).
```

## Automation

### `auto`
Automatic proof search.
```coq
auto.
auto with arith.
auto with *.
```

### `trivial`
Solve trivial goals.
```coq
trivial.
```

### `easy`
Combination of trivial tactics.
```coq
easy.
```

### `tauto`
Propositional tautology solver.
```coq
tauto.
```

### `intuition`
Propositional reasoning with simplification.
```coq
intuition.
intuition auto.
```

### `firstorder`
First-order reasoning.
```coq
firstorder.
```

### `congruence`
Equality reasoning with congruence closure.
```coq
congruence.
```

### `lia`
Linear integer arithmetic (requires `Require Import Lia`).
```coq
lia.
```

### `nia`
Non-linear integer arithmetic.
```coq
nia.
```

## Logical Reasoning

### `split`
Split conjunction or biconditional.
```coq
split.
- (* Prove left part *)
- (* Prove right part *)
```

### `left` / `right`
Choose disjunction branch.
```coq
left.   (* Prove P in P \/ Q *)
right.  (* Prove Q in P \/ Q *)
```

### `exists <term>`
Provide witness for existential.
```coq
exists 42.
exists (n + m).
```

### `constructor`
Apply a constructor of an inductive type.
```coq
constructor.
constructor 2.  (* Apply second constructor *)
```

### `discriminate`
Derive contradiction from impossible equality.
```coq
discriminate.
discriminate H.
```

### `injection`
Extract equalities from constructor equality.
```coq
injection H.
injection H as H1 H2.
```

### `inversion <hyp>`
Invert an inductive predicate.
```coq
inversion H.
inversion H as [x y H1 H2].
inversion H; subst.
```

### `contradiction`
Derive contradiction.
```coq
contradiction.
```

### `exfalso`
Prove anything from False.
```coq
exfalso.
```

## Arithmetic

### `lia`
Linear integer arithmetic (Require Import Lia).
```coq
lia.
```

### `nia`
Non-linear integer arithmetic (Require Import Lia).
```coq
nia.
```

### `ring`
Ring solver (Require Import Ring).
```coq
ring.
```

### `field`
Field solver (Require Import Field).
```coq
field.
```

### `omega`
Deprecated (use lia instead).
```coq
omega.
```

## Common Proof Patterns

### Pattern: Conjunction
**Goal**: `P /\ Q`
```coq
split.
- (* Prove P *)
- (* Prove Q *)
```

### Pattern: Implication
**Goal**: `P -> Q`
```coq
intro H.
(* Now have H: P, prove Q *)
```

### Pattern: Universal Quantification
**Goal**: `forall x, P x`
```coq
intro x.
(* Now prove P x for arbitrary x *)
```

### Pattern: Existential Quantification
**Goal**: `exists x, P x`
```coq
exists witness.
(* Now prove P witness *)
```

### Pattern: Disjunction
**Goal**: `P \/ Q`
```coq
left.   (* Choose to prove P *)
(* or *)
right.  (* Choose to prove Q *)
```

### Pattern: Negation
**Goal**: `~ P`
```coq
intro H.
(* Now have H: P, derive contradiction *)
```

### Pattern: List Induction
**Goal**: `forall l, P l`
```coq
intro l.
induction l as [|x l' IHl'].
- (* Base case: l = [] *)
  simpl. reflexivity.
- (* Inductive case: l = x :: l' *)
  (* IHl': P l' *)
  simpl. rewrite IHl'. reflexivity.
```

### Pattern: Natural Number Induction
**Goal**: `forall n, P n`
```coq
intro n.
induction n as [|n' IHn'].
- (* Base case: n = 0 *)
  reflexivity.
- (* Inductive case: n = S n' *)
  (* IHn': P n' *)
  simpl. rewrite IHn'. reflexivity.
```

### Pattern: Case Analysis on Option
**Goal**: `forall o, P o`
```coq
intro o.
destruct o as [x|].
- (* Case: o = Some x *)
  simpl. reflexivity.
- (* Case: o = None *)
  simpl. reflexivity.
```

### Pattern: Boolean Case Analysis
**Goal**: `forall b, P b`
```coq
intro b.
destruct b.
- (* Case: b = true *)
  reflexivity.
- (* Case: b = false *)
  reflexivity.
```

## Tactic Combinators

### `;` (semicolon)
Apply second tactic to all subgoals from first.
```coq
split; reflexivity.
induction n; simpl; auto.
```

### `try <tactic>`
Try tactic, don't fail if it doesn't work.
```coq
try reflexivity.
```

### `repeat <tactic>`
Repeat tactic until it fails.
```coq
repeat rewrite H.
```

### `<tactic1> || <tactic2>`
Try first tactic, if fails try second.
```coq
reflexivity || auto.
```

### `<tactic>; [<tac1> | <tac2> | ...]`
Apply different tactics to different subgoals.
```coq
split; [auto | reflexivity].
```

## Advanced Tactics

### `generalize dependent <var>`
Generalize a variable and its dependencies.
```coq
generalize dependent n.
```

### `remember <term> as <name>`
Remember a complex term.
```coq
remember (n + m) as k.
```

### `clear <hyp>`
Remove hypothesis from context.
```coq
clear H.
clear H1 H2.
```

### `revert <var>`
Move variable back to goal (opposite of intro).
```coq
revert n.
```

### `specialize (<hyp> <args>)`
Specialize a hypothesis with arguments.
```coq
specialize (H n).
```

### `f_equal`
Prove equality by proving arguments equal.
```coq
f_equal.
```

### `eapply <term>`
Apply with existential variables.
```coq
eapply H.
```

### `eauto`
Auto with existential variables.
```coq
eauto.
```
