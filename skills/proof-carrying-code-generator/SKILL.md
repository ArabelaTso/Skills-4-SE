---
name: proof-carrying-code-generator
description: Generate executable code together with formal proofs certifying safety and correctness properties in Isabelle/HOL or Coq. Use when building verified software, safety-critical systems, or when formal guarantees are required. Produces code with accompanying proofs for memory safety, bounds checking, functional correctness, invariant preservation, and termination. Supports extraction to OCaml/Haskell/SML and integration with existing codebases.
---

# Proof-Carrying Code Generator

Generate executable code bundled with formal proofs that certify key safety and correctness properties.

## Overview

Proof-carrying code (PCC) is executable code accompanied by formal proofs that certify specific properties. This skill helps generate:

1. **Verified implementations** with correctness proofs
2. **Safety certificates** for memory safety, bounds checking, null safety
3. **Functional specifications** with pre/postconditions
4. **Invariant proofs** for data structure integrity
5. **Extracted code** from verified specifications

The generated code can be extracted to mainstream languages (OCaml, Haskell, SML) while maintaining proof certificates.

## PCC Generation Workflow

```
Requirements
    ↓
Formal Specification
    ↓
Verified Implementation
    ↓
Proof Obligations
    ↓
Certified Code + Proofs
    ↓
Code Extraction
```

## Core Approaches

### Approach 1: Specification-First

Start with formal specification, implement, then prove.

**Steps:**
1. Write formal specification
2. Implement function/algorithm
3. State correctness theorem
4. Prove theorem
5. Extract code

**Example (Isabelle):**
```isabelle
(* Specification *)
definition sorted_spec :: "nat list ⇒ nat list ⇒ bool" where
  "sorted_spec input output ≡ sorted output ∧ mset output = mset input"

(* Implementation *)
fun insertion_sort :: "nat list ⇒ nat list" where
  "insertion_sort [] = []" |
  "insertion_sort (x # xs) = insert x (insertion_sort xs)"

(* Correctness theorem *)
theorem insertion_sort_correct:
  "sorted_spec input (insertion_sort input)"
proof (induction input)
  case Nil
  then show ?case by (simp add: sorted_spec_def)
next
  case (Cons x xs)
  then show ?case
    using insert_sorted mset_insert
    by (auto simp: sorted_spec_def)
qed

(* Extract code *)
export_code insertion_sort in SML file "sort.sml"
```

### Approach 2: Refinement-Based

Start abstract, refine to concrete with proofs at each step.

**Steps:**
1. Abstract specification
2. Refine to intermediate level
3. Prove refinement correct
4. Refine to executable code
5. Prove final refinement
6. Extract code

**Example (Coq):**
```coq
(* Abstract specification *)
Definition find_spec {A} (P : A → bool) (l : list A) : option A :=
  (* Nondeterministic: any element satisfying P *)
  ...

(* Concrete implementation *)
Fixpoint find {A} (P : A → bool) (l : list A) : option A :=
  match l with
  | [] => None
  | x :: xs => if P x then Some x else find P xs
  end.

(* Refinement proof *)
Theorem find_refines : forall A P l,
  find P l = find_spec P l.
Proof.
  (* Proof that concrete refines abstract *)
Qed.

(* Extract *)
Extraction "find.ml" find.
```

### Approach 3: Program-First

Write code with annotations, generate proof obligations, prove them.

**Steps:**
1. Write function with contracts
2. Generate verification conditions
3. Prove verification conditions
4. Certify code

**Example (Coq with Program):**
```coq
Require Import Program.

Program Definition safe_div (a b : nat) (H : b ≠ 0) : nat :=
  a / b.

(* Proof obligation automatically generated *)
Next Obligation.
  (* Prove division is safe *)
Qed.
```

## Safety Properties

### Memory Safety

**Property:** No buffer overflows, out-of-bounds access.

**Pattern:**
```isabelle
lemma array_access_safe:
  "⟦ i < length arr ⟧ ⟹ ∃v. arr ! i = v"
  by auto

fun safe_get :: "'a list ⇒ nat ⇒ 'a option" where
  "safe_get [] _ = None" |
  "safe_get (x # xs) 0 = Some x" |
  "safe_get (x # xs) (Suc n) = safe_get xs n"

lemma safe_get_bounds:
  "safe_get xs i = Some v ⟹ i < length xs"
  by (induction xs i rule: safe_get.induct) auto
```

