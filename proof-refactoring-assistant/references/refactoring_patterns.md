# Proof Refactoring Patterns Reference

This reference catalogs common refactoring patterns for Isabelle and Coq proofs to improve readability, modularity, and maintainability.

## Table of Contents

1. [Extract Helper Lemma](#extract-helper-lemma)
2. [Inline Trivial Lemma](#inline-trivial-lemma)
3. [Break Down Long Proof](#break-down-long-proof)
4. [Extract Common Pattern](#extract-common-pattern)
5. [Simplify Proof Structure](#simplify-proof-structure)
6. [Improve Naming](#improve-naming)
7. [Add Documentation](#add-documentation)
8. [Strengthen Induction Hypothesis](#strengthen-induction-hypothesis)
9. [Generalize Lemma](#generalize-lemma)
10. [Replace Manual Proof with Automation](#replace-manual-proof-with-automation)

## Extract Helper Lemma

**When to apply:** Long proof with repeated reasoning or complex subgoal

**Before (Coq):**
```coq
Lemma complex_theorem : forall n m : nat,
  n > 0 -> m > 0 -> n + m > 0 /\ n * m > 0.
Proof.
  intros n m Hn Hm.
  split.
  - (* Prove n + m > 0 *)
    destruct n.
    + inversion Hn.
    + destruct m.
      * inversion Hm.
      * simpl. lia.
  - (* Prove n * m > 0 *)
    destruct n.
    + inversion Hn.
    + destruct m.
      * inversion Hm.
      * simpl. apply Nat.mul_pos_pos; lia.
Qed.
```

**After (Coq):**
```coq
Lemma add_pos : forall n m : nat,
  n > 0 -> m > 0 -> n + m > 0.
Proof.
  intros. lia.
Qed.

Lemma mul_pos : forall n m : nat,
  n > 0 -> m > 0 -> n * m > 0.
Proof.
  intros. apply Nat.mul_pos_pos; lia.
Qed.

Lemma complex_theorem : forall n m : nat,
  n > 0 -> m > 0 -> n + m > 0 /\ n * m > 0.
Proof.
  intros. split.
  - apply add_pos; assumption.
  - apply mul_pos; assumption.
Qed.
```

**Benefits:**
- Reusable helper lemmas
- Clearer proof structure
- Easier to understand and maintain

**Before (Isabelle):**
```isabelle
lemma complex_list: "length (xs @ ys) = length xs + length ys ∧
                      length (rev xs) = length xs"
proof -
  have "length (xs @ ys) = length xs + length ys"
    by (induction xs) auto
  moreover have "length (rev xs) = length xs"
    by (induction xs) auto
  ultimately show ?thesis by simp
qed
```

**After (Isabelle):**
```isabelle
lemma append_length: "length (xs @ ys) = length xs + length ys"
  by (induction xs) auto

lemma rev_length: "length (rev xs) = length xs"
  by (induction xs) auto

lemma complex_list: "length (xs @ ys) = length xs + length ys ∧
                      length (rev xs) = length xs"
  using append_length rev_length by simp
```

## Inline Trivial Lemma

**When to apply:** Helper lemma used only once and proof is trivial

**Before (Coq):**
```coq
Lemma helper : forall n : nat, n + 0 = n.
Proof.
  intros. lia.
Qed.

Lemma main : forall n m : nat, n + 0 + m = n + m.
Proof.
  intros. rewrite helper. reflexivity.
Qed.
```

**After (Coq):**
```coq
Lemma main : forall n m : nat, n + 0 + m = n + m.
Proof.
  intros. lia.
Qed.
```

**Benefits:**
- Reduces clutter
- Fewer lemmas to maintain
- Clearer when proof is simple

## Break Down Long Proof

**When to apply:** Proof has many cases or complex nested structure

**Before (Coq):**
```coq
Lemma long_proof : forall n : nat,
  match n with
  | 0 => True
  | S n' => match n' with
            | 0 => True
            | S n'' => n'' < n
            end
  end.
Proof.
  intros. destruct n.
  - simpl. trivial.
  - destruct n.
    + simpl. trivial.
    + simpl. lia.
Qed.
```

**After (Coq):**
```coq
Lemma case_zero :
  match 0 with
  | 0 => True
  | S n' => match n' with
            | 0 => True
            | S n'' => n'' < 0
            end
  end.
Proof.
  simpl. trivial.
Qed.

Lemma case_one :
  match 1 with
  | 0 => True
  | S n' => match n' with
            | 0 => True
            | S n'' => n'' < 1
            end
  end.
Proof.
  simpl. trivial.
Qed.

Lemma case_succ_succ : forall n : nat,
  match S (S n) with
  | 0 => True
  | S n' => match n' with
            | 0 => True
            | S n'' => n'' < S (S n)
            end
  end.
Proof.
  intros. simpl. lia.
Qed.

Lemma long_proof : forall n : nat,
  match n with
  | 0 => True
  | S n' => match n' with
            | 0 => True
            | S n'' => n'' < n
            end
  end.
Proof.
  intros. destruct n.
  - apply case_zero.
  - destruct n.
    + apply case_one.
    + apply case_succ_succ.
Qed.
```

## Extract Common Pattern

**When to apply:** Same proof pattern repeated multiple times

**Before (Isabelle):**
```isabelle
lemma prop1: "P x ⟹ Q x ⟹ R x"
  by (cases x) auto

lemma prop2: "P y ⟹ Q y ⟹ R y"
  by (cases y) auto

lemma prop3: "P z ⟹ Q z ⟹ R z"
  by (cases z) auto
```

**After (Isabelle):**
```isabelle
lemma general_pattern: "⋀x. P x ⟹ Q x ⟹ R x"
  by (cases x) auto

lemma prop1: "P x ⟹ Q x ⟹ R x"
  by (rule general_pattern)

lemma prop2: "P y ⟹ Q y ⟹ R y"
  by (rule general_pattern)

lemma prop3: "P z ⟹ Q z ⟹ R z"
  by (rule general_pattern)
```

**Before (Coq):**
```coq
Lemma list1_not_nil : forall (A : Type) (x : A) (xs : list A),
  x :: xs <> [].
Proof.
  intros. discriminate.
Qed.

Lemma list2_not_nil : forall (A : Type) (x y : A) (xs : list A),
  x :: y :: xs <> [].
Proof.
  intros. discriminate.
Qed.
```

**After (Coq):**
```coq
Lemma cons_not_nil : forall (A : Type) (x : A) (xs : list A),
  x :: xs <> [].
Proof.
  intros. discriminate.
Qed.

Lemma list2_not_nil : forall (A : Type) (x y : A) (xs : list A),
  x :: y :: xs <> [].
Proof.
  intros. apply cons_not_nil.
Qed.
```

## Simplify Proof Structure

**When to apply:** Proof uses complex tactics when simpler ones suffice

**Before (Coq):**
```coq
Lemma add_comm : forall n m : nat, n + m = m + n.
Proof.
  intros n m.
  induction n.
  - simpl. rewrite <- plus_n_O. reflexivity.
  - simpl. rewrite IHn. rewrite <- plus_n_Sm. reflexivity.
Qed.
```

**After (Coq):**
```coq
Lemma add_comm : forall n m : nat, n + m = m + n.
Proof.
  intros. lia.
Qed.
```

**Before (Isabelle):**
```isabelle
lemma simple: "x + 0 = x"
proof (induction x)
  case 0
  then show ?case by simp
next
  case (Suc x)
  then show ?case by simp
qed
```

**After (Isabelle):**
```isabelle
lemma simple: "x + 0 = x"
  by simp
```

## Improve Naming

**When to apply:** Names are unclear or don't follow conventions

**Before (Coq):**
```coq
Lemma l1 : forall n : nat, n + 0 = n.
Proof. intros. lia. Qed.

Lemma l2 : forall n m : nat, n + m = m + n.
Proof. intros. lia. Qed.

Lemma thm : forall n m : nat, n + 0 + m = m + n.
Proof.
  intros. rewrite l1. apply l2.
Qed.
```

**After (Coq):**
```coq
Lemma add_zero_r : forall n : nat, n + 0 = n.
Proof. intros. lia. Qed.

Lemma add_comm : forall n m : nat, n + m = m + n.
Proof. intros. lia. Qed.

Lemma add_zero_comm : forall n m : nat, n + 0 + m = m + n.
Proof.
  intros. rewrite add_zero_r. apply add_comm.
Qed.
```

**Naming conventions:**
- Use descriptive names that indicate what the lemma proves
- Follow project/library naming patterns
- Use suffixes like `_comm`, `_assoc`, `_zero`, `_one` for common properties
- Avoid generic names like `lemma1`, `helper`, `aux`

## Add Documentation

**When to apply:** Complex lemmas lack explanation

**Before (Coq):**
```coq
Lemma partition_spec : forall (A : Type) (f : A -> bool) (l : list A),
  let (l1, l2) := partition f l in
  filter f l = l1 /\ filter (fun x => negb (f x)) l = l2.
Proof.
  (* 20 lines of proof *)
Admitted.
```

**After (Coq):**
```coq
(** Specification of list partition function.

    Given a predicate f and a list l, partition splits l into two lists:
    - l1 contains all elements satisfying f
    - l2 contains all elements not satisfying f

    This lemma proves that partition is equivalent to filtering twice.
*)
Lemma partition_spec : forall (A : Type) (f : A -> bool) (l : list A),
  let (l1, l2) := partition f l in
  filter f l = l1 /\ filter (fun x => negb (f x)) l = l2.
Proof.
  (* 20 lines of proof *)
Admitted.
```

**Before (Isabelle):**
```isabelle
lemma fold_append: "fold f (xs @ ys) a = fold f ys (fold f xs a)"
  by (induction xs arbitrary: a) auto
```

**After (Isabelle):**
```isabelle
text ‹
  Folding over an appended list is equivalent to folding over the first list,
  then using that result as the accumulator for folding over the second list.
  This is a fundamental property for reasoning about fold operations.
›

lemma fold_append: "fold f (xs @ ys) a = fold f ys (fold f xs a)"
  by (induction xs arbitrary: a) auto
```

## Strengthen Induction Hypothesis

**When to apply:** Induction gets stuck due to weak hypothesis

**Before (Coq):**
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
  - simpl. (* Gets stuck - IH not strong enough *)
Admitted.
```

**After (Coq):**
```coq
(* Strengthen by generalizing *)
Lemma sum_formula_gen : forall n acc : nat,
  2 * (sum n + acc) = n * (n + 1) + 2 * acc.
Proof.
  induction n; intros.
  - simpl. lia.
  - simpl. rewrite IHn. lia.
Qed.

Lemma sum_formula : forall n : nat, 2 * sum n = n * (n + 1).
Proof.
  intros. pose proof (sum_formula_gen n 0). lia.
Qed.
```

## Generalize Lemma

**When to apply:** Lemma is too specific, making it less reusable

**Before (Isabelle):**
```isabelle
lemma map_double_list: "map (λx. 2 * x) [1, 2, 3] = [2, 4, 6]"
  by simp
```

**After (Isabelle):**
```isabelle
lemma map_double: "map (λx. 2 * x) xs = map ((*) 2) xs"
  by simp

lemma map_double_list: "map (λx. 2 * x) [1, 2, 3] = [2, 4, 6]"
  by simp
```

**Before (Coq):**
```coq
Lemma rev_three : forall (A : Type) (x y z : A),
  rev [x; y; z] = [z; y; x].
Proof.
  intros. simpl. reflexivity.
Qed.
```

**After (Coq):**
```coq
Lemma rev_involutive : forall (A : Type) (l : list A),
  rev (rev l) = l.
Proof.
  intros. induction l; simpl; auto.
  rewrite rev_app_distr. simpl. rewrite IHl. reflexivity.
Qed.

(* Original lemma becomes trivial *)
Lemma rev_three : forall (A : Type) (x y z : A),
  rev [x; y; z] = [z; y; x].
Proof.
  intros. reflexivity.
Qed.
```

## Replace Manual Proof with Automation

**When to apply:** Proof is tedious but automatable

**Before (Coq):**
```coq
Lemma arithmetic : forall n m : nat,
  n + m + n = 2 * n + m.
Proof.
  intros n m.
  rewrite <- plus_assoc.
  rewrite (plus_comm m n).
  rewrite plus_assoc.
  rewrite <- mult_n_Sm.
  rewrite <- mult_n_O.
  rewrite plus_comm.
  reflexivity.
Qed.
```

**After (Coq):**
```coq
Lemma arithmetic : forall n m : nat,
  n + m + n = 2 * n + m.
Proof.
  intros. lia.
Qed.
```

**Before (Isabelle):**
```isabelle
lemma list_props: "length (xs @ ys) = length xs + length ys ∧
                    length (rev xs) = length xs"
proof
  show "length (xs @ ys) = length xs + length ys"
  proof (induction xs)
    case Nil
    then show ?case by simp
  next
    case (Cons a xs)
    then show ?case by simp
  qed
next
  show "length (rev xs) = length xs"
  proof (induction xs)
    case Nil
    then show ?case by simp
  next
    case (Cons a xs)
    then show ?case by simp
  qed
qed
```

**After (Isabelle):**
```isabelle
lemma list_props: "length (xs @ ys) = length xs + length ys ∧
                    length (rev xs) = length xs"
  by (induction xs) auto
```

## Refactoring Anti-Patterns

### Anti-Pattern 1: Over-Extraction

**Problem:** Creating too many tiny lemmas

**Bad:**
```coq
Lemma one_plus_zero : 1 + 0 = 1.
Proof. reflexivity. Qed.

Lemma two_plus_zero : 2 + 0 = 2.
Proof. reflexivity. Qed.

Lemma three_plus_zero : 3 + 0 = 3.
Proof. reflexivity. Qed.
```

**Good:**
```coq
(* Use general lemma from standard library *)
(* Or prove once: forall n, n + 0 = n *)
```

### Anti-Pattern 2: Premature Generalization

**Problem:** Generalizing before understanding the specific case

**Bad:**
```coq
(* Trying to prove general case without understanding specifics *)
Lemma general_complex : forall (A B : Type) (f : A -> B) (g : B -> A) ...,
  (* Very complex statement *)
```

**Good:**
```coq
(* Start with specific case *)
Lemma specific_case : forall (f : nat -> nat), ...

(* Then generalize once understood *)
Lemma general_case : forall (A B : Type) (f : A -> B), ...
```

### Anti-Pattern 3: Inconsistent Naming

**Problem:** No naming convention

**Bad:**
```coq
Lemma thm1 : ...
Lemma helper_for_main : ...
Lemma IMPORTANT : ...
Lemma aux_lemma_2 : ...
```

**Good:**
```coq
Lemma list_append_assoc : ...
Lemma list_append_nil_r : ...
Lemma list_rev_involutive : ...
Lemma list_length_append : ...
```

## Refactoring Checklist

Before refactoring:
- [ ] Understand the proof completely
- [ ] Identify code smells (long proofs, repeated patterns, unclear names)
- [ ] Check if lemmas are reusable elsewhere
- [ ] Verify all proofs still work after changes

During refactoring:
- [ ] Extract helper lemmas for complex subgoals
- [ ] Simplify proof tactics where possible
- [ ] Improve naming for clarity
- [ ] Add documentation for complex lemmas
- [ ] Remove unused lemmas
- [ ] Generalize overly specific lemmas

After refactoring:
- [ ] Verify all proofs still compile
- [ ] Check proof performance (some refactorings may slow down compilation)
- [ ] Update related documentation
- [ ] Review with team if applicable

## Common Refactoring Scenarios

### Scenario 1: Inherited Legacy Proof

**Characteristics:**
- Long, monolithic proofs
- No helper lemmas
- Poor naming
- No documentation

**Refactoring strategy:**
1. Add documentation first
2. Identify natural break points
3. Extract helper lemmas
4. Improve naming
5. Simplify tactics

### Scenario 2: Quick Prototype Proof

**Characteristics:**
- Works but messy
- Uses sledgehammer/automation heavily
- No structure

**Refactoring strategy:**
1. Understand what automation does
2. Make proof more explicit if needed for maintainability
3. Extract reusable parts
4. Add documentation

### Scenario 3: Duplicated Proofs

**Characteristics:**
- Same pattern repeated
- Copy-paste code
- Minor variations

**Refactoring strategy:**
1. Identify common pattern
2. Extract general lemma
3. Specialize for each case
4. Remove duplication

## Tools and Techniques

### Isabelle

- `sledgehammer` - Find proof automatically
- `try` - Try multiple tactics
- `proof (induction ...)` vs `by (induction ...)` - Choose appropriate proof style
- `moreover`/`ultimately` - Structure complex proofs
- `have`/`obtain` - Introduce intermediate facts

### Coq

- `lia`/`nia` - Arithmetic automation
- `auto`/`eauto` - Proof search
- `intuition` - Propositional logic
- `congruence` - Equality reasoning
- `firstorder` - First-order logic
- `assert` - Introduce intermediate lemmas
- `enough` - Backward reasoning
