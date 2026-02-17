# Common Proof Patterns and Lemma Categories

Catalog of frequently needed lemmas organized by proof pattern and domain.

## List Lemmas

### Append Lemmas

**Associativity and identity:**
```
append_nil_left: [] ++ xs = xs
append_nil_right: xs ++ [] = xs
append_assoc: (xs ++ ys) ++ zs = xs ++ (ys ++ zs)
```

**Length preservation:**
```
length_append: length (xs ++ ys) = length xs + length ys
```

**Interaction with other operations:**
```
map_append: map f (xs ++ ys) = map f xs ++ map f ys
filter_append: filter P (xs ++ ys) = filter P xs ++ filter P ys
reverse_append: reverse (xs ++ ys) = reverse ys ++ reverse xs
```

**When to use:** Proofs involving list concatenation, especially in induction steps.

### Map Lemmas

**Composition:**
```
map_id: map id xs = xs
map_compose: map f (map g xs) = map (f ∘ g) xs
map_append: map f (xs ++ ys) = map f xs ++ map f ys
```

**Length preservation:**
```
length_map: length (map f xs) = length xs
```

**Functoriality:**
```
map_ext: (∀x. f x = g x) → map f xs = map g xs
```

**When to use:** Proofs about transformations, function composition, or preserving structure.

### Filter Lemmas

**Idempotence:**
```
filter_filter: filter P (filter P xs) = filter P xs
filter_true: filter (λx. true) xs = xs
filter_false: filter (λx. false) xs = []
```

**Composition:**
```
filter_and: filter P (filter Q xs) = filter (λx. P x ∧ Q x) xs
```

**Length bounds:**
```
length_filter_le: length (filter P xs) ≤ length xs
```

**When to use:** Proofs about selection, filtering, or subset properties.

### Reverse Lemmas

**Involution:**
```
reverse_involutive: reverse (reverse xs) = xs
```

**Distribution:**
```
reverse_append: reverse (xs ++ ys) = reverse ys ++ reverse xs
reverse_singleton: reverse [x] = [x]
```

**Length preservation:**
```
length_reverse: length (reverse xs) = length xs
```

**When to use:** Proofs about symmetry, palindromes, or reversing operations.

### Fold Lemmas

**Universal property:**
```
fold_append: fold f (xs ++ ys) acc = fold f ys (fold f xs acc)
fold_map: fold f (map g xs) acc = fold (λa x. f a (g x)) xs acc
```

**Special cases:**
```
fold_nil: fold f [] acc = acc
fold_singleton: fold f [x] acc = f acc x
```

**When to use:** Proofs about aggregation, accumulation, or recursive computations.

## Arithmetic Lemmas

### Addition Lemmas

**Identity and commutativity:**
```
add_zero_left: 0 + n = n
add_zero_right: n + 0 = n
add_comm: m + n = n + m
add_assoc: (m + n) + p = m + (n + p)
```

**Cancellation:**
```
add_cancel_left: k + m = k + n → m = n
add_cancel_right: m + k = n + k → m = n
```

**Monotonicity:**
```
add_le_mono: m ≤ n → p ≤ q → m + p ≤ n + q
add_lt_mono: m < n → p < q → m + p < n + q
```

**When to use:** Arithmetic reasoning, especially with inequalities.

### Multiplication Lemmas

**Identity and annihilation:**
```
mult_zero_left: 0 * n = 0
mult_zero_right: n * 0 = 0
mult_one_left: 1 * n = n
mult_one_right: n * 1 = n
```

**Commutativity and associativity:**
```
mult_comm: m * n = n * m
mult_assoc: (m * n) * p = m * (n * p)
```

**Distributivity:**
```
mult_add_distr_left: m * (n + p) = m * n + m * p
mult_add_distr_right: (m + n) * p = m * p + n * p
```

**When to use:** Algebraic manipulation, especially with distributive laws.

### Ordering Lemmas

**Reflexivity, transitivity, antisymmetry:**
```
le_refl: n ≤ n
le_trans: m ≤ n → n ≤ p → m ≤ p
le_antisym: m ≤ n → n ≤ m → m = n
```

