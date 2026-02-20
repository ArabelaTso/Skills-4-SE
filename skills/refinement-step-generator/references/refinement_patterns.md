# Common Refinement Patterns

Catalog of frequently used refinement patterns across different domains.

## Data Structure Refinement

### Set Refinements

#### Set → List

**When to use:** Simple set operations, small sets, order doesn't matter.

**Abstraction:**
```
α(xs) = set(xs)
```

**Operations:**
- Empty: `[] ↔ ∅`
- Insert: `x :: xs ↔ {x} ∪ S`
- Member: `x ∈ set(xs) ↔ x ∈ S`
- Union: `xs ++ ys ↔ S₁ ∪ S₂`

**Proof obligations:**
- Preserve set semantics
- Handle duplicates correctly

**Example (Isabelle):**
```isabelle
definition set_insert_list :: "'a ⇒ 'a list ⇒ 'a list" where
  "set_insert_list x xs = (if x ∈ set xs then xs else x # xs)"

lemma "set (set_insert_list x xs) = insert x (set xs)"
  by (auto simp: set_insert_list_def)
```

#### Set → Sorted List

**When to use:** Need efficient membership testing, maintain order.

**Abstraction:**
```
α(xs) = set(xs) where sorted(xs)
```

**Operations:**
- Insert: Binary search insertion
- Member: Binary search
- Union: Merge operation

**Invariant:** List remains sorted after each operation.

#### Set → Binary Search Tree

**When to use:** Efficient insert/lookup, balanced operations.

**Abstraction:**
```
α(tree) = {x | x in tree}
```

**Operations:**
- Insert: O(log n) average
- Member: O(log n) average
- Delete: O(log n) average

**Invariant:** BST property maintained.

#### Set → Hash Set

**When to use:** Very large sets, constant-time operations needed.

**Abstraction:**
```
α(buckets) = ⋃ᵢ set(buckets[i])
```

**Operations:**
- Insert: O(1) average
- Member: O(1) average
- Collision handling required

### Map Refinements

#### Map → Association List

**When to use:** Small maps, simple implementation.

**Abstraction:**
```
α([(k₁,v₁), ..., (kₙ,vₙ)]) = {k₁ ↦ v₁, ..., kₙ ↦ vₙ}
```

**Operations:**
- Lookup: Linear search
- Update: Prepend new binding
- Delete: Filter out key

**Example (Coq):**
```coq
Fixpoint alist_lookup {K V} (eq : K -> K -> bool) (k : K) (al : list (K * V)) :=
  match al with
  | [] => None
  | (k', v) :: rest => if eq k k' then Some v else alist_lookup eq k rest
  end.
```

#### Map → Binary Search Tree Map

**When to use:** Ordered keys, efficient operations.

**Abstraction:**
```
α(tree) = {k ↦ v | (k,v) in tree}
```

**Operations:**
- Lookup: O(log n)
- Update: O(log n)
- Ordered iteration possible

#### Map → Hash Map

**When to use:** Large maps, no ordering needed.

**Abstraction:**
```
α(buckets) = ⋃ᵢ map_of(buckets[i])
```

**Operations:**
- Lookup: O(1) average
- Update: O(1) average
- Hash function required

### Sequence Refinements

#### Sequence → Array

**When to use:** Random access, fixed size.

**Abstraction:**
```
α(arr) = [arr[0], arr[1], ..., arr[n-1]]
```

**Operations:**
- Index: O(1)
- Update: O(1)
- Length: O(1)

**Constraint:** Fixed size after creation.

#### Sequence → Linked List

**When to use:** Frequent insertions/deletions at ends.

**Abstraction:**
```
α(list) = sequence of elements
```

**Operations:**
- Prepend: O(1)
- Head: O(1)
- Tail: O(1)
- Index: O(n)

#### Sequence → Dynamic Array

**When to use:** Variable size, amortized constant append.

