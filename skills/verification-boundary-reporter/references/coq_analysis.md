# Coq Verification Boundary Analysis

Guide for analyzing verification boundaries in Coq projects.

## Identifying Verified Components

### Complete Proofs

**Indicators of verified code:**
```coq
(* VERIFIED: Complete proof *)
Lemma my_property : statement.
Proof.
  (* proof steps *)
Qed.

(* VERIFIED: Automatic proof *)
Lemma simple_property : statement.
Proof.
  auto.
Qed.

(* VERIFIED: Tactic proof *)
Lemma proven : statement.
Proof.
  intros. induction x; simpl; auto.
Qed.
```

### Checking Proof Status

**Commands:**
```coq
(* Check if definition exists *)
Check my_lemma.

(* Print proof term *)
Print my_lemma.

(* Search for incomplete proofs *)
Search "Admitted".
```

## Identifying Assumptions

### Admitted and Admit

**Incomplete proofs:**
```coq
(* ASSUMED: Proof incomplete *)
Lemma unproven : statement.
Proof.
  (* some steps *)
Admitted.

(* ASSUMED: Proof step admitted *)
Lemma partial : statement.
Proof.
  intros.
  admit.  (* RED FLAG: proof step skipped *)
Qed.

(* ASSUMED: Proof obligation not discharged *)
Program Definition func := ...
Next Obligation.
Admitted.  (* RED FLAG *)
```

### Axioms

**Explicit axioms:**
```coq
(* ASSUMED: Axiom *)
Axiom functional_extensionality : forall A B (f g : A -> B),
  (forall x, f x = g x) -> f = g.

(* ASSUMED: Parameter without definition *)
Parameter mysterious_constant : nat -> nat.

(* ASSUMED: Axiom from standard library *)
Require Import Classical.
(* Imports excluded_middle axiom *)
```

### Common Standard Axioms

**Frequently used axioms:**
```coq
(* Classical logic *)
Axiom classic : forall P : Prop, P \/ ~ P.
Axiom excluded_middle : forall P : Prop, P \/ ~ P.

(* Functional extensionality *)
Axiom functional_extensionality : ...

(* Propositional extensionality *)
Axiom propositional_extensionality : forall P Q : Prop,
  (P <-> Q) -> P = Q.

(* Proof irrelevance *)
Axiom proof_irrelevance : forall (P : Prop) (p1 p2 : P), p1 = p2.
```

**Report template:**
```markdown
### functional_extensionality
**Type:** Axiom (Standard Library)
**Source:** Coq.Logic.FunctionalExtensionality
**Statement:** Functions equal if pointwise equal
**Justification:** Standard axiom, consistent with Coq's logic
**Risk Level:** Low - well-understood, widely used
```

## Trusted Computing Base

### Coq Kernel

**Always in TCB:**
- Coq kernel (type checker and proof checker)
- Calculus of Inductive Constructions (CIC)
- Core tactics
- Conversion checking

**Documentation:**
```markdown
### Coq Kernel
**Type:** Proof Assistant Kernel
**Description:** Core type checker implementing CIC
**Justification:** Cannot verify the verifier within itself
**Mitigation:** Small kernel, formally specified, decades of use
```

### Standard Library

**Library usage:**
```coq
(* TCB: Standard library *)
Require Import List.
Require Import Arith.
Require Import Sorted.

(* Document each import *)
```

### Extraction

**Code extraction:**
```coq
(* TCB: Extraction *)
Require Extraction.
Extraction Language OCaml.
Extraction "output.ml" my_function.
```

**Report template:**
```markdown
### Extraction to OCaml
**Type:** Code Extraction Tool
**Description:** Translates Coq definitions to OCaml
**Justification:** Enables execution of verified code
**Mitigation:** Extraction erases proofs but preserves computational content.
Extraction correctness is not formally verified.
**Risk:** Medium - semantic gaps possible, especially with:
  - Native integers vs Coq nat
  - Side effects and I/O
  - Extraction of axioms
```

### Extraction Customization

**Custom extraction:**
```coq
(* TCB: Custom type mapping *)
Extract Inductive nat => "int"
  [ "0" "(fun x -> x + 1)" ]
  "(fun zero succ n -> if n = 0 then zero else succ (n - 1))".

(* TCB: Custom constant mapping *)
Extract Constant plus => "(+)".
```

