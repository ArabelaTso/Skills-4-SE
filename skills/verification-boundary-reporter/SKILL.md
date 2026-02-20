---
name: verification-boundary-reporter
description: Analyze formal verification artifacts (Isabelle, Coq, Dafny, etc.) and produce structured reports identifying the precise boundary between verified, assumed, and unverified components. Use when assessing verification coverage, understanding trust boundaries, auditing formal proofs, or documenting verification scope. Reports explicitly list verified code, assumptions, axioms, trusted computing base, and unverified components. Conservative and explicit about verification status without attempting to repair or mask gaps.
---

# Verification Boundary Reporter

Analyze formal verification artifacts and produce clear reports on what is verified, what is assumed, and what remains unverified.

## Overview

When working with formally verified code, it's critical to understand exactly what guarantees the verification provides and where the boundaries lie. This skill analyzes verification artifacts and produces structured reports that:

1. **Identify verified components** - Code with completed proofs
2. **List assumptions and axioms** - What is taken on trust
3. **Document the trusted computing base (TCB)** - External dependencies
4. **Highlight unverified components** - Gaps in verification coverage
5. **Explain verification limitations** - Why certain parts aren't verified

**Core principle:** Be conservative and explicit. Never overstate verification coverage.

## Analysis Workflow

```
Verification Artifacts
    ↓
Parse & Identify Components
    ↓
Classify Each Component
    ↓
Analyze Dependencies
    ↓
Generate Boundary Report
```

## Component Classification

### Verified Components

**Definition:** Code with complete, checked proofs of stated properties.

**Criteria:**
- All proof obligations discharged
- No `sorry`, `admit`, `Admitted` in proofs
- Proof checked by verifier (Isabelle, Coq, Dafny, etc.)
- Properties explicitly stated and proven

**Example identification:**
```isabelle
(* VERIFIED *)
theorem insertion_sort_correct:
  "sorted (insertion_sort xs) ∧ mset (insertion_sort xs) = mset xs"
proof (induction xs)
  case Nil
  then show ?case by simp
next
  case (Cons x xs)
  then show ?case using insert_sorted mset_insert by auto
qed
```

### Assumed Components

**Definition:** Statements accepted without proof.

**Criteria:**
- Marked with `axiom`, `sorry`, `admit`, `Admitted`, `assume`
- Declared without proof
- Explicitly stated as assumptions

**Example identification:**
```coq
(* ASSUMED *)
Axiom functional_extensionality : forall A B (f g : A -> B),
  (forall x, f x = g x) -> f = g.

(* ASSUMED - proof incomplete *)
Theorem complex_property : ...
Proof.
  (* ... *)
Admitted.
```

### Trusted Computing Base (TCB)

**Definition:** External components that must be trusted.

**Components:**
- Proof assistant kernel (Isabelle, Coq, Dafny verifier)
- Standard libraries used without verification
- Code extraction/generation tools
- Operating system and hardware
- External functions or FFI calls

**Example identification:**
```isabelle
(* TCB: Relies on Isabelle kernel *)
export_code my_function in SML file "output.sml"

(* TCB: Uses unverified standard library *)
definition process_file :: "string ⇒ unit" where
  "process_file path = ..." (* Calls OS file operations *)
```

### Unverified Components

**Definition:** Code without formal verification.

**Reasons:**
- Not yet verified (work in progress)
- Intentionally left unverified (low criticality)
- Cannot be verified (external dependencies)
- Verification attempted but incomplete

**Example identification:**
```dafny
// UNVERIFIED: No method body verification
method ProcessData(input: seq<int>) returns (output: seq<int>)
  // No ensures clause - postcondition not specified
{
  // Implementation without verification
}
```

## Analysis Process

### Step 1: Identify All Components

Scan verification artifacts for:
- Definitions and implementations
- Theorems and lemmas
- Axioms and assumptions
- External dependencies
- Extracted/generated code

### Step 2: Check Verification Status

For each component, determine:
- Is there a proof? (Complete/incomplete/absent)
- Are there assumptions or axioms?
- What properties are claimed?
- What properties are proven?

### Step 3: Trace Dependencies

Map dependencies to understand:
- What verified code depends on
- Assumption propagation
- TCB elements used
- Unverified code interactions

### Step 4: Assess Coverage

