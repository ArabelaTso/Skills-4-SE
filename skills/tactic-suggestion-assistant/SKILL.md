---
name: tactic-suggestion-assistant
description: "Analyze proof states in Isabelle or Coq and suggest applicable tactics to make progress. Use when users need help with: (1) Choosing the next tactic in an interactive proof, (2) Understanding what tactics apply to their current goal, (3) Getting unstuck in a proof, (4) Learning which tactics work for specific goal structures (conjunctions, implications, induction, etc.). Provides 3-5 ranked tactic suggestions with explanations for intermediate-level proofs in both Isabelle/Isar and Coq."
---

# Tactic Suggestion Assistant

Analyze proof states and suggest applicable tactics to make progress in Isabelle or Coq.

## Overview

This skill helps you navigate interactive proofs by analyzing the current proof state and suggesting 3-5 ranked tactics that can make progress. It works with both Isabelle/Isar and Coq, providing system-specific suggestions with explanations.

## How to Use

Provide the current proof state including:
1. **System**: Isabelle or Coq
2. **Goal**: The current goal to prove
3. **Context**: Available hypotheses/assumptions (if any)
4. **Variables**: Types of variables involved (optional but helpful)

The assistant will analyze the state and suggest tactics ranked by likelihood of success.

## Analysis Process

### Step 1: Identify the Proof System

Determine whether you're working in Isabelle or Coq based on syntax:
- Isabelle: Uses `⟹`, `∧`, `∨`, `∀`, `∃`, `'a list`, etc.
- Coq: Uses `->`, `/\`, `\/`, `forall`, `exists`, `list A`, etc.

### Step 2: Analyze Goal Structure

Examine the goal's logical form:
- **Conjunction**: `P ∧ Q` / `P /\ Q` → Split tactics
- **Implication**: `P ⟹ Q` / `P -> Q` → Introduction tactics
- **Quantification**: `∀x. P` / `forall x, P` → Variable introduction
- **Equality**: `t1 = t2` → Simplification or rewriting
- **Inductive types**: Lists, nat, trees → Induction or case analysis

### Step 3: Examine Context

Look at available hypotheses:
- **Equations**: Can be used for rewriting
- **Inductive predicates**: Can be inverted or used directly
- **Conjunctions**: Can be decomposed
- **Disjunctions**: Require case analysis

### Step 4: Consider Variable Types

Type information guides tactic choice:
- **Lists**: Suggest induction or case analysis (empty vs cons)
- **Natural numbers**: Suggest induction or case analysis (0 vs successor)
- **Options**: Suggest case analysis (None vs Some)
- **Custom types**: Suggest structural induction

### Step 5: Rank Suggestions

Provide 3-5 tactics ranked by:
1. Structural match with goal
2. Simplicity and directness
3. Automation potential
4. Common proof patterns
5. Context support

## Suggestion Format

For each suggested tactic, provide:

1. **Tactic**: The exact tactic syntax
2. **Rationale**: Why this tactic applies
3. **Effect**: What happens after applying it
4. **Likelihood**: High/Medium/Low

## Example: Isabelle Proof State

**Proof state**:
```isabelle
goal (1 subgoal):
 1. ⋀xs ys. length xs = length ys ⟹ length (xs @ ys) = 2 * length xs
