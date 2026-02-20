# Isabelle/HOL Syntax Reference

Quick reference for Isabelle/HOL syntax when modeling functional programs.

## Basic Types

```isabelle
nat          -- Natural numbers (0, 1, 2, ...)
int          -- Integers
bool         -- Booleans (True, False)
'a           -- Type variable (polymorphic)
'a list      -- List of 'a elements
'a option    -- Optional value (None | Some x)
'a set       -- Set of 'a elements
'a ⇒ 'b      -- Function type (a to b)
'a × 'b      -- Product type (pairs)
```

## Data Types

```isabelle
datatype 'a tree = Leaf | Node "'a" "'a tree" "'a tree"
datatype 'a option = None | Some 'a
datatype ('a, 'b) either = Left 'a | Right 'b
```

## Function Definitions

### Simple Functions
```isabelle
fun factorial :: "nat ⇒ nat" where
  "factorial 0 = 1" |
  "factorial (Suc n) = Suc n * factorial n"
```

### Pattern Matching
```isabelle
fun length :: "'a list ⇒ nat" where
  "length [] = 0" |
  "length (x # xs) = 1 + length xs"
```

### Non-Primitive Recursion
```isabelle
function gcd :: "nat ⇒ nat ⇒ nat" where
  "gcd m n = (if n = 0 then m else gcd n (m mod n))"
by pat_completeness auto
termination by (relation "measure snd") auto
```

### Definitions (Non-Recursive)
```isabelle
definition compose :: "('b ⇒ 'c) ⇒ ('a ⇒ 'b) ⇒ ('a ⇒ 'c)" where
  "compose f g = (λx. f (g x))"
```

## List Operations

```isabelle
[]              -- Empty list
x # xs          -- Cons (prepend x to xs)
xs @ ys         -- Append
hd xs           -- Head (first element)
tl xs           -- Tail (rest of list)
length xs       -- Length
map f xs        -- Map function over list
filter p xs     -- Filter elements satisfying predicate
fold f acc xs   -- Left fold
foldr f xs acc  -- Right fold
rev xs          -- Reverse
set xs          -- Convert list to set
mset xs         -- Convert list to multiset
```

## Common Predicates

```isabelle
sorted xs                    -- List is sorted
distinct xs                  -- No duplicates
x ∈ set xs                   -- Element membership
mset xs = mset ys           -- Permutation (multiset equality)
∀x ∈ set xs. P x            -- All elements satisfy P
∃x ∈ set xs. P x            -- Some element satisfies P
```

## Logical Operators

```isabelle
¬ P              -- Negation (not P)
P ∧ Q            -- Conjunction (and)
P ∨ Q            -- Disjunction (or)
P ⟹ Q           -- Implication
P ⟷ Q           -- Bi-implication (iff)
∀x. P x          -- Universal quantification
∃x. P x          -- Existential quantification
```

## Set Operations

```isabelle
{}               -- Empty set
{x, y, z}        -- Finite set
x ∈ A            -- Membership
A ⊆ B            -- Subset
A ∪ B            -- Union
A ∩ B            -- Intersection
A - B            -- Difference
{x. P x}         -- Set comprehension
```

## Option Type

```isabelle
None                         -- No value
Some x                       -- Value x
case opt of None ⇒ ... | Some x ⇒ ...
```

## Lambda Expressions

```isabelle
λx. x + 1                    -- Lambda (anonymous function)
λx y. x + y                  -- Multi-argument lambda
```

## Case Expressions

```isabelle
case xs of
  [] ⇒ 0 |
  (x # xs) ⇒ x + sum xs

case tree of
  Leaf ⇒ 0 |
  Node v l r ⇒ 1 + size l + size r
```

## Let Bindings

```isabelle
let x = expr1 in expr2
let x = expr1; y = expr2 in expr3
```

## Common Lemma Patterns

### Induction
```isabelle
lemma "P xs"
proof (induction xs)
  case Nil
  show ?case ...
next
  case (Cons x xs)
  show ?case ...
qed
```

### Case Analysis
```isabelle
lemma "P x"
proof (cases x)
  case None
  show ?thesis ...
next
  case (Some y)
  show ?thesis ...
qed
```

### Structural Properties
```isabelle
lemma length_append: "length (xs @ ys) = length xs + length ys"
lemma map_compose: "map f (map g xs) = map (f ∘ g) xs"
lemma filter_filter: "filter p (filter q xs) = filter (λx. p x ∧ q x) xs"
```

## Type Classes

```isabelle
'a::ord          -- Ordered type (has ≤, <)
'a::linorder     -- Linear order (total order)
'a::zero         -- Has zero element
'a::one          -- Has one element
'a::plus         -- Has addition
'a::times        -- Has multiplication
```

## Useful Functions

```isabelle
min x y          -- Minimum
max x y          -- Maximum
abs x            -- Absolute value
x div y          -- Integer division
x mod y          -- Modulo
x ^ n            -- Exponentiation
sum_list xs      -- Sum of list elements
prod_list xs     -- Product of list elements
zip xs ys        -- Zip two lists
take n xs        -- First n elements
drop n xs        -- Drop first n elements
```
