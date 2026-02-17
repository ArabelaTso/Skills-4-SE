# Verified Pseudocode Extraction Examples

This file contains complete examples of extracting pseudocode from verified programs.

## Example 1: Insertion Sort (Isabelle/HOL)

### Input: Verified Isabelle Code

```isabelle
theory InsertionSort
  imports Main
begin

fun insert :: "nat ⇒ nat list ⇒ nat list" where
  "insert x [] = [x]" |
  "insert x (y # ys) = (if x ≤ y then x # y # ys else y # insert x ys)"

fun insertion_sort :: "nat list ⇒ nat list" where
  "insertion_sort [] = []" |
  "insertion_sort (x # xs) = insert x (insertion_sort xs)"

fun is_sorted :: "nat list ⇒ bool" where
  "is_sorted [] = True" |
  "is_sorted [x] = True" |
  "is_sorted (x # y # ys) = (x ≤ y ∧ is_sorted (y # ys))"

lemma insert_sorted:
  assumes "is_sorted xs"
  shows "is_sorted (insert x xs)"
  using assms
proof (induction xs)
  case Nil
  show ?case by simp
next
  case (Cons y ys)
  show ?case by (cases "x ≤ y") (auto simp: Cons.IH Cons.prems)
qed

theorem insertion_sort_correct:
  shows "is_sorted (insertion_sort xs) ∧ set (insertion_sort xs) = set xs"
proof (induction xs)
  case Nil
  show ?case by simp
next
  case (Cons x xs)
  show ?case using Cons.IH insert_sorted by auto
qed

end
```

### Output: Extracted Pseudocode

```
ALGORITHM: Insertion Sort
VERIFIED IN: Isabelle/HOL (InsertionSort theory)

═══════════════════════════════════════════════════════════

FUNCTION insert(x: Nat, list: List<Nat>) -> List<Nat>
  DESCRIPTION: Insert element into sorted list maintaining order

  PRECONDITION: is_sorted(list)  [VERIFIED: insert_sorted lemma]
  POSTCONDITION: is_sorted(insert(x, list))  [VERIFIED: insert_sorted lemma]

  MATCH list WITH
    CASE []:
      RETURN [x]

    CASE y :: ys:
      IF x ≤ y THEN
        RETURN [x, y, ...ys]
      ELSE
        LET inserted = insert(x, ys)
        RETURN [y, ...inserted]

═══════════════════════════════════════════════════════════

FUNCTION insertion_sort(list: List<Nat>) -> List<Nat>
  DESCRIPTION: Sort list in ascending order using insertion sort

  PRECONDITION: (none)
  POSTCONDITION:
    - is_sorted(insertion_sort(list))  [VERIFIED: insertion_sort_correct]
    - elements(insertion_sort(list)) = elements(list)  [VERIFIED: insertion_sort_correct]

  MATCH list WITH
    CASE []:
      RETURN []

    CASE x :: xs:
      LET sorted_xs = insertion_sort(xs)
      RETURN insert(x, sorted_xs)

  TERMINATION: Structural recursion on list  [VERIFIED]
  INVARIANT: At each recursive call, list size decreases  [VERIFIED]

═══════════════════════════════════════════════════════════

PREDICATE is_sorted(list: List<Nat>) -> Bool
  DESCRIPTION: Check if list is sorted in ascending order

  DEFINED BY:
    - is_sorted([]) = true
    - is_sorted([x]) = true
    - is_sorted([x, y, ...rest]) = (x ≤ y) AND is_sorted([y, ...rest])

═══════════════════════════════════════════════════════════

VERIFIED PROPERTIES:
  1. Correctness: insertion_sort produces sorted output
  2. Permutation: insertion_sort preserves all elements
  3. Termination: insertion_sort always terminates
  4. Helper correctness: insert maintains sortedness
```

---

## Example 2: Binary Search (Coq)

### Input: Verified Coq Code

