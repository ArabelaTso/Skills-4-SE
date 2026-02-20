# Proof State Analysis Patterns

Guide for analyzing proof states and suggesting appropriate tactics.

## Analysis Framework

When analyzing a proof state, examine:

1. **Goal structure**: What logical form does the goal have?
2. **Available hypotheses**: What facts are in the context?
3. **Variable types**: What are we working with (nat, list, custom types)?
4. **Recursion opportunities**: Can we apply induction or case analysis?
5. **Simplification potential**: Can computation or rewriting help?

## Pattern Matching by Goal Structure

### Goal: Conjunction `P ∧ Q` (Isabelle) / `P /\ Q` (Coq)

**Analysis**: Need to prove both parts separately.

**Isabelle suggestions**:
1. `apply (rule conjI)` - Split into two subgoals
2. `by auto` - If both parts are trivial
3. `by simp` - If simplification proves both

**Coq suggestions**:
1. `split.` - Split into two subgoals
2. `auto.` - If both parts are trivial
3. `intuition.` - Propositional reasoning

### Goal: Implication `P ⟹ Q` (Isabelle) / `P -> Q` (Coq)

**Analysis**: Assume P and prove Q.

**Isabelle suggestions**:
1. `apply (rule impI)` - Move P to assumptions
2. `proof -` then `assume "P"` - Structured proof
3. `by auto` - If Q follows from P automatically

**Coq suggestions**:
1. `intro H.` - Introduce hypothesis H: P
2. `intros.` - Introduce all implications
3. `auto.` - If Q follows automatically

### Goal: Universal Quantification `∀x. P x` (Isabelle) / `forall x, P x` (Coq)

**Analysis**: Prove for arbitrary x.

**Isabelle suggestions**:
1. `apply (rule allI)` - Introduce arbitrary x
2. `proof -` then `fix x` - Structured proof
3. `by auto` - If automation handles it

**Coq suggestions**:
1. `intro x.` - Introduce arbitrary x
2. `intros.` - Introduce all quantifiers
3. `auto.` - If automation handles it

### Goal: Existential Quantification `∃x. P x` (Isabelle) / `exists x, P x` (Coq)

**Analysis**: Need to provide a witness.

**Isabelle suggestions**:
1. `apply (rule exI[where x="witness"])` - Provide witness
2. `by auto` - If witness can be found automatically
3. `by force` - Aggressive search for witness

**Coq suggestions**:
1. `exists witness.` - Provide witness
2. `eauto.` - Search for witness automatically
3. `firstorder.` - First-order reasoning

### Goal: Disjunction `P ∨ Q` (Isabelle) / `P \/ Q` (Coq)

**Analysis**: Choose which side to prove.

**Isabelle suggestions**:
1. `apply (rule disjI1)` - Prove left side (P)
2. `apply (rule disjI2)` - Prove right side (Q)
3. `by auto` - If automation can choose

**Coq suggestions**:
1. `left.` - Prove left side (P)
2. `right.` - Prove right side (Q)
3. `auto.` - If automation can choose

### Goal: Equality `t1 = t2`

**Analysis**: Can we compute, rewrite, or simplify?

**Isabelle suggestions**:
1. `by simp` - Simplification
2. `by (simp add: defs)` - Unfold definitions
3. `apply (subst rule)` - Rewrite with equation
4. `by auto` - Automatic reasoning

**Coq suggestions**:
1. `reflexivity.` - If equal by computation
2. `simpl. reflexivity.` - Simplify then check
3. `rewrite H. reflexivity.` - Rewrite with hypothesis
4. `auto.` - Automatic reasoning

### Goal: Negation `¬P` (Isabelle) / `~ P` (Coq)

**Analysis**: Assume P and derive contradiction.

**Isabelle suggestions**:
1. `apply (rule notI)` - Introduce P, prove False
2. `by contradiction` - Derive contradiction
3. `by auto` - If contradiction is obvious

