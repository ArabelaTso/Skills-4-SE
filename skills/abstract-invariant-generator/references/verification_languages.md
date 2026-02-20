# Verification Language Syntax

## Dafny

### Basic Syntax

**Function Contract**:
```dafny
method MethodName(param: Type) returns (result: Type)
  requires precondition
  ensures postcondition
  modifies objects
{
  // implementation
}
```

**Loop Invariant**:
```dafny
while condition
  invariant loop_invariant
  decreases termination_measure
{
  // body
}
```

### Common Constructs

**Quantifiers**:
```dafny
forall i :: 0 <= i < arr.Length ==> arr[i] > 0
exists i :: 0 <= i < arr.Length && arr[i] == target
```

**Array/Sequence Operations**:
```dafny
arr[..]              // entire array as sequence
arr[i..j]            // slice from i to j-1
arr.Length           // array length
|seq|                // sequence length
x in seq             // membership
```

**Predicates**:
```dafny
predicate sorted(s: seq<int>) {
  forall i, j :: 0 <= i < j < |s| ==> s[i] <= s[j]
}
```

**Old Values**:
```dafny
ensures arr[..] == old(arr[..])
ensures x > old(x)
```

**Multiset**:
```dafny
ensures multiset(arr[..]) == multiset(old(arr[..]))
```

### Complete Example

```dafny
method BinarySearch(arr: array<int>, target: int) returns (index: int)
  requires arr.Length > 0
  requires forall i, j :: 0 <= i < j < arr.Length ==> arr[i] <= arr[j]
  ensures index == -1 || (0 <= index < arr.Length && arr[index] == target)
  ensures index != -1 ==> arr[index] == target
  ensures index == -1 ==> forall i :: 0 <= i < arr.Length ==> arr[i] != target
{
  var low := 0;
  var high := arr.Length - 1;

  while low <= high
    invariant 0 <= low <= high + 1 <= arr.Length
    invariant forall i :: 0 <= i < low ==> arr[i] < target
    invariant forall i :: high < i < arr.Length ==> arr[i] > target
    decreases high - low
  {
    var mid := (low + high) / 2;
    if arr[mid] == target {
      return mid;
    } else if arr[mid] < target {
      low := mid + 1;
    } else {
      high := mid - 1;
    }
  }
  return -1;
}
```

## Isabelle/HOL

### Basic Syntax

**Function Definition**:
```isabelle
definition function_name :: "type1 ⇒ type2 ⇒ type3" where
  "function_name x y = expression"
```

**Lemma**:
```isabelle
lemma lemma_name:
  assumes "precondition"
  shows "postcondition"
```

**Proof**:
```isabelle
proof -
  (* proof steps *)
qed
```

### Common Constructs

**Quantifiers**:
```isabelle
∀x. P x                    (* forall *)
∃x. P x                    (* exists *)
∀x ∈ set. P x             (* bounded forall *)
```

**List Operations**:
```isabelle
length xs                  (* list length *)
xs ! i                     (* list indexing *)
take n xs                  (* first n elements *)
drop n xs                  (* all but first n *)
xs @ ys                    (* concatenation *)
x # xs                     (* cons *)
set xs                     (* convert to set *)
```

**Set Operations**:
```isabelle
x ∈ S                      (* membership *)
S ⊆ T                      (* subset *)
S ∪ T                      (* union *)
S ∩ T                      (* intersection *)
```

**Predicates**:
```isabelle
definition sorted :: "int list ⇒ bool" where
  "sorted xs = (∀i j. i < j ∧ j < length xs ⟶ xs ! i ≤ xs ! j)"
```

### Complete Example

```isabelle
fun binary_search :: "int list ⇒ int ⇒ int" where
  "binary_search xs target = binary_search_aux xs target 0 (length xs - 1)"

fun binary_search_aux :: "int list ⇒ int ⇒ nat ⇒ nat ⇒ int" where
  "binary_search_aux xs target low high =
    (if low > high then -1
     else let mid = (low + high) div 2 in
       if xs ! mid = target then int mid
       else if xs ! mid < target then binary_search_aux xs target (mid + 1) high
       else binary_search_aux xs target low (mid - 1))"

lemma binary_search_correct:
  assumes "sorted xs"
  assumes "length xs > 0"
  shows "(binary_search xs target = -1 ∧ target ∉ set xs) ∨
         (binary_search xs target ≥ 0 ∧
          xs ! nat (binary_search xs target) = target)"
proof -
  (* proof *)
qed
```

