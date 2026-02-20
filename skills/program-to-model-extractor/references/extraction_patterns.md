# Extraction Patterns for Mathematical Models

This reference provides patterns for extracting high-level mathematical models from functional code for Isabelle/HOL reasoning.

## Core Extraction Principles

1. **Focus on essence**: Extract the mathematical properties and invariants, not implementation details
2. **Abstract away syntax**: Convert language-specific constructs to mathematical notation
3. **Preserve semantics**: Ensure the model captures the intended behavior
4. **Identify invariants**: Highlight pre/post-conditions and loop invariants

## Pattern 1: List Operations

### Source Pattern (Haskell/OCaml/F#)
```haskell
-- Recursive list processing
process :: [a] -> [b]
process [] = []
process (x:xs) = f x : process xs
```

### Isabelle Model
```isabelle
fun process :: "'a list ⇒ 'b list" where
  "process [] = []" |
  "process (x # xs) = f x # process xs"

lemma process_length: "length (process xs) = length xs"
lemma process_preserves: "∀x ∈ set xs. P x ⟹ ∀y ∈ set (process xs). Q y"
```

**Key extractions:**
- Structural recursion → Isabelle function definition
- Length preservation property
- Element-wise property preservation

## Pattern 2: Sorting and Permutations

### Source Pattern
```haskell
quicksort :: Ord a => [a] -> [a]
quicksort [] = []
quicksort (p:xs) = quicksort lesser ++ [p] ++ quicksort greater
  where lesser  = filter (< p) xs
        greater = filter (>= p) xs
```

### Isabelle Model
```isabelle
fun quicksort :: "'a::linorder list ⇒ 'a list" where
  "quicksort [] = []" |
  "quicksort (p # xs) =
     quicksort (filter (λx. x < p) xs) @ [p] @
     quicksort (filter (λx. x ≥ p) xs)"

lemma quicksort_permutes: "mset (quicksort xs) = mset xs"
lemma quicksort_sorted: "sorted (quicksort xs)"
lemma quicksort_correct: "sorted (quicksort xs) ∧ mset (quicksort xs) = mset xs"
```

**Key extractions:**
- Partition logic → filter operations
- Sorting property → `sorted` predicate
- Permutation property → multiset equality

## Pattern 3: Tree Structures

### Source Pattern
```ocaml
type 'a tree = Leaf | Node of 'a * 'a tree * 'a tree

let rec fold f acc = function
  | Leaf -> acc
  | Node (v, l, r) -> f v (fold f acc l) (fold f acc r)
```

### Isabelle Model
```isabelle
datatype 'a tree = Leaf | Node "'a" "'a tree" "'a tree"

fun fold :: "('a ⇒ 'b ⇒ 'b ⇒ 'b) ⇒ 'b ⇒ 'a tree ⇒ 'b" where
  "fold f acc Leaf = acc" |
  "fold f acc (Node v l r) = f v (fold f acc l) (fold f acc r)"

lemma fold_linear: "fold (λv l r. l + r + 1) 0 t = size t"
lemma fold_commutative: "comm f ⟹ fold f acc t = fold f acc (mirror t)"
```

**Key extractions:**
- Algebraic data type → Isabelle datatype
- Structural recursion → pattern matching
- Accumulation invariants → lemmas about fold behavior

## Pattern 4: Higher-Order Functions

### Source Pattern
```fsharp
let compose f g x = f (g x)
let pipeline xs = xs |> List.filter p |> List.map f |> List.fold (+) 0
```

### Isabelle Model
```isabelle
definition compose :: "('b ⇒ 'c) ⇒ ('a ⇒ 'b) ⇒ ('a ⇒ 'c)" where
  "compose f g = (λx. f (g x))"

definition pipeline :: "'a list ⇒ int" where
  "pipeline xs = fold (+) 0 (map f (filter p xs))"

lemma compose_assoc: "compose f (compose g h) = compose (compose f g) h"
lemma pipeline_fusion: "pipeline xs = fold (λx acc. if p x then acc + f x else acc) 0 xs"
```

**Key extractions:**
- Function composition → mathematical composition
- Pipeline operations → nested function applications
- Fusion opportunities → optimized single-pass lemmas

## Pattern 5: Monadic Operations

### Source Pattern
```haskell
safeDivide :: Int -> Int -> Maybe Int
safeDivide _ 0 = Nothing
safeDivide x y = Just (x `div` y)

chain :: Maybe a -> (a -> Maybe b) -> Maybe b
chain Nothing _ = Nothing
chain (Just x) f = f x
```

### Isabelle Model
```isabelle
fun safeDivide :: "int ⇒ int ⇒ int option" where
  "safeDivide x 0 = None" |
  "safeDivide x y = Some (x div y)"

definition chain :: "'a option ⇒ ('a ⇒ 'b option) ⇒ 'b option" where
  "chain mx f = (case mx of None ⇒ None | Some x ⇒ f x)"

lemma chain_none: "chain None f = None"
lemma chain_some: "chain (Some x) f = f x"
lemma chain_assoc: "chain (chain m f) g = chain m (λx. chain (f x) g)"
```

**Key extractions:**
- Partial functions → option types
- Monadic bind → case analysis
- Monad laws → associativity and identity lemmas

## Pattern 6: Accumulation and State

### Source Pattern
```ocaml
let rec sum_with_state acc = function
  | [] -> acc
  | x::xs -> sum_with_state (acc + x) xs

let factorial n =
  let rec aux acc n =
    if n <= 1 then acc else aux (acc * n) (n - 1)
  in aux 1 n
```

### Isabelle Model
```isabelle
fun sum_with_state :: "int ⇒ int list ⇒ int" where
  "sum_with_state acc [] = acc" |
  "sum_with_state acc (x # xs) = sum_with_state (acc + x) xs"

lemma sum_accumulates: "sum_with_state acc xs = acc + sum_list xs"

function factorial_aux :: "int ⇒ int ⇒ int" where
  "factorial_aux acc n = (if n ≤ 1 then acc else factorial_aux (acc * n) (n - 1))"
by pat_completeness auto
termination by (relation "measure snd") auto

definition factorial :: "int ⇒ int" where
  "factorial n = factorial_aux 1 n"

lemma factorial_correct: "n ≥ 0 ⟹ factorial n = fact n"
```

**Key extractions:**
- Tail recursion → accumulator pattern
- Termination argument → measure function
- Correctness → equivalence to mathematical definition

## Extraction Workflow

1. **Identify the core algorithm**: What is the essential computation?
2. **Extract data structures**: Convert to Isabelle datatypes
3. **Model the function**: Use `fun`, `function`, or `definition`
4. **State properties**: What should be true about the result?
5. **Add invariants**: What holds during computation?
6. **Prove correctness**: Relate to mathematical specification