### Null Safety

**Property:** No null pointer dereferences.

**Pattern:**
```coq
Definition safe_head {A} (l : list A) (H : l ≠ []) : A :=
  match l with
  | [] => match H eq_refl with end
  | x :: _ => x
  end.

Lemma safe_head_correct : forall A (l : list A) H,
  l ≠ [] → safe_head l H = hd_error l.
Proof.
  intros. destruct l; auto. contradiction.
Qed.
```

### Bounds Checking

**Property:** All array accesses within bounds.

**Pattern:**
```isabelle
definition bounded_access :: "'a array ⇒ nat ⇒ 'a option" where
  "bounded_access arr i = (if i < array_length arr
                           then Some (array_get arr i)
                           else None)"

lemma bounded_access_safe:
  "bounded_access arr i = Some v ⟹ i < array_length arr"
  by (simp add: bounded_access_def split: if_splits)
```

## Correctness Properties

### Functional Correctness

**Property:** Function computes correct result.

**Pattern:**
```isabelle
fun factorial :: "nat ⇒ nat" where
  "factorial 0 = 1" |
  "factorial (Suc n) = Suc n * factorial n"

function fact_spec :: "nat ⇒ nat" where
  "fact_spec 0 = 1" |
  "fact_spec n = n * fact_spec (n - 1)"
  by auto

theorem factorial_correct:
  "factorial n = fact_spec n"
  by (induction n) auto
```

### Invariant Preservation

**Property:** Data structure invariants maintained.

**Pattern:**
```coq
Inductive BST : tree → Prop :=
  | BST_leaf : BST Leaf
  | BST_node : forall l x r,
      BST l → BST r →
      (forall y, In y l → y < x) →
      (forall y, In y r → x < y) →
      BST (Node l x r).

Fixpoint insert (x : nat) (t : tree) : tree :=
  match t with
  | Leaf => Node Leaf x Leaf
  | Node l y r =>
      if x <? y then Node (insert x l) y r
      else if y <? x then Node l y (insert x r)
      else t
  end.

Theorem insert_preserves_BST : forall x t,
  BST t → BST (insert x t).
Proof.
  induction t; intros; simpl.
  - constructor; constructor.
  - inversion H; subst.
    destruct (x <? n) eqn:E1.
    + (* Insert left *)
    + destruct (n <? x) eqn:E2.
      * (* Insert right *)
      * (* Equal, no change *)
Qed.
```

### Termination

**Property:** Function always terminates.

**Pattern:**
```isabelle
function gcd :: "nat ⇒ nat ⇒ nat" where
  "gcd a 0 = a" |
  "gcd a b = gcd b (a mod b)"
  by auto
termination
  by (relation "measure (λ(a, b). b)") auto

lemma gcd_terminates:
  "∃result. gcd a b = result"
  by auto
```

## Framework-Specific Guidance

### Isabelle/HOL PCC

For Isabelle-specific code generation, extraction, and certification patterns, see [references/isabelle_pcc.md](references/isabelle_pcc.md).

Key features:
- Code generation to SML, OCaml, Haskell, Scala
- Refinement framework for verified implementations
- Sepref for imperative code with proofs
- Export with proof certificates

### Coq PCC

For Coq-specific extraction, Program framework, and certification, see [references/coq_pcc.md](references/coq_pcc.md).

Key features:
- Extraction to OCaml, Haskell, Scheme
- Program for proof obligations
- Equations for well-founded recursion
- Certified compilation

## Common Safety Properties

For detailed safety and correctness property patterns, see [references/safety_properties.md](references/safety_properties.md).

Categories include:
- Memory safety (bounds, null, use-after-free)
- Type safety (no type confusion)
- Arithmetic safety (no overflow, division by zero)
- Concurrency safety (no data races, deadlocks)
- Information flow security (no leaks)

## Complete Example: Verified Binary Search