**Report:**
```markdown
### Custom Extraction: nat to int
**Type:** Extraction Customization
**Description:** Maps Coq nat to OCaml int
**Risk:** HIGH - Coq nat is unbounded, OCaml int is bounded
**Impact:** Potential integer overflow in extracted code
**Recommendation:** Add overflow checks or use Big_int
```

## Unverified Components

### Definitions Without Properties

**Unverified code:**
```coq
(* UNVERIFIED: No properties proven *)
Fixpoint my_function (n : nat) : nat :=
  match n with
  | 0 => 0
  | S n' => n + my_function n'
  end.
(* No theorems about my_function *)
```

### External Code

**Opaque definitions:**
```coq
(* UNVERIFIED: External implementation *)
Parameter external_func : nat -> nat.
Extract Constant external_func => "ExternalModule.func".
```

**Report:**
```markdown
### external_func
**Location:** Module.v:42
**Reason:** Implemented in external OCaml code
**Risk Assessment:** HIGH - no formal verification
**Recommendation:** Verify or replace with Coq implementation
```

## Dependency Analysis

### Finding Dependencies

**Commands:**
```coq
(* Print dependencies *)
Print Assumptions my_theorem.

(* Shows all axioms and parameters used *)
```

**Example output:**
```
Axioms:
functional_extensionality : ...
classic : ...

Parameters:
mysterious_constant : nat -> nat
```

### Assumption Propagation

**Example:**
```coq
Axiom unproven : P.

Lemma depends_on_axiom : Q.
Proof.
  apply unproven.  (* Uses axiom *)
  (* ... *)
Qed.

Theorem final_result : R.
Proof.
  apply depends_on_axiom.  (* Indirectly uses axiom *)
  (* ... *)
Qed.
```

**Check:**
```coq
Print Assumptions final_result.
(* Output: Axioms: unproven : P *)
```

**Report:**
```markdown
### Assumption Propagation

Axiom: unproven
  ↓ (used by)
Lemma: depends_on_axiom
  ↓ (used by)
Theorem: final_result

**Command:** `Print Assumptions final_result`
**Result:** Depends on axiom 'unproven'
**Risk Level:** HIGH
```

## Coverage Analysis

### Calculating Coverage

**Metrics:**
```
Total definitions: Count Fixpoint, Definition, Inductive
Total lemmas: Count Lemma, Theorem, Corollary
Verified: Lemmas ending with Qed
Assumed: Lemmas ending with Admitted, or using admit
Axioms: Count Axiom, Parameter
```

**Example:**
```markdown
## Verification Statistics

- Total definitions: 12
- Total lemmas: 18
- Verified: 15 (83%)
- Admitted: 3 (17%)
- Axioms: 2
- Extracted functions: 8
```

## Red Flags

### Critical Issues

**High-priority red flags:**
```coq
(* RED FLAG: Core theorem unproven *)
Theorem main_correctness : critical_property.
Proof.
Admitted.

(* RED FLAG: Axiom without justification *)
Axiom mysterious : unexplained_property.

(* RED FLAG: Admitted in proof *)
Lemma key_lemma : important.
Proof.
  intros.
  admit.  (* RED FLAG *)
Qed.

(* RED FLAG: Unsafe extraction *)
Extract Inductive nat => "int" [...].
(* Potential overflow *)
```

### Warning Signs

**Medium-priority warnings:**
```coq
(* WARNING: Proof by admit *)
Lemma complex : statement.
Proof.
  (* ... *)
  admit.
Qed.

(* WARNING: Parameter without specification *)
Parameter mystery_func : nat -> nat.
(* No properties stated *)

(* WARNING: Extraction of axiom *)
Axiom external_property : P.
Extraction "output.ml" theorem_using_external_property.
(* Axiom will be extracted as 'assert false' *)
```

## Program Framework

### Proof Obligations

**Program-generated obligations:**
```coq
Program Definition safe_div (a b : nat) (H : b <> 0) : nat :=
  a / b.

(* VERIFIED if obligation proven *)
Next Obligation.
  (* proof *)
Qed.

(* ASSUMED if obligation admitted *)
Next Obligation.
Admitted.  (* RED FLAG *)
```

