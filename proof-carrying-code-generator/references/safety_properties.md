# Safety and Correctness Properties

Catalog of common safety and correctness properties to certify in proof-carrying code.

## Memory Safety Properties

### Bounds Checking

**Property:** All array/list accesses are within valid bounds.

**Specification:**
```
∀i. access(arr, i) = Some v ⟹ 0 ≤ i < length(arr)
```

**Example patterns:**
```isabelle
(* Isabelle *)
lemma safe_access:
  "i < length xs ⟹ ∃v. xs ! i = v"

lemma safe_nth_option:
  "nth_option xs i = Some v ⟹ i < length xs ∧ xs ! i = v"
```

```coq
(* Coq *)
Lemma safe_nth : forall A (l : list A) n v,
  nth_error l n = Some v → n < length l.
```

**When to certify:** Array operations, indexing, buffer access.

### No Buffer Overflow

**Property:** Write operations don't exceed allocated space.

**Specification:**
```
∀i v. update(arr, i, v) succeeds ⟹ i < capacity(arr)
```

**Example patterns:**
```isabelle
lemma safe_update:
  "⟦ i < length arr; length arr ≤ capacity ⟧
   ⟹ ∃arr'. update arr i v = Some arr'"
```

**When to certify:** Buffer writes, string operations, dynamic arrays.

### No Use-After-Free

**Property:** No access to deallocated memory.

**Specification:**
```
∀ptr. access(ptr) ⟹ allocated(ptr)
```

**Example patterns:**
```isabelle
(* Use linear types or ownership *)
lemma no_use_after_free:
  "⟦ owns(ctx, ptr); freed(ctx, ptr) ⟧
   ⟹ ¬ can_access(ctx, ptr)"
```

**When to certify:** Manual memory management, resource handling.

## Null Safety Properties

### No Null Dereference

**Property:** Never dereference null pointers.

**Specification:**
```
∀ptr. dereference(ptr) ⟹ ptr ≠ null
```

**Example patterns:**
```isabelle
(* Use option types *)
lemma safe_deref:
  "deref opt = Some v ⟹ opt ≠ None"
```

```coq
(* Use dependent types *)
Definition safe_head {A} (l : list A) (H : l ≠ []) : A :=
  match l with
  | [] => match H eq_refl with end
  | x :: _ => x
  end.
```

**When to certify:** Pointer operations, optional values, head/tail operations.

### Non-Empty Guarantees

**Property:** Operations on non-empty collections.

**Specification:**
```
∀xs. head(xs) defined ⟹ xs ≠ []
```

**Example patterns:**
```isabelle
typedef 'a nonempty_list = "{xs :: 'a list. xs ≠ []}"

lemma head_nonempty:
  "xs ≠ [] ⟹ ∃x. hd xs = x"
```

**When to certify:** Head, tail, minimum, maximum operations.

## Arithmetic Safety Properties

### No Division by Zero

**Property:** Divisor is never zero.

**Specification:**
```
∀a b. divide(a, b) defined ⟹ b ≠ 0
```

**Example patterns:**
```isabelle
definition safe_div :: "nat ⇒ nat ⇒ nat option" where
  "safe_div a b = (if b ≠ 0 then Some (a div b) else None)"

lemma safe_div_correct:
  "safe_div a b = Some q ⟹ b ≠ 0 ∧ a div b = q"
```

```coq
Program Definition safe_div (a b : nat) (H : b ≠ 0) : nat :=
  a / b.
```

**When to certify:** Division, modulo, rational operations.

### No Integer Overflow

**Property:** Arithmetic operations stay within bounds.

**Specification:**
```
∀a b. add(a, b) = c ⟹ c ≤ MAX_INT
```

**Example patterns:**
```isabelle
definition safe_add :: "nat ⇒ nat ⇒ nat option" where
  "safe_add a b = (if a + b ≤ MAX_NAT then Some (a + b) else None)"

lemma safe_add_no_overflow:
  "safe_add a b = Some c ⟹ c ≤ MAX_NAT"
```

**When to certify:** Arithmetic on bounded integers, financial calculations.

### No Underflow

**Property:** Subtraction doesn't go negative (for unsigned).

**Specification:**
```
∀a b. subtract(a, b) = c ⟹ a ≥ b
```

**Example patterns:**
```isabelle
definition safe_sub :: "nat ⇒ nat ⇒ nat option" where
  "safe_sub a b = (if a ≥ b then Some (a - b) else None)"
```

