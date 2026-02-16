---
name: proof-refactoring-assistant
description: Restructure and improve Isabelle or Coq proofs to enhance readability, modularity, and maintainability without changing semantics. Use when proofs are long and monolithic, have repeated patterns, use unclear naming, lack documentation, or when the user asks to refactor, clean up, improve, or reorganize their formal proofs.
---

# Proof Refactoring Assistant

## Overview

Improve proof quality by restructuring Isabelle and Coq proofs for better readability, modularity, and maintainability while preserving semantics. This skill applies proven refactoring patterns to make proofs easier to understand and maintain.

## Refactoring Workflow

### Step 1: Analyze Current Proof

Identify code smells and improvement opportunities:

1. **Structure issues:**
   - Long, monolithic proofs (>20 lines)
   - Deep nesting of proof steps
   - Repeated proof patterns
   - Complex case analysis

2. **Naming issues:**
   - Generic names (lemma1, helper, aux)
   - Inconsistent naming conventions
   - Names don't describe what lemma proves

3. **Documentation issues:**
   - Missing comments
   - No explanation of complex steps
   - Unclear proof strategy

4. **Modularity issues:**
   - No helper lemmas
   - Duplicated reasoning
   - Overly specific lemmas

5. **Complexity issues:**
   - Manual proofs when automation available
   - Weak induction hypotheses
   - Unnecessarily complex tactics

### Step 2: Identify Refactoring Opportunities

Choose appropriate refactoring patterns:

**Extract Helper Lemma:**
- Long proof with complex subgoals
- Repeated reasoning
- Reusable intermediate results

**Inline Trivial Lemma:**
- Helper used only once
- Proof is trivial
- Adds unnecessary indirection

**Break Down Long Proof:**
- Many cases to handle
- Complex nested structure
- Hard to follow logic

**Extract Common Pattern:**
- Same proof repeated
- Similar lemmas with minor variations
- Opportunity for generalization

**Simplify Proof Structure:**
- Complex tactics when simpler ones work
- Manual steps that automation handles
- Unnecessary proof verbosity

**Improve Naming:**
- Unclear or generic names
- Inconsistent conventions
- Names don't match content

**Add Documentation:**
- Complex lemmas without explanation
- Non-obvious proof strategies
- Important invariants not stated

**Strengthen Induction Hypothesis:**
- Induction gets stuck
- Need more general statement
- Weak hypothesis insufficient

**Generalize Lemma:**
- Overly specific statement
- Could be more reusable
- Hardcoded constants

**Replace Manual Proof with Automation:**
- Tedious manual steps
- Arithmetic or logic reasoning
- Standard library tactics available

### Step 3: Apply Refactoring

Execute the refactoring safely:

1. **Preserve semantics:**
   - Don't change what is proved
   - Keep same logical content
   - Maintain correctness

2. **Make incremental changes:**
   - One refactoring at a time
   - Verify after each change
   - Easy to revert if needed

3. **Test continuously:**
   - Recompile after each change
   - Check dependent proofs
   - Verify no breakage

4. **Document changes:**
   - Add comments explaining complex parts
   - Note proof strategy
   - Explain design decisions

### Step 4: Verify Improvements

Ensure refactoring achieved goals:

1. **Readability:**
   - Easier to understand?
   - Clear structure?
   - Good naming?

2. **Modularity:**
   - Reusable components?
   - Appropriate abstraction level?
   - Clear dependencies?

3. **Maintainability:**
   - Easier to modify?
   - Well documented?
   - Follows conventions?

4. **Performance:**
   - Compilation time acceptable?
   - No significant slowdown?
   - Automation effective?

## Common Refactoring Patterns

For detailed patterns and examples, see [refactoring_patterns.md](references/refactoring_patterns.md).

### Quick Reference

