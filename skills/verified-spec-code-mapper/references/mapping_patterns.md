# Verified Spec-Code Mapping Patterns

This reference provides patterns for establishing traceability between formal specifications and verified code components.

## Table of Contents

1. [Specification Types](#specification-types)
2. [Mapping Patterns](#mapping-patterns)
3. [Coverage Analysis](#coverage-analysis)
4. [Report Templates](#report-templates)
5. [Verification Evidence](#verification-evidence)

## Specification Types

### Preconditions

**Definition:** Conditions that must hold before a function/method executes.

**Coq Example:**
```coq
Definition divide (n m : nat) : option nat :=
  if m =? 0 then None else Some (n / m).

Lemma divide_spec : forall n m : nat,
  m <> 0 ->  (* PRECONDITION *)
  exists q, divide n m = Some q.
```

**Dafny Example:**
```dafny
method Divide(n: int, m: int) returns (q: int)
  requires m != 0  // PRECONDITION
  ensures q * m <= n < (q + 1) * m
{
  q := n / m;
}
```

**Isabelle Example:**
```isabelle
definition divide :: "nat ⇒ nat ⇒ nat option" where
  "divide n m = (if m = 0 then None else Some (n div m))"

lemma divide_defined:
  assumes "m ≠ 0"  (* PRECONDITION *)
  shows "∃q. divide n m = Some q"
```

### Postconditions

**Definition:** Conditions guaranteed to hold after successful execution.

**Coq Example:**
```coq
Fixpoint factorial (n : nat) : nat :=
  match n with
  | 0 => 1
  | S n' => n * factorial n'
  end.

Lemma factorial_positive : forall n : nat,
  factorial n >= 1.  (* POSTCONDITION *)
```

**Dafny Example:**
```dafny
function factorial(n: nat): nat
  ensures factorial(n) >= 1  // POSTCONDITION
{
  if n == 0 then 1 else n * factorial(n - 1)
}
```

### Loop Invariants

**Definition:** Properties that hold at the start of each loop iteration.

**Coq Example:**
```coq
Fixpoint sum_to_n_aux (n i acc : nat) : nat :=
  match n with
  | 0 => acc
  | S n' =>
      if i <? n then
        sum_to_n_aux n (S i) (acc + i)
      else acc
  end.

(* LOOP INVARIANT: acc = sum of 0..i-1 *)
Lemma sum_invariant : forall n i acc,
  i <= n ->
  sum_to_n_aux n i acc = acc + (sum of 0 to i-1).
```

**Dafny Example:**
```dafny
method SumToN(n: nat) returns (sum: nat)
  ensures sum == n * (n - 1) / 2
{
  sum := 0;
  var i := 0;
  while i < n
    invariant 0 <= i <= n  // LOOP INVARIANT
    invariant sum == i * (i - 1) / 2  // LOOP INVARIANT
  {
    sum := sum + i;
    i := i + 1;
  }
}
```

### Class Invariants

**Definition:** Properties that hold for all instances of a class.

**Dafny Example:**
```dafny
class BankAccount {
  var balance: int

  // CLASS INVARIANT
  predicate Valid()
    reads this
  {
    balance >= 0
  }

  constructor(initial: int)
    requires initial >= 0
    ensures Valid()
    ensures balance == initial
  {
    balance := initial;
  }

  method Deposit(amount: int)
    requires Valid()
    requires amount >= 0
    modifies this
    ensures Valid()
    ensures balance == old(balance) + amount
  {
    balance := balance + amount;
  }
}
```

### Functional Correctness

**Definition:** The function computes the correct result.

**Coq Example:**
```coq
Fixpoint reverse (l : list nat) : list nat :=
  match l with
  | [] => []
  | x :: xs => reverse xs ++ [x]
  end.

(* FUNCTIONAL CORRECTNESS *)
Lemma reverse_involutive : forall l : list nat,
  reverse (reverse l) = l.
```

## Mapping Patterns

### Pattern 1: Direct Specification Mapping

**Structure:**
```
Specification → Code Component → Proof
```

**Example (Coq):**
```markdown
## Specification: Division Safety

**Precondition:** `m ≠ 0`
**Postcondition:** `divide n m = Some q` where `q = n / m`

**Code Component:**
- Function: `divide` (line 5-7)
- Definition: Returns `Some (n / m)` when `m ≠ 0`

**Verification:**
- Theorem: `divide_spec` (line 10-13)
- Status: ✓ Fully Verified
- Proof: By case analysis on `m =? 0`
```

### Pattern 2: Composite Specification Mapping

**Structure:**
```
Multiple Specifications → Single Code Component → Multiple Proofs
```

**Example (Dafny):**
```markdown
## Code Component: `BankAccount.Deposit`

### Specifications:

1. **Precondition: Valid State**
   - Specification: `requires Valid()`
   - Verification: Checked by Dafny verifier
   - Status: ✓ Fully Verified

2. **Precondition: Non-negative Amount**
   - Specification: `requires amount >= 0`
   - Verification: Checked by Dafny verifier
   - Status: ✓ Fully Verified

3. **Postcondition: Maintains Invariant**
   - Specification: `ensures Valid()`
   - Verification: Checked by Dafny verifier
   - Status: ✓ Fully Verified

4. **Postcondition: Correct Balance**
   - Specification: `ensures balance == old(balance) + amount`
   - Verification: Checked by Dafny verifier
   - Status: ✓ Fully Verified
```

### Pattern 3: Hierarchical Specification Mapping

**Structure:**
```
High-level Spec → Intermediate Specs → Low-level Code → Proofs
```

**Example (Isabelle):**
```markdown
## High-Level Specification: Sorting Correctness

### Intermediate Specification 1: Permutation
- **Specification:** `sorted_list` is a permutation of input
- **Code:** `sort` function
- **Proof:** `sort_permutes` lemma
- **Status:** ✓ Fully Verified

### Intermediate Specification 2: Ordering
- **Specification:** Result is sorted (all elements in order)
- **Code:** `sort` function
- **Proof:** `sort_sorted` lemma
- **Status:** ✓ Fully Verified

### Combined Correctness
- **Specification:** `sort` produces sorted permutation
- **Code:** `sort` function
- **Proof:** `sort_correct` (uses both lemmas)
- **Status:** ✓ Fully Verified
```

### Pattern 4: Assumed Specification Mapping

**Structure:**
```
Specification → Code Component → Axiom/Assumption (not proved)
```

**Example (Coq):**
```markdown
## Specification: Cryptographic Hash Properties

**Property:** Collision resistance
**Code Component:** `hash` function
**Verification:** ⚠ ASSUMED (axiom `hash_collision_resistant`)
**Status:** ⚠ Partially Verified (assumed without proof)

**Justification:** Cryptographic properties cannot be formally verified
within the proof system; relies on external cryptographic assumptions.
```

## Coverage Analysis

### Coverage Levels

**Fully Verified (✓):**
- All specifications have corresponding proofs
- All proofs are complete (no `Admitted`, `sorry`, etc.)
- All preconditions checked
- All postconditions established

**Partially Verified (⚠):**
- Some specifications proved
- Some proofs incomplete
- Some properties assumed

**Unverified (✗):**
- No formal verification
- Specifications stated but not proved
- Implementation only

### Coverage Metrics

**Specification Coverage:**
```
Coverage = (Verified Specs / Total Specs) × 100%
```

**Code Coverage:**
```
Coverage = (Verified Functions / Total Functions) × 100%
```

**Proof Completeness:**
```
Completeness = (Complete Proofs / Total Proofs) × 100%
```

### Coverage Report Template

```markdown
# Verification Coverage Report

## Summary
- Total Specifications: X
- Fully Verified: Y (Z%)
- Partially Verified: A (B%)
- Unverified: C (D%)

## Detailed Coverage

### Module: [Module Name]

#### Function: [Function Name]
- **Preconditions:** X total, Y verified (Z%)
- **Postconditions:** X total, Y verified (Z%)
- **Invariants:** X total, Y verified (Z%)
- **Overall Status:** [Fully/Partially/Un]verified

### Assumptions
1. [Assumption 1] - Used in [Proof 1, Proof 2]
2. [Assumption 2] - Used in [Proof 3]

### Gaps
1. [Unverified Property 1] - Reason: [...]
2. [Incomplete Proof 1] - Reason: [...]
```

## Report Templates

### Template 1: Function-Centric Report

```markdown
# Verification Report: [Function Name]

## Function Signature
```[language]
[function signature]
```

## Specifications

### Preconditions
1. **[Precondition Name]**
   - Specification: `[formal statement]`
   - Location: [file:line]
   - Status: [✓/⚠/✗]

### Postconditions
1. **[Postcondition Name]**
   - Specification: `[formal statement]`
   - Location: [file:line]
   - Status: [✓/⚠/✗]

### Invariants
1. **[Invariant Name]**
   - Specification: `[formal statement]`
   - Location: [file:line]
   - Status: [✓/⚠/✗]

## Verification Evidence

### Theorem: [Theorem Name]
- **Statement:** `[formal statement]`
- **Location:** [file:line]
- **Proof Status:** [Complete/Incomplete/Assumed]
- **Dependencies:** [List of lemmas/axioms used]

## Coverage Summary
- Specifications: X total, Y verified (Z%)
- Status: [Fully/Partially/Un]verified
```

### Template 2: Specification-Centric Report

```markdown
# Verification Report: [Specification Name]

## Specification Statement
```[language]
[formal specification]
```

## Mapped Code Components

### Component 1: [Component Name]
- **Type:** [Function/Method/Class]
- **Location:** [file:line]
- **Role:** [How it relates to specification]

### Component 2: [Component Name]
- **Type:** [Function/Method/Class]
- **Location:** [file:line]
- **Role:** [How it relates to specification]

## Verification Proofs

### Proof 1: [Proof Name]
- **Theorem:** `[formal statement]`
- **Location:** [file:line]
- **Status:** [✓/⚠/✗]
- **Method:** [Induction/Case analysis/etc.]

### Proof 2: [Proof Name]
- **Theorem:** `[formal statement]`
- **Location:** [file:line]
- **Status:** [✓/⚠/✗]
- **Method:** [Induction/Case analysis/etc.]

## Dependencies
- **Lemmas Used:** [List]
- **Axioms Used:** [List]
- **External Libraries:** [List]

## Verification Status
- Overall: [✓ Fully Verified / ⚠ Partially Verified / ✗ Unverified]
- Confidence: [High/Medium/Low]
- Assumptions: [List any assumptions]
```

### Template 3: Module-Level Report

```markdown
# Verification Report: [Module Name]

## Module Overview
- **Purpose:** [Description]
- **Total Functions:** X
- **Total Specifications:** Y
- **Verification Coverage:** Z%

## Function Summary

| Function | Preconditions | Postconditions | Invariants | Status |
|----------|---------------|----------------|------------|--------|
| func1    | 2/2 ✓         | 3/3 ✓          | 1/1 ✓      | ✓      |
| func2    | 1/2 ⚠         | 2/2 ✓          | 0/1 ✗      | ⚠      |
| func3    | 0/1 ✗         | 0/2 ✗          | N/A        | ✗      |

## Detailed Mappings

### [Function 1]
[Detailed mapping as per Template 1]

### [Function 2]
[Detailed mapping as per Template 1]

## Module-Level Properties

### Property 1: [Property Name]
- **Specification:** `[formal statement]`
- **Verified By:** [Theorem name]
- **Status:** [✓/⚠/✗]

## Assumptions and Axioms
1. **[Axiom Name]**
   - Statement: `[formal statement]`
   - Used in: [List of proofs]
   - Justification: [Why assumed]

## Verification Gaps
1. **[Gap Description]**
   - Affected: [Functions/Properties]
   - Reason: [Why not verified]
   - Priority: [High/Medium/Low]
```

## Verification Evidence

### Evidence Types

**1. Complete Proof:**
```coq
Lemma example : forall n : nat, n + 0 = n.
Proof.
  intros. lia.
Qed.  (* Complete - ends with Qed *)
```
**Status:** ✓ Fully Verified

**2. Incomplete Proof:**
```coq
Lemma example : forall n : nat, n + 0 = n.
Proof.
  intros. (* proof incomplete *)
Admitted.  (* Incomplete - ends with Admitted *)
```
**Status:** ✗ Unverified

**3. Assumed Axiom:**
```coq
Axiom functional_extensionality : forall (A B : Type) (f g : A -> B),
  (forall x, f x = g x) -> f = g.
```
**Status:** ⚠ Assumed (no proof)

**4. External Verification:**
```dafny
method Sort(a: array<int>)
  modifies a
  ensures sorted(a[..])
  ensures multiset(a[..]) == multiset(old(a[..]))
{
  // Implementation
}
// Verified by Dafny verifier
```
**Status:** ✓ Fully Verified (by tool)

### Evidence Strength

**Strong Evidence:**
- Complete formal proof
- Verified by proof assistant
- No axioms or assumptions
- All dependencies verified

**Medium Evidence:**
- Proof with standard axioms (e.g., functional extensionality)
- Verified by automated tool (SMT solver)
- Some dependencies assumed

**Weak Evidence:**
- Incomplete proofs
- Many assumptions
- Unverified dependencies
- Manual verification only

## Traceability Matrix Example

```markdown
# Traceability Matrix

| Spec ID | Specification | Code Component | Proof/Theorem | Status |
|---------|---------------|----------------|---------------|--------|
| REQ-001 | Division safety: m ≠ 0 | `divide` (line 5) | `divide_spec` | ✓ |
| REQ-002 | Factorial ≥ 1 | `factorial` (line 12) | `factorial_positive` | ✓ |
| REQ-003 | Sort correctness | `sort` (line 45) | `sort_correct` | ✓ |
| REQ-004 | Hash collision resistance | `hash` (line 78) | `hash_axiom` | ⚠ |
| REQ-005 | List reverse involutive | `reverse` (line 92) | `reverse_involutive` | ✓ |

**Legend:**
- ✓ Fully Verified
- ⚠ Partially Verified (assumptions)
- ✗ Unverified
```

## Best Practices

### 1. Explicit Specification Identification

**Good:**
```markdown
**Precondition:** `n >= 0` (line 15, requires clause)
**Postcondition:** `result >= 1` (line 16, ensures clause)
```

**Bad:**
```markdown
**Precondition:** n should be non-negative
**Postcondition:** result is positive
```

### 2. Clear Proof References

**Good:**
```markdown
**Verification:** Theorem `factorial_positive` (lines 25-30)
**Proof Method:** Induction on n
**Status:** ✓ Complete (ends with Qed)
```

**Bad:**
```markdown
**Verification:** Proved somewhere
**Status:** Verified
```

### 3. Honest Coverage Reporting

**Good:**
```markdown
**Status:** ⚠ Partially Verified
**Reason:** Relies on axiom `functional_extensionality`
**Impact:** Standard axiom, widely accepted
```

**Bad:**
```markdown
**Status:** ✓ Fully Verified
(hiding the axiom dependency)
```

### 4. Assumption Documentation

**Good:**
```markdown
## Assumptions
1. **Cryptographic Hash Security**
   - Axiom: `hash_collision_resistant`
   - Location: crypto.v:45
   - Justification: Cryptographic properties beyond formal verification
   - Used in: `authenticate_spec`, `verify_signature_spec`
```

**Bad:**
```markdown
## Assumptions
1. Hash is secure (assumed)
```

## Common Pitfalls

### Pitfall 1: Inferring Without Evidence

**Wrong:**
```markdown
**Status:** ✓ Verified
(no proof actually exists)
```

**Right:**
```markdown
**Status:** ✗ Unverified
**Reason:** No formal proof provided
```

### Pitfall 2: Merging Specifications

**Wrong:**
```markdown
**Combined Spec:** Function is safe and correct
**Proof:** combined_proof
```

**Right:**
```markdown
**Spec 1:** Safety (m ≠ 0)
**Proof 1:** safety_proof

**Spec 2:** Correctness (result = n/m)
**Proof 2:** correctness_proof
```

### Pitfall 3: Weakening Specifications

**Wrong:**
```markdown
**Original Spec:** `forall n m, n > 0 -> m > 0 -> result > 0`
**Reported Spec:** `result > 0` (dropped preconditions)
```

**Right:**
```markdown
**Specification:** `forall n m, n > 0 -> m > 0 -> result > 0`
(report complete specification)
```

### Pitfall 4: Ignoring Dependencies

**Wrong:**
```markdown
**Proof:** theorem_name
**Status:** ✓ Verified
```

**Right:**
```markdown
**Proof:** theorem_name
**Dependencies:**
- Lemma: helper_lemma (verified)
- Axiom: functional_extensionality (assumed)
**Status:** ⚠ Verified with assumptions
```
