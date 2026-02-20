# Extraction Patterns for Verified Code

## Table of Contents
1. Isabelle/HOL Extraction Patterns
2. Coq Extraction Patterns
3. Common Abstraction Rules
4. Verification Annotation Handling

## 1. Isabelle/HOL Extraction Patterns

### Function Definitions

**Pattern**: Extract `fun` definitions
```isabelle
fun insertion_sort :: "nat list ⇒ nat list" where
  "insertion_sort [] = []" |
  "insertion_sort (x # xs) = insert x (insertion_sort xs)"
```

**Extract to**:
```
FUNCTION insertion_sort(list: List<Nat>) -> List<Nat>
  IF list is empty THEN
    RETURN empty list
  ELSE
    LET x = head of list
    LET xs = tail of list
    LET sorted_xs = insertion_sort(xs)
    RETURN insert(x, sorted_xs)
```

### Preconditions and Postconditions

**Pattern**: Extract `assumes` and `shows`
```isabelle
lemma insertion_sort_correct:
  assumes "True"  (* No precondition *)
  shows "is_sorted (insertion_sort xs) ∧ set (insertion_sort xs) = set xs"
```

**Extract to**:
```
VERIFIED PROPERTY: insertion_sort_correct
  PRECONDITION: (none)
  POSTCONDITION:
    - is_sorted(insertion_sort(xs))
    - elements(insertion_sort(xs)) = elements(xs)
```

### Loop Invariants

**Pattern**: Extract from proof structure
```isabelle
proof (induction xs)
  case Nil
  (* Base case: sorted [] *)
  case (Cons x xs)
  (* Inductive case: sorted xs ⟹ sorted (insert x xs) *)
```

**Extract to**:
```
INVARIANT (structural induction on list):
  BASE: For empty list, property holds
  STEP: If property holds for xs, then holds for (x :: xs)
```

### Verified Helper Functions

**Pattern**: Extract lemmas used in main proof
```isabelle
lemma insert_sorted:
  assumes "is_sorted xs"
  shows "is_sorted (insert x xs)"
```

**Extract to**:
```
VERIFIED HELPER: insert_sorted
  PRECONDITION: is_sorted(xs)
  POSTCONDITION: is_sorted(insert(x, xs))
```

## 2. Coq Extraction Patterns

### Fixpoint Definitions

**Pattern**: Extract `Fixpoint` definitions
```coq
Fixpoint insertion_sort (l : list nat) : list nat :=
  match l with
  | [] => []
  | x :: xs => insert x (insertion_sort xs)
  end.
```

**Extract to**:
```
FUNCTION insertion_sort(l: List<Nat>) -> List<Nat>
  MATCH l WITH
    CASE []:
      RETURN []
    CASE x :: xs:
      LET sorted_xs = insertion_sort(xs)
      RETURN insert(x, sorted_xs)
```

### Specifications

**Pattern**: Extract theorem statements
```coq
Theorem insertion_sort_correct :
  forall l,
    is_sorted (insertion_sort l) /\
    Permutation l (insertion_sort l).
```

**Extract to**:
```
VERIFIED PROPERTY: insertion_sort_correct
  FOR ALL l:
    - is_sorted(insertion_sort(l))
    - permutation(l, insertion_sort(l))
```

### Inductive Predicates

**Pattern**: Extract inductive definitions
```coq
Inductive sorted : list nat -> Prop :=
  | sorted_nil : sorted []
  | sorted_single : forall x, sorted [x]
  | sorted_cons : forall x y l,
      x <= y -> sorted (y :: l) -> sorted (x :: y :: l).
```

**Extract to**:
```
PREDICATE sorted(list: List<Nat>) -> Bool
  DEFINED BY:
    - sorted([]) = true
    - sorted([x]) = true
    - sorted([x, y, ...rest]) = (x <= y) AND sorted([y, ...rest])
```

### Dependent Types

**Pattern**: Extract dependent function types
```coq
Definition safe_head (l : list nat) (H : l <> []) : nat :=
  match l with
  | [] => match H eq_refl with end
  | x :: _ => x
  end.
```

**Extract to**:
```
FUNCTION safe_head(l: List<Nat>) -> Nat
  PRECONDITION: l ≠ []  [VERIFIED]
  MATCH l WITH
    CASE []:
      UNREACHABLE  [precondition ensures this case impossible]
    CASE x :: _:
      RETURN x
```

## 3. Common Abstraction Rules

### Rule 1: Type Abstraction

**From**: Language-specific types
```
nat list, 'a list, list A
```