**When to certify:** Natural number arithmetic, unsigned operations.

## Type Safety Properties

### No Type Confusion

**Property:** Values used according to their types.

**Specification:**
```
∀v T. typeof(v) = T ⟹ operations_on(v) valid_for T
```

**Example patterns:**
```isabelle
(* Strong typing prevents this *)
datatype value = IntVal int | BoolVal bool

fun eval :: "expr ⇒ value option" where
  "eval (Add e1 e2) = (case (eval e1, eval e2) of
    (Some (IntVal n1), Some (IntVal n2)) ⇒ Some (IntVal (n1 + n2))
  | _ ⇒ None)"
```

**When to certify:** Dynamic typing, type casts, variant types.

### Well-Typed Programs

**Property:** All expressions have valid types.

**Specification:**
```
∀e Γ. typecheck(Γ, e) = Some T ⟹ well_typed(Γ, e, T)
```

**Example patterns:**
```coq
Inductive has_type : context → expr → type → Prop :=
  | T_Var : forall Γ x T,
      lookup Γ x = Some T →
      has_type Γ (Var x) T
  | T_App : forall Γ e1 e2 T1 T2,
      has_type Γ e1 (Arrow T1 T2) →
      has_type Γ e2 T1 →
      has_type Γ (App e1 e2) T2.
```

**When to certify:** Type checkers, interpreters, compilers.

## Functional Correctness Properties

### Input-Output Specification

**Property:** Function produces correct output for given input.

**Specification:**
```
∀input. output = f(input) ⟹ spec(input, output)
```

**Example patterns:**
```isabelle
definition sort_spec :: "'a list ⇒ 'a list ⇒ bool" where
  "sort_spec input output ≡ sorted output ∧ mset output = mset input"

theorem sort_correct:
  "sort_spec input (my_sort input)"
```

```coq
Definition sort_spec (input output : list nat) : Prop :=
  Sorted le output /\ Permutation input output.

Theorem sort_correct : forall input,
  sort_spec input (my_sort input).
```

**When to certify:** All functions with clear specifications.

### Precondition-Postcondition

**Property:** If precondition holds, postcondition holds after execution.

**Specification:**
```
∀input. pre(input) ⟹ post(input, f(input))
```

**Example patterns:**
```isabelle
lemma binary_search_correct:
  "⟦ sorted xs; target ∈ set xs ⟧
   ⟹ ∃i. binary_search xs target = Some i ∧ xs ! i = target"
```

**When to certify:** Functions with assumptions about inputs.

### Equivalence to Specification

**Property:** Implementation equivalent to abstract specification.

**Specification:**
```
∀input. impl(input) = spec(input)
```

**Example patterns:**
```isabelle
definition factorial_spec :: "nat ⇒ nat" where
  "factorial_spec n = (if n = 0 then 1 else n * factorial_spec (n - 1))"

theorem factorial_correct:
  "factorial_impl n = factorial_spec n"
```

**When to certify:** Optimized implementations, refactored code.

## Invariant Properties

### Data Structure Invariants

**Property:** Invariant maintained by all operations.

**Specification:**
```
∀ds op. invariant(ds) ∧ ds' = op(ds) ⟹ invariant(ds')
```

**Example patterns:**
```isabelle
(* Binary search tree invariant *)
fun bst :: "nat tree ⇒ bool" where
  "bst Leaf = True" |
  "bst (Node l x r) = (bst l ∧ bst r ∧
    (∀y ∈ set_tree l. y < x) ∧
    (∀y ∈ set_tree r. x < y))"

theorem insert_preserves_bst:
  "bst t ⟹ bst (insert x t)"
```

```coq
Inductive BST : tree → Prop :=
  | BST_leaf : BST Leaf
  | BST_node : forall l x r,
      BST l → BST r →
      (forall y, In y l → y < x) →
      (forall y, In y r → x < y) →
      BST (Node l x r).

Theorem insert_preserves_BST : forall x t,
  BST t → BST (insert x t).
```

**When to certify:** Data structures (trees, heaps, graphs), containers.

### Loop Invariants

**Property:** Invariant holds before, during, and after loop.

**Specification:**
```
invariant(init) ∧
(∀state. invariant(state) ∧ condition(state) ⟹ invariant(step(state))) ∧
(∀state. invariant(state) ∧ ¬condition(state) ⟹ postcondition(state))
```