Calculate:
- Percentage of code verified
- Critical vs non-critical components
- Verification depth (shallow vs deep properties)

### Step 5: Generate Report

Produce structured Markdown report with:
- Executive summary
- Verified components list
- Assumptions and axioms
- TCB documentation
- Unverified components
- Verification gaps and limitations

## Report Structure

### Template

```markdown
# Verification Boundary Report

**Project:** [Name]
**Date:** [Date]
**Verifier:** [Isabelle/Coq/Dafny/etc.]
**Analyst:** [Name]

## Executive Summary

[Brief overview of verification coverage and key findings]

## Verification Statistics

- Total components: X
- Verified: Y (Z%)
- Assumed: A
- Unverified: B
- TCB elements: C

## Verified Components

### [Component Name]

**Location:** [File:Line]
**Properties Proven:**
- [Property 1]
- [Property 2]

**Proof Status:** ✓ Complete
**Dependencies:** [List verified dependencies]

## Assumptions and Axioms

### [Assumption Name]

**Location:** [File:Line]
**Statement:** [Formal statement]
**Justification:** [Why this is assumed]
**Impact:** [What depends on this]
**Risk Level:** [Low/Medium/High]

## Trusted Computing Base

### [TCB Element]

**Type:** [Kernel/Library/Tool/OS/Hardware]
**Description:** [What is trusted]
**Justification:** [Why it must be trusted]
**Mitigation:** [How risk is managed]

## Unverified Components

### [Component Name]

**Location:** [File:Line]
**Reason:** [Why unverified]
**Risk Assessment:** [Impact if incorrect]
**Recommendation:** [Should it be verified?]

## Verification Gaps

[List areas where verification is incomplete or absent]

## Limitations

[Explicit statement of what the verification does NOT guarantee]

## Recommendations

[Suggestions for improving verification coverage]
```

## Framework-Specific Analysis

### Isabelle/HOL Analysis

For Isabelle-specific verification boundary analysis, see [references/isabelle_analysis.md](references/isabelle_analysis.md).

Key aspects:
- Identifying `sorry` and incomplete proofs
- Checking axiom usage
- Analyzing code generation trust
- Sledgehammer and automation reliance

### Coq Analysis

For Coq-specific verification boundary analysis, see [references/coq_analysis.md](references/coq_analysis.md).

Key aspects:
- Identifying `Admitted` and `admit`
- Checking axiom usage (functional extensionality, etc.)
- Analyzing extraction trust
- Program obligations

### Dafny Analysis

For Dafny-specific verification boundary analysis, see [references/dafny_analysis.md](references/dafny_analysis.md).

Key aspects:
- Checking method verification
- Identifying assume statements
- Analyzing external methods
- Verification timeout issues

## Common Patterns

For common verification boundary patterns and red flags, see [references/boundary_patterns.md](references/boundary_patterns.md).

Patterns include:
- Assumption propagation
- Partial verification
- Verification by testing
- Trusted wrappers
- Verification escape hatches

## Example Analysis

**Input: Verified sorting implementation**

```isabelle
theory VerifiedSort
imports Main "HOL-Library.Multiset"
begin

fun insert :: "nat ⇒ nat list ⇒ nat list" where
  "insert x [] = [x]" |
  "insert x (y # ys) = (if x ≤ y then x # y # ys else y # insert x ys)"

fun insertion_sort :: "nat list ⇒ nat list" where
  "insertion_sort [] = []" |
  "insertion_sort (x # xs) = insert x (insertion_sort xs)"

lemma insert_sorted:
  "sorted xs ⟹ sorted (insert x xs)"
  by (induction xs) auto

lemma mset_insert:
  "mset (insert x xs) = {#x#} + mset xs"
  by (induction xs) (auto simp: ac_simps)

theorem insertion_sort_correct:
  "sorted (insertion_sort xs) ∧ mset (insertion_sort xs) = mset xs"
  by (induction xs) (auto simp: insert_sorted mset_insert)

export_code insertion_sort in SML file "sort.sml"

end
```

**Output: Verification Boundary Report**

