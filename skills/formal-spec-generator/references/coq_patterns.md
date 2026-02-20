# Coq Specification Patterns

## Table of Contents
1. Function Definitions
2. Data Type Definitions
3. Predicates and Properties
4. Pre/Post-conditions and Invariants
5. Common Patterns and Idioms

## 1. Function Definitions

### Basic Function Definition
```coq
Definition function_name (x : type1) (y : type2) : return_type :=
  expression.
```

### Recursive Function with Fixpoint
```coq
Fixpoint length {A : Type} (l : list A) : nat :=
  match l with
  | nil => 0
  | _ :: t => S (length t)
  end.
```

### Function with Pattern Matching
```coq
Definition max (x y : nat) : nat :=
  if x >=? y then x else y.
```

## 2. Data Type Definitions

### Simple Inductive Type
```coq
Inductive option (A : Type) : Type :=
  | None : option A
  | Some : A -> option A.
```

### Recursive Inductive Type
```coq
Inductive tree (A : Type) : Type :=
  | Leaf : tree A
  | Node : tree A -> A -> tree A -> tree A.
```

### Record Type
```coq
Record person := mkPerson {
  name : string;
  age : nat
}.
```

## 3. Predicates and Properties

### Simple Predicate Definition
```coq
Definition is_sorted (l : list nat) : Prop :=
  forall i j, i < j < length l -> nth i l 0 <= nth j l 0.
```

### Inductive Predicate
```coq
Inductive sorted : list nat -> Prop :=
  | sorted_nil : sorted nil
  | sorted_single : forall x, sorted (x :: nil)
  | sorted_cons : forall x y l,
      x <= y -> sorted (y :: l) -> sorted (x :: y :: l).
```

## 4. Pre/Post-conditions and Invariants

### Function Specification
```coq
Definition sort_spec (input output : list nat) : Prop :=
  is_sorted output /\
  Permutation input output.
```

### Loop Invariant Pattern
```coq
Definition loop_invariant (i : nat) (xs : list nat) : Prop :=
  i <= length xs /\
  forall j k, j < k < i -> nth j xs 0 <= nth k xs 0.
```

## 5. Common Patterns and Idioms

### Correctness Theorem
```coq
Theorem function_correct :
  forall input,
    precondition input ->
    postcondition (function input).
```

### Well-Founded Recursion
```coq
Program Fixpoint f (n : nat) {measure n} : nat :=
  match n with
  | 0 => 0
  | S n' => f n' + 1
  end.
```

### Quantifiers and Logical Operators
- Universal: `forall x, P x`
- Existential: `exists x, P x`
- Implication: `P -> Q`
- Conjunction: `P /\ Q`
- Disjunction: `P \/ Q`
- Negation: `~ P`
- Equivalence: `P <-> Q`

### List Operations
- Empty list: `nil`
- Cons: `x :: xs`
- Append: `xs ++ ys`
- Length: `length xs`
- Nth element: `nth n xs default`
- Map: `map f xs`
- Filter: `filter P xs`
- Fold: `fold_left f xs init` or `fold_right f xs init`

### Common Tactics (for reference)
- `intros`: Introduce hypotheses
- `apply`: Apply a theorem
- `induction`: Proof by induction
- `simpl`: Simplify expressions
- `reflexivity`: Prove equality
- `rewrite`: Rewrite using equality
- `destruct`: Case analysis
- `auto`: Automatic proof search
