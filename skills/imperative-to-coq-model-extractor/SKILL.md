---
name: imperative-to-coq-model-extractor
description: Extract abstract mathematical models from imperative code (C, C++, Python, Java, etc.) suitable for formal reasoning in Coq. Use when the user asks to model imperative code in Coq, create Coq specifications from imperative programs, extract mathematical models for verification, or translate imperative algorithms to Coq for formal reasoning and proof.
---

# Imperative to Coq Model Extractor

## Overview

Extract abstract mathematical models from imperative code that can be used for formal reasoning and verification in Coq. This skill transforms imperative programs into functional Coq definitions with explicit state modeling, enabling formal proofs about program behavior.

## Extraction Workflow

### Step 1: Analyze Imperative Code

Understand the program structure and semantics:

1. **Identify components:**
   - Functions and their signatures
   - Data structures and types
   - State and mutable variables
   - Control flow (loops, conditionals)
   - Side effects and I/O

2. **Understand semantics:**
   - What does the program compute?
   - What state does it maintain?
   - What are the invariants?
   - What are preconditions and postconditions?

3. **Note modeling challenges:**
   - Mutable state
   - Imperative loops
   - Pointers and memory
   - Side effects

### Step 2: Design Coq Model Structure

Plan the Coq representation:

1. **Choose appropriate types:**
   - `Z` for arbitrary precision integers
   - `nat` for natural numbers
   - `bool` for booleans
   - `list` for sequences
   - `Record` for structured state
   - Inductive types for enumerations

2. **Model state explicitly:**
   - Pure functions: Direct translation
   - Mutable state: State transformation functions
   - Side effects: Explicit state passing

3. **Plan control flow translation:**
   - Conditionals → Pattern matching or if-then-else
   - Loops → Recursive functions (Fixpoint)
   - Early returns → Conditional expressions

### Step 3: Extract Core Model

Translate imperative constructs to Coq:

**Pattern: Pure function**
```c
// Imperative
int add(int a, int b) {
    return a + b;
}
```

```coq
(* Coq Model *)
Definition add (a b : Z) : Z := a + b.
```

**Pattern: Function with state**
```c
// Imperative
int counter = 0;
void increment() {
    counter++;
}
```

```coq
(* Coq Model *)
Definition counter_state : Type := Z.
Definition increment (c : counter_state) : counter_state := c + 1.
```

**Pattern: Loop → Recursion**
```c
// Imperative
int sum(int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += i;
    }
    return total;
}
```

```coq
(* Coq Model *)
Fixpoint sum_aux (n i total : nat) : nat :=
  match n with
  | 0 => total
  | S n' =>
      if i <? n then
        sum_aux n (S i) (total + i)
      else
        total
  end.

Definition sum (n : nat) : nat := sum_aux n 0 0.
```

### Step 4: Add Specifications

Enhance the model with formal specifications:

1. **Function specifications:**
   ```coq
   Definition abs (n : Z) : Z :=
     if n <? 0 then -n else n.

   Lemma abs_nonneg : forall n : Z, abs n >= 0.
   Proof.
     intros n. unfold abs.
     destruct (n <? 0) eqn:E.
     - apply Z.ltb_lt in E. lia.
     - apply Z.ltb_ge in E. lia.
   Qed.
   ```

2. **Loop invariants:**
   ```coq
   (* Invariant: sum = sum of first i elements *)
   Lemma sum_invariant : forall n i total,
     i <= n ->
     sum_aux n i total = total + (sum of 0..i-1).
   Proof.
     (* Proof by induction *)
   Admitted.
   ```

3. **Correctness properties:**
   ```coq
   Lemma sum_correct : forall n,
     sum n = n * (n - 1) / 2.
   Proof.
     (* Proof *)
   Admitted.
   ```

### Step 5: Verify and Test

Ensure the model is correct:

1. **Type check:**
   ```bash
   coqc model.v
   ```

2. **Test with examples:**
   ```coq
   Compute add 2 3.        (* Should output 5 *)
   Compute sum 5.          (* Should output 10 *)
   ```

3. **Compare semantics:**
   - Run original imperative program
   - Evaluate Coq model
   - Verify outputs match

### Step 6: Refine and Document

Improve the extracted model:

1. **Simplify definitions:**
   - Use standard library functions
   - Remove redundant constructs
   - Factor out common patterns

2. **Add documentation:**
   ```coq
   (* Computes the absolute value of an integer *)
   Definition abs (n : Z) : Z := ...
   ```

3. **Organize proofs:**
   - Group related lemmas
   - Add proof sketches
   - Document proof strategies

## Common Extraction Patterns

For detailed patterns, see [extraction_patterns.md](references/extraction_patterns.md).

### Quick Reference

| Imperative | Coq Model |
|------------|-----------|
| `int x = 10` | `Definition x : Z := 10` |
| `x = x + 1` | `x + 1` (functional update) |
| `if (x > 0)` | `if x >? 0 then ... else ...` |
| `for (i=0; i<n; i++)` | `Fixpoint loop (i : nat) ...` |
| `while (cond)` | `Fixpoint loop ... if cond then ...` |
| `struct S { int x; }` | `Record S := { x : Z }` |
| `int arr[5]` | `list Z` or `Definition arr := [...]` |
| `return x` | `x` (last expression) |

