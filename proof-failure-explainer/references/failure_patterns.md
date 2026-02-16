# Proof Failure Patterns Reference

This reference catalogs common proof failure patterns in Isabelle and Coq, their causes, and solutions.

## Table of Contents

1. [Type Errors](#type-errors)
2. [Unification Failures](#unification-failures)
3. [Missing Assumptions](#missing-assumptions)
4. [Incorrect Goals](#incorrect-goals)
5. [Tactic Failures](#tactic-failures)
6. [Scope and Context Issues](#scope-and-context-issues)
7. [Induction Problems](#induction-problems)
8. [Rewriting Issues](#rewriting-issues)

## Type Errors

### Pattern: Type Mismatch

**Isabelle Example:**
```isabelle
lemma "1 + True = 2"
```

**Error:**
```
Type unification failed: Type error in application: incompatible operand type
```

**Explanation:**
- `True` has type `bool`
- `+` expects numeric types
- Cannot add a number and a boolean

**Solution:**
- Ensure all operands have compatible types
- Check type annotations
- Use type coercion if needed

**Coq Example:**
```coq
Lemma bad_types : 1 + true = 2.
```

**Error:**
```
The term "true" has type "bool" while it is expected to have type "nat".
```

**Solution:**
```coq
Lemma correct_types : 1 + 1 = 2.
Proof. reflexivity. Qed.
```

### Pattern: Wrong Function Type

**Coq Example:**
```coq
Definition double (n : nat) : nat := n + n.

Lemma test : double true = 2.
```

**Error:**
```
The term "true" has type "bool" while it is expected to have type "nat".
```

**Explanation:**
- `double` expects `nat` argument
- Provided `bool` instead

**Solution:**
- Check function signature
- Provide correct argument type

## Unification Failures

### Pattern: Cannot Unify Terms

**Isabelle Example:**
```isabelle
lemma "x + y = y + z"
  by simp
```

**Error:**
```
Failed to apply initial proof method
```

**Explanation:**
- Goal requires `x = z` to be true
- No such assumption exists
- Simplification cannot prove arbitrary equality

**Solution:**
- Add necessary assumptions: `assumes "x = z"`
- Or prove the relationship first

**Coq Example:**
```coq
Lemma unify_fail : forall x y z : nat, x + y = y + z.
Proof.
  intros. reflexivity.
Qed.
```

**Error:**
```
Unable to unify "x + y" with "y + z".
```

**Explanation:**
- `reflexivity` requires both sides to be syntactically equal
- `x + y` and `y + z` are not equal without knowing `x = z`

**Solution:**
```coq
Lemma unify_correct : forall x y : nat, x + y = y + x.
Proof.
  intros. lia.  (* or use commutativity *)
Qed.
```

### Pattern: Existential Variable Issues

**Coq Example:**
```coq
Lemma exists_problem : exists n : nat, n + 1 = 5.
Proof.
  exists ?n.
  reflexivity.
Qed.
```

**Error:**
```
Unable to unify "?n + 1" with "5".
```

**Explanation:**
- Existential variable `?n` not instantiated
- Coq cannot solve for `?n` automatically

**Solution:**
```coq
Lemma exists_correct : exists n : nat, n + 1 = 5.
Proof.
  exists 4.
  reflexivity.
Qed.
```

## Missing Assumptions

### Pattern: Unprovable Without Hypothesis

**Isabelle Example:**
```isabelle
lemma "x > 0 ⟹ x + y > y"
  by simp
```

**Error:**
```
Failed to apply initial proof method
```

**Explanation:**
- For integers, this requires `x > 0`
- Assumption is stated but simplification alone insufficient
- Need arithmetic reasoning

**Solution:**
```isabelle
lemma "x > (0::int) ⟹ x + y > y"
  by arith
```

**Coq Example:**
```coq
Lemma missing_hyp : forall n : nat, n > 0 -> n + 1 > 1.
Proof.
  intros. reflexivity.
Qed.
```

**Error:**
```
Unable to unify "n + 1" with "1".
```

**Explanation:**
- Need to use the hypothesis `n > 0`
- `reflexivity` doesn't use hypotheses

**Solution:**
```coq
Lemma with_hyp : forall n : nat, n > 0 -> n + 1 > 1.
Proof.
  intros. lia.
Qed.
```

### Pattern: Missing Precondition

**Coq Example:**
```coq
Lemma div_example : forall n m : nat, n / m * m = n.
```

**Error:**
```
(After attempting proof) Fails for m = 0
```

**Explanation:**
- Division by zero is undefined
- Need precondition `m <> 0`

**Solution:**
```coq
Lemma div_correct : forall n m : nat, m <> 0 -> n / m * m <= n.
Proof.
  intros. (* proof here *)
Admitted.
```

## Incorrect Goals

### Pattern: Goal Too Strong

**Isabelle Example:**
```isabelle
lemma list_append: "xs @ ys = ys @ xs"
```

**Error:**
```
Failed to apply initial proof method
```

**Explanation:**
- List append is not commutative
- Goal is false in general
- Only true when `xs = ys` or one is empty

**Solution:**
```isabelle
lemma list_append_assoc: "(xs @ ys) @ zs = xs @ (ys @ zs)"
  by simp
```

**Coq Example:**
```coq
Lemma too_strong : forall n m : nat, n + m = m + n + 1.
```

**Explanation:**
- Goal claims `n + m = m + n + 1`
- This is false (off by 1)
- Should be `n + m = m + n`

**Solution:**
```coq
Lemma correct_goal : forall n m : nat, n + m = m + n.
Proof.
  intros. lia.
Qed.
```

### Pattern: Wrong Quantifier Order

**Coq Example:**
```coq
Lemma wrong_order : (exists x : nat, forall y : nat, x > y).
```

**Explanation:**
- Claims there exists an `x` greater than all `y`
- This is false for natural numbers
- Should be: `forall y, exists x, x > y`

**Solution:**
```coq
Lemma correct_order : forall y : nat, exists x : nat, x > y.
Proof.
  intros. exists (S y). lia.
Qed.
```

## Tactic Failures

### Pattern: Tactic Not Applicable

**Isabelle Example:**
```isabelle
lemma "P ∨ Q"
  by (rule conjI)
```

**Error:**
```
Failed to apply rule
```

**Explanation:**
- `conjI` is for conjunction (`∧`)
- Goal is disjunction (`∨`)
- Wrong introduction rule

**Solution:**
```isabelle
lemma "P ⟹ P ∨ Q"
  by (rule disjI1)
```

**Coq Example:**
```coq
Lemma tactic_fail : forall P Q : Prop, P -> P \/ Q.
Proof.
  intros. split.
Qed.
```

**Error:**
```
Unable to unify "?P /\ ?Q" with "P \/ Q".
```

**Explanation:**
- `split` is for conjunction (`/\`)
- Goal is disjunction (`\/`)

**Solution:**
```coq
Lemma tactic_correct : forall P Q : Prop, P -> P \/ Q.
Proof.
  intros. left. assumption.
Qed.
```

### Pattern: Induction Hypothesis Too Weak

**Coq Example:**
```coq
Fixpoint sum (n : nat) : nat :=
  match n with
  | 0 => 0
  | S n' => n + sum n'
  end.

Lemma sum_formula : forall n : nat, 2 * sum n = n * (n + 1).
Proof.
  induction n.
  - reflexivity.
  - simpl. (* Gets stuck *)
Admitted.
```

**Explanation:**
- Induction hypothesis not strong enough
- Need to strengthen or generalize

**Solution:**
```coq
(* Use better induction or strengthen hypothesis *)
Lemma sum_formula : forall n : nat, 2 * sum n = n * (n + 1).
Proof.
  induction n.
  - reflexivity.
  - simpl. rewrite IHn. lia.
Qed.
```

## Scope and Context Issues

### Pattern: Variable Not in Scope

**Coq Example:**
```coq
Lemma scope_issue : forall x : nat, x + y = y + x.
```

**Error:**
```
The reference y was not found in the current environment.
```

**Explanation:**
- Variable `y` not quantified
- Not in scope

**Solution:**
```coq
Lemma scope_correct : forall x y : nat, x + y = y + x.
Proof.
  intros. lia.
Qed.
```

### Pattern: Shadowed Variable

**Isabelle Example:**
```isabelle
lemma "⋀x. (⋀x. P x) ⟹ P x"
```

**Explanation:**
- Inner `x` shadows outer `x`
- May cause confusion
- Both refer to different variables

**Solution:**
- Use distinct variable names
- Be careful with nested quantifiers

## Induction Problems

### Pattern: Wrong Induction Variable

**Coq Example:**
```coq
Lemma app_length : forall (A : Type) (l1 l2 : list A),
  length (l1 ++ l2) = length l1 + length l2.
Proof.
  intros. induction l2.
```

**Explanation:**
- Should induct on `l1`, not `l2`
- Append is defined recursively on first argument

**Solution:**
```coq
Lemma app_length : forall (A : Type) (l1 l2 : list A),
  length (l1 ++ l2) = length l1 + length l2.
Proof.
  intros. induction l1.
  - reflexivity.
  - simpl. rewrite IHl1. reflexivity.
Qed.
```

### Pattern: Need to Generalize First

**Coq Example:**
```coq
Lemma rev_length : forall (A : Type) (l : list A),
  length (rev l) = length l.
Proof.
  intros. induction l.
  - reflexivity.
  - simpl. (* Gets stuck - need to generalize *)
Admitted.
```

**Explanation:**
- Induction hypothesis not general enough
- Need to generalize before induction

**Solution:**
```coq
(* May need helper lemma or generalization *)
Lemma rev_length : forall (A : Type) (l : list A),
  length (rev l) = length l.
Proof.
  intros. induction l.
  - reflexivity.
  - simpl. rewrite app_length. simpl. rewrite IHl. lia.
Qed.
```

## Rewriting Issues

### Pattern: Cannot Rewrite Under Binder

**Coq Example:**
```coq
Lemma rewrite_binder : forall f g : nat -> nat,
  (forall x, f x = g x) -> (fun x => f x) = (fun x => g x).
Proof.
  intros. rewrite H.
Qed.
```

**Error:**
```
Found no subterm matching "f ?M" in the current goal.
```

**Explanation:**
- Cannot directly rewrite under lambda
- Need functional extensionality

**Solution:**
```coq
Require Import FunctionalExtensionality.

Lemma rewrite_binder : forall f g : nat -> nat,
  (forall x, f x = g x) -> (fun x => f x) = (fun x => g x).
Proof.
  intros. apply functional_extensionality. intro. apply H.
Qed.
```

### Pattern: Rewrite Direction Wrong

**Coq Example:**
```coq
Lemma rewrite_dir : forall n m : nat, n = m -> m + 1 = n + 1.
Proof.
  intros. rewrite H. reflexivity.
Qed.
```

**Works, but if we had:**
```coq
Lemma rewrite_dir2 : forall n m : nat, n = m -> n + 1 = m + 1.
Proof.
  intros. rewrite <- H. reflexivity.
Qed.
```

**Explanation:**
- `rewrite H` replaces `n` with `m`
- `rewrite <- H` replaces `m` with `n`
- Direction matters

## Common Error Messages

### Isabelle

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| "Type unification failed" | Type mismatch | Check types of all terms |
| "Failed to apply initial proof method" | Tactic not applicable or goal unprovable | Try different tactic or check goal |
| "No unifiers" | Terms cannot be unified | Check if goal is correct |
| "Illegal schematic variable" | Variable scope issue | Check quantifiers |

### Coq

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| "Unable to unify" | Terms don't match | Check goal statement or use different tactic |
| "The term ... has type ... while it is expected to have type ..." | Type error | Fix type annotations |
| "The reference ... was not found" | Variable not in scope | Add quantifier or definition |
| "Tactic failure" | Tactic not applicable | Try different tactic |
| "No applicable tactic" | Goal structure doesn't match tactic | Check goal and use appropriate tactic |

## Debugging Strategies

### For Isabelle

1. **Check types:** Use `term "expression"` to check types
2. **Simplify goal:** Use `apply simp` to see simplified form
3. **Check assumptions:** Use `using assms` to see available facts
4. **Try auto:** Use `try auto` or `try fastforce` to see if goal is trivial
5. **Use sledgehammer:** Let automated tools find proof

### For Coq

1. **Check types:** Use `Check term` to see type
2. **Inspect goal:** Use `Show Proof` to see proof term
3. **Print context:** Use `Show` to see current goal and hypotheses
4. **Simplify:** Use `simpl` or `compute` to evaluate
5. **Search:** Use `Search pattern` to find relevant lemmas
6. **Use automation:** Try `auto`, `lia`, `omega`, or `intuition`
