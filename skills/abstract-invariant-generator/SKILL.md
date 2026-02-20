---
name: abstract-invariant-generator
description: Uses abstract interpretation to automatically infer loop invariants, function preconditions, and postconditions for formal verification. Generates invariants that capture program behavior and support correctness proofs in Dafny, Isabelle, Coq, and other verification systems. Use when adding formal specifications to code, generating verification conditions, inferring contracts for functions, or discovering loop invariants for proofs.
---

# Abstract Invariant Generator

## Overview

This skill uses abstract interpretation to automatically infer loop invariants, function preconditions, and postconditions. It generates formal specifications that support verification and reasoning about program correctness.

## Invariant Generation Workflow

### Step 1: Identify Specification Points

Analyze the code to identify where invariants are needed:

**Loop Invariants**: For each loop
```python
while condition:
    # Need: invariant that holds before/after each iteration
    body
```

**Function Contracts**: For each function
```python
def function(params):
    # Need: precondition (what must be true on entry)
    body
    # Need: postcondition (what is guaranteed on exit)
```

**Assertions**: For verification points
```python
# Need: invariant that holds at this point
assert property
```

### Step 2: Perform Abstract Interpretation

Use abstract domains to infer properties:

**Interval Analysis**: Infer numeric ranges
```python
i = 0
while i < n:
    # Inferred: 0 ≤ i < n
    i += 1
# Inferred: i = n
```

**Relational Analysis**: Infer relationships between variables
```python
i = 0
j = 0
while i < n:
    # Inferred: i = j
    i += 1
    j += 1
```

**Shape Analysis**: Infer data structure properties
```python
while node is not None:
    # Inferred: node is in the linked list
    node = node.next
```

### Step 3: Generate Loop Invariants

For each loop, generate an invariant that:
1. Holds before the loop (initialization)
2. Is preserved by the loop body (maintenance)
3. Combined with loop exit, implies desired property (termination)

**Template-Based Generation**:

**Counter Loop**:
```python
i = 0
while i < n:
    arr[i] = 0
    i += 1
```

**Generated Invariant**:
```
invariant 0 ≤ i ≤ n
invariant ∀k. 0 ≤ k < i ⟹ arr[k] = 0
```

**Accumulator Loop**:
```python
sum = 0
i = 0
while i < len(arr):
    sum += arr[i]
    i += 1
```

**Generated Invariant**:
```
invariant 0 ≤ i ≤ len(arr)
invariant sum = Σ(arr[0..i-1])
```

**Search Loop**:
```python
i = 0
found = False
while i < len(arr) and not found:
    if arr[i] == target:
        found = True
    else:
        i += 1
```

**Generated Invariant**:
```
invariant 0 ≤ i ≤ len(arr)
invariant ∀k. 0 ≤ k < i ⟹ arr[k] ≠ target
invariant found ⟹ arr[i] = target
```

### Step 4: Generate Function Preconditions

Infer what must be true for the function to work correctly:

**Array Access Function**:
```python
def get_element(arr, index):
    return arr[index]
```

**Generated Precondition**:
```
requires 0 ≤ index < len(arr)
requires arr is not None
```

**Division Function**:
```python
def divide(x, y):
    return x / y
```

**Generated Precondition**:
```
requires y ≠ 0
```

**Linked List Function**:
```python
def get_next(node):
    return node.next
```

**Generated Precondition**:
```
requires node is not None
```

### Step 5: Generate Function Postconditions

Infer what the function guarantees on exit:

**Maximum Function**:
```python
def find_max(arr):
    max_val = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val
```

**Generated Postcondition**:
```
ensures result ∈ arr
ensures ∀x ∈ arr. x ≤ result
```

**Sorting Function**:
```python
def sort(arr):
    # ... sorting logic ...
    return sorted_arr
```

**Generated Postcondition**:
```
ensures len(result) = len(arr)
ensures ∀i. 0 ≤ i < len(result)-1 ⟹ result[i] ≤ result[i+1]
ensures multiset(result) = multiset(arr)
```

**Search Function**:
```python
def binary_search(arr, target):
    # ... search logic ...
    return index
```

**Generated Postcondition**:
```
ensures result = -1 ∨ (0 ≤ result < len(arr) ∧ arr[result] = target)
ensures result ≠ -1 ⟹ arr[result] = target
ensures result = -1 ⟹ target ∉ arr
```

### Step 6: Express in Target Language

Format invariants for the target verification system:

**Dafny**:
```dafny
method FindMax(arr: array<int>) returns (max: int)
  requires arr.Length > 0
  ensures max in arr[..]
  ensures forall i :: 0 <= i < arr.Length ==> arr[i] <= max
{
  max := arr[0];
  var i := 1;
  while i < arr.Length
    invariant 1 <= i <= arr.Length
    invariant max in arr[..i]
    invariant forall k :: 0 <= k < i ==> arr[k] <= max
  {
    if arr[i] > max {
      max := arr[i];
    }
    i := i + 1;
  }
}
```

**Isabelle/HOL**:
```isabelle
lemma find_max_correct:
  assumes "length arr > 0"
  shows "find_max arr ∈ set arr ∧
         (∀x ∈ set arr. x ≤ find_max arr)"
```

**Coq**:
```coq
Lemma find_max_correct : forall (arr : list nat),
  length arr > 0 ->
  In (find_max arr) arr /\
  (forall x, In x arr -> x <= find_max arr).
```

