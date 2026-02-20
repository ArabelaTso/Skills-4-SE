# Imperative Code to Coq Model Extraction Patterns

This reference provides detailed patterns for extracting mathematical models from imperative code for reasoning in Coq.

## Table of Contents

1. [Basic Data Types](#basic-data-types)
2. [State and Variables](#state-and-variables)
3. [Functions and Procedures](#functions-and-procedures)
4. [Control Flow](#control-flow)
5. [Data Structures](#data-structures)
6. [Memory and Pointers](#memory-and-pointers)
7. [Specifications](#specifications)

## Basic Data Types

### Integers

**Imperative Code:**
```c
int x = 42;
unsigned int y = 10;
```

**Coq Model:**
```coq
(* Use Z for arbitrary precision integers *)
Definition x : Z := 42.

(* Use nat for natural numbers *)
Definition y : nat := 10.
```

### Booleans

**Imperative Code:**
```c
bool flag = true;
```

**Coq Model:**
```coq
Definition flag : bool := true.
```

### Enumerations

**Imperative Code:**
```c
enum Color { RED, GREEN, BLUE };
```

**Coq Model:**
```coq
Inductive Color : Type :=
  | RED : Color
  | GREEN : Color
  | BLUE : Color.
```

## State and Variables

### Program State

**Imperative Code:**
```c
int x = 0;
int y = 0;

void update() {
    x = x + 1;
    y = y * 2;
}
```

**Coq Model:**
```coq
(* Model state as a record *)
Record State : Type := mkState {
  x : Z;
  y : Z
}.

(* Initial state *)
Definition init_state : State := {|
  x := 0;
  y := 0
|}.

(* State update function *)
Definition update (s : State) : State := {|
  x := s.(x) + 1;
  y := s.(y) * 2
|}.
```

### Mutable Variables

**Imperative Code:**
```python
counter = 0

def increment():
    global counter
    counter += 1
```

**Coq Model:**
```coq
(* Model as state transformation *)
Definition counter_state : Type := Z.

Definition init_counter : counter_state := 0.

Definition increment (c : counter_state) : counter_state :=
  c + 1.
```

## Functions and Procedures

### Pure Functions

**Imperative Code:**
```c
int add(int a, int b) {
    return a + b;
}
```

**Coq Model:**
```coq
Definition add (a b : Z) : Z := a + b.
```

### Functions with Side Effects

**Imperative Code:**
```c
int global_sum = 0;

void add_to_sum(int x) {
    global_sum += x;
}
```

**Coq Model:**
```coq
(* Model state explicitly *)
Definition add_to_sum (x : Z) (sum : Z) : Z :=
  sum + x.

(* Or use a state monad *)
Definition add_to_sum_stateful (x : Z) : State -> State :=
  fun s => {| sum := s.(sum) + x |}.
```

### Procedures with Multiple Effects

**Imperative Code:**
```c
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}
```

**Coq Model:**
```coq
(* Model as tuple transformation *)
Definition swap (ab : Z * Z) : Z * Z :=
  let (a, b) := ab in (b, a).

(* Or with explicit state *)
Record SwapState : Type := mkSwapState {
  a : Z;
  b : Z
}.

Definition swap_state (s : SwapState) : SwapState := {|
  a := s.(b);
  b := s.(a)
|}.
```

## Control Flow

### Conditionals

**Imperative Code:**
```c
int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

**Coq Model:**
```coq
Definition max (a b : Z) : Z :=
  if a >? b then a else b.
```

### Loops as Recursion

**Imperative Code:**
```c
int factorial(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
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

(* Or model the loop state explicitly *)
Record FactState : Type := mkFactState {
  i : nat;
  result : nat
}.

Fixpoint factorial_loop (n : nat) (s : FactState) : nat :=
  match n with
  | 0 => s.(result)
  | S n' =>
      if s.(i) <=? n then
        factorial_loop n' {| i := S s.(i); result := s.(result) * s.(i) |}
      else
        s.(result)
  end.
```

### While Loops

**Imperative Code:**
```c
int sum_to_n(int n) {
    int sum = 0;
    int i = 0;
    while (i < n) {
        sum += i;
        i++;
    }
    return sum;
}
```

**Coq Model:**
```coq
(* Model as tail-recursive function *)
Fixpoint sum_to_n_aux (n i sum : nat) : nat :=
  match n with
  | 0 => sum
  | S n' =>
      if i <? n then
        sum_to_n_aux n (S i) (sum + i)
      else
        sum
  end.

Definition sum_to_n (n : nat) : nat :=
  sum_to_n_aux n 0 0.
```

## Data Structures

### Arrays

**Imperative Code:**
```c
int arr[5] = {1, 2, 3, 4, 5};
int sum = 0;
for (int i = 0; i < 5; i++) {
    sum += arr[i];
}
```

**Coq Model:**
```coq
Require Import List.
Import ListNotations.

Definition arr : list Z := [1; 2; 3; 4; 5].

Fixpoint sum_list (l : list Z) : Z :=
  match l with
  | [] => 0
  | x :: xs => x + sum_list xs
  end.

Definition sum : Z := sum_list arr.
```

### Structs/Records

**Imperative Code:**
```c
struct Point {
    int x;
    int y;
};

int distance_squared(struct Point p) {
    return p.x * p.x + p.y * p.y;
}
```

**Coq Model:**
```coq
Record Point : Type := mkPoint {
  x : Z;
  y : Z
}.

Definition distance_squared (p : Point) : Z :=
  p.(x) * p.(x) + p.(y) * p.(y).
```

### Linked Lists

**Imperative Code:**
```c
struct Node {
    int data;
    struct Node* next;
};
```

**Coq Model:**
```coq
(* Use Coq's built-in list type *)
Inductive list (A : Type) : Type :=
  | nil : list A
  | cons : A -> list A -> list A.

(* Or define custom inductive type *)
Inductive IntList : Type :=
  | Empty : IntList
  | Node : Z -> IntList -> IntList.
```

## Memory and Pointers

### Pointer Dereferencing

**Imperative Code:**
```c
int get_value(int *ptr) {
    return *ptr;
}
```

**Coq Model:**
```coq
(* Model memory as a map *)
Require Import FMaps.

Definition Memory := FMap.t Z Z.

Definition get_value (addr : Z) (mem : Memory) : option Z :=
  FMap.find addr mem.
```

### Memory Updates

**Imperative Code:**
```c
void set_value(int *ptr, int value) {
    *ptr = value;
}
```

**Coq Model:**
```coq
Definition set_value (addr : Z) (value : Z) (mem : Memory) : Memory :=
  FMap.add addr value mem.
```

### Heap Allocation

**Imperative Code:**
```c
int* allocate() {
    int* ptr = malloc(sizeof(int));
    *ptr = 42;
    return ptr;
}
```

**Coq Model:**
```coq
(* Model heap as state with fresh address generation *)
Record HeapState : Type := mkHeapState {
  memory : Memory;
  next_addr : Z
}.

Definition allocate (value : Z) (h : HeapState) : Z * HeapState :=
  let addr := h.(next_addr) in
  let new_mem := FMap.add addr value h.(memory) in
  (addr, {| memory := new_mem; next_addr := addr + 1 |}).
```

## Specifications

### Preconditions and Postconditions

**Imperative Code:**
```c
// Requires: n >= 0
// Ensures: result >= 0
int abs(int n) {
    if (n < 0) return -n;
    else return n;
}
```

**Coq Model:**
```coq
Definition abs (n : Z) : Z :=
  if n <? 0 then -n else n.

(* Specification *)
Lemma abs_nonneg : forall n : Z,
  abs n >= 0.
Proof.
  intros n.
  unfold abs.
  destruct (n <? 0) eqn:E.
  - (* n < 0 case *)
    apply Z.ltb_lt in E.
    lia.
  - (* n >= 0 case *)
    apply Z.ltb_ge in E.
    lia.
Qed.

Lemma abs_spec : forall n : Z,
  (n >= 0 -> abs n = n) /\ (n < 0 -> abs n = -n).
Proof.
  intros n.
  unfold abs.
  split; intros H.
  - (* n >= 0 *)
    destruct (n <? 0) eqn:E.
    + apply Z.ltb_lt in E. lia.
    + reflexivity.
  - (* n < 0 *)
    destruct (n <? 0) eqn:E.
    + reflexivity.
    + apply Z.ltb_ge in E. lia.
Qed.
```

### Loop Invariants

**Imperative Code:**
```c
// Invariant: sum = sum of arr[0..i-1]
int array_sum(int arr[], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum;
}
```

**Coq Model:**
```coq
Require Import List.
Import ListNotations.

Fixpoint sum_first_n (l : list Z) (n : nat) : Z :=
  match n, l with
  | 0, _ => 0
  | S n', x :: xs => x + sum_first_n xs n'
  | S n', [] => 0
  end.

Fixpoint array_sum_aux (l : list Z) (i : nat) (sum : Z) : Z :=
  match l with
  | [] => sum
  | x :: xs =>
      if i <? length (x :: xs) then
        array_sum_aux xs (S i) (sum + x)
      else
        sum
  end.

(* Invariant: sum = sum_first_n original_list i *)
Lemma array_sum_invariant : forall l i sum,
  array_sum_aux l i sum = sum + sum_first_n l (length l - i).
Proof.
  (* Proof by induction *)
Admitted.
```

### Functional Correctness

**Imperative Code:**
```c
// Returns the maximum element in array
int find_max(int arr[], int n) {
    int max = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}
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

(* Specification: result is in the list *)
Lemma find_max_in_list : forall l default,
  l <> [] ->
  In (find_max l default) l.
Proof.
  (* Proof by induction *)
Admitted.

(* Specification: result is >= all elements *)
Lemma find_max_is_max : forall l default x,
  In x l ->
  x <= find_max l default.
Proof.
  (* Proof by induction *)
Admitted.
```

## Common Patterns

### State Machine

**Imperative Code:**
```c
enum State { IDLE, RUNNING, STOPPED };
enum State current_state = IDLE;

void start() {
    if (current_state == IDLE) {
        current_state = RUNNING;
    }
}

void stop() {
    if (current_state == RUNNING) {
        current_state = STOPPED;
    }
}
```

**Coq Model:**
```coq
Inductive MachineState : Type :=
  | IDLE : MachineState
  | RUNNING : MachineState
  | STOPPED : MachineState.

Definition start (s : MachineState) : MachineState :=
  match s with
  | IDLE => RUNNING
  | _ => s
  end.

Definition stop (s : MachineState) : MachineState :=
  match s with
  | RUNNING => STOPPED
  | _ => s
  end.

(* Specify valid transitions *)
Inductive valid_transition : MachineState -> MachineState -> Prop :=
  | trans_start : valid_transition IDLE RUNNING
  | trans_stop : valid_transition RUNNING STOPPED
  | trans_stay : forall s, valid_transition s s.
```

### Binary Search

**Imperative Code:**
```c
int binary_search(int arr[], int n, int target) {
    int left = 0;
    int right = n - 1;
    while (left <= right) {
        int mid = (left + right) / 2;
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}
```

**Coq Model:**
```coq
Require Import List.
Import ListNotations.

Fixpoint binary_search_aux (l : list Z) (target : Z) (left right : nat) : option nat :=
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
