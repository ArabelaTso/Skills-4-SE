# Isabelle/HOL Standard Library Guide

## Table of Contents
1. Core Theories
2. List Theory
3. Set Theory
4. Arithmetic Theories
5. Option and Sum Types
6. Common Lemmas by Category

## 1. Core Theories

### Main
The base theory, automatically imported.

**Key lemmas**:
- `refl`: `x = x`
- `sym`: `x = y ⟹ y = x`
- `trans`: `x = y ⟹ y = z ⟹ x = z`
- `subst`: `x = y ⟹ P x ⟹ P y`

### HOL
Higher-order logic foundations.

**Key lemmas**:
- `conjI`: `P ⟹ Q ⟹ P ∧ Q`
- `conjE`: `P ∧ Q ⟹ (P ⟹ Q ⟹ R) ⟹ R`
- `disjI1`: `P ⟹ P ∨ Q`
- `disjI2`: `Q ⟹ P ∨ Q`
- `impI`: `(P ⟹ Q) ⟹ P ⟶ Q`
- `mp`: `P ⟶ Q ⟹ P ⟹ Q`
- `allI`: `(⋀x. P x) ⟹ ∀x. P x`
- `exI`: `P x ⟹ ∃x. P x`

## 2. List Theory

**Import**: `imports Main` (included by default)

### Basic Operations

**Constructors**:
- `[]`: Empty list
- `x # xs`: Cons

**Functions**:
- `hd :: 'a list ⇒ 'a`: Head
- `tl :: 'a list ⇒ 'a list`: Tail
- `length :: 'a list ⇒ nat`: Length
- `rev :: 'a list ⇒ 'a list`: Reverse
- `@ :: 'a list ⇒ 'a list ⇒ 'a list`: Append
- `! :: 'a list ⇒ nat ⇒ 'a`: Nth element
- `take :: nat ⇒ 'a list ⇒ 'a list`: Take first n
- `drop :: nat ⇒ 'a list ⇒ 'a list`: Drop first n
- `map :: ('a ⇒ 'b) ⇒ 'a list ⇒ 'b list`: Map
- `filter :: ('a ⇒ bool) ⇒ 'a list ⇒ 'a list`: Filter
- `fold :: ('a ⇒ 'b ⇒ 'b) ⇒ 'a list ⇒ 'b ⇒ 'b`: Fold

### Key Lemmas

**Length**:
- `length_Nil`: `length [] = 0`
- `length_Cons`: `length (x # xs) = Suc (length xs)`
- `length_append`: `length (xs @ ys) = length xs + length ys`
- `length_rev`: `length (rev xs) = length xs`
- `length_map`: `length (map f xs) = length xs`

**Append**:
- `append_Nil`: `[] @ xs = xs`
- `append_Nil2`: `xs @ [] = xs`
- `append_assoc`: `(xs @ ys) @ zs = xs @ (ys @ zs)`
- `append_Cons`: `(x # xs) @ ys = x # (xs @ ys)`

**Reverse**:
- `rev_rev_ident`: `rev (rev xs) = xs`
- `rev_append`: `rev (xs @ ys) = rev ys @ rev xs`
- `rev_map`: `rev (map f xs) = map f (rev xs)`

**Map**:
- `map_append`: `map f (xs @ ys) = map f xs @ map f ys`
- `map_map`: `map f (map g xs) = map (f ∘ g) xs`
- `map_ident`: `map id xs = xs`

