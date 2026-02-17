---
name: program-to-model-extractor
description: "Extract abstract mathematical models from functional code (Haskell, OCaml, F#) for formal reasoning in Isabelle/HOL. Use when users need to: (1) Convert functional programs to Isabelle definitions, (2) Extract high-level algorithm essence from implementation code, (3) Generate formal specifications and properties from code, (4) Create verification-ready models that capture mathematical properties while abstracting away implementation details. Focuses on structural recursion, algebraic data types, higher-order functions, and invariant extraction."
---

# Program-to-Model Extractor

Extract high-level mathematical models from functional code for formal reasoning in Isabelle/HOL.

## Overview

This skill transforms functional programs (Haskell, OCaml, F#) into abstract mathematical models suitable for formal verification in Isabelle/HOL. The extraction focuses on the algorithm's mathematical essence—capturing core properties, invariants, and structural patterns while abstracting away language-specific implementation details.

## Extraction Workflow

### 1. Analyze the Source Code

Identify key elements:
- **Data structures**: Algebraic types, lists, trees, custom types
- **Core functions**: Main computational logic
- **Recursion patterns**: Structural, tail, mutual recursion
- **Properties**: What should be true about inputs/outputs?

### 2. Extract Data Types

Convert source language types to Isabelle datatypes:

```haskell
-- Haskell
data Tree a = Leaf | Node a (Tree a) (Tree a)
```

```isabelle
(* Isabelle *)
datatype 'a tree = Leaf | Node "'a" "'a tree" "'a tree"
```

### 3. Model Functions

Choose the appropriate Isabelle construct:

**For primitive recursion** (terminates obviously):
```isabelle
fun length :: "'a list ⇒ nat" where
  "length [] = 0" |
  "length (x # xs) = 1 + length xs"
```

**For general recursion** (needs termination proof):
```isabelle
function gcd :: "nat ⇒ nat ⇒ nat" where
  "gcd m n = (if n = 0 then m else gcd n (m mod n))"
by pat_completeness auto
termination by (relation "measure snd") auto
```

**For non-recursive definitions**:
```isabelle
definition compose :: "('b ⇒ 'c) ⇒ ('a ⇒ 'b) ⇒ ('a ⇒ 'c)" where
  "compose f g = (λx. f (g x))"
```

### 4. State Properties

Extract and formalize key properties as lemmas:

```isabelle
lemma length_append: "length (xs @ ys) = length xs + length ys"
lemma quicksort_permutes: "mset (quicksort xs) = mset xs"
lemma quicksort_sorted: "sorted (quicksort xs)"
```

### 5. Identify Invariants

For stateful or accumulator-based functions, state what holds during computation:

```isabelle
fun sum_acc :: "int ⇒ int list ⇒ int" where
  "sum_acc acc [] = acc" |
  "sum_acc acc (x # xs) = sum_acc (acc + x) xs"

lemma sum_acc_correct: "sum_acc acc xs = acc + sum_list xs"
```

## Common Extraction Patterns

### List Processing

**Source**: Recursive list operations
**Model**: Isabelle list functions with length/permutation properties
**See**: [extraction_patterns.md](references/extraction_patterns.md#pattern-1-list-operations)

### Sorting Algorithms

**Source**: Comparison-based sorting
**Model**: Functions with `sorted` and `mset` (permutation) properties
**See**: [extraction_patterns.md](references/extraction_patterns.md#pattern-2-sorting-and-permutations)

### Tree Operations

**Source**: Recursive tree traversals and folds
**Model**: Isabelle datatypes with structural recursion
**See**: [extraction_patterns.md](references/extraction_patterns.md#pattern-3-tree-structures)

### Higher-Order Functions

**Source**: map, filter, fold, composition
**Model**: Isabelle higher-order definitions with fusion lemmas
**See**: [extraction_patterns.md](references/extraction_patterns.md#pattern-4-higher-order-functions)

### Partial Functions

**Source**: Functions that may fail (division, lookup)
**Model**: Option types with case analysis
**See**: [extraction_patterns.md](references/extraction_patterns.md#pattern-5-monadic-operations)

### Tail Recursion

**Source**: Accumulator-based functions
**Model**: Functions with accumulator correctness lemmas
**See**: [extraction_patterns.md](references/extraction_patterns.md#pattern-6-accumulation-and-state)

## Abstraction Guidelines

Focus on **high-level mathematical essence**:

✓ **Do extract**:
- Core algorithm structure
- Mathematical properties (sorted, permutation, etc.)
- Invariants and pre/post-conditions
- Structural recursion patterns
- Type relationships

✗ **Don't extract**:
- Performance optimizations
- Language-specific syntax details
- Implementation tricks
- Memory layout concerns
- Specific evaluation strategies

## Example: Complete Extraction

**Source (Haskell)**:
```haskell
quicksort :: Ord a => [a] -> [a]
quicksort [] = []
quicksort (p:xs) = quicksort lesser ++ [p] ++ quicksort greater
  where lesser  = filter (< p) xs
        greater = filter (>= p) xs
```

**Extracted Model (Isabelle)**:
```isabelle
fun quicksort :: "'a::linorder list ⇒ 'a list" where
  "quicksort [] = []" |
  "quicksort (p # xs) =
     quicksort (filter (λx. x < p) xs) @ [p] @
     quicksort (filter (λx. x ≥ p) xs)"

(* Key properties *)
lemma quicksort_permutes: "mset (quicksort xs) = mset xs"
lemma quicksort_sorted: "sorted (quicksort xs)"
lemma quicksort_correct:
  "sorted (quicksort xs) ∧ mset (quicksort xs) = mset xs"
```

**Explanation**:
- Converted type constraint `Ord a` to `'a::linorder`
- Preserved structural recursion pattern
- Extracted two key properties: permutation and sortedness
- Combined into correctness specification

## References

- **[extraction_patterns.md](references/extraction_patterns.md)**: Detailed patterns for common functional programming constructs
- **[isabelle_syntax.md](references/isabelle_syntax.md)**: Quick reference for Isabelle/HOL syntax

## Tips

- Start with the simplest functions first to build up the model incrementally
- Use `mset` (multisets) to express permutation properties elegantly
- For complex recursion, explicitly state the termination measure
- Group related lemmas together (e.g., all properties of a single function)
- Use meaningful names that reflect mathematical concepts, not implementation details
