# Isabelle/HOL Proof Tactics and Patterns

## Table of Contents
1. Basic Proof Structure
2. Common Tactics
3. Proof Patterns by Type
4. Induction Patterns
5. Case Analysis Patterns

## 1. Basic Proof Structure

### Simple Proof
```isabelle
theorem theorem_name:
  "statement"
  by tactic
```

### Structured Proof (Isar)
```isabelle
theorem theorem_name:
  "statement"
proof -
  (* proof steps *)
  show ?thesis by tactic
qed
```

### Proof with Assumptions
```isabelle
theorem theorem_name:
  assumes "assumption1" "assumption2"
  shows "conclusion"
proof -
  (* proof steps *)
qed
```

## 2. Common Tactics

### Automatic Tactics
- `auto` - Automatic proof search with simplification
- `simp` - Simplification using rewrite rules
- `blast` - Fast tableau prover
- `fastforce` - Combination of fast and force
- `force` - More powerful than auto
- `clarsimp` - Clarification + simplification
- `sledgehammer` - Invoke external provers (comment in skeleton)

### Manual Tactics
- `rule` - Apply a rule
- `erule` - Elimination rule
- `drule` - Destruction rule
- `subst` - Substitution
- `unfold` - Unfold definitions

### Structural Tactics
- `induction` - Proof by induction
- `cases` - Case analysis
- `split` - Split on conditionals

## 3. Proof Patterns by Type

### Equality Proofs
```isabelle
theorem equality_example:
  "f x = g x"
proof -
  have "f x = intermediate" by simp
  also have "... = g x" by simp
  finally show ?thesis .
qed
```

### Implication Proofs
```isabelle
theorem implication_example:
  assumes "P"
  shows "Q"
proof -
  from assms have "intermediate" by simp
  then show ?thesis by simp
qed
```

### Universal Quantification
```isabelle
theorem forall_example:
  "∀x. P x ⟶ Q x"
proof (intro allI impI)
  fix x
  assume "P x"
  (* prove Q x *)
  show "Q x" sorry
qed
```

### Existential Quantification
```isabelle
theorem exists_example:
  "∃x. P x"
proof -
  have "P witness" sorry
  then show ?thesis by blast
qed
```

## 4. Induction Patterns

### List Induction
```isabelle
theorem list_theorem:
  "P xs"
proof (induction xs)
  case Nil
  (* Base case: P [] *)
  show ?case sorry
next
  case (Cons x xs)
  (* Inductive case: P xs ⟹ P (x # xs) *)
  (* IH: Cons.IH is "P xs" *)
  show ?case sorry
qed
```

### Natural Number Induction
```isabelle
theorem nat_theorem:
  "P n"
proof (induction n)
  case 0
  (* Base case: P 0 *)
  show ?case sorry
next
  case (Suc n)
  (* Inductive case: P n ⟹ P (Suc n) *)
  (* IH: Suc.IH is "P n" *)
  show ?case sorry
qed
```

### Structural Induction (Custom Types)
```isabelle
theorem tree_theorem:
  "P t"
proof (induction t)
  case Leaf
  show ?case sorry
next
  case (Node l x r)
  (* IH: Node.IH(1) is "P l", Node.IH(2) is "P r" *)
  show ?case sorry
qed
```

## 5. Case Analysis Patterns

### Boolean Case Split
```isabelle
theorem bool_cases:
  "P b"
proof (cases b)
  case True
  (* Assume b = True *)
  show ?thesis sorry
next
  case False
  (* Assume b = False *)
  show ?thesis sorry
qed
```

### Option Case Split
```isabelle
theorem option_cases:
  "P opt"
proof (cases opt)
  case None
  show ?thesis sorry
next
  case (Some x)
  (* opt = Some x *)
  show ?thesis sorry
qed
```

### Custom Datatype Cases
```isabelle
theorem datatype_cases:
  "P x"
proof (cases x)
  case Constructor1
  show ?thesis sorry
next
  case (Constructor2 arg1 arg2)
  show ?thesis sorry
qed
```

## Key Proof Strategies

### Forward Reasoning
Use `have` to establish intermediate facts:
```isabelle
proof -
  have step1: "fact1" by simp
  have step2: "fact2" using step1 by simp
  show ?thesis using step2 by simp
qed
```

### Backward Reasoning
Use `show` with subgoals:
```isabelle
proof -
  show ?thesis
  proof (rule some_rule)
    show "subgoal1" sorry
    show "subgoal2" sorry
  qed
qed
```

### Using Assumptions
```isabelle
proof -
  from assms have "derived_fact" by simp
  with additional_fact have "another_fact" by simp
  using all_facts show ?thesis by simp
qed
```
