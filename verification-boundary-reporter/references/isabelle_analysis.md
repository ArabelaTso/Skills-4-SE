# Isabelle/HOL Verification Boundary Analysis

Guide for analyzing verification boundaries in Isabelle/HOL projects.

## Identifying Verified Components

### Complete Proofs

**Indicators of verified code:**
```isabelle
(* VERIFIED: Complete proof *)
lemma my_property: "statement"
proof (method)
  (* proof steps *)
qed

(* VERIFIED: Automatic proof *)
lemma simple_property: "statement"
  by auto

(* VERIFIED: Sledgehammer proof *)
lemma complex_property: "statement"
  by (metis lemma1 lemma2 lemma3)
```

### Checking Proof Status

**Commands to verify:**
```isabelle
(* Check if theory is complete *)
print_theorems

(* Find incomplete proofs *)
find_theorems name: "sorry"
```

## Identifying Assumptions

### Sorry and Oops

**Incomplete proofs:**
```isabelle
(* ASSUMED: Proof incomplete *)
lemma unproven: "statement"
  sorry

(* ASSUMED: Proof abandoned *)
lemma attempted: "statement"
proof -
  (* some steps *)
  show ?thesis sorry
qed

(* UNVERIFIED: Proof explicitly abandoned *)
lemma test: "statement"
  oops
```

### Axioms

**Explicit axioms:**
```isabelle
(* ASSUMED: Axiom without proof *)
axiom functional_extensionality:
  "⟦ ∀x. f x = g x ⟧ ⟹ f = g"

(* ASSUMED: Axiomatization *)
axiomatization
  my_constant :: "'a ⇒ 'b"
where
  my_axiom: "property my_constant"
```

### Assumptions in Proofs

**Local assumptions:**
```isabelle
lemma with_assumption:
  assumes "P x"  (* ASSUMPTION: P x must hold *)
  shows "Q x"
proof -
  (* proof using assumption *)
qed
```

## Trusted Computing Base

### Isabelle Kernel

**Always in TCB:**
- Isabelle/HOL logical kernel
- Type checker
- Proof checker
- Core inference rules

**Documentation:**
```markdown
### Isabelle/HOL Kernel
**Type:** Proof Assistant Kernel
**Description:** The core logical kernel that validates all proofs
**Justification:** Cannot verify the verifier within itself
**Mitigation:** Small, well-audited kernel (LCF-style architecture)
```

### Standard Libraries

**Library usage:**
```isabelle
(* TCB: Standard library *)
imports Main
imports "HOL-Library.Multiset"
imports "HOL-Library.Code_Target_Nat"

(* Document in report *)
```

**Report template:**
```markdown
### HOL-Library.Multiset
**Type:** Standard Library
**Description:** Multiset operations for permutation reasoning
**Justification:** Part of standard Isabelle distribution
**Mitigation:** Widely used and tested; part of Isabelle release
```

### Code Generation

**Code extraction:**
```isabelle
(* TCB: Code generation *)
export_code my_function in SML file "output.sml"
export_code my_function in OCaml file "output.ml"
export_code my_function in Haskell file "Output.hs"
```

**Report template:**
```markdown
### Code Generation to SML
**Type:** Code Extraction Tool
**Description:** Translates Isabelle definitions to executable SML
**Justification:** Enables execution of verified algorithms
**Mitigation:** Code generator is part of Isabelle, but translation
correctness is not formally verified. Generated code semantics must
be trusted to match Isabelle semantics.
**Risk:** Medium - semantic gaps possible between Isabelle and target language
```

### Sledgehammer and Automation

**Automated proofs:**
```isabelle
(* Uses external ATPs *)
lemma auto_proven: "statement"
  by sledgehammer

(* Uses SMT solvers *)
lemma smt_proven: "statement"
  by (smt lemma1 lemma2)
```

**Report template:**
```markdown
### Sledgehammer (External ATPs)
**Type:** Proof Automation
**Description:** Uses external automated theorem provers (E, SPASS, Z3, etc.)
**Justification:** Finds proofs automatically, but proofs are reconstructed
and checked by Isabelle kernel
**Mitigation:** External provers only suggest proofs; Isabelle kernel validates
all proof steps. The kernel remains the trust boundary.
**Risk:** Low - kernel checks all proofs
```

## Unverified Components

### Incomplete Definitions

**Partial definitions:**
```isabelle
(* UNVERIFIED: No properties proven *)
definition my_function :: "nat ⇒ nat" where
  "my_function n = n + 1"
(* No theorems about my_function *)
```

### Untrusted Code

**External code:**
```isabelle
(* UNVERIFIED: External code *)
code_printing
  constant my_function ⇀ (SML) "ExternalModule.my_function"
```

**Report:**
```markdown
### my_function (External SML)
**Location:** Theory.thy:42
**Reason:** Implemented in external SML code
**Risk Assessment:** High - no formal verification of external implementation
**Recommendation:** Verify or replace with Isabelle implementation
```

## Dependency Analysis

### Tracing Dependencies

**Find what a theorem depends on:**
```isabelle
(* Check dependencies *)
thm my_theorem
print_statement my_theorem

(* Find all uses of an axiom *)
find_theorems name: "my_axiom"
```

### Assumption Propagation