**Specification:**
```isabelle
definition binary_search_spec :: "nat list ⇒ nat ⇒ nat option" where
  "binary_search_spec xs target = (
    if sorted xs ∧ target ∈ set xs
    then Some (THE i. i < length xs ∧ xs ! i = target)
    else None)"
```

**Implementation:**
```isabelle
fun binary_search :: "nat list ⇒ nat ⇒ nat option" where
  "binary_search xs target = bs_aux xs target 0 (length xs)"

fun bs_aux :: "nat list ⇒ nat ⇒ nat ⇒ nat ⇒ nat option" where
  "bs_aux xs target low high = (
    if low ≥ high then None
    else let mid = (low + high) div 2 in
         if xs ! mid = target then Some mid
         else if xs ! mid < target then bs_aux xs target (mid + 1) high
         else bs_aux xs target low mid)"
```

**Safety proofs:**
```isabelle
lemma bs_aux_bounds:
  "⟦ bs_aux xs target low high = Some i; low ≤ high; high ≤ length xs ⟧
   ⟹ low ≤ i ∧ i < high"
proof (induction xs target low high rule: bs_aux.induct)
  case (1 xs target low high)
  then show ?case
    by (auto simp: Let_def split: if_splits)
qed

lemma bs_aux_no_overflow:
  "⟦ low ≤ high; high ≤ length xs ⟧
   ⟹ (low + high) div 2 < length xs"
  by auto
```

**Correctness proof:**
```isabelle
theorem binary_search_correct:
  "sorted xs ⟹ binary_search xs target = binary_search_spec xs target"
proof -
  assume "sorted xs"
  show ?thesis
  proof (cases "target ∈ set xs")
    case True
    then show ?thesis
      using binary_search_finds_target[OF `sorted xs` True]
      by (simp add: binary_search_spec_def)
  next
    case False
    then show ?thesis
      using binary_search_not_found[OF `sorted xs` False]
      by (simp add: binary_search_spec_def)
  qed
qed
```

**Code extraction:**
```isabelle
export_code binary_search in SML file "binary_search.sml"
export_code binary_search in OCaml file "binary_search.ml"
```

## Best Practices

1. **Start with Specifications**: Clear specs before implementation
2. **Incremental Verification**: Verify small pieces, compose
3. **Reuse Lemmas**: Build library of certified components
4. **Automate Proofs**: Use tactics and automation where possible
5. **Test Extracted Code**: Verify extraction produces correct code
6. **Document Properties**: Clearly state what's certified
7. **Modular Design**: Separate concerns, verify independently

## Verification Checklist

Before finalizing proof-carrying code:

- [ ] All safety properties proven
- [ ] Functional correctness established
- [ ] Termination proven (if applicable)
- [ ] Invariants maintained
- [ ] Bounds checking verified
- [ ] Code extracts successfully
- [ ] Extracted code tested
- [ ] Proof certificates included
- [ ] Documentation complete

## Integration Patterns

### Integrating with Existing Code

**Pattern:** Verify critical components, interface with unverified code.

**Example:**
```isabelle
(* Verified core *)
definition verified_sort :: "nat list ⇒ nat list" where
  "verified_sort = insertion_sort"

theorem verified_sort_correct:
  "sorted (verified_sort xs) ∧ mset (verified_sort xs) = mset xs"
  by (simp add: verified_sort_def insertion_sort_correct)

(* Export for use in larger system *)
export_code verified_sort in OCaml file "verified_sort.ml"
```

### Certified Libraries

**Pattern:** Build library of verified functions.

**Example:**
```coq
Module VerifiedList.
  (* Verified operations *)
  Definition safe_nth := ...
  Definition safe_update := ...
  Definition verified_map := ...

  (* Correctness theorems *)
  Theorem safe_nth_correct : ...
  Theorem safe_update_correct : ...
  Theorem verified_map_correct : ...
End VerifiedList.

(* Extract entire module *)
Extraction "verified_list.ml" VerifiedList.
```

## Additional Resources

For detailed guidance on specific aspects:
- [Isabelle PCC](references/isabelle_pcc.md) - Isabelle/HOL code generation and certification
- [Coq PCC](references/coq_pcc.md) - Coq extraction and Program framework
- [Safety Properties](references/safety_properties.md) - Common safety and correctness properties