| Code Smell | Refactoring | When to Apply |
|-------------|-------------|---------------|
| Long proof (>20 lines) | Extract Helper Lemma | Complex subgoals, repeated reasoning |
| One-use trivial lemma | Inline Trivial Lemma | Proof is simple, used once |
| Many cases | Break Down Long Proof | Complex case analysis |
| Repeated pattern | Extract Common Pattern | Same proof multiple times |
| Complex tactics | Simplify Proof Structure | Simpler tactics available |
| Generic names | Improve Naming | Unclear what lemma proves |
| No comments | Add Documentation | Complex or non-obvious proof |
| Stuck induction | Strengthen Hypothesis | Need more general statement |
| Too specific | Generalize Lemma | Could be more reusable |
| Tedious manual proof | Use Automation | Standard tactics available |

## Examples

### Example 1: Extract Helper Lemma

**Before (Coq):**
```coq
Lemma complex_theorem : forall n m : nat,
  n > 0 -> m > 0 -> n + m > 0 /\ n * m > 0.
Proof.
  intros n m Hn Hm.
  split.
  - destruct n. inversion Hn.
    destruct m. inversion Hm.
    simpl. lia.
  - destruct n. inversion Hn.
    destruct m. inversion Hm.
    simpl. apply Nat.mul_pos_pos; lia.
Qed.
```

**After (Coq):**
```coq
Lemma add_pos : forall n m : nat,
  n > 0 -> m > 0 -> n + m > 0.
Proof. intros. lia. Qed.

Lemma mul_pos : forall n m : nat,
  n > 0 -> m > 0 -> n * m > 0.
Proof. intros. apply Nat.mul_pos_pos; lia. Qed.

Lemma complex_theorem : forall n m : nat,
  n > 0 -> m > 0 -> n + m > 0 /\ n * m > 0.
Proof.
  intros. split.
  - apply add_pos; assumption.
  - apply mul_pos; assumption.
Qed.
```

**Improvements:**
- Extracted reusable helper lemmas
- Main proof now clear and concise
- Helpers can be used elsewhere

### Example 2: Simplify Proof Structure

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

**Improvements:**
- Replaced manual proof with automation
- Much shorter and clearer
- Less maintenance burden

### Example 3: Improve Naming

**Before (Isabelle):**
```isabelle
lemma l1: "length (xs @ ys) = length xs + length ys"
  by (induction xs) auto

lemma l2: "length (rev xs) = length xs"
  by (induction xs) auto

lemma thm: "length (xs @ ys) = length xs + length ys ∧
            length (rev xs) = length xs"
  using l1 l2 by simp
```

**After (Isabelle):**
```isabelle
lemma append_length: "length (xs @ ys) = length xs + length ys"
  by (induction xs) auto

lemma rev_length: "length (rev xs) = length xs"
  by (induction xs) auto

lemma list_length_properties:
  "length (xs @ ys) = length xs + length ys ∧
   length (rev xs) = length xs"
  using append_length rev_length by simp
```

**Improvements:**
- Descriptive names indicate what each lemma proves
- Follows naming conventions
- Easier to find and understand

### Example 4: Add Documentation

**Before (Coq):**
```coq
Lemma partition_spec : forall (A : Type) (f : A -> bool) (l : list A),
  let (l1, l2) := partition f l in
  filter f l = l1 /\ filter (fun x => negb (f x)) l = l2.
Proof.
  (* Complex 20-line proof *)
Admitted.
```

**After (Coq):**
```coq
(** Specification of list partition function.

    Given a predicate f and a list l, partition splits l into two lists:
    - l1 contains all elements satisfying f
    - l2 contains all elements not satisfying f

    This lemma proves that partition is equivalent to filtering twice.

    Proof strategy: Induction on l, with case analysis on f(head).
*)
Lemma partition_spec : forall (A : Type) (f : A -> bool) (l : list A),
  let (l1, l2) := partition f l in
  filter f l = l1 /\ filter (fun x => negb (f x)) l = l2.
Proof.
  (* Complex 20-line proof *)
Admitted.
```