**Report:**
```markdown
### safe_div obligations
**Location:** Module.v:15
**Obligations:** 1
**Proven:** 0
**Admitted:** 1
**Risk Level:** HIGH - safety property not verified
```

## Equations Plugin

### Well-Founded Recursion

**Termination obligations:**
```coq
Require Import Equations.Equations.

Equations quicksort (l : list nat) : list nat by wf (length l) lt :=
  quicksort [] := [];
  quicksort (pivot :: xs) := ...

(* VERIFIED if termination proven *)
(* ASSUMED if termination admitted *)
```

## Report Generation

### Section: Verified Components

**Template:**
```markdown
### [Lemma/Theorem Name]

**Location:** [File.v:Line]
**Type:** [Lemma/Theorem/Corollary]
**Statement:** ```coq [formal statement] ```
**Proof Status:** ✓ Complete (Qed)
**Proof Method:** [auto/induction/manual/...]
**Dependencies:** [List of lemmas used]
**Assumptions:** [Output of Print Assumptions]
```

### Section: Assumptions

**Template:**
```markdown
### [Axiom/Admitted Name]

**Location:** [File.v:Line]
**Type:** [Axiom/Parameter/Admitted]
**Statement:** ```coq [formal statement] ```
**Source:** [Standard library/User-defined]
**Justification:** [Why assumed]
**Used By:** [Theorems depending on this]
**Impact:** [Number of theorems affected]
**Risk Level:** [Low/Medium/High]
```

## Example Analysis

**Input:**
```coq
Require Import List.
Import ListNotations.

Axiom magic : forall n, n > 0.

Fixpoint sum (l : list nat) : nat :=
  match l with
  | [] => 0
  | x :: xs => x + sum xs
  end.

Lemma sum_positive : forall l,
  l <> [] -> sum l > 0.
Proof.
  intros. destruct l.
  - contradiction.
  - simpl. apply magic.
Qed.

Theorem main : forall l, l <> [] -> sum l >= 1.
Proof.
  intros. apply sum_positive in H.
Admitted.

Extraction "sum.ml" sum.
```

**Output report excerpt:**
```markdown
## Verification Statistics

- Total definitions: 1 (sum)
- Total lemmas: 2
- Verified: 1 (50%)
- Admitted: 1 (50%)
- Axioms: 1
- Extracted: 1 function

## Verified Components

### sum_positive
**Location:** Example.v:12
**Statement:** forall l, l <> [] -> sum l > 0
**Proof Status:** ✓ Complete (Qed)
**Dependencies:** magic (axiom)
**Assumptions:** magic

⚠️ **Warning:** Depends on unproven axiom

## Assumptions and Axioms

### magic (Axiom)
**Location:** Example.v:4
**Statement:** forall n, n > 0
**Justification:** None provided
**Used By:** sum_positive, main (transitively)
**Impact:** 2 theorems depend on this
**Risk Level:** HIGH - obviously false axiom (0 > 0 is false)
**Recommendation:** CRITICAL - This axiom is inconsistent!

### main (Admitted)
**Location:** Example.v:19
**Statement:** forall l, l <> [] -> sum l >= 1
**Reason:** Proof incomplete
**Dependencies:** sum_positive
**Risk Level:** MEDIUM - should be provable from sum_positive

## Trusted Computing Base

### Coq Kernel
[Standard entry]

### Coq.Lists.List
**Type:** Standard Library
**Description:** List operations
**Risk Level:** Low

### Extraction to OCaml
**Type:** Code Extraction
**Description:** Extracts sum to OCaml
**Risk:** Medium - extraction correctness not verified

## Critical Issues

1. **Inconsistent axiom:** magic axiom is false (0 > 0)
2. **Main theorem unproven:** main theorem admitted
3. **Unsound verification:** sum_positive proof relies on false axiom

## Recommendations

1. **Remove magic axiom:** Prove sum_positive without axioms
2. **Complete main proof:** Should be straightforward from sum_positive
3. **Review all uses of magic:** Check if other theorems depend on it
```
