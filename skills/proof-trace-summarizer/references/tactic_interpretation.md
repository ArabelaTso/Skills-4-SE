# Tactic Interpretation Guide

Guide for interpreting tactics and methods into high-level reasoning steps.

## Isabelle Tactics to Reasoning Steps

### Structural Tactics

| Tactic | Reasoning Step |
|--------|----------------|
| `proof (induction xs)` | Begin proof by induction on xs |
| `proof (cases x)` | Perform case analysis on x |
| `proof -` | Begin direct proof |
| `show ?case` | Prove the current case |
| `show ?thesis` | Prove the goal |
| `qed` | Complete the proof |

### Simplification

| Tactic | Reasoning Step |
|--------|----------------|
| `by simp` | Simplification proves the goal |
| `by (simp add: rules)` | Simplification with additional rules proves the goal |
| `by simp_all` | Simplification proves all subgoals |
| `by clarsimp` | Clarification and simplification prove the goal |
| `by force` | Aggressive simplification with classical reasoning proves the goal |

### Automation

| Tactic | Reasoning Step |
|--------|----------------|
| `by auto` | Automatic proof search succeeds |
| `by fastforce` | Fast automatic proof search succeeds |
| `by blast` | Classical reasoning proves the goal |
| `by metis` | Resolution-based prover succeeds |
| `sledgehammer` | External automated provers find a proof |

### Logical Reasoning

| Tactic | Reasoning Step |
|--------|----------------|
| `apply (rule conjI)` | Split conjunction into two subgoals |
| `apply (rule impI)` | Introduce implication (assume antecedent) |
| `apply (rule allI)` | Introduce universal quantifier |
| `apply (rule exI[where x="t"])` | Provide witness t for existential |
| `apply (erule conjE)` | Eliminate conjunction (extract both parts) |
| `using assms` | Use the assumptions |
| `from H have ...` | Derive fact from hypothesis H |

### Rewriting

| Tactic | Reasoning Step |
|--------|----------------|
| `apply (subst rule)` | Rewrite using equation |
| `unfold def` | Unfold definition |
| `fold def` | Fold definition |
| `using H by simp` | Simplify using hypothesis H |

### Arithmetic

| Tactic | Reasoning Step |
|--------|----------------|
| `by arith` | Arithmetic decision procedure proves the goal |
| `by linarith` | Linear arithmetic solver proves the goal |
| `by presburger` | Presburger arithmetic proves the goal |

## Coq Tactics to Reasoning Steps

### Structural Tactics

| Tactic | Reasoning Step |
|--------|----------------|
| `intro x.` | Introduce variable x |
| `intros.` | Introduce all variables and hypotheses |
| `apply H.` | Apply hypothesis or lemma H |
| `exact H.` | Goal is exactly H |
| `assumption.` | Goal matches an assumption |
| `Qed.` | Complete the proof |

### Simplification

| Tactic | Reasoning Step |
|--------|----------------|
| `simpl.` | Simplify by computation |
| `cbn.` | Normalize by call-by-name |
| `unfold def.` | Unfold definition |
| `fold def.` | Fold definition |
| `compute.` | Fully compute the goal |

### Induction and Cases

| Tactic | Reasoning Step |
|--------|----------------|
| `induction n as [|n' IH].` | Begin proof by induction on n |
| `destruct n as [|n'].` | Perform case analysis on n |
| `destruct H as [H1 H2].` | Extract components from H |
| `inversion H.` | Invert inductive predicate H |
| `inversion H; subst.` | Invert H and substitute equalities |

### Rewriting

| Tactic | Reasoning Step |
|--------|----------------|
| `rewrite H.` | Rewrite goal using equation H |
| `rewrite <- H.` | Rewrite goal using H (right-to-left) |
| `rewrite H in H2.` | Rewrite hypothesis H2 using H |
| `subst.` | Substitute all equations |
| `replace t1 with t2.` | Replace t1 with t2 (generates subgoal) |

### Automation

| Tactic | Reasoning Step |
|--------|----------------|
| `auto.` | Automatic proof search succeeds |
| `trivial.` | Trivial proof succeeds |
| `easy.` | Easy proof succeeds |
| `tauto.` | Tautology solver proves the goal |
| `intuition.` | Propositional reasoning proves the goal |
| `firstorder.` | First-order reasoning proves the goal |
| `congruence.` | Congruence closure proves the goal |

### Logical Reasoning

| Tactic | Reasoning Step |
|--------|----------------|
| `split.` | Split conjunction into two subgoals |
| `left.` | Prove left side of disjunction |
| `right.` | Prove right side of disjunction |
| `exists t.` | Provide witness t for existential |
| `constructor.` | Apply appropriate constructor |
| `discriminate.` | Derive contradiction from impossible equality |
| `injection H.` | Extract equalities from constructor equality |
| `contradiction.` | Derive contradiction |
| `exfalso.` | Prove by contradiction (goal becomes False) |

### Arithmetic

