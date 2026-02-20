# Isabelle Tactics and Proof Methods

Comprehensive reference for Isabelle/Isar tactics organized by proof situation.

## Table of Contents
- [Structural Tactics](#structural-tactics)
- [Simplification](#simplification)
- [Induction and Cases](#induction-and-cases)
- [Rewriting](#rewriting)
- [Automation](#automation)
- [Logical Reasoning](#logical-reasoning)
- [Arithmetic](#arithmetic)

## Structural Tactics

### `apply <method>`
Apply a proof method to the current goal.
```isabelle
apply (rule conjI)
apply simp
```

### `by <method>`
Complete the proof with a single method application.
```isabelle
by simp
by auto
by (induction xs)
```

### `proof <method>`
Start a structured proof with initial method.
```isabelle
proof (induction xs)
proof (cases x)
proof -
```

### `show "goal"`
Prove a specific goal in structured proofs.
```isabelle
show "P ∧ Q"
show ?thesis
```

### `have "lemma"`
Prove an intermediate lemma.
```isabelle
have "length xs = length ys" by simp
have aux: "P x" by auto
```

### `from <facts>`
Use specific facts in the next step.
```isabelle
from assms show ?thesis
from IH have "P (Suc n)"
```

### `using <facts>`
Add facts to the proof context.
```isabelle
using assms by simp
using IH by auto
```

## Simplification

### `simp`
Simplify using rewrite rules.
```isabelle
by simp
apply simp
proof simp
```

**Options:**
- `simp add: rules` - Add specific rules
- `simp del: rules` - Remove rules
- `simp only: rules` - Use only specified rules

### `simp_all`
Simplify all goals.
```isabelle
by simp_all
```

### `clarsimp`
Clarify and simplify (combines `clarify` and `simp`).
```isabelle
by clarsimp
```

### `force`
Aggressive simplification with classical reasoning.
```isabelle
by force
```

## Induction and Cases

### `induction <var>`
Proof by induction on a variable.
```isabelle
proof (induction xs)
  case Nil
  show ?case by simp
next
  case (Cons x xs)
  show ?case using Cons.IH by simp
qed
```

**Variants:**
- `induction xs arbitrary: ys` - Generalize over variables
- `induction xs rule: custom_induct` - Use custom induction rule

### `cases <var>`
Case analysis on a variable.
```isabelle
proof (cases xs)
  case Nil
  show ?thesis by simp
next
  case (Cons x xs')
  show ?thesis by simp
qed
```

### `case_tac <var>`
Apply-style case analysis.
```isabelle
apply (case_tac xs)
```

### `induct_tac <var>`
Apply-style induction.
```isabelle
apply (induct_tac xs)
```

## Rewriting

### `subst <rule>`
Substitute using an equation (left-to-right).
```isabelle
apply (subst eq_rule)
```

### `subst (asm) <rule>`
Substitute in assumptions.
```isabelle
apply (subst (asm) eq_rule)
```

### `unfold <def>`
Unfold definitions.
```isabelle
apply (unfold my_def)
by (unfold my_def) simp
```

### `fold <def>`
Fold definitions (reverse of unfold).
```isabelle
apply (fold my_def)
```

## Automation

### `auto`
Automatic proof search with simplification and classical reasoning.
```isabelle
by auto
apply auto
```

**Options:**
- `auto simp: rules` - Add simplification rules
- `auto intro: rules` - Add introduction rules
- `auto dest: rules` - Add destruction rules

### `fastforce`
Fast automatic proof search.
```isabelle
by fastforce
```

### `blast`
Classical reasoning with depth-first search.
```isabelle
by blast
```

### `metis`
Resolution-based automated prover.
```isabelle
by (metis assms)
```

### `sledgehammer`
Invoke external ATPs (not a method, but a command).
```isabelle
sledgehammer
```

## Logical Reasoning

### `rule <rule>`
Apply an introduction rule.
```isabelle
apply (rule conjI)
apply (rule impI)
```

### `erule <rule>`
Apply an elimination rule.
```isabelle
apply (erule conjE)
apply (erule exE)
```

### `drule <rule>`
Apply a destruction rule.
```isabelle
apply (drule spec)
```

### `intro`
Apply introduction rules automatically.
```isabelle
by (intro conjI impI)
```

### `elim`
Apply elimination rules automatically.
```isabelle
by (elim conjE disjE)
```

### `assumption`
Solve goal by matching an assumption.
```isabelle
by assumption
```

### `contradiction`
Derive contradiction from assumptions.
```isabelle
by contradiction
```

## Arithmetic

### `arith`
Arithmetic decision procedure.
```isabelle
by arith
```

### `linarith`
Linear arithmetic solver.
```isabelle
by linarith
```

### `presburger`
Presburger arithmetic (linear arithmetic with quantifiers).
```isabelle
by presburger
```

## Common Proof Patterns

### Pattern: Conjunction
**Goal**: `⊢ P ∧ Q`
```isabelle
apply (rule conjI)
  (* Now two goals: ⊢ P and ⊢ Q *)
```

### Pattern: Implication
**Goal**: `⊢ P ⟹ Q`
```isabelle
apply (rule impI)
  (* Now: P ⊢ Q *)
```

### Pattern: Universal Quantification
**Goal**: `⊢ ∀x. P x`
```isabelle
apply (rule allI)
  (* Now: ⊢ P x for arbitrary x *)
```

### Pattern: Existential Quantification
**Goal**: `⊢ ∃x. P x`
```isabelle
apply (rule exI[where x="witness"])
  (* Now: ⊢ P witness *)
```

### Pattern: Disjunction
**Goal**: `⊢ P ∨ Q`
```isabelle
apply (rule disjI1)  (* Choose left *)
  (* Now: ⊢ P *)
```

### Pattern: Negation
**Goal**: `⊢ ¬P`
```isabelle
apply (rule notI)
  (* Now: P ⊢ False *)
```

### Pattern: List Induction
**Goal**: `⊢ P xs`
```isabelle
proof (induction xs)
  case Nil
  (* Show: P [] *)
  show ?case by simp
next
  case (Cons x xs)
  (* IH: P xs *)
  (* Show: P (x # xs) *)
  show ?case using Cons.IH by simp
qed
```

### Pattern: Natural Number Induction
**Goal**: `⊢ P n`
```isabelle
proof (induction n)
  case 0
  (* Show: P 0 *)
  show ?case by simp
next
  case (Suc n)
  (* IH: P n *)
  (* Show: P (Suc n) *)
  show ?case using Suc.IH by simp
qed
```

### Pattern: Case Analysis on Option
**Goal**: `⊢ P opt`
```isabelle
proof (cases opt)
  case None
  (* opt = None *)
  show ?thesis by simp
next
  case (Some x)
  (* opt = Some x *)
  show ?thesis by simp
qed
```

## Method Combinators

### `<method>+`
Apply method repeatedly (at least once).
```isabelle
by (simp+)
```

### `<method>?`
Apply method optionally (zero or one time).
```isabelle
by (simp?)
```

### `<method1>, <method2>`
Sequential composition.
```isabelle
by (simp, auto)
```

### `<method1> | <method2>`
Alternative (try first, if fails try second).
```isabelle
by (simp | auto)
```