**Example patterns:**
```isabelle
lemma sum_loop_correct:
  "⟦ i ≤ n; sum = sum_upto i ⟧
   ⟹ (WHILE i < n DO (sum := sum + i; i := i + 1))
      terminates with sum = sum_upto n"
```

**When to certify:** Iterative algorithms, accumulation loops.

## Termination Properties

### Total Correctness

**Property:** Function always terminates with correct result.

**Specification:**
```
∀input. ∃output. f(input) = output ∧ spec(input, output)
```

**Example patterns:**
```isabelle
function gcd :: "nat ⇒ nat ⇒ nat" where
  "gcd a 0 = a" |
  "gcd a b = gcd b (a mod b)"
  by auto
termination
  by (relation "measure (λ(a, b). b)") auto

theorem gcd_terminates:
  "∃result. gcd a b = result"
```

**When to certify:** Recursive functions, loops, algorithms.

### Decreasing Measure

**Property:** Recursive calls decrease a well-founded measure.

**Specification:**
```
∀args. recursive_call(args') ⟹ measure(args') < measure(args)
```

**Example patterns:**
```coq
Require Import Equations.Equations.

Equations quicksort (l : list nat) : list nat by wf (length l) lt :=
  quicksort [] := [];
  quicksort (pivot :: xs) :=
    let (smaller, larger) := partition pivot xs in
    quicksort smaller ++ [pivot] ++ quicksort larger.
```

**When to certify:** Recursive algorithms, divide-and-conquer.

## Concurrency Safety Properties

### No Data Races

**Property:** No concurrent access to shared mutable state.

**Specification:**
```
∀t1 t2 loc. access(t1, loc) ∧ access(t2, loc) ⟹ synchronized(t1, t2, loc)
```

**Example patterns:**
```isabelle
(* Use separation logic *)
lemma no_race:
  "⟦ thread1_owns loc; thread2_owns loc ⟧ ⟹ False"
```

**When to certify:** Concurrent programs, parallel algorithms.

### Deadlock Freedom

**Property:** No circular wait for resources.

**Specification:**
```
∀threads. waiting_for(threads) ⟹ ∃t. can_proceed(t)
```

**Example patterns:**
```isabelle
(* Use resource ordering *)
lemma deadlock_free:
  "⟦ lock_order(l1, l2); holds(t, l1) ⟧
   ⟹ can_acquire(t, l2)"
```

**When to certify:** Lock-based synchronization, resource allocation.

## Information Flow Security

### Non-Interference

**Property:** High-security inputs don't affect low-security outputs.

**Specification:**
```
∀input1 input2. input1 =_low input2 ⟹ f(input1) =_low f(input2)
```

**Example patterns:**
```isabelle
definition noninterference :: "('a ⇒ 'b) ⇒ bool" where
  "noninterference f ≡
    ∀x y. low_equiv x y ⟹ low_equiv (f x) (f y)"

theorem secure_function:
  "noninterference my_function"
```

**When to certify:** Security-critical code, cryptography.

### No Information Leakage

**Property:** Secret data not revealed through side channels.

**Specification:**
```
∀secret1 secret2. observable(f(secret1)) = observable(f(secret2))
```

**Example patterns:**
```isabelle
lemma constant_time:
  "∀x y. execution_time (f x) = execution_time (f y)"
```

**When to certify:** Cryptographic implementations, secure protocols.

## Completeness Properties

### Total Function

**Property:** Function defined for all inputs.

**Specification:**
```
∀input. ∃output. f(input) = output
```

**Example patterns:**
```isabelle
lemma total_function:
  "∀x. ∃y. f x = y"
```

**When to certify:** Functions that should handle all cases.

### Exhaustive Pattern Matching

**Property:** All cases covered.

**Specification:**
```
∀value. ∃branch. matches(value, branch)
```

**Example patterns:**
```coq
Definition handle_all (b : bool) : nat :=
  match b with
  | true => 1
  | false => 0
  end.

(* Coq ensures exhaustiveness *)
```

**When to certify:** Case analysis, pattern matching.

## Property Selection Guide

### Critical Systems

**Must certify:**
- Memory safety (bounds, null, use-after-free)
- Arithmetic safety (division by zero, overflow)
- Functional correctness
- Termination

### Security Systems

**Must certify:**
- Information flow security
- No side channels
- Cryptographic correctness
- Access control

### General Software

**Should certify:**
- Functional correctness
- Key invariants
- Termination of critical loops
- Bounds checking for arrays

### Performance-Critical Code

**Should certify:**
- Functional correctness
- Complexity bounds
- Resource usage limits
