# Proof Summarization Patterns

Patterns for identifying and summarizing common proof structures in Isabelle and Coq.

## Table of Contents
- [Induction Proofs](#induction-proofs)
- [Case Analysis Proofs](#case-analysis-proofs)
- [Equational Reasoning](#equational-reasoning)
- [Lemma Application](#lemma-application)
- [Automation-Heavy Proofs](#automation-heavy-proofs)
- [Nested Subproofs](#nested-subproofs)

## Induction Proofs

### Recognition Patterns

**Isabelle indicators**:
- `proof (induction ...)`
- `case Nil` / `case (Cons ...)`
- `case 0` / `case (Suc ...)`
- Induction hypothesis references: `Cons.IH`, `Suc.IH`

**Coq indicators**:
- `induction ... as [|...]`
- Base case: `- (* n = 0 *)` or `- (* l = [] *)`
- Inductive case with IH: `IHn`, `IHl`

### Summarization Template

```
Proof by induction on <variable>
├─ Base case: <variable> = <base_value>
│  └─ <how it's proven>
└─ Inductive case: <variable> = <constructor> <subterm>
   ├─ Induction hypothesis: <IH_statement>
   └─ <how IH is used to prove goal>
```

### Example: Isabelle List Induction

**Proof script**:
```isabelle
lemma length_append: "length (xs @ ys) = length xs + length ys"
proof (induction xs)
  case Nil
  show ?case by simp
next
  case (Cons x xs)
  show ?case using Cons.IH by simp
qed
```

**Summary**:
```
Proof by induction on xs
├─ Base case: xs = []
│  └─ Simplification proves length ([] @ ys) = length [] + length ys
└─ Inductive case: xs = x # xs'
   ├─ IH: length (xs' @ ys) = length xs' + length ys
   └─ Simplification with IH proves length ((x # xs') @ ys) = length (x # xs') + length ys
```

### Example: Coq Natural Number Induction

**Proof script**:
```coq
Theorem plus_n_O : forall n, n + 0 = n.
Proof.
  induction n as [|n' IHn'].
  - reflexivity.
  - simpl. rewrite IHn'. reflexivity.
Qed.
```

**Summary**:
```
Proof by induction on n
├─ Base case: n = 0
│  └─ Reflexivity proves 0 + 0 = 0
└─ Inductive case: n = S n'
   ├─ IH: n' + 0 = n'
   └─ Simplify to S (n' + 0), rewrite with IH, then reflexivity
```

## Case Analysis Proofs

### Recognition Patterns

**Isabelle indicators**:
- `proof (cases ...)`
- Multiple `case` blocks without induction
- Pattern matching on constructors

**Coq indicators**:
- `destruct ... as [...]`
- Multiple `-` branches
- Case analysis without induction

### Summarization Template

```
Proof by case analysis on <variable>
├─ Case: <variable> = <constructor1>
│  └─ <how this case is proven>
├─ Case: <variable> = <constructor2>
│  └─ <how this case is proven>
└─ ...
```

### Example: Isabelle Option Case Analysis

**Proof script**:
```isabelle
lemma option_map_Some: "map_option f x = Some y ⟹ ∃z. x = Some z ∧ f z = y"
proof (cases x)
  case None
  then show ?thesis by simp
next
  case (Some z)
  then show ?thesis by auto
qed
```

**Summary**:
```
Proof by case analysis on x
├─ Case: x = None
│  └─ Contradiction: map_option f None ≠ Some y
└─ Case: x = Some z
   └─ Witness z satisfies x = Some z and f z = y
```

## Equational Reasoning

### Recognition Patterns

**Isabelle indicators**:
- Multiple `have` statements with equations
- `also ... finally` chains
- Explicit `subst` or rewriting

**Coq indicators**:
- Multiple `rewrite` steps
- `replace ... with ...`
- Equation chains

### Summarization Template

```
Equational reasoning
├─ Start: <initial_expression>
├─ = <step1> (by <justification1>)
├─ = <step2> (by <justification2>)
└─ = <final_expression> (goal)
```

### Example: Isabelle Calculation

**Proof script**:
```isabelle
lemma "2 * (n + 1) = 2 * n + 2"
proof -
  have "2 * (n + 1) = 2 * n + 2 * 1" by (simp add: algebra_simps)
  also have "... = 2 * n + 2" by simp
  finally show ?thesis .
qed
```

**Summary**:
```
Equational reasoning
├─ Start: 2 * (n + 1)
├─ = 2 * n + 2 * 1 (distributivity)
├─ = 2 * n + 2 (arithmetic)
└─ Goal established
```

## Lemma Application

### Recognition Patterns

**Isabelle indicators**:
- `using <lemmas>`
- `by (rule <lemma>)`
- `from <lemmas> have ...`

**Coq indicators**:
- `apply <lemma>`
- `pose proof <lemma>`
- `assert` with lemma reference

### Summarization Template

```
Apply lemma <lemma_name>
├─ Lemma states: <lemma_statement>
├─ Instantiate with: <parameters>
└─ Yields: <result>
```

### Example: Isabelle Lemma Application

**Proof script**:
```isabelle
lemma sorted_append_sorted:
  assumes "sorted xs" "sorted ys" "∀x∈set xs. ∀y∈set ys. x ≤ y"
  shows "sorted (xs @ ys)"
  using assms by (auto simp: sorted_append)
```

**Summary**:
```
Apply lemma sorted_append
├─ Assumptions: xs sorted, ys sorted, all xs elements ≤ all ys elements
└─ Conclusion: xs @ ys is sorted
```

## Automation-Heavy Proofs

### Recognition Patterns

**Isabelle indicators**:
- `by auto`, `by simp`, `by blast`, `by force`
- `sledgehammer` results
- Minimal manual steps

**Coq indicators**:
- `auto.`, `intuition.`, `tauto.`
- `lia.`, `nia.`, `omega.`
- Single-line proofs

### Summarization Template

```
Automated proof using <method>
└─ <brief description of what automation handles>
```

### Example: Isabelle Auto

**Proof script**:
```isabelle
lemma list_properties: "length xs = length ys ⟹ length (rev xs) = length (rev ys)"
  by auto
```

**Summary**:
```
Automated proof using auto
└─ Simplification with list lemmas establishes length preservation under reversal
```

## Nested Subproofs

### Recognition Patterns

**Isabelle indicators**:
- Multiple levels of `proof ... qed`
- Nested `have` statements
- Subgoal structure

**Coq indicators**:
- Nested `assert` blocks
- Multiple indentation levels
- Subgoal management with `{ ... }`

### Summarization Template

```
Main proof structure
├─ Subgoal 1: <statement>
│  ├─ Sub-subgoal 1.1: <statement>
│  │  └─ <proof>
│  └─ Sub-subgoal 1.2: <statement>
│     └─ <proof>
└─ Subgoal 2: <statement>
   └─ <proof>
```

### Example: Isabelle Nested Proof

**Proof script**:
```isabelle
lemma complex_property: "P x ∧ Q x ⟹ R x"
proof -
  assume "P x ∧ Q x"
  then have "P x" and "Q x" by simp_all
  have "R1 x"
  proof -
    from `P x` show ?thesis by (rule P_implies_R1)
  qed
  moreover have "R2 x"
  proof -
    from `Q x` show ?thesis by (rule Q_implies_R2)
  qed
  ultimately show "R x" by (rule R1_R2_implies_R)
qed
```

**Summary**:
```
Main proof: P x ∧ Q x ⟹ R x
├─ Extract: P x and Q x from conjunction
├─ Subproof 1: Prove R1 x
│  └─ Apply P_implies_R1 to P x
├─ Subproof 2: Prove R2 x
│  └─ Apply Q_implies_R2 to Q x
└─ Combine: Apply R1_R2_implies_R to get R x
```

## Proof Structure Recognition

### High-Level Structure Indicators

1. **Linear proof**: Sequential steps, each building on previous
2. **Branching proof**: Multiple cases or subgoals handled separately
3. **Hierarchical proof**: Nested subproofs with dependencies
4. **Calculational proof**: Chain of equations or inequalities
5. **Hybrid proof**: Combination of above patterns

### Summarization Strategy by Structure

**Linear**: List steps in order with brief justifications

**Branching**: Tree structure showing all branches

**Hierarchical**: Nested outline with indentation

**Calculational**: Equation chain with transformations

**Hybrid**: Combine appropriate formats for different sections