**Totality:**
```
le_total: m ≤ n ∨ n ≤ m
```

**Successor properties:**
```
le_succ: n ≤ n + 1
lt_succ: n < n + 1
succ_le_mono: m ≤ n → m + 1 ≤ n + 1
```

**When to use:** Comparison proofs, ordering arguments.

## Set and Map Lemmas

### Set Operations

**Union:**
```
union_empty_left: ∅ ∪ A = A
union_empty_right: A ∪ ∅ = A
union_comm: A ∪ B = B ∪ A
union_assoc: (A ∪ B) ∪ C = A ∪ (B ∪ C)
union_idempotent: A ∪ A = A
```

**Intersection:**
```
inter_empty_left: ∅ ∩ A = ∅
inter_empty_right: A ∩ ∅ = ∅
inter_comm: A ∩ B = B ∩ A
inter_assoc: (A ∩ B) ∩ C = A ∩ (B ∩ C)
inter_idempotent: A ∩ A = A
```

**Membership:**
```
mem_union: x ∈ A ∪ B ↔ x ∈ A ∨ x ∈ B
mem_inter: x ∈ A ∩ B ↔ x ∈ A ∧ x ∈ B
mem_diff: x ∈ A - B ↔ x ∈ A ∧ x ∉ B
```

**When to use:** Set-theoretic reasoning, membership proofs.

### Map Operations

**Lookup:**
```
lookup_empty: lookup k ∅ = None
lookup_insert_eq: lookup k (insert k v m) = Some v
lookup_insert_neq: k ≠ k' → lookup k (insert k' v m) = lookup k m
```

**Update:**
```
insert_insert: insert k v2 (insert k v1 m) = insert k v2 m
insert_comm: k ≠ k' → insert k v (insert k' v' m) = insert k' v' (insert k v m)
```

**When to use:** Dictionary/map reasoning, key-value proofs.

## Induction Strengthening Patterns

### Accumulator Pattern

**Problem:** Direct induction fails.

**Solution:** Add accumulator parameter.

**Example:**
```
(* Direct: fails *)
sum_formula: sum_upto n = n * (n + 1) / 2

(* With accumulator: succeeds *)
sum_formula_acc: sum_upto_acc n acc = acc + n * (n + 1) / 2
```

**When to use:** Tail-recursive functions, accumulating computations.

### Generalization Pattern

**Problem:** Statement too specific.

**Solution:** Generalize to arbitrary parameter.

**Example:**
```
(* Specific: fails *)
reverse_append_singleton: reverse (xs ++ [x]) = x :: reverse xs

(* General: succeeds *)
reverse_append: reverse (xs ++ ys) = reverse ys ++ reverse xs
```

**When to use:** When induction hypothesis doesn't cover needed cases.

### Simultaneous Induction Pattern

**Problem:** Need multiple properties together.

**Solution:** Prove conjunction of properties.

**Example:**
```
(* Separate: difficult *)
even_not_odd: even n → ¬ odd n
odd_not_even: odd n → ¬ even n

(* Together: easier *)
even_odd_exclusive: (even n ↔ ¬ odd n) ∧ (odd n ↔ ¬ even n)
```

**When to use:** Mutually recursive definitions, interdependent properties.

### Strengthening Pattern

**Problem:** Induction hypothesis too weak.

**Solution:** Prove stronger statement.

**Example:**
```
(* Weak: fails *)
sorted_insert: sorted xs → sorted (insert x xs)

(* Strong: succeeds *)
sorted_insert_strong: sorted xs → (∀y ∈ xs. y ≤ max_elem) →
  sorted (insert x xs) ∧ (∀y ∈ insert x xs. y ≤ max (x, max_elem))
```

**When to use:** When simple property insufficient for induction.

## Rewriting Patterns

### Definitional Unfolding

**Pattern:** Unfold definitions to expose structure.

**Example:**
```
comp_apply: (f ∘ g) x = f (g x)
id_apply: id x = x
const_apply: const c x = c
```