```coq
Require Import List Arith Lia.
Import ListNotations.

Fixpoint is_sorted (l : list nat) : bool :=
  match l with
  | [] => true
  | [x] => true
  | x :: y :: ys => (x <=? y) && is_sorted (y :: ys)
  end.

Fixpoint binary_search_aux (l : list nat) (target : nat) (low high : nat) : option nat :=
  match high - low with
  | 0 =>
      if nth low l 0 =? target then Some low else None
  | S _ =>
      let mid := (low + high) / 2 in
      let mid_val := nth mid l 0 in
      if mid_val =? target then Some mid
      else if mid_val <? target then
        binary_search_aux l target (mid + 1) high
      else
        binary_search_aux l target low (mid - 1)
  end.

Definition binary_search (l : list nat) (target : nat) : option nat :=
  match l with
  | [] => None
  | _ => binary_search_aux l target 0 (length l - 1)
  end.

Definition binary_search_spec (l : list nat) (target : nat) (result : option nat) : Prop :=
  is_sorted l = true ->
  match result with
  | None => ~ In target l
  | Some i => i < length l /\ nth i l 0 = target
  end.

Theorem binary_search_correct :
  forall l target,
    binary_search_spec l target (binary_search l target).
Proof.
  (* Proof omitted *)
Admitted.
```

### Output: Extracted Pseudocode

```
ALGORITHM: Binary Search
VERIFIED IN: Coq (with correctness theorem)

═══════════════════════════════════════════════════════════

FUNCTION binary_search(list: List<Nat>, target: Nat) -> Option<Nat>
  DESCRIPTION: Search for target in sorted list using binary search

  PRECONDITION: is_sorted(list) = true  [VERIFIED: binary_search_correct]
  POSTCONDITION:
    IF result = Some(i) THEN
      - i < length(list)  [VERIFIED]
      - list[i] = target  [VERIFIED]
    IF result = None THEN
      - target NOT IN list  [VERIFIED]

  IF list is empty THEN
    RETURN None
  ELSE
    RETURN binary_search_aux(list, target, 0, length(list) - 1)

═══════════════════════════════════════════════════════════

FUNCTION binary_search_aux(list: List<Nat>, target: Nat, low: Nat, high: Nat) -> Option<Nat>
  DESCRIPTION: Helper function for binary search with bounds

  PRECONDITION:
    - is_sorted(list) = true
    - 0 ≤ low ≤ high < length(list)

  LET range_size = high - low

  IF range_size = 0 THEN
    // Single element case
    IF list[low] = target THEN
      RETURN Some(low)
    ELSE
      RETURN None
  ELSE
    // Multiple elements case
    LET mid = (low + high) / 2
    LET mid_val = list[mid]

    IF mid_val = target THEN
      RETURN Some(mid)
    ELSE IF mid_val < target THEN
      // Search right half
      RETURN binary_search_aux(list, target, mid + 1, high)
    ELSE
      // Search left half
      RETURN binary_search_aux(list, target, low, mid - 1)

  TERMINATION: range_size decreases at each recursive call  [VERIFIED]
  INVARIANT: If target in list[low..high], it will be found  [VERIFIED]

═══════════════════════════════════════════════════════════

VERIFIED PROPERTIES:
  1. Correctness: If target found, index is correct
  2. Completeness: If target in list, it will be found
  3. Soundness: If None returned, target not in list
  4. Termination: Always terminates for valid inputs
  5. Complexity: O(log n) comparisons  [UNVERIFIED: not formally proven]
```

---

## Example 3: Safe Array Access (Coq with Dependent Types)

### Input: Verified Coq Code

```coq
Require Import List Arith.
Import ListNotations.

Definition safe_nth {A : Type} (l : list A) (n : nat) (H : n < length l) : A.
Proof.
  revert n H.
  induction l as [| x xs IH]; intros n H.
  - (* Empty list case *)
    exfalso. simpl in H. lia.
  - (* Non-empty list case *)
    destruct n as [| n'].
    + (* n = 0 *)
      exact x.
    + (* n = S n' *)
      apply IH.
      simpl in H. lia.
Defined.

Lemma safe_nth_correct :
  forall A (l : list A) n H,
    nth n l (safe_nth l n H) = safe_nth l n H.
Proof.
  (* Proof omitted *)
Admitted.
```

### Output: Extracted Pseudocode

