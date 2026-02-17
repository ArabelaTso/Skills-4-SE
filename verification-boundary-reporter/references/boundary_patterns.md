# Verification Boundary Patterns

Common patterns, anti-patterns, and red flags in verification boundaries.

## Assumption Propagation Patterns

### Pattern: Transitive Assumptions

**Description:** Assumptions propagate through dependency chains.

**Example:**
```
Axiom A
  ↓ (used by)
Lemma B (proven using A)
  ↓ (used by)
Theorem C (proven using B)
  ↓ (used by)
Main Result (proven using C)
```

**Impact:** Main Result depends on Axiom A, even if not directly referenced.

**Detection:**
- Trace all dependencies
- Use `Print Assumptions` (Coq) or similar
- Build dependency graph

**Report:**
```markdown
### Transitive Dependency on Axiom A

Main Result → Theorem C → Lemma B → Axiom A

**Risk:** Main Result's correctness depends on unproven Axiom A
**Recommendation:** Prove or justify Axiom A
```

### Pattern: Assumption Amplification

**Description:** Multiple assumptions combine to create larger trust gap.

**Example:**
```
Axiom A1: Property P
Axiom A2: Property Q
Theorem T: Property R
  Proof uses both A1 and A2
```

**Impact:** Theorem T depends on both axioms; failure of either invalidates T.

**Risk Assessment:**
```
Risk(T) = Risk(A1) + Risk(A2) + Risk(interaction)
```

## Partial Verification Patterns

### Pattern: Verified Core, Unverified Wrapper

**Description:** Core algorithm verified, but wrapper code unverified.

**Example:**
```isabelle
(* VERIFIED: Core algorithm *)
function core_algorithm :: "input ⇒ output" where
  "core_algorithm x = ..."

theorem core_correct: "spec (core_algorithm x)"

(* UNVERIFIED: Wrapper with I/O *)
definition wrapper :: "string ⇒ unit" where
  "wrapper filename = (
    let input = read_file filename in  (* UNVERIFIED *)
    let result = core_algorithm input in  (* VERIFIED *)
    write_file result  (* UNVERIFIED *)
  )"
```

**Boundary:**
```
[Unverified I/O] → [Verified Core] → [Unverified I/O]
```

**Report:**
```markdown
### Verification Boundary: Core vs Wrapper

**Verified:** core_algorithm (functional correctness)
**Unverified:** File I/O operations
**TCB:** File system, OS

**Guarantees:**
- IF input is valid, THEN output is correct
- File operations are NOT verified

**Limitations:**
- No guarantee about file reading correctness
- No guarantee about file writing correctness
- No verification of error handling
```

### Pattern: Shallow Verification

**Description:** Only basic properties verified, not full correctness.

**Example:**
```dafny
// SHALLOW: Only type safety
method Process(a: array<int>)
  requires a.Length > 0
  modifies a
{
  a[0] := 0;
}

// vs

// DEEP: Functional correctness
method Process(a: array<int>)
  requires a.Length > 0
  modifies a
  ensures a[0] == 0
  ensures forall i :: 1 <= i < a.Length ==> a[i] == old(a[i])
{
  a[0] := 0;
}
```

**Report:**
```markdown
### Verification Depth: Shallow

**Verified Properties:**
- Type safety
- Memory safety (no out-of-bounds)

**Unverified Properties:**
- Functional correctness (what the method does)
- Side effects on array elements
- Relationship between input and output

**Risk:** Method may be memory-safe but functionally incorrect
```

## Verification Escape Hatches

### Pattern: Sorry/Admit/Admitted

**Description:** Proof explicitly incomplete.

**Red flags:**
```isabelle
lemma important: "critical_property"
  sorry  (* RED FLAG *)

lemma key_step: "intermediate"
proof -
  have "crucial" sorry  (* RED FLAG *)
  (* ... *)
qed
```