```markdown
# Verification Boundary Report

**Project:** VerifiedSort
**Date:** 2026-02-17
**Verifier:** Isabelle/HOL
**Analyst:** Verification Boundary Reporter

## Executive Summary

The insertion sort implementation is fully verified with complete proofs of
correctness (sorting and permutation preservation). The verification relies
on Isabelle's standard library and kernel as the trusted computing base.
Code extraction to SML is part of the TCB.

## Verification Statistics

- Total components: 5
- Verified: 3 (60%)
- Assumed: 0 (0%)
- Unverified: 0 (0%)
- TCB elements: 2 (40%)

## Verified Components

### insert function
**Location:** VerifiedSort.thy:5-7
**Properties Proven:**
- Preserves sortedness (insert_sorted)
- Preserves multiset (mset_insert)
**Proof Status:** ✓ Complete
**Dependencies:** None (base case)

### insertion_sort function
**Location:** VerifiedSort.thy:9-11
**Properties Proven:**
- Produces sorted output
- Preserves all elements (permutation)
**Proof Status:** ✓ Complete
**Dependencies:** insert, insert_sorted, mset_insert

### Correctness theorem
**Location:** VerifiedSort.thy:18-19
**Statement:** sorted (insertion_sort xs) ∧ mset (insertion_sort xs) = mset xs
**Proof Status:** ✓ Complete
**Proof Method:** Induction with auto

## Assumptions and Axioms

None. All proofs are complete without axioms.

## Trusted Computing Base

### Isabelle/HOL Kernel
**Type:** Proof Assistant Kernel
**Description:** The Isabelle/HOL logical kernel that checks all proofs
**Justification:** Fundamental to all verification; cannot be verified within itself
**Mitigation:** Small, well-audited kernel; decades of use

### Isabelle Standard Library
**Type:** Library
**Description:** HOL-Library.Multiset for multiset operations
**Justification:** Used for permutation reasoning
**Mitigation:** Part of standard Isabelle distribution, widely used and tested

### Code Generation
**Type:** Tool
**Description:** export_code mechanism that generates SML
**Justification:** Translates verified Isabelle code to executable SML
**Mitigation:** Code generator is part of Isabelle, but translation correctness
is not formally verified. Generated code must be trusted to match semantics.

## Unverified Components

None. All algorithmic components are verified.

## Verification Gaps

None identified in the core algorithm.

## Limitations

1. **Code extraction trust:** The generated SML code is not verified to match
   the Isabelle semantics. The code generator is trusted.

2. **Termination:** While termination is proven by Isabelle's function package,
   the extracted code's termination depends on the SML runtime.

3. **I/O and side effects:** Any I/O operations in the extracted code are
   outside the verification boundary.

4. **Numeric representation:** The verification uses mathematical integers (nat),
   but extracted code uses machine integers which may overflow.

## Recommendations

1. **Consider verified extraction:** Use a verified code generator or
   certified compilation if higher assurance is needed.

2. **Add overflow checks:** If using extracted code with large inputs,
   add runtime checks for integer overflow.

3. **Document TCB:** Clearly communicate to users that code extraction
   is part of the trusted base.
```

## Best Practices

1. **Be Conservative:** When in doubt, classify as unverified
2. **Be Explicit:** State exactly what is and isn't verified
3. **Trace Dependencies:** Show how assumptions propagate
4. **Quantify Coverage:** Provide statistics and percentages
5. **Assess Risk:** Evaluate impact of unverified components
6. **Document TCB:** Clearly list all trusted elements
7. **No Speculation:** Don't guess about verification status

## Red Flags

Watch for:
- `sorry`, `admit`, `Admitted` in proofs
- Axioms without justification
- Missing specifications
- Incomplete proofs
- External function calls
- Code generation without verification
- Timeout-based "verification"
- Comments like "TODO: prove this"

## Reporting Principles

### Principle 1: Completeness

Report ALL components, not just verified ones.

### Principle 2: Honesty

Never overstate verification coverage.

### Principle 3: Clarity

Use clear, unambiguous language.

### Principle 4: Traceability

Link every claim to specific artifacts.

### Principle 5: Risk Assessment

Evaluate impact of verification gaps.

## Additional Resources

For detailed guidance on specific aspects:
- [Isabelle Analysis](references/isabelle_analysis.md) - Isabelle-specific boundary analysis
- [Coq Analysis](references/coq_analysis.md) - Coq-specific boundary analysis
- [Dafny Analysis](references/dafny_analysis.md) - Dafny-specific boundary analysis
- [Boundary Patterns](references/boundary_patterns.md) - Common patterns and red flags