**Set Conversion**:
- `set_empty`: `set [] = {}`
- `set_append`: `set (xs @ ys) = set xs ∪ set ys`
- `set_rev`: `set (rev xs) = set xs`
- `set_map`: `set (map f xs) = f ` set xs`

**Membership**:
- `in_set_member`: `x ∈ set xs ⟷ (∃i < length xs. xs ! i = x)`
- `hd_in_set`: `xs ≠ [] ⟹ hd xs ∈ set xs`

## 3. Set Theory

**Import**: `imports Main`

### Basic Operations

**Constructors**:
- `{}`: Empty set
- `{x}`: Singleton
- `{x, y, z}`: Finite set

**Operations**:
- `∪`: Union
- `∩`: Intersection
- `-`: Difference
- `⊆`: Subset
- `∈`: Membership
- `card`: Cardinality

### Key Lemmas

**Basic**:
- `empty_iff`: `x ∈ {} ⟷ False`
- `insert_iff`: `x ∈ insert y A ⟷ x = y ∨ x ∈ A`
- `Un_iff`: `x ∈ A ∪ B ⟷ x ∈ A ∨ x ∈ B`
- `Int_iff`: `x ∈ A ∩ B ⟷ x ∈ A ∧ x ∈ B`

**Subset**:
- `subset_refl`: `A ⊆ A`
- `subset_trans`: `A ⊆ B ⟹ B ⊆ C ⟹ A ⊆ C`
- `subset_antisym`: `A ⊆ B ⟹ B ⊆ A ⟹ A = B`

**Union/Intersection**:
- `Un_commute`: `A ∪ B = B ∪ A`
- `Un_assoc`: `(A ∪ B) ∪ C = A ∪ (B ∪ C)`
- `Int_commute`: `A ∩ B = B ∩ A`
- `Int_assoc`: `(A ∩ B) ∩ C = A ∩ (B ∩ C)`

## 4. Arithmetic Theories

### Nat (Natural Numbers)

**Import**: `imports Main`

**Operations**:
- `+`: Addition
- `-`: Subtraction (saturating)
- `*`: Multiplication
- `div`, `mod`: Division and modulo
- `<`, `≤`: Ordering

**Key Lemmas**:
- `add_0`: `0 + n = n`
- `add_Suc`: `Suc m + n = Suc (m + n)`
- `add_commute`: `m + n = n + m`
- `add_assoc`: `(m + n) + k = m + (n + k)`
- `mult_0`: `0 * n = 0`
- `mult_Suc`: `Suc m * n = n + m * n`
- `mult_commute`: `m * n = n * m`
- `mult_assoc`: `(m * n) * k = m * (n * k)`
- `add_mult_distrib`: `(m + n) * k = m * k + n * k`

### Int (Integers)

**Import**: `imports "HOL-Library.Int"`

**Key Lemmas**:
- Similar to Nat but without saturation
- `int_distrib`: Conversion lemmas

### Real

**Import**: `imports "HOL-Analysis.Analysis"`

**Key Lemmas**:
- Field properties
- Ordering properties
- Absolute value lemmas

## 5. Option and Sum Types

### Option

**Constructors**:
- `None`
- `Some x`

**Functions**:
- `the :: 'a option ⇒ 'a`: Extract value
- `map_option :: ('a ⇒ 'b) ⇒ 'a option ⇒ 'b option`

**Key Lemmas**:
- `option.distinct`: `None ≠ Some x`
- `option.inject`: `Some x = Some y ⟹ x = y`

### Sum Types

**Constructors**:
- `Inl :: 'a ⇒ 'a + 'b`
- `Inr :: 'b ⇒ 'a + 'b`

## 6. Common Lemmas by Category

### Equality and Substitution

When proving: `x = y`
- `refl`, `sym`, `trans`
- `subst`: Substitute in context
- `arg_cong`: `x = y ⟹ f x = f y`
- `fun_cong`: `f = g ⟹ f x = g x`

### Conjunction and Disjunction

When proving: `P ∧ Q`
- `conjI`: Split into two goals

When proving: `P ∨ Q`
- `disjI1`, `disjI2`: Choose which side

When using: `P ∧ Q`
- `conjunct1`, `conjunct2`: Extract parts

### Implication

When proving: `P ⟶ Q`
- `impI`: Assume P, prove Q

When using: `P ⟶ Q` and `P`
- `mp`: Modus ponens

### Quantifiers

When proving: `∀x. P x`
- `allI`: Fix arbitrary x

When proving: `∃x. P x`
- `exI`: Provide witness

When using: `∀x. P x`
- `spec`: Instantiate with specific value

### Induction

For lists:
- `list.induct`: Structural induction

For natural numbers:
- `nat_induct`: Mathematical induction
- `nat_less_induct`: Strong induction

### Arithmetic

For linear arithmetic:
- `arith`: Automatic arithmetic solver
- `linarith`: Linear arithmetic

For simplification:
- `simp add: algebra_simps`: Algebraic simplifications

## Finding Lemmas

### Using find_theorems

```isabelle
find_theorems "rev (rev _) = _"
find_theorems name: "append" "_ @ _ = _"
find_theorems "length" "map"
```

### Using sledgehammer

```isabelle
lemma "length (rev xs) = length xs"
  sledgehammer
  (* Suggests: by simp *)
```

### Common Search Patterns

- List properties: `find_theorems "length" "append"`
- Arithmetic: `find_theorems "_ + _ = _ + _"`
- Set operations: `find_theorems "_ ∪ _ = _ ∪ _"`
- Membership: `find_theorems "_ ∈ set _"`