**Risk levels:**
- **HIGH:** Core theorem with sorry
- **MEDIUM:** Helper lemma with sorry
- **LOW:** Test/example code with sorry

### Pattern: Axiom Without Justification

**Description:** Axiom declared without explanation.

**Example:**
```coq
Axiom magic_property : forall x, P x.
(* No comment explaining why this is assumed *)
```

**Report:**
```markdown
### Unjustified Axiom: magic_property

**Risk Level:** HIGH
**Reason:** No justification provided
**Recommendation:** Either:
1. Prove the property
2. Document why it must be assumed
3. Show it's consistent with the logic
```

### Pattern: Assume in Critical Path

**Description:** Assumption in production code.

**Example:**
```dafny
method CriticalOperation(x: int) returns (y: int)
  ensures y > 0
{
  assume x > 0;  (* RED FLAG: Assumption in production *)
  y := x;
}
```

**Risk:** Correctness depends on unverified assumption.

## Trusted Computing Base Patterns

### Pattern: Minimized TCB

**Description:** Small, well-defined trusted base.

**Good example:**
```
TCB:
- Proof assistant kernel (small, audited)
- Standard library (widely used)
- Code generator (tested)

Total TCB: ~3 components
```

### Pattern: Bloated TCB

**Description:** Large, poorly defined trusted base.

**Bad example:**
```
TCB:
- Proof assistant kernel
- 50+ unverified library modules
- Custom code generator
- External SMT solver
- Unverified runtime
- Operating system
- Hardware
- ...

Total TCB: Unclear, large
```

**Report:**
```markdown
### TCB Assessment: Bloated

**Issues:**
- Too many unverified dependencies
- Unclear boundaries
- High risk of bugs in TCB

**Recommendation:** Minimize TCB by:
1. Verifying critical library modules
2. Using standard, audited components
3. Clearly documenting TCB boundaries
```

### Pattern: Hidden TCB Elements

**Description:** TCB elements not explicitly documented.

**Example:**
```isabelle
(* Uses sledgehammer *)
lemma auto_proven: "statement"
  by sledgehammer

(* Hidden: External ATPs in TCB? *)
(* Answer: No, proofs are reconstructed and checked by kernel *)
```

**Report:**
```markdown
### Hidden TCB: Sledgehammer

**Apparent TCB:** External ATPs (E, SPASS, Z3)
**Actual TCB:** Isabelle kernel only
**Explanation:** ATPs suggest proofs, but Isabelle kernel validates
**Risk Level:** Low - kernel checks all proofs
```

## Code Generation Patterns

### Pattern: Unverified Extraction

**Description:** Code generation without correctness proof.

**Example:**
```isabelle
export_code my_function in SML file "output.sml"
(* Code generator correctness not verified *)
```

**Boundary:**
```
[Verified Isabelle Code] → [Unverified Translation] → [Unverified SML Code]
```

**Report:**
```markdown
### Code Generation Trust Gap

**Verified:** Isabelle implementation
**Unverified:** Translation to SML
**Risk:** Semantic mismatch between Isabelle and SML

**Specific Risks:**
- Integer overflow (Isabelle nat vs SML int)
- Lazy vs eager evaluation
- Exception handling
- Side effects

**Mitigation:** Testing, but not formal verification
```

### Pattern: Custom Extraction

**Description:** Custom type/constant mappings.

**Example:**
```coq
Extract Inductive nat => "int" [...].
(* Maps unbounded nat to bounded int *)
```

**Risk:** HIGH - semantic mismatch.

## Verification Timeout Patterns

### Pattern: Timeout as "Verification"

**Description:** Treating timeout as verification failure.

**Anti-pattern:**
```dafny
method Complex(x: int) returns (y: int)
  ensures y > 0
{
  // Complex implementation
}
// Dafny: Verification timed out

// WRONG: "This is unverified"
// CORRECT: "Verification status unknown (timeout)"
```