**Abstraction:**
```
α(arr, size, capacity) = arr[0..size-1]
```

**Operations:**
- Append: O(1) amortized
- Index: O(1)
- Resize: O(n) when needed

**Invariant:** `size ≤ capacity`

## Algorithmic Refinement

### Specification to Divide-and-Conquer

**Pattern:** Refine specification to recursive decomposition.

**Example: Sorting**

**Abstract:**
```
sort(xs) = ys where sorted(ys) ∧ perm(xs, ys)
```

**Refined (Merge Sort):**
```
sort(xs) = if |xs| ≤ 1 then xs
           else merge(sort(left), sort(right))
           where (left, right) = split(xs)
```

**Proof obligations:**
- Termination: Size decreases
- Correctness: Merge preserves sorting and permutation

### Specification to Greedy Algorithm

**Pattern:** Refine to locally optimal choices.

**Example: Minimum Spanning Tree**

**Abstract:**
```
MST(G) = T where tree(T) ∧ spans(T, G) ∧ minimal_weight(T)
```

**Refined (Kruskal's):**
```
MST(G) =
  edges_sorted = sort_by_weight(edges(G))
  forest = empty
  for e in edges_sorted:
    if not creates_cycle(forest, e):
      forest = forest ∪ {e}
  return forest
```

### Specification to Dynamic Programming

**Pattern:** Refine to memoized recursion.

**Example: Fibonacci**

**Abstract:**
```
fib(n) = if n ≤ 1 then n else fib(n-1) + fib(n-2)
```

**Refined (Memoized):**
```
fib_memo(n, memo) =
  if n in memo: return memo[n]
  if n ≤ 1: result = n
  else: result = fib_memo(n-1, memo) + fib_memo(n-2, memo)
  memo[n] = result
  return result
```

## Implementation Refinement

### Naive to Tail-Recursive

**Pattern:** Eliminate stack growth with accumulator.

**Example: List Reversal**

**Naive:**
```
reverse([]) = []
reverse(x :: xs) = reverse(xs) ++ [x]
```

**Tail-Recursive:**
```
reverse_acc([], acc) = acc
reverse_acc(x :: xs, acc) = reverse_acc(xs, x :: acc)

reverse(xs) = reverse_acc(xs, [])
```

**Proof obligation:**
```
reverse_acc(xs, acc) = reverse(xs) ++ acc
```

### Functional to Imperative

**Pattern:** Refine pure functions to stateful procedures.

**Example: Array Sum**

**Functional:**
```
sum([]) = 0
sum(x :: xs) = x + sum(xs)
```

**Imperative:**
```
sum_imperative(arr):
  total = 0
  for i = 0 to length(arr) - 1:
    total = total + arr[i]
  return total
```

**Proof obligation:**
```
Loop invariant: total = sum(arr[0..i-1])
```

### Single-Pass to Multi-Pass

**Pattern:** Trade time for space or vice versa.

**Example: Finding Min and Max**

**Single-Pass:**
```
min_max(xs):
  min = max = xs[0]
  for x in xs[1..]:
    if x < min: min = x
    if x > max: max = x
  return (min, max)
```

**Multi-Pass:**
```
min_max(xs):
  return (minimum(xs), maximum(xs))
```

## Optimization Refinements

### Quadratic to Linear

**Pattern:** Eliminate nested loops or redundant computation.

**Example: Two Sum Problem**

**Quadratic:**
```
two_sum(arr, target):
  for i in 0..n-1:
    for j in i+1..n-1:
      if arr[i] + arr[j] = target:
        return (i, j)
```

**Linear (with hash map):**
```
two_sum(arr, target):
  seen = {}
  for i in 0..n-1:
    complement = target - arr[i]
    if complement in seen:
      return (seen[complement], i)
    seen[arr[i]] = i
```

### Exponential to Polynomial

**Pattern:** Memoization or dynamic programming.

**Example: Longest Common Subsequence**

**Exponential:**
```
lcs(s1, s2) =
  if s1 = [] or s2 = []: return 0
  if head(s1) = head(s2):
    return 1 + lcs(tail(s1), tail(s2))
  else:
    return max(lcs(tail(s1), s2), lcs(s1, tail(s2)))
```

**Polynomial (DP):**
```
lcs_dp(s1, s2):
  dp[i][j] = length of LCS of s1[0..i] and s2[0..j]
  for i in 0..len(s1):
    for j in 0..len(s2):
      if s1[i] = s2[j]:
        dp[i+1][j+1] = dp[i][j] + 1
      else:
        dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
  return dp[len(s1)][len(s2)]
```

## Concurrency Refinements

### Sequential to Parallel

**Pattern:** Identify independent computations.

**Example: Map Operation**

**Sequential:**
```
map(f, xs) = [f(x) for x in xs]
```

**Parallel:**
```
parallel_map(f, xs):
  results = array[len(xs)]
  parallel for i in 0..len(xs)-1:
    results[i] = f(xs[i])
  return results
```

**Proof obligation:** `f` must be pure (no side effects).

### Blocking to Non-Blocking

**Pattern:** Refine synchronous to asynchronous operations.

**Example: I/O Operations**

**Blocking:**
```
process_files(files):
  results = []
  for file in files:
    content = read_file(file)  // Blocks
    results.append(process(content))
  return results
```

**Non-Blocking:**
```
async process_files(files):
  tasks = [read_file_async(f) for f in files]
  contents = await gather(tasks)
  return [process(c) for c in contents]
```

## Refinement Composition

### Sequential Composition

**Pattern:** Chain multiple refinement steps.

```
Abstract Spec
    ↓ [Refinement 1]
Intermediate 1
    ↓ [Refinement 2]
Intermediate 2
    ↓ [Refinement 3]
Concrete Implementation
```

**Proof:** Transitivity of refinement relation.

### Parallel Composition

**Pattern:** Refine components independently.

```
Component A (Abstract) ⊗ Component B (Abstract)
         ↓                        ↓
Component A (Concrete) ⊗ Component B (Concrete)
```

**Proof:** Show each component refinement preserves composition.

## Refinement Anti-Patterns

### Over-Refinement

**Problem:** Too many small refinement steps.

**Solution:** Combine related refinements into larger steps.

### Under-Specification

**Problem:** Abstract specification too vague.

**Solution:** Add precise preconditions and postconditions.

### Broken Abstraction

**Problem:** Concrete implementation exposes details.

**Solution:** Maintain clear abstraction boundary.

### Missing Invariants

**Problem:** Refinement doesn't preserve key properties.

**Solution:** Explicitly state and prove invariants.

## Refinement Strategies

### Top-Down Refinement

1. Start with high-level specification
2. Identify major components
3. Refine each component
4. Compose refined components
5. Prove composition correct

### Bottom-Up Refinement

1. Implement concrete operations
2. Define abstraction relation
3. Prove operations refine abstract spec
4. Build larger components
5. Compose and verify

### Middle-Out Refinement

1. Start with intermediate abstraction
2. Refine downward to implementation
3. Abstract upward to specification
4. Prove both directions

## Verification Patterns

### Simulation Proofs

**Forward Simulation:**
```
concrete_step(c) = c'
abs(c) = a
⟹ ∃a'. abstract_step(a) = a' ∧ abs(c') = a'
```

**Backward Simulation:**
```
abstract_step(a) = a'
abs(c) = a
⟹ ∃c'. concrete_step(c) = c' ∧ abs(c') = a'
```

### Invariant Preservation

**Pattern:** Show refinement preserves invariants.

```
Invariant(abstract_state)
Refinement: concrete_state ⊑ abstract_state
⟹ Invariant(concrete_state)
```

### Equivalence Proofs

**Pattern:** Show concrete and abstract are equivalent.

```
∀input. abstract_output(input) = concrete_output(input)
```