## Examples

### Example 1: Simple Algorithm

**Imperative Input (C):**
```c
int factorial(int n) {
    int result = 1;
    while (n > 1) {
        result *= n;
        n--;
    }
    return result;
}
```

**Coq Model:**
```coq
Fixpoint factorial (n : nat) : nat :=
  match n with
  | 0 => 1
  | S n' => n * factorial n'
  end.

Lemma factorial_positive : forall n,
  factorial n >= 1.
Proof.
  induction n.
  - simpl. lia.
  - simpl. lia.
Qed.
```

### Example 2: Array Processing

**Imperative Input (Python):**
```python
def find_max(arr):
    max_val = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val
```

**Coq Model:**
```coq
Require Import List.
Import ListNotations.

Fixpoint find_max (l : list Z) (default : Z) : Z :=
  match l with
  | [] => default
  | [x] => x
  | x :: xs => Z.max x (find_max xs default)
  end.

Lemma find_max_in_list : forall l default,
  l <> [] ->
  In (find_max l default) l.
Proof.
  (* Proof by induction *)
Admitted.

Lemma find_max_is_max : forall l default x,
  In x l ->
  x <= find_max l default.
Proof.
  (* Proof by induction *)
Admitted.
```

### Example 3: Stateful Program

**Imperative Input (Java):**
```java
class Counter {
    private int count = 0;

    public void increment() {
        count++;
    }

    public int getCount() {
        return count;
    }
}
```

**Coq Model:**
```coq
Record CounterState : Type := mkCounter {
  count : nat
}.

Definition init_counter : CounterState := {|
  count := 0
|}.

Definition increment (s : CounterState) : CounterState := {|
  count := S s.(count)
|}.

Definition getCount (s : CounterState) : nat :=
  s.(count).

(* Specification *)
Lemma increment_increases : forall s,
  getCount (increment s) = S (getCount s).
Proof.
  intros s. unfold increment, getCount. simpl. reflexivity.
Qed.
```

### Example 4: Binary Search

**Imperative Input (C++):**
```cpp
int binary_search(int arr[], int n, int target) {
    int left = 0, right = n - 1;
    while (left <= right) {
        int mid = (left + right) / 2;
        if (arr[mid] == target)
            return mid;
        else if (arr[mid] < target)
            left = mid + 1;
        else
            right = mid - 1;
    }
    return -1;
}
```

**Coq Model:**
```coq
Require Import List.
Import ListNotations.

Fixpoint binary_search_aux (l : list Z) (target : Z)
                            (left right : nat) : option nat :=
  match right - left with
  | 0 =>
      match nth_error l left with
      | Some v => if v =? target then Some left else None
      | None => None
      end
  | S _ =>
      if left <=? right then
        let mid := (left + right) / 2 in
        match nth_error l mid with
        | Some v =>
            if v =? target then Some mid
            else if v <? target then
              binary_search_aux l target (S mid) right
            else
              binary_search_aux l target left (mid - 1)
        | None => None
        end
      else None
  end.

Definition binary_search (l : list Z) (target : Z) : option nat :=
  binary_search_aux l target 0 (length l - 1).

(* Specification: if result is Some i, then l[i] = target *)
Lemma binary_search_correct : forall l target i,
  binary_search l target = Some i ->
  nth_error l i = Some target.
Proof.
  (* Proof *)
Admitted.
```

## Best Practices

1. **Model state explicitly:** Make all state transformations visible in function signatures
2. **Use appropriate types:** Choose `nat` for non-negative values, `Z` for integers
3. **Preserve semantics:** Ensure the Coq model computes the same results as the original
4. **Add specifications:** Document expected behavior with lemmas and theorems
5. **Test incrementally:** Verify small pieces before combining
6. **Use standard library:** Leverage existing Coq definitions and tactics
7. **Document assumptions:** Make implicit assumptions explicit in the model
8. **Handle edge cases:** Explicitly model boundary conditions

## Key Differences: Imperative vs Coq Model

1. **Mutability:** Imperative code mutates variables; Coq models use functional updates
2. **Loops:** Imperative loops become recursive functions in Coq
3. **State:** Imperative state is implicit; Coq models make state explicit
4. **Side effects:** Imperative side effects become explicit state transformations
5. **Types:** Imperative types may be implicit; Coq requires explicit types
6. **Verification:** Coq models enable formal proofs about program behavior

## Limitations and Considerations

1. **Abstraction level:** Models abstract away low-level details (memory layout, performance)
2. **Undefined behavior:** Imperative undefined behavior must be handled explicitly
3. **Concurrency:** Multi-threaded code requires more sophisticated modeling
4. **I/O:** Input/output operations need special treatment in pure models
5. **Pointers:** Pointer arithmetic requires explicit memory modeling
6. **Complexity:** Some imperative patterns are complex to model functionally

## Resources

- **Extraction patterns:** See [extraction_patterns.md](references/extraction_patterns.md) for comprehensive pattern catalog
- **Coq documentation:** https://coq.inria.fr/documentation
- **Software Foundations:** https://softwarefoundations.cis.upenn.edu/
- **Coq standard library:** https://coq.inria.fr/library/