## Coq

### Basic Syntax

**Function Definition**:
```coq
Definition function_name (x : type1) (y : type2) : type3 :=
  expression.
```

**Fixpoint (Recursive)**:
```coq
Fixpoint function_name (x : type) : type :=
  match x with
  | pattern1 => expression1
  | pattern2 => expression2
  end.
```

**Theorem**:
```coq
Theorem theorem_name : forall (x : type),
  precondition -> postcondition.
```

**Proof**:
```coq
Proof.
  (* proof tactics *)
Qed.
```

### Common Constructs

**Quantifiers**:
```coq
forall x : nat, P x        (* universal *)
exists x : nat, P x        (* existential *)
```

**List Operations**:
```coq
length l                   (* list length *)
nth n l default            (* nth element *)
l ++ l'                    (* concatenation *)
x :: l                     (* cons *)
In x l                     (* membership *)
```

**Propositions**:
```coq
/\                         (* and *)
\/                         (* or *)
->                         (* implies *)
<->                        (* iff *)
~                          (* not *)
```

**Predicates**:
```coq
Fixpoint sorted (l : list nat) : Prop :=
  match l with
  | [] => True
  | [x] => True
  | x :: y :: rest => x <= y /\ sorted (y :: rest)
  end.
```

### Complete Example

```coq
Require Import List.
Import ListNotations.

Fixpoint binary_search_aux (l : list nat) (target : nat)
                           (low high : nat) : option nat :=
  match high - low with
  | 0 => if nth low l 0 =? target then Some low else None
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
  match length l with
  | 0 => None
  | S n => binary_search_aux l target 0 n
  end.

Theorem binary_search_correct : forall (l : list nat) (target : nat),
  sorted l ->
  (binary_search l target = None /\ ~In target l) \/
  (exists n, binary_search l target = Some n /\ nth n l 0 = target).
Proof.
  (* proof *)
Admitted.
```

## ACSL (ANSI/ISO C Specification Language)

### Basic Syntax

**Function Contract**:
```c
/*@ requires precondition;
  @ ensures postcondition;
  @ assigns modified_variables;
  @*/
return_type function_name(parameters) {
  // implementation
}
```

**Loop Invariant**:
```c
/*@ loop invariant invariant_expression;
  @ loop variant termination_measure;
  @*/
while (condition) {
  // body
}
```

### Common Constructs

**Quantifiers**:
```c
\forall integer i; 0 <= i < n ==> P(i)
\exists integer i; 0 <= i < n && P(i)
```

**Memory Predicates**:
```c
\valid(ptr)                          // pointer is valid
\valid(ptr + (0..n-1))              // array is valid
\valid_read(ptr)                     // readable
\separated(ptr1, ptr2)               // non-overlapping
```

**Old Values**:
```c
\old(expression)                     // value at function entry
\at(expression, Label)               // value at label
```

**Logic Functions**:
```c
/*@ logic integer sum(integer *arr, integer n) =
  @   (n <= 0) ? 0 : arr[n-1] + sum(arr, n-1);
  @*/
```

**Predicates**:
```c
/*@ predicate sorted(int *arr, integer n) =
  @   \forall integer i, j; 0 <= i < j < n ==> arr[i] <= arr[j];
  @*/
```

### Complete Example

```c
/*@ predicate sorted(int *arr, integer n) =
  @   \forall integer i, j; 0 <= i < j < n ==> arr[i] <= arr[j];
  @*/

/*@ requires n > 0;
  @ requires \valid(arr + (0..n-1));
  @ requires sorted(arr, n);
  @ ensures \result == -1 || (0 <= \result < n && arr[\result] == target);
  @ ensures \result != -1 ==> arr[\result] == target;
  @ ensures \result == -1 ==>
  @   \forall integer i; 0 <= i < n ==> arr[i] != target;
  @*/
int binary_search(int arr[], int n, int target) {
  int low = 0;
  int high = n - 1;

  /*@ loop invariant 0 <= low <= high + 1 <= n;
    @ loop invariant
    @   \forall integer i; 0 <= i < low ==> arr[i] < target;
    @ loop invariant
    @   \forall integer i; high < i < n ==> arr[i] > target;
    @ loop variant high - low;
    @*/
  while (low <= high) {
    int mid = (low + high) / 2;
    if (arr[mid] == target) {
      return mid;
    } else if (arr[mid] < target) {
      low = mid + 1;
    } else {
      high = mid - 1;
    }
  }
  return -1;
}
```