**Coq suggestions**:
1. `intro H.` - Introduce hypothesis H: P
2. `contradiction.` - Derive contradiction
3. `auto.` - If contradiction is obvious

## Pattern Matching by Variable Types

### Working with Lists

**Indicators**: Variables of type `'a list` (Isabelle) or `list A` (Coq)

**Isabelle suggestions**:
1. `proof (induction xs)` - List induction
2. `proof (cases xs)` - Case analysis (empty vs cons)
3. `by (simp add: list_rules)` - Simplify with list lemmas

**Coq suggestions**:
1. `induction l as [|x l' IH].` - List induction
2. `destruct l as [|x l'].` - Case analysis
3. `simpl. auto.` - Simplify and auto

### Working with Natural Numbers

**Indicators**: Variables of type `nat`

**Isabelle suggestions**:
1. `proof (induction n)` - Natural number induction
2. `proof (cases n)` - Case analysis (0 vs Suc)
3. `by arith` - Arithmetic decision procedure

**Coq suggestions**:
1. `induction n as [|n' IH].` - Natural number induction
2. `destruct n as [|n'].` - Case analysis
3. `lia.` - Linear arithmetic solver

### Working with Options

**Indicators**: Variables of type `'a option` (Isabelle) or `option A` (Coq)

**Isabelle suggestions**:
1. `proof (cases opt)` - Case analysis (None vs Some)
2. `by (auto split: option.split)` - Auto with case split

**Coq suggestions**:
1. `destruct opt as [x|].` - Case analysis
2. `destruct opt eqn:E.` - Case analysis with equation

### Working with Custom Datatypes

**Indicators**: Variables of custom inductive types (trees, etc.)

**Isabelle suggestions**:
1. `proof (induction t)` - Structural induction
2. `proof (cases t)` - Case analysis on constructors
3. `by (auto split: datatype.split)` - Auto with splits

**Coq suggestions**:
1. `induction t.` - Structural induction
2. `destruct t.` - Case analysis on constructors
3. `auto.` - Automatic reasoning

## Pattern Matching by Hypotheses

### Hypothesis: Conjunction `H: P ∧ Q` (Isabelle) / `H: P /\ Q` (Coq)

**Analysis**: Can extract both parts.

**Isabelle suggestions**:
1. `from H have "P" and "Q" by simp_all` - Extract both
2. `using H by simp` - Use directly

**Coq suggestions**:
1. `destruct H as [HP HQ].` - Extract both parts
2. `apply H.` - Use directly if applicable

### Hypothesis: Disjunction `H: P ∨ Q` (Isabelle) / `H: P \/ Q` (Coq)

**Analysis**: Need case analysis.

**Isabelle suggestions**:
1. `proof (cases rule: H)` - Case analysis on H
2. `using H by auto` - Let automation handle

**Coq suggestions**:
1. `destruct H as [HP|HQ].` - Case analysis
2. `intuition.` - Let automation handle

### Hypothesis: Existential `H: ∃x. P x` (Isabelle) / `H: exists x, P x` (Coq)

**Analysis**: Extract witness.

**Isabelle suggestions**:
1. `from H obtain x where "P x" by auto` - Extract witness
2. `using H by auto` - Use directly

**Coq suggestions**:
1. `destruct H as [x HP].` - Extract witness
2. `apply H.` - Use directly if applicable

### Hypothesis: Equation `H: t1 = t2`

**Analysis**: Can rewrite with it.

**Isabelle suggestions**:
1. `using H by simp` - Simplify with equation
2. `apply (subst H)` - Substitute in goal
3. `from H show ?thesis` - Use directly

**Coq suggestions**:
1. `rewrite H.` - Rewrite in goal
2. `rewrite H in *.` - Rewrite everywhere
3. `subst.` - Substitute all equations

### Hypothesis: Inductive Predicate

**Analysis**: Can invert to get structure.