**Example:**
```isabelle
axiom unproven_base: "P"

lemma depends_on_axiom: "Q"
proof -
  have "P" by (rule unproven_base)  (* Uses axiom *)
  (* ... *)
qed

theorem final_result: "R"
proof -
  have "Q" by (rule depends_on_axiom)  (* Indirectly uses axiom *)
  (* ... *)
qed
```

**Report:**
```markdown
### Assumption Propagation Chain

axiom unproven_base
  ↓ (used by)
lemma depends_on_axiom
  ↓ (used by)
theorem final_result

**Impact:** final_result depends on unproven_base axiom
**Risk Level:** High - core result depends on assumption
```

## Coverage Analysis

### Calculating Coverage

**Metrics:**
```
Total definitions: Count all fun, definition, function
Total theorems: Count all lemma, theorem
Verified theorems: Theorems with complete proofs (no sorry)
Assumed statements: Count axiom, sorry, oops
```

**Example:**
```markdown
## Verification Statistics

- Total definitions: 15
- Total theorems: 23
- Verified theorems: 20 (87%)
- Incomplete proofs: 3 (13%)
- Axioms: 1
- Code generation: 5 functions
```

## Red Flags

### Critical Issues

**High-priority red flags:**
```isabelle
(* RED FLAG: Core theorem unproven *)
theorem main_correctness: "critical_property"
  sorry

(* RED FLAG: Axiom without justification *)
axiom mysterious_fact: "unexplained_property"

(* RED FLAG: Proof by sorry in critical path *)
lemma key_lemma: "important"
proof -
  (* ... *)
  have "crucial_step" sorry  (* RED FLAG *)
  (* ... *)
qed
```

### Warning Signs

**Medium-priority warnings:**
```isabelle
(* WARNING: Sledgehammer timeout *)
lemma complex: "statement"
  by sledgehammer  (* May have timed out *)

(* WARNING: Overly complex proof *)
lemma intricate: "statement"
proof -
  (* 200 lines of manual proof *)
  (* May contain errors *)
qed

(* WARNING: No specification *)
definition mystery_function :: "nat ⇒ nat" where
  "mystery_function = undefined"
(* No properties stated or proven *)
```

## Report Generation

### Section: Verified Components

**Template:**
```markdown
### [Function/Theorem Name]

**Location:** [File.thy:Line]
**Type:** [Definition/Lemma/Theorem]
**Properties Proven:**
- [Property 1 with reference]
- [Property 2 with reference]

**Proof Method:** [auto/induction/sledgehammer/manual]
**Proof Status:** ✓ Complete
**Dependencies:** [List of lemmas used]
**Lines of Proof:** [Number]
```

### Section: Assumptions

**Template:**
```markdown
### [Axiom/Sorry Name]

**Location:** [File.thy:Line]
**Type:** [axiom/sorry/oops]
**Statement:** ```isabelle [formal statement] ```
**Justification:** [Why this is assumed - if documented]
**Used By:** [List of theorems that depend on this]
**Impact:** [How many theorems transitively depend on this]
**Risk Level:** [Low/Medium/High]
**Recommendation:** [Should this be proven? Can it be proven?]
```

### Section: TCB Elements

**Template:**
```markdown
### [TCB Element Name]

**Type:** [Kernel/Library/Tool/External]
**Description:** [What is trusted]
**Version:** [Isabelle version, library version]
**Justification:** [Why it must be trusted]
**Alternatives:** [Could this be avoided?]
**Mitigation:** [How is risk managed?]
**Risk Level:** [Low/Medium/High]
```

## Example Analysis

**Input theory:**
```isabelle
theory Example
imports Main
begin

axiom controversial: "∀x. P x"

definition my_func :: "nat ⇒ nat" where
  "my_func n = n + 1"

lemma my_func_positive: "my_func n > 0"
  sorry

lemma my_func_monotone: "n < m ⟹ my_func n < my_func m"
  by (simp add: my_func_def)

theorem main_result: "Q"
proof -
  have "P x" for x by (rule controversial)
  have "my_func n > 0" for n by (rule my_func_positive)
  (* ... *)
qed

export_code my_func in SML file "func.sml"

end
```

**Output report excerpt:**
```markdown
## Verification Statistics

- Total definitions: 1
- Total theorems: 3
- Verified: 1 (33%)
- Assumed: 2 (67%)
- TCB elements: 3

## Verified Components

### my_func_monotone
**Location:** Example.thy:12
**Statement:** n < m ⟹ my_func n < my_func m
**Proof Status:** ✓ Complete
**Proof Method:** simp
**Dependencies:** my_func_def

## Assumptions and Axioms

### controversial (axiom)
**Location:** Example.thy:5
**Statement:** ∀x. P x
**Justification:** None provided
**Used By:** main_result
**Impact:** 1 theorem depends on this
**Risk Level:** HIGH - unproven axiom used in main result

### my_func_positive (sorry)
**Location:** Example.thy:10
**Statement:** my_func n > 0
**Reason:** Proof incomplete
**Used By:** main_result
**Impact:** 1 theorem depends on this
**Risk Level:** MEDIUM - should be provable

## Trusted Computing Base

### Isabelle/HOL Kernel
[Standard entry]

### Code Generation to SML
**Type:** Code Extraction
**Description:** Exports my_func to SML
**Risk:** Semantic gap between Isabelle and SML

## Verification Gaps

1. **Axiom without justification:** controversial axiom has no explanation
2. **Incomplete proof:** my_func_positive should be proven
3. **Main result depends on assumptions:** main_result transitively depends
   on both controversial and my_func_positive
```