**ACSL (for C)**:
```c
/*@ requires n > 0;
  @ requires \valid(arr + (0..n-1));
  @ ensures \result >= 0 && \result < n;
  @ ensures \forall integer k; 0 <= k < n ==> arr[k] <= arr[\result];
  @*/
int find_max(int arr[], int n) {
  int max_idx = 0;
  /*@ loop invariant 1 <= i <= n;
    @ loop invariant 0 <= max_idx < i;
    @ loop invariant \forall integer k; 0 <= k < i ==> arr[k] <= arr[max_idx];
    @ loop variant n - i;
    @*/
  for (int i = 1; i < n; i++) {
    if (arr[i] > arr[max_idx]) {
      max_idx = i;
    }
  }
  return max_idx;
}
```

## Complete Example

**Input Code** (Python):
```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
```

**Analysis**:

**Outer Loop** (for i in range(1, len(arr))):
- i ranges from 1 to len(arr)
- After each iteration, arr[0..i] is sorted
- Elements are permutation of original

**Inner Loop** (while j >= 0 and arr[j] > key):
- j decreases from i-1 to -1
- Shifts elements greater than key to the right
- Maintains: arr[j+2..i+1] contains elements > key

**Generated Invariants** (Dafny):
```dafny
method InsertionSort(arr: array<int>)
  requires arr.Length >= 0
  ensures sorted(arr[..])
  ensures multiset(arr[..]) == multiset(old(arr[..]))
  modifies arr
{
  var i := 1;
  while i < arr.Length
    invariant 1 <= i <= arr.Length
    invariant sorted(arr[..i])
    invariant multiset(arr[..]) == multiset(old(arr[..]))
  {
    var key := arr[i];
    var j := i - 1;

    while j >= 0 && arr[j] > key
      invariant -1 <= j < i
      invariant sorted(arr[..j+1])
      invariant sorted(arr[j+2..i+1])
      invariant forall k :: j+2 <= k <= i ==> arr[k] > key
      invariant multiset(arr[..]) == multiset(old(arr[..]))
    {
      arr[j + 1] := arr[j];
      j := j - 1;
    }

    arr[j + 1] := key;
    i := i + 1;
  }
}

predicate sorted(s: seq<int>) {
  forall i, j :: 0 <= i < j < |s| ==> s[i] <= s[j]
}
```

**Explanation**:

**Outer Loop Invariants**:
1. `1 <= i <= arr.Length`: Loop counter bounds
2. `sorted(arr[..i])`: First i elements are sorted
3. `multiset(arr[..]) == multiset(old(arr[..]))`: Permutation preservation

**Inner Loop Invariants**:
1. `-1 <= j < i`: Loop counter bounds
2. `sorted(arr[..j+1])`: Elements before j+1 remain sorted
3. `sorted(arr[j+2..i+1])`: Shifted elements remain sorted
4. `forall k :: j+2 <= k <= i ==> arr[k] > key`: Shifted elements are greater than key
5. `multiset(arr[..]) == multiset(old(arr[..]))`: Permutation preservation

## Invariant Patterns

### Numeric Bounds
```
invariant 0 ≤ i ≤ n
invariant low ≤ mid ≤ high
```

### Array Properties
```
invariant ∀k. 0 ≤ k < i ⟹ P(arr[k])
invariant sorted(arr[0..i])
invariant arr[i] = max(arr[0..i])
```

### Relationships
```
invariant i + j = n
invariant i = 2 * j
invariant sum = Σ(arr[0..i-1])
```

### Data Structure Properties
```
invariant acyclic(list)
invariant node ∈ reachable(head)
invariant size(tree) = n
```

### Permutation
```
invariant multiset(arr) = multiset(old(arr))
invariant set(arr) = set(old(arr))
```

## Strengthening Weak Invariants

Sometimes initial invariants are too weak. Strengthen them:

**Weak**:
```
invariant 0 ≤ i ≤ n
```

**Strengthened**:
```
invariant 0 ≤ i ≤ n
invariant ∀k. 0 ≤ k < i ⟹ processed(arr[k])
```

**Technique**: Add properties about what has been accomplished so far.

## Handling Complex Loops

### Nested Loops

Generate invariants for each level:
```python
for i in range(n):
    for j in range(m):
        matrix[i][j] = 0
```

**Invariants**:
```
Outer loop:
  invariant 0 ≤ i ≤ n
  invariant ∀r. 0 ≤ r < i ⟹ (∀c. 0 ≤ c < m ⟹ matrix[r][c] = 0)

Inner loop:
  invariant 0 ≤ j ≤ m
  invariant ∀c. 0 ≤ c < j ⟹ matrix[i][c] = 0
```

### Multiple Exit Conditions

Handle all exit paths:
```python
while i < n and not found:
    if arr[i] == target:
        found = True
    i += 1
```

**Invariants**:
```
invariant 0 ≤ i ≤ n
invariant found ⟹ arr[i-1] = target
invariant ¬found ⟹ (∀k. 0 ≤ k < i ⟹ arr[k] ≠ target)
```

## References

For detailed invariant generation techniques and patterns:
- **references/loop_invariants.md**: Loop invariant patterns and generation strategies
- **references/function_contracts.md**: Precondition and postcondition inference
- **references/invariant_templates.md**: Common invariant templates by algorithm type
- **references/verification_languages.md**: Syntax for different verification systems