**Improvements:**
- Clear explanation of what lemma proves
- Documents proof strategy
- Easier for others to understand

### Example 5: Break Down Long Proof

**Before (Isabelle):**
```isabelle
lemma complex_cases: "P x"
proof (cases x)
  case (C1 a b c)
  (* 15 lines of proof *)
  then show ?thesis by auto
next
  case (C2 d e)
  (* 12 lines of proof *)
  then show ?thesis by auto
next
  case (C3 f)
  (* 10 lines of proof *)
  then show ?thesis by auto
qed
```

**After (Isabelle):**
```isabelle
lemma case_C1: "⋀a b c. x = C1 a b c ⟹ P x"
  (* 15 lines of proof *)
  by auto

lemma case_C2: "⋀d e. x = C2 d e ⟹ P x"
  (* 12 lines of proof *)
  by auto

lemma case_C3: "⋀f. x = C3 f ⟹ P x"
  (* 10 lines of proof *)
  by auto

lemma complex_cases: "P x"
  by (cases x) (auto simp: case_C1 case_C2 case_C3)
```

**Improvements:**
- Each case in separate lemma
- Main proof now simple
- Cases can be tested independently

### Example 6: Strengthen Induction Hypothesis

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
(* Strengthen by generalizing with accumulator *)
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

**Improvements:**
- Generalized lemma with stronger IH
- Original lemma now follows easily
- Proof completes successfully

## Refactoring Guidelines

### When to Refactor

**Good times:**
- After proof works but before moving on
- When adding related proofs
- During code review
- When proof is hard to understand
- Before major changes

**Bad times:**
- While proof is still broken
- Under tight deadline
- Without understanding the proof
- When it already works well

### What to Refactor

**High priority:**
- Long, monolithic proofs
- Unclear naming
- Missing documentation
- Duplicated code
- Overly complex tactics

**Low priority:**
- Working proofs that are clear
- Well-structured code
- Good naming and documentation
- Appropriate abstraction level

### How Much to Refactor

**Balance:**
- Improve readability vs. time spent
- Modularity vs. over-engineering
- Generality vs. simplicity
- Documentation vs. verbosity

**Guidelines:**
- Stop when proof is clear and maintainable
- Don't over-abstract
- Keep it simple
- Follow project conventions

## Best Practices

1. **Understand before refactoring:** Know what the proof does
2. **One change at a time:** Incremental refactoring
3. **Test continuously:** Verify after each change
4. **Preserve semantics:** Don't change what's proved
5. **Follow conventions:** Match project style
6. **Document complex parts:** Add helpful comments
7. **Use automation wisely:** When it improves clarity
8. **Keep it simple:** Don't over-engineer

## Anti-Patterns to Avoid

1. **Over-extraction:** Too many tiny lemmas
2. **Premature generalization:** Generalize before understanding
3. **Inconsistent naming:** No naming convention
4. **Over-documentation:** Obvious comments
5. **Breaking working code:** Refactor without testing
6. **Ignoring performance:** Slow compilation after refactoring

## Refactoring Checklist

**Before:**
- [ ] Understand the proof completely
- [ ] Identify specific issues to fix
- [ ] Plan refactoring approach
- [ ] Backup current version

**During:**
- [ ] Make one change at a time
- [ ] Test after each change
- [ ] Keep semantics unchanged
- [ ] Follow naming conventions
- [ ] Add documentation where needed

**After:**
- [ ] All proofs compile
- [ ] No performance regression
- [ ] Improved readability
- [ ] Better modularity
- [ ] Adequate documentation

## Resources

- **Refactoring patterns:** See [refactoring_patterns.md](references/refactoring_patterns.md) for comprehensive catalog
- **Isabelle documentation:** https://isabelle.in.tum.de/documentation.html
- **Coq documentation:** https://coq.inria.fr/documentation
- **Proof engineering:** Best practices for formal proof development