```

**Analysis**:
- Goal: Implication with equality
- Hypothesis: `length xs = length ys`
- Variables: Lists `xs` and `ys`

**Suggestions**:

1. **`by simp`** (High likelihood)
   - Rationale: Goal is an arithmetic equality that simplification can handle
   - Effect: Simplifies `length (xs @ ys)` to `length xs + length ys`, then uses hypothesis
   - Try this first for simple arithmetic goals

2. **`apply (subst length_append)`** (Medium likelihood)
   - Rationale: Explicitly unfold the append length property
   - Effect: Rewrites `length (xs @ ys)` to `length xs + length ys`
   - More explicit than simp, useful if simp fails

3. **`using assms by auto`** (Medium likelihood)
   - Rationale: Use assumptions with automation
   - Effect: Combines hypothesis with automatic reasoning
   - Good fallback if simp doesn't work

## Example: Coq Proof State

**Proof state**:
```coq
1 subgoal
n : nat
IHn : even n -> even (n + 2)
============================
even n -> even (S (S n))
```

**Analysis**:
- Goal: Implication
- Hypothesis: Induction hypothesis `IHn`
- Variables: Natural number `n`
- Context: In an induction proof

**Suggestions**:

1. **`intro H.`** (High likelihood)
   - Rationale: Goal is an implication, introduce the hypothesis
   - Effect: Adds `H: even n` to context, goal becomes `even (S (S n))`
   - Standard first step for implications

2. **`intros. simpl. apply IHn. assumption.`** (High likelihood)
   - Rationale: Complete proof chain using IH
   - Effect: Introduces hypothesis, simplifies, applies IH, solves with assumption
   - Direct solution if `S (S n)` simplifies to `n + 2`

3. **`intro H. rewrite <- plus_n_Sm. rewrite <- plus_n_O. apply IHn. exact H.`** (Medium likelihood)
   - Rationale: Rewrite to match IH form
   - Effect: Converts `S (S n)` to `n + 2` form to use IH
   - Needed if simplification doesn't automatically match

4. **`auto.`** (Low likelihood)
   - Rationale: Try automation
   - Effect: May solve if proof is straightforward
   - Worth trying but may not have enough hints

## Common Situations

### Situation: Conjunction Goal

**Isabelle**: `⊢ P ∧ Q`
- `apply (rule conjI)` - Split into two goals
- `by auto` - If both parts are trivial
- `by simp` - If simplification proves both

**Coq**: `P /\ Q`
- `split.` - Split into two goals
- `auto.` - If both parts are trivial
- `intuition.` - Propositional reasoning

### Situation: Need Induction

**Indicators**: Goal about all elements of a list/nat, recursive structure

**Isabelle**:
- `proof (induction xs)` - List induction
- `proof (induction n)` - Nat induction
- `proof (induction t)` - Custom type induction

**Coq**:
- `induction l as [|x l' IH].` - List induction
- `induction n as [|n' IH].` - Nat induction
- `induction t.` - Custom type induction

### Situation: Case Analysis Needed

**Indicators**: Goal or hypothesis with conditional, pattern match

**Isabelle**:
- `proof (cases xs)` - Case analysis on variable
- `proof (cases "condition")` - Case split on boolean
- `by (auto split: if_split)` - Auto with case split

**Coq**:
- `destruct l as [|x l'].` - Case analysis on variable
- `destruct (condition).` - Case split on boolean
- `case_eq term.` - Case analysis with equation

### Situation: Arithmetic Goal

**Indicators**: Goal with +, -, *, <, ≤

**Isabelle**:
- `by arith` - Arithmetic decision procedure
- `by linarith` - Linear arithmetic
- `by simp` - Simplification

**Coq**:
- `lia.` - Linear integer arithmetic
- `nia.` - Non-linear arithmetic
- `ring.` - Ring solver

### Situation: Stuck on Complex Goal

**Indicators**: Many connectives, nested structure

**Isabelle**:
- `by auto` - Full automation
- `by fastforce` - Aggressive automation
- `sledgehammer` - External provers

**Coq**:
- `auto.` - Automation
- `intuition.` - Propositional reasoning
- `firstorder.` - First-order reasoning
- `tauto.` - Tautology solver

## References

Detailed tactic references and patterns:

- **[isabelle_tactics.md](references/isabelle_tactics.md)**: Complete Isabelle/Isar tactic reference
- **[coq_tactics.md](references/coq_tactics.md)**: Complete Coq tactic reference
- **[proof_patterns.md](references/proof_patterns.md)**: Detailed proof state analysis patterns

Load these references when you need:
- Complete tactic syntax and options
- Advanced tactic usage
- Detailed pattern matching rules
- Tactic combinators and composition

## Tips for Effective Suggestions

1. **Start simple**: Suggest automation (`auto`, `simp`) before manual tactics
2. **Match structure**: Prioritize tactics that directly match the goal form
3. **Consider context**: Use available hypotheses in suggestions
4. **Explain effects**: Clearly state what happens after applying the tactic
5. **Provide alternatives**: Offer 3-5 options ranked by likelihood
6. **Be specific**: Give exact syntax, not just tactic names
7. **Learn from failures**: If a suggested tactic fails, analyze why and suggest alternatives