**Isabelle suggestions**:
1. `from H show ?thesis by (cases H)` - Case analysis
2. `using H by auto` - Use directly

**Coq suggestions**:
1. `inversion H.` - Invert the predicate
2. `inversion H; subst.` - Invert and substitute
3. `apply H.` - Use directly if applicable

## Situation-Based Suggestions

### Situation: Stuck on Complex Goal

**Indicators**: Goal has many connectives, nested structure

**Isabelle suggestions**:
1. `by auto` - Try full automation
2. `by fastforce` - Aggressive automation
3. `by (auto intro: rules)` - Auto with hints
4. `sledgehammer` - Invoke external provers

**Coq suggestions**:
1. `auto.` - Try automation
2. `intuition.` - Propositional reasoning
3. `firstorder.` - First-order reasoning
4. `tauto.` - Tautology solver

### Situation: Need Intermediate Lemma

**Indicators**: Direct proof seems difficult, need stepping stone

**Isabelle suggestions**:
1. `have "intermediate_fact" by method` - Prove intermediate
2. `from assms have "fact" by method` - Derive from assumptions

**Coq suggestions**:
1. `assert (H: intermediate_fact).` - State intermediate
2. `pose proof (lemma args) as H.` - Use existing lemma

### Situation: Induction Hypothesis Not Strong Enough

**Indicators**: IH doesn't apply, need generalization

**Isabelle suggestions**:
1. `proof (induction xs arbitrary: ys)` - Generalize variables
2. Restart with stronger statement

**Coq suggestions**:
1. `generalize dependent y.` - Generalize before induction
2. `revert y.` - Move variable back to goal
3. Restart with stronger statement

### Situation: Case Analysis Needed

**Indicators**: Goal or hypothesis has conditional, pattern match

**Isabelle suggestions**:
1. `proof (cases "condition")` - Case split on condition
2. `by (auto split: if_split)` - Auto with if-split
3. `proof (cases var)` - Case analysis on variable

**Coq suggestions**:
1. `destruct (condition).` - Case split
2. `destruct var.` - Case analysis on variable
3. `case_eq term.` - Case analysis with equation

### Situation: Arithmetic Goal

**Indicators**: Goal involves +, -, *, <, ≤, etc.

**Isabelle suggestions**:
1. `by arith` - Arithmetic decision procedure
2. `by linarith` - Linear arithmetic
3. `by simp` - Simplification may suffice

**Coq suggestions**:
1. `lia.` - Linear integer arithmetic
2. `nia.` - Non-linear arithmetic
3. `ring.` - Ring solver

### Situation: Equality with Constructors

**Indicators**: Hypothesis like `Cons x xs = Cons y ys` or `S n = S m`

**Isabelle suggestions**:
1. `by simp` - Simplification extracts equalities
2. `by auto` - Automatic reasoning

**Coq suggestions**:
1. `injection H.` - Extract equalities
2. `injection H as H1 H2.` - Extract and name
3. `inversion H; subst.` - Invert and substitute

### Situation: Impossible Equality

**Indicators**: Hypothesis like `[] = x :: xs` or `0 = S n`

**Isabelle suggestions**:
1. `by simp` - Simplification derives contradiction
2. `by auto` - Automatic reasoning

**Coq suggestions**:
1. `discriminate.` - Derive contradiction
2. `discriminate H.` - Use specific hypothesis
3. `inversion H.` - Invert (also finds contradiction)

## Ranking Tactics by Likelihood

When multiple tactics apply, rank by:

1. **Structural match**: Does the tactic directly match the goal form?
2. **Simplicity**: Simpler tactics before complex ones
3. **Automation potential**: Can automation solve it?
4. **Common patterns**: Is this a standard proof pattern?
5. **Context fit**: Do hypotheses support this approach?

**Example ranking for goal `P ∧ Q`**:
1. Split tactic (direct structural match)
2. Auto (if both parts are simple)
3. Manual proof of each part (fallback)