**When to use:** Simplification, exposing underlying operations.

### Conditional Rewriting

**Pattern:** Rewrite under specific conditions.

**Example:**
```
if_true: (if true then x else y) = x
if_false: (if false then x else y) = y
if_same: (if b then x else x) = x
```

**When to use:** Case analysis, conditional expressions.

### Associativity Rewriting

**Pattern:** Reassociate operations.

**Example:**
```
add_assoc: (m + n) + p = m + (n + p)
mult_assoc: (m * n) * p = m * (n * p)
append_assoc: (xs ++ ys) ++ zs = xs ++ (ys ++ zs)
```

**When to use:** Rearranging nested operations.

## Case Analysis Patterns

### Constructor Discrimination

**Pattern:** Different constructors are distinct.

**Example:**
```
nil_not_cons: [] ≠ x :: xs
zero_not_succ: 0 ≠ S n
true_not_false: true ≠ false
```

**When to use:** Contradiction proofs, constructor distinctness.

### Constructor Injectivity

**Pattern:** Constructors are injective.

**Example:**
```
cons_injective: x :: xs = y :: ys → x = y ∧ xs = ys
succ_injective: S m = S n → m = n
pair_injective: (a, b) = (c, d) → a = c ∧ b = d
```

**When to use:** Extracting information from equations.

### Exhaustiveness

**Pattern:** Cover all cases of a type.

**Example:**
```
list_cases: xs = [] ∨ (∃y ys. xs = y :: ys)
nat_cases: n = 0 ∨ (∃m. n = S m)
bool_cases: b = true ∨ b = false
```

**When to use:** Case analysis, covering all possibilities.

## Structural Lemmas

### Tree Lemmas

**Height:**
```
height_leaf: height Leaf = 0
height_node: height (Node l x r) = 1 + max (height l) (height r)
```

**Size:**
```
size_leaf: size Leaf = 0
size_node: size (Node l x r) = 1 + size l + size r
```

**Membership:**
```
mem_leaf: ¬ member x Leaf
mem_node: member x (Node l y r) ↔ x = y ∨ member x l ∨ member x r
```

**When to use:** Tree-based data structures, recursive structures.

### Graph Lemmas

**Path properties:**
```
path_refl: path x x
path_trans: path x y → path y z → path x z
path_edge: edge x y → path x y
```

**Reachability:**
```
reachable_refl: reachable x x
reachable_trans: reachable x y → reachable y z → reachable x z
```

**When to use:** Graph algorithms, connectivity proofs.

## Proof Strategy Selection

### When to Use Induction

- Recursive data structures (lists, trees, natural numbers)
- Recursive functions
- Properties that hold "for all elements"
- Structural properties

### When to Use Case Analysis

- Finite types (booleans, small enums)
- Conditional expressions
- Pattern matching
- Constructor discrimination

### When to Use Rewriting

- Equations and identities
- Simplification
- Substitution
- Definitional unfolding

### When to Use Contradiction

- Proving negations
- Impossibility results
- Constructor distinctness
- Inconsistent assumptions

## Lemma Naming Conventions

**Operation + Property:**
```
append_assoc, map_compose, filter_idempotent
```

**Type + Operation + Property:**
```
list_append_nil, nat_add_comm, bool_and_true
```

**Property + Type:**
```
sorted_list, even_nat, balanced_tree
```

**Descriptive names:**
```
length_filter_le, reverse_involutive, insert_preserves_sorted
```

## Common Proof Failures and Solutions

### Failure: Induction hypothesis too weak

**Solution:** Strengthen by generalizing or adding parameters.

### Failure: Missing intermediate step

**Solution:** Introduce lemma for intermediate property.

### Failure: Wrong induction variable

**Solution:** Try induction on different variable or use well-founded induction.

### Failure: Case not covered

**Solution:** Add exhaustiveness lemma or handle all cases.

### Failure: Circular reasoning

**Solution:** Reorder lemmas or use different proof strategy.

### Failure: Simplification stuck

**Solution:** Add rewrite lemmas or unfold definitions.