**To**: Generic types
```
List<Nat>, List<T>, List<A>
```

### Rule 2: Pattern Matching

**From**: Language-specific syntax
```isabelle
case xs of [] ⇒ ... | (x # xs) ⇒ ...
```
```coq
match l with | [] => ... | x :: xs => ... end
```

**To**: Unified syntax
```
MATCH xs WITH
  CASE []: ...
  CASE x :: xs: ...
```

### Rule 3: Recursion

**From**: Structural recursion with termination proofs
```isabelle
fun f :: "nat ⇒ nat" where
  "f 0 = 0" |
  "f (Suc n) = f n + 1"
```

**To**: Clear recursive structure
```
FUNCTION f(n: Nat) -> Nat
  IF n = 0 THEN
    RETURN 0
  ELSE
    RETURN f(n - 1) + 1
  [VERIFIED: terminates (decreasing n)]
```

### Rule 4: Quantifiers

**From**: Formal logic quantifiers
```
∀x. P x, ∃x. P x
forall x, P x, exists x, P x
```

**To**: Readable quantifiers
```
FOR ALL x: P(x)
EXISTS x: P(x)
```

### Rule 5: Logical Operators

**From**: Formal operators
```
∧, ∨, ⟶, ⟷, ¬
/\, \/, ->, <->, ~
```

**To**: Standard operators
```
AND, OR, IMPLIES, IFF, NOT
```

## 4. Verification Annotation Handling

### Verified Components

**Mark as verified**:
```
[VERIFIED] - Component has formal proof
[VERIFIED: property] - Specific property verified
```

**Example**:
```
FUNCTION binary_search(arr: Array<Int>, target: Int) -> Option<Int>
  PRECONDITION: is_sorted(arr)  [VERIFIED]
  POSTCONDITION:
    IF result = Some(i) THEN arr[i] = target  [VERIFIED]
    IF result = None THEN target NOT IN arr  [VERIFIED]
```

### Unverified Components

**Mark as unverified**:
```
[ASSUMED] - Not formally verified
[UNVERIFIED] - Implementation detail without proof
```

**Example**:
```
FUNCTION process_data(data: Data) -> Result
  [ASSUMED: data is well-formed]
  ...
```

### Partial Verification

**Mark partial verification**:
```
[VERIFIED: correctness]
[UNVERIFIED: termination]
```

**Example**:
```
FUNCTION complex_algorithm(input: Input) -> Output
  [VERIFIED: correctness - output satisfies specification]
  [UNVERIFIED: time complexity]
  ...
```

### Proof-Specific Details to Remove

**Remove**:
- Proof tactics (`by simp`, `auto`, `lia`)
- Proof structure (`proof`, `qed`, `Proof`, `Qed`)
- Intermediate lemmas used only for proof
- Type class constraints used only for proof
- Proof hints and annotations

**Keep**:
- Algorithmic structure
- Control flow
- Data dependencies
- Verified properties
- Essential preconditions/postconditions
- Loop invariants

### Language-Specific Details to Remove

**Remove**:
- Syntax sugar (`#` vs `::`, `@` vs `++`)
- Type annotations for inference
- Implicit arguments
- Module qualifications (unless essential)
- Proof-carrying code

**Keep**:
- Essential type information
- Explicit parameters
- Function names
- Data structure definitions

## Extraction Workflow

### Step 1: Identify Verified Components

Scan for:
- Function definitions with proofs
- Theorems about functions
- Verified properties
- Preconditions and postconditions

### Step 2: Extract Core Algorithm

Remove:
- Proof code
- Type system details
- Language-specific syntax

Preserve:
- Control flow
- Data flow
- Algorithmic logic

### Step 3: Add Verification Annotations

Mark:
- Verified properties
- Preconditions
- Postconditions
- Invariants
- Unverified assumptions

### Step 4: Simplify and Clarify

- Use clear variable names
- Add comments for complex logic
- Structure code readably
- Maintain semantic equivalence

## Examples of What to Preserve vs. Remove

### Preserve

✓ Control flow (if/then/else, loops, recursion)
✓ Data dependencies (which values depend on which)
✓ Algorithmic steps (what operations are performed)
✓ Verified properties (what has been proven)
✓ Preconditions and postconditions
✓ Loop invariants
✓ Function signatures (name, parameters, return type)

### Remove

✗ Proof tactics and commands
✗ Type class constraints for proof only
✗ Intermediate proof lemmas
✗ Language-specific syntax sugar
✗ Module system details
✗ Proof annotations
✗ Type inference hints
✗ Proof-carrying code constructs
