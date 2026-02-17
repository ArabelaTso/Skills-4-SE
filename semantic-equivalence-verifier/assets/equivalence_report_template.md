# Semantic Equivalence Verification Report

**Date:** [YYYY-MM-DD]
**Analyzer:** [Name/Tool]
**Analysis Type:** [Strict / Partial / Observable Equivalence]

---

## Executive Summary

**Equivalence Status:** [✓ EQUIVALENT / ✗ NOT EQUIVALENT / ⚠ PARTIALLY EQUIVALENT]

**Brief Summary:**
[1-2 sentence summary of findings]

---

## Artifacts Under Analysis

### Artifact A
- **Location:** [file path:line numbers]
- **Type:** [Function / Class / Module]
- **Language:** [Programming language]
- **Signature:**
  ```
  [function/class signature]
  ```

### Artifact B
- **Location:** [file path:line numbers]
- **Type:** [Function / Class / Module]
- **Language:** [Programming language]
- **Signature:**
  ```
  [function/class signature]
  ```

---

## Analysis Methodology

**Techniques Applied:**
- [ ] Static analysis (control flow, data flow)
- [ ] Dynamic analysis (test execution)
- [ ] Symbolic execution
- [ ] Formal verification
- [ ] Manual code review

**Scope:**
- **Input domain:** [Description of input constraints considered]
- **Equivalence type:** [Strict / Partial / Observable]
- **Assumptions:** [Any assumptions made during analysis]

---

## Detailed Findings

### Control Flow Analysis

**Control Flow Graph Comparison:**
- Artifact A: [Number of nodes, branches, loops]
- Artifact B: [Number of nodes, branches, loops]

**Structural Differences:**
[Describe any differences in control flow structure]

**Assessment:**
[✓ Equivalent / ✗ Different / ⚠ Potentially equivalent]

### Data Flow Analysis

**Variable Dependencies:**
| Variable | Artifact A | Artifact B | Status |
|----------|-----------|-----------|---------|
| [var1]   | [deps]    | [deps]    | [✓/✗]   |
| [var2]   | [deps]    | [deps]    | [✓/✗]   |

**Computation Sequences:**
[Describe how data flows through each artifact]

**Assessment:**
[✓ Equivalent / ✗ Different / ⚠ Potentially equivalent]

### Behavioral Analysis

**Input-Output Mapping:**

| Test Case | Input | Artifact A Output | Artifact B Output | Match |
|-----------|-------|-------------------|-------------------|-------|
| TC1       | [in]  | [out]             | [out]             | [✓/✗] |
| TC2       | [in]  | [out]             | [out]             | [✓/✗] |
| TC3       | [in]  | [out]             | [out]             | [✓/✗] |

**Edge Cases Tested:**
- [ ] Null/empty inputs
- [ ] Boundary values
- [ ] Invalid inputs
- [ ] Large inputs
- [ ] Special values (NaN, infinity, etc.)

**Side Effects:**
| Effect Type | Artifact A | Artifact B | Match |
|-------------|-----------|-----------|-------|
| File I/O    | [desc]    | [desc]    | [✓/✗] |
| Network     | [desc]    | [desc]    | [✓/✗] |
| State       | [desc]    | [desc]    | [✓/✗] |
| Memory      | [desc]    | [desc]    | [✓/✗] |

**Assessment:**
[✓ Equivalent / ✗ Different / ⚠ Partially equivalent]

---

## Equivalence Verdict

### [✓ EQUIVALENT] (Use this section if equivalent)

**Equivalence Type:** [Strict / Partial / Observable]

**Evidence:**
1. [Key evidence point 1]
2. [Key evidence point 2]
3. [Key evidence point 3]

**Confidence Level:** [High / Medium / Low]

**Notes:**
- [Any caveats or conditions]
- [Performance differences if any]
- [Style or implementation differences]

---

### [✗ NOT EQUIVALENT] (Use this section if not equivalent)

**Divergence Points:**

#### Difference 1: [Brief description]
- **Location:** [Where the difference occurs]
- **Nature:** [Control flow / Data flow / Output / Side effect]
- **Severity:** [Critical / Major / Minor]

**Artifact A Behavior:**
```
[Code or description]
```

**Artifact B Behavior:**
```
[Code or description]
```

**Counterexample:**
```
Input: [specific input that demonstrates difference]
Artifact A output: [output]
Artifact B output: [output]
```

**Root Cause:**
[Explanation of why the difference exists]

---

#### Difference 2: [Brief description]
[Repeat structure above for each difference]

---

### [⚠ PARTIALLY EQUIVALENT] (Use this section if partially equivalent)

**Equivalence Domain:**
[Describe the input domain where artifacts are equivalent]

**Non-Equivalence Domain:**
[Describe the input domain where artifacts differ]

**Conditions for Equivalence:**
- [Condition 1]
- [Condition 2]

---

## Recommendations

### For Achieving Full Equivalence

**Priority 1 - Critical Changes:**
1. **[Change description]**
   - **Artifact to modify:** [A / B / Both]
   - **Suggested modification:**
     ```
     [Code change]
     ```
   - **Rationale:** [Why this change is needed]

**Priority 2 - Important Changes:**
[Repeat structure above]

**Priority 3 - Optional Improvements:**
[Repeat structure above]

### Alternative Approaches

If full equivalence is not required:
- [Alternative 1: Description and trade-offs]
- [Alternative 2: Description and trade-offs]

---

## Performance Comparison

**Time Complexity:**
- Artifact A: [O-notation]
- Artifact B: [O-notation]

**Space Complexity:**
- Artifact A: [O-notation]
- Artifact B: [O-notation]

**Benchmark Results (if available):**
| Input Size | Artifact A Time | Artifact B Time | Difference |
|------------|----------------|----------------|------------|
| [size]     | [time]         | [time]         | [%]        |

**Note:** Performance differences do not affect semantic equivalence unless specified in requirements.

---

## Additional Observations

**Code Quality:**
- Readability: [A vs B comparison]
- Maintainability: [A vs B comparison]
- Best practices: [A vs B comparison]

**Security Considerations:**
[Any security-relevant differences]

**Portability:**
[Platform or environment-specific behaviors]

---

## Appendix

### Test Cases

**Test Case 1:**
```
Input: [input]
Expected: [expected output]
Artifact A: [actual output]
Artifact B: [actual output]
Status: [PASS/FAIL]
```

### Symbolic Execution Traces

[If applicable, include symbolic execution paths]

### Formal Proofs

[If applicable, include proof sketches or verification conditions]

---

## Conclusion

[Final summary paragraph synthesizing all findings and providing clear guidance on equivalence status and next steps]

---

**Report Generated:** [Timestamp]
**Tool Version:** [If applicable]
**Contact:** [For questions about this report]