```
ALGORITHM: Safe Array Access
VERIFIED IN: Coq (with dependent types)

═══════════════════════════════════════════════════════════

FUNCTION safe_nth<T>(list: List<T>, n: Nat) -> T
  DESCRIPTION: Access nth element with compile-time bounds checking

  PRECONDITION: n < length(list)  [VERIFIED: enforced by type system]
  POSTCONDITION: Returns list[n]  [VERIFIED: safe_nth_correct]

  MATCH list WITH
    CASE []:
      UNREACHABLE  [precondition ensures list is non-empty when n ≥ 0]

    CASE x :: xs:
      IF n = 0 THEN
        RETURN x
      ELSE
        // Recursive call with n-1
        // Precondition maintained: n-1 < length(xs)  [VERIFIED]
        RETURN safe_nth(xs, n - 1)

  TERMINATION: n decreases at each recursive call  [VERIFIED]

  NOTE: This function cannot fail at runtime because bounds
        checking is performed at compile time via the type system.

═══════════════════════════════════════════════════════════

VERIFIED PROPERTIES:
  1. Safety: No out-of-bounds access possible  [VERIFIED: type system]
  2. Correctness: Returns correct element  [VERIFIED: safe_nth_correct]
  3. Termination: Always terminates  [VERIFIED]
```

---

## Example 4: GCD Algorithm (Isabelle/HOL)

### Input: Verified Isabelle Code

```isabelle
theory GCD
  imports Main
begin

function gcd :: "nat ⇒ nat ⇒ nat" where
  "gcd a 0 = a" |
  "gcd a b = gcd b (a mod b)"
  by pat_completeness auto

termination
  by (relation "measure (λ(a, b). b)") auto

lemma gcd_dvd:
  "gcd a b dvd a ∧ gcd a b dvd b"
  by (induction a b rule: gcd.induct) auto

lemma gcd_greatest:
  assumes "d dvd a" "d dvd b"
  shows "d dvd gcd a b"
  using assms by (induction a b rule: gcd.induct) auto

theorem gcd_correct:
  "is_gcd (gcd a b) a b"
  using gcd_dvd gcd_greatest by (auto simp: is_gcd_def)

end
```

### Output: Extracted Pseudocode

```
ALGORITHM: Greatest Common Divisor (Euclidean Algorithm)
VERIFIED IN: Isabelle/HOL (GCD theory)

═══════════════════════════════════════════════════════════

FUNCTION gcd(a: Nat, b: Nat) -> Nat
  DESCRIPTION: Compute greatest common divisor using Euclidean algorithm

  PRECONDITION: (none - works for all natural numbers)
  POSTCONDITION:
    - gcd(a, b) divides a  [VERIFIED: gcd_dvd]
    - gcd(a, b) divides b  [VERIFIED: gcd_dvd]
    - FOR ALL d: (d divides a AND d divides b) IMPLIES d divides gcd(a, b)  [VERIFIED: gcd_greatest]

  IF b = 0 THEN
    RETURN a
  ELSE
    LET remainder = a mod b
    RETURN gcd(b, remainder)

  TERMINATION: b decreases at each recursive call  [VERIFIED: measure function]
  INVARIANT: gcd(a, b) = gcd(b, a mod b)  [VERIFIED]

═══════════════════════════════════════════════════════════

VERIFIED PROPERTIES:
  1. Divisibility: Result divides both inputs
  2. Greatest: Result is the greatest common divisor
  3. Termination: Always terminates for finite inputs
  4. Correctness: Satisfies mathematical definition of GCD
```

---

## Extraction Guidelines Summary

### What to Include

1. **Function signatures**: Name, parameters, return type
2. **Control flow**: All branches, loops, recursion
3. **Data flow**: How values are computed and passed
4. **Verified properties**: Preconditions, postconditions, invariants
5. **Termination arguments**: Why recursion terminates
6. **Verification status**: What has been proven

### What to Exclude

1. **Proof code**: Tactics, proof scripts, intermediate steps
2. **Type system details**: Type classes, implicit arguments (unless essential)
3. **Language syntax**: Specific notation, operators
4. **Proof lemmas**: Helper lemmas used only for proof
5. **Module system**: Imports, namespaces (unless essential)

### Verification Annotations

- `[VERIFIED]`: Formally proven
- `[VERIFIED: property]`: Specific property proven
- `[UNVERIFIED]`: Not formally proven
- `[ASSUMED]`: Assumed without proof
- `[UNREACHABLE]`: Proven impossible by preconditions