## Why3

### Basic Syntax

**Function Specification**:
```why3
val function_name (x: type1) (y: type2) : type3
  requires { precondition }
  ensures { postcondition }
```

**Implementation**:
```why3
let function_name (x: type1) (y: type2) : type3
  requires { precondition }
  ensures { postcondition }
= expression
```

**Loop**:
```why3
while condition do
  invariant { loop_invariant }
  variant { termination_measure }
  body
done
```

### Common Constructs

**Quantifiers**:
```why3
forall i: int. 0 <= i < n -> P i
exists i: int. 0 <= i < n /\ P i
```

**Array Operations**:
```why3
a[i]                       (* array access *)
a[i <- v]                  (* array update *)
a.length                   (* array length *)
```

**Old Values**:
```why3
old(expression)
```

**Predicates**:
```why3
predicate sorted (a: array int) (l u: int) =
  forall i j: int. l <= i < j < u -> a[i] <= a[j]
```

### Complete Example

```why3
use int.Int
use array.Array

predicate sorted (a: array int) (l u: int) =
  forall i j: int. l <= i < j < u -> a[i] <= a[j]

let binary_search (a: array int) (target: int) : int
  requires { a.length > 0 }
  requires { sorted a 0 a.length }
  ensures { result = -1 \/ (0 <= result < a.length /\ a[result] = target) }
  ensures { result <> -1 -> a[result] = target }
  ensures { result = -1 -> forall i: int. 0 <= i < a.length -> a[i] <> target }
=
  let ref low = 0 in
  let ref high = a.length - 1 in

  while low <= high do
    invariant { 0 <= low <= high + 1 <= a.length }
    invariant { forall i: int. 0 <= i < low -> a[i] < target }
    invariant { forall i: int. high < i < a.length -> a[i] > target }
    variant { high - low }

    let mid = (low + high) / 2 in
    if a[mid] = target then
      return mid
    else if a[mid] < target then
      low <- mid + 1
    else
      high <- mid - 1
  done;
  -1
```

## Comparison Table

| Feature | Dafny | Isabelle | Coq | ACSL | Why3 |
|---------|-------|----------|-----|------|------|
| **Quantifiers** | `forall`, `exists` | `∀`, `∃` | `forall`, `exists` | `\forall`, `\exists` | `forall`, `exists` |
| **Implication** | `==>` | `⟶` | `->` | `==>` | `->` |
| **Conjunction** | `&&` | `∧` | `/\` | `&&` | `/\` |
| **Disjunction** | `\|\|` | `∨` | `\/` | `\|\|` | `\/` |
| **Old values** | `old(x)` | N/A | N/A | `\old(x)` | `old(x)` |
| **Array length** | `arr.Length` | `length xs` | `length l` | `n` (parameter) | `a.length` |
| **Array access** | `arr[i]` | `xs ! i` | `nth i l def` | `arr[i]` | `a[i]` |
| **Membership** | `x in seq` | `x ∈ set xs` | `In x l` | N/A | N/A |

## Tips for Each Language

**Dafny**:
- Use `decreases` for termination proofs
- Leverage automatic verification
- Use `calc` for calculation proofs

**Isabelle**:
- Use `sledgehammer` for automatic proof search
- Leverage extensive library of lemmas
- Use `simp` and `auto` tactics

**Coq**:
- Use `induction` for recursive structures
- Leverage `omega` for arithmetic
- Use `auto` and `intuition` tactics

**ACSL**:
- Use Frama-C for verification
- Specify memory safety with `\valid`
- Use `\separated` for pointer aliasing

**Why3**:
- Supports multiple provers
- Use `ref` for mutable variables
- Leverage SMT solvers for automation