**Report:**
```markdown
### Verification Timeout

**Status:** UNKNOWN (not verified, not disproven)
**Reason:** Verifier timeout
**Risk:** May be correct but unverifiable with current resources
**Recommendation:**
1. Simplify code
2. Add intermediate assertions
3. Increase timeout
4. Manual proof
```

## Specification Completeness Patterns

### Pattern: Under-Specification

**Description:** Specification too weak to ensure correctness.

**Example:**
```dafny
method Sort(a: array<int>)
  modifies a
  ensures a.Length == old(a.Length)
  // Missing: sorted property, permutation
```

**Risk:** Implementation may satisfy weak spec but be incorrect.

### Pattern: Over-Specification

**Description:** Specification too strong, constrains implementation unnecessarily.

**Example:**
```dafny
method Sort(a: array<int>)
  modifies a
  ensures sorted(a)
  ensures permutation(a, old(a))
  ensures a[0] <= a[1] <= a[2] <= ...  // Redundant
  ensures forall i :: 0 <= i < a.Length ==> ...  // Redundant
```

**Issue:** Redundant specifications make verification harder.

## Dependency Patterns

### Pattern: Circular Dependencies

**Description:** Mutual dependencies between components.

**Example:**
```
Lemma A depends on Lemma B
Lemma B depends on Lemma A
```

**Risk:** Circular reasoning, unsound.

**Detection:** Build dependency graph, check for cycles.

### Pattern: Deep Dependency Chains

**Description:** Long chains of dependencies.

**Example:**
```
Axiom A → Lemma B → Lemma C → Lemma D → ... → Theorem Z
```

**Risk:** Assumption propagates through entire chain.

**Report:**
```markdown
### Deep Dependency Chain

**Length:** 10 lemmas
**Root:** Axiom A
**Leaf:** Theorem Z

**Risk:** Any error in chain invalidates Z
**Recommendation:** Shorten chain, prove intermediate results independently
```

## Testing vs Verification Patterns

### Pattern: Verification by Testing

**Anti-pattern:**
```
// WRONG: "Tested on 1000 inputs, so it's verified"
```

**Correct:**
```
// Testing provides confidence, not verification
// Verification proves correctness for ALL inputs
```

### Pattern: Complementary Testing

**Good practice:**
```
1. Verify functional correctness formally
2. Test extracted code for:
   - Performance
   - Integration
   - Edge cases not covered by spec
```

## Red Flag Checklist

### Critical Red Flags (HIGH Risk)

- [ ] Core theorem with sorry/admit/Admitted
- [ ] Axiom without justification
- [ ] Assume in production code
- [ ] Inconsistent axiom (provably false)
- [ ] Circular dependencies
- [ ] Verification timeout on critical code
- [ ] No specification on critical method
- [ ] Custom extraction with semantic mismatch

### Warning Signs (MEDIUM Risk)

- [ ] Helper lemma with sorry
- [ ] Standard axiom without documentation
- [ ] Weak specification
- [ ] External method without spec
- [ ] Large TCB
- [ ] Deep dependency chains
- [ ] Opaque functions without properties

### Minor Issues (LOW Risk)

- [ ] Test code with sorry
- [ ] Example code unverified
- [ ] Documentation gaps
- [ ] Redundant specifications

## Reporting Best Practices

### Be Explicit About Unknowns

**Bad:**
```
"Method X is verified"
(But verification timed out)
```

**Good:**
```
"Method X verification status: UNKNOWN (timeout)"
```

### Quantify Risk

**Bad:**
```
"There are some assumptions"
```

**Good:**
```
"3 axioms, affecting 15 theorems (60% of codebase)"
```

### Provide Context

**Bad:**
```
"Uses axiom A"
```

**Good:**
```
"Uses axiom A (functional extensionality, standard and consistent)"
```

### Recommend Actions

**Bad:**
```
"Lemma B is unproven"
```

**Good:**
```
"Lemma B is unproven. Recommendation: Should be provable using
existing lemmas C and D. Estimated effort: 1-2 hours."
```
