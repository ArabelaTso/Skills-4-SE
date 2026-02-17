# Isabelle/HOL Specification Patterns

## Table of Contents
1. Function Definitions
2. Data Type Definitions
3. Predicates and Properties
4. Pre/Post-conditions and Invariants
5. Common Patterns and Idioms

## 1. Function Definitions

### Basic Function Definition
```isabelle
fun function_name :: "type1 ⇒ type2 ⇒ return_type" where
  "function_name x y = expression"
```

### Recursive Function with Pattern Matching
```isabelle
fun length :: "'a list ⇒ nat" where
  "length [] = 0" |
  "length (x # xs) = 1 + length xs"
```

### Function with Multiple Clauses
```isabelle
fun max :: "nat ⇒ nat ⇒ nat" where
  "max x y = (if x ≥ y then x else y)"
```

## 2. Data Type Definitions

### Simple Algebraic Data Type
```isabelle
datatype 'a option = None | Some 'a
```

### Recursive Data Type
```isabelle
datatype 'a tree = Leaf | Node "'a tree" 'a "'a tree"
```

### Record Type
```isabelle
record person =
  name :: string
  age :: nat
```

## 3. Predicates and Properties

### Simple Predicate
```isabelle
definition is_sorted :: "nat list ⇒ bool" where
  "is_sorted xs ≡ (∀i j. i < j ∧ j < length xs ⟶ xs ! i ≤ xs ! j)"
```

### Inductive Predicate
```isabelle
inductive sorted :: "nat list ⇒ bool" where
  sorted_nil: "sorted []" |
  sorted_single: "sorted [x]" |
  sorted_cons: "⟦x ≤ y; sorted (y # ys)⟧ ⟹ sorted (x # y # ys)"
```

## 4. Pre/Post-conditions and Invariants

### Function Specification with Pre/Post-conditions
```isabelle
definition sort_spec :: "nat list ⇒ nat list ⇒ bool" where
  "sort_spec xs ys ≡
    is_sorted ys ∧
    set xs = set ys ∧
    length xs = length ys"
```

### Loop Invariant Pattern
```isabelle
definition loop_invariant :: "nat ⇒ nat list ⇒ bool" where
  "loop_invariant i xs ≡
    i ≤ length xs ∧
    (∀j k. j < k ∧ k < i ⟶ xs ! j ≤ xs ! k)"
```

## 5. Common Patterns and Idioms

### Correctness Theorem
```isabelle
theorem function_correct:
  "precondition input ⟹ postcondition (function input)"
```

### Termination Measure
```isabelle
function f :: "nat ⇒ nat" where
  "f 0 = 0" |
  "f (Suc n) = f n + 1"
by pat_completeness auto
termination by (relation "measure id") auto
```

### Quantifiers and Logical Operators
- Universal: `∀x. P x` or `⋀x. P x`
- Existential: `∃x. P x`
- Implication: `P ⟶ Q` or `P ⟹ Q`
- Conjunction: `P ∧ Q`
- Disjunction: `P ∨ Q`
- Negation: `¬P`
- Equivalence: `P ⟷ Q` or `P ≡ Q`

### List Operations
- Empty list: `[]`
- Cons: `x # xs`
- Append: `xs @ ys`
- Length: `length xs`
- Nth element: `xs ! n`
- Set conversion: `set xs`
- Map: `map f xs`
- Filter: `filter P xs`
- Fold: `fold f xs init`