| Tactic | Reasoning Step |
|--------|----------------|
| `lia.` | Linear integer arithmetic proves the goal |
| `nia.` | Non-linear integer arithmetic proves the goal |
| `ring.` | Ring solver proves the goal |
| `field.` | Field solver proves the goal |

## Interpreting Tactic Sequences

### Sequential Composition

**Pattern**: `tactic1. tactic2. tactic3.`

**Interpretation**: Apply tactic1, then tactic2, then tactic3 in sequence

**Summary format**: List each step with its effect

### Semicolon Composition (Coq)

**Pattern**: `tactic1; tactic2.`

**Interpretation**: Apply tactic1, then apply tactic2 to all resulting subgoals

**Summary format**: "Apply tactic1, then tactic2 to all subgoals"

### Alternative Composition (Isabelle)

**Pattern**: `by (method1 | method2)`

**Interpretation**: Try method1, if it fails try method2

**Summary format**: "Proof by method1 (or method2 as fallback)"

### Repetition

**Pattern**: `repeat tactic.` (Coq) or `method+` (Isabelle)

**Interpretation**: Apply tactic repeatedly until it fails

**Summary format**: "Repeatedly apply tactic until no progress"

## Interpreting Proof Context

### Assumptions and Hypotheses

**Isabelle**:
- `assumes "P"` → Assumption: P
- `from H` → Using hypothesis H
- `using assms` → Using all assumptions

**Coq**:
- `H: P` in context → Hypothesis H states P
- `apply H` → Apply hypothesis H
- `pose proof H as H2` → Add H to context as H2

### Intermediate Facts

**Isabelle**:
- `have "P" by method` → Intermediate fact: P (proven by method)
- `have aux: "P" by method` → Named intermediate fact aux: P

**Coq**:
- `assert (H: P).` → Intermediate fact H: P (requires proof)
- `pose proof (lemma args) as H` → Intermediate fact H from lemma

### Subgoal Structure

**Isabelle**:
- `case Nil` → Base case: empty list
- `case (Cons x xs)` → Inductive case: non-empty list
- `Cons.IH` → Induction hypothesis from Cons case

**Coq**:
- `- (* n = 0 *)` → Base case: n = 0
- `- (* n = S n' *)` → Inductive case: n = S n'
- `IHn'` → Induction hypothesis for n'

## Common Proof Patterns and Their Summaries

### Pattern: Proof by Simplification

**Isabelle**: `by simp`
**Coq**: `reflexivity.` or `simpl. reflexivity.`

**Summary**: "Direct proof by simplification/computation"

### Pattern: Proof by Automation

**Isabelle**: `by auto`
**Coq**: `auto.` or `intuition.`

**Summary**: "Automatic proof using [method]"

### Pattern: Proof by Induction

**Isabelle**: `proof (induction ...) ... qed`
**Coq**: `induction ... as [...]. ... Qed.`

**Summary**: Hierarchical outline with base and inductive cases

### Pattern: Proof by Case Analysis

**Isabelle**: `proof (cases ...) ... qed`
**Coq**: `destruct ... as [...]. ... Qed.`

**Summary**: Hierarchical outline with all cases

### Pattern: Proof by Rewriting

**Isabelle**: `using H by simp` or `apply (subst H)`
**Coq**: `rewrite H. reflexivity.`

**Summary**: "Rewrite using [equation], then [method]"

### Pattern: Proof by Lemma Application

**Isabelle**: `by (rule lemma)`
**Coq**: `apply lemma.`

**Summary**: "Apply lemma [name] to prove goal"

### Pattern: Proof with Intermediate Lemmas

**Isabelle**: Multiple `have` statements
**Coq**: Multiple `assert` statements

**Summary**: List intermediate facts and how they combine

## Handling Complex Proofs

### Strategy 1: Identify Main Structure

1. Look for top-level proof method (induction, cases, direct)
2. Identify major branches or subgoals
3. Summarize each branch separately

### Strategy 2: Group Related Steps

1. Identify sequences of related tactics
2. Group them into logical units
3. Summarize each unit with a single high-level step

### Strategy 3: Abstract Automation

1. When automation is used, don't list individual steps
2. Summarize as "Automatic proof handles [aspect]"
3. Only detail manual steps

### Strategy 4: Highlight Key Insights

1. Identify non-obvious steps (lemma applications, clever rewrites)
2. Give these more detail in summary
3. Minimize detail on routine steps

## Summary Quality Guidelines

### Good Summary Characteristics

- **Hierarchical**: Shows proof structure clearly
- **Concise**: Omits routine details
- **Informative**: Captures key reasoning steps
- **Readable**: Uses natural language, not just tactic names
- **Accurate**: Faithfully represents the proof logic

### What to Include

- Main proof strategy (induction, cases, direct)
- Key lemmas or theorems applied
- Non-obvious reasoning steps
- Case structure and how cases are resolved
- Intermediate facts that are crucial

### What to Omit

- Routine simplification steps
- Obvious arithmetic
- Trivial case analysis
- Repetitive patterns
- Low-level tactic details
