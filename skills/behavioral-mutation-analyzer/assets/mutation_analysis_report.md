# Mutation Analysis Report

**Project:** [Project Name]
**Date:** [YYYY-MM-DD]
**Mutation Tool:** [PIT / Stryker / mutmut / etc.]
**Tool Version:** [Version]
**Analyzer:** [Name/Tool]

---

## Executive Summary

**Mutation Score:** [X]% ([killed]/[total] mutants killed)
**Adjusted Score:** [X]% (excluding no-coverage mutants)

**Key Findings:**
- [Number] surviving mutants identified
- [Number] equivalent mutants detected
- [Number] new tests generated
- [Number] test improvements suggested

**Recommendation:** [Overall assessment and priority actions]

---

## Mutation Testing Results

### Overall Statistics

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Mutants | [total] | 100% |
| Killed | [killed] | [%] |
| Survived | [survived] | [%] |
| No Coverage | [no_coverage] | [%] |
| Timeout | [timeout] | [%] |
| Error | [error] | [%] |

### Mutation Score Trend

[If available, show historical mutation scores]

| Date | Mutation Score | Change |
|------|----------------|--------|
| [date] | [score]% | - |
| [date] | [score]% | [+/-X]% |

---

## Surviving Mutants Analysis

### Summary by Category

| Category | Count | Percentage | Priority |
|----------|-------|------------|----------|
| Insufficient Coverage | [count] | [%] | High |
| Weak Assertions | [count] | [%] | High |
| Missed Edge Cases | [count] | [%] | Medium |
| Equivalent Mutants | [count] | [%] | Low |
| State/Timing Issues | [count] | [%] | Medium |

### Summary by File

| File | Total Mutants | Survived | Mutation Score |
|------|---------------|----------|----------------|
| [file1] | [total] | [survived] | [%] |
| [file2] | [total] | [survived] | [%] |
| [file3] | [total] | [survived] | [%] |

---

## Detailed Mutant Analysis

### Category 1: Insufficient Coverage ([count] mutants)

These mutants survived because the mutated code was never executed by any test.

#### Mutant #[ID]: [Brief Description]

**Location:** `[file]:[line]`
**Method:** `[method_name]`
**Mutation Operator:** [operator]

**Original Code:**
```[language]
[original code]
```

**Mutated Code:**
```[language]
[mutated code]
```

**Root Cause:**
[Explanation of why this code is not covered]

**Coverage Analysis:**
- Line coverage: [X]%
- Branch coverage: [X]%
- This specific path: Not covered

**Impact:** [High/Medium/Low]
**Reason:** [Why this mutant matters or doesn't matter]

**Recommended Action:**
[Specific guidance on what test to add]

**Generated Test:**
```[language]
[test code]
```

---

#### Mutant #[ID]: [Brief Description]

[Repeat structure for each mutant in this category]

---

### Category 2: Weak Assertions ([count] mutants)

These mutants were executed by tests but not detected due to insufficient assertions.

#### Mutant #[ID]: [Brief Description]

**Location:** `[file]:[line]`
**Method:** `[method_name]`
**Mutation Operator:** [operator]

**Original Code:**
```[language]
[original code]
```

**Mutated Code:**
```[language]
[mutated code]
```

**Root Cause:**
Test executes the mutated code but doesn't verify the affected behavior.

**Covering Tests:**
- `[test_name_1]` - [Why it doesn't catch the mutant]
- `[test_name_2]` - [Why it doesn't catch the mutant]

**Current Assertion:**
```[language]
[current weak assertion]
```

**Problem:**
[Explain why the assertion is too weak]

**Impact:** [High/Medium/Low]

**Recommended Action:**
Strengthen assertion to verify exact expected value.

**Enhanced Test:**
```[language]
[improved test code with stronger assertion]
```

---

### Category 3: Missed Edge Cases ([count] mutants)

These mutants survived because tests don't cover boundary conditions or special values.

#### Mutant #[ID]: [Brief Description]

**Location:** `[file]:[line]`
**Method:** `[method_name]`
**Mutation Operator:** [operator]

**Original Code:**
```[language]
[original code]
```

**Mutated Code:**
```[language]
[mutated code]
```

**Root Cause:**
Tests don't cover [specific edge case: null, zero, empty, boundary, etc.]

**Missing Test Cases:**
- [ ] Null input
- [ ] Empty collection
- [ ] Boundary value: [value]
- [ ] Negative value
- [ ] Maximum value
- [ ] Minimum value

**Impact:** [High/Medium/Low]

**Recommended Action:**
Add edge case tests for [specific cases].

**Generated Tests:**
```[language]
[edge case test code]
```

---

### Category 4: Equivalent Mutants ([count] mutants)

These mutants are semantically equivalent to the original code and cannot be killed.

#### Mutant #[ID]: [Brief Description]

**Location:** `[file]:[line]`
**Method:** `[method_name]`
**Mutation Operator:** [operator]

**Original Code:**
```[language]
[original code]
```

**Mutated Code:**
```[language]
[mutated code]
```

**Equivalence Reasoning:**
[Detailed explanation of why the mutant is equivalent]

**Mathematical/Logical Proof:**
[If applicable, show why the behaviors are identical]

**Impact:** None (equivalent mutant)

**Recommended Action:**
Configure mutation tool to skip this mutant:

```[config format]
[configuration to exclude this mutant]
```

**Documentation:**
Add comment in code explaining the equivalence:
```[language]
// Mutation testing note: [explanation]
[original code]
```

---

### Category 5: State and Timing Issues ([count] mutants)

These mutants affect state transitions, concurrency, or timing-dependent behavior.

#### Mutant #[ID]: [Brief Description]

**Location:** `[file]:[line]`
**Method:** `[method_name]`
**Mutation Operator:** [operator]

**Original Code:**
```[language]
[original code]
```

**Mutated Code:**
```[language]
[mutated code]
```

**Root Cause:**
Tests don't verify [state changes / side effects / timing behavior].

**State Analysis:**
- Initial state: [description]
- Expected state after operation: [description]
- Current test verification: [what's checked]
- Missing verification: [what's not checked]

**Impact:** [High/Medium/Low]

**Recommended Action:**
Add state verification or integration test.

**Generated Test:**
```[language]
[state verification test code]
```

---

## Test Suite Improvements

### New Tests Generated

**Total new tests:** [count]

#### Test 1: [Test Name]

**Purpose:** Kill mutants [#ID1, #ID2, #ID3]
**Category:** [Unit / Integration / Edge Case]
**Priority:** [High / Medium / Low]

**Test Code:**
```[language]
[complete test code]
```

**Mutants Killed:**
- Mutant #[ID]: [description]
- Mutant #[ID]: [description]

---

### Existing Tests to Enhance

**Total enhancements:** [count]

#### Enhancement 1: [Test Name]

**Current Test:**
```[language]
[current test code]
```

**Problem:**
[What's weak about the current test]

**Enhanced Test:**
```[language]
[improved test code]
```

**Additional Mutants Killed:**
- Mutant #[ID]: [description]
- Mutant #[ID]: [description]

---

## Prioritized Action Plan

### High Priority (Critical)

1. **[Action 1]**
   - Mutants affected: [#ID1, #ID2, ...]
   - Impact: [description]
   - Effort: [Low / Medium / High]
   - Test file: `[file]`

2. **[Action 2]**
   - Mutants affected: [#ID1, #ID2, ...]
   - Impact: [description]
   - Effort: [Low / Medium / High]
   - Test file: `[file]`

### Medium Priority (Important)

1. **[Action 1]**
   - Mutants affected: [#ID1, #ID2, ...]
   - Impact: [description]
   - Effort: [Low / Medium / High]

### Low Priority (Optional)

1. **[Action 1]**
   - Mutants affected: [#ID1, #ID2, ...]
   - Impact: [description]
   - Effort: [Low / Medium / High]

---

## Code Quality Insights

### High-Risk Areas

Files with lowest mutation scores (highest risk):

1. **[file1]** - [X]% mutation score
   - [Number] surviving mutants
   - Primary issues: [coverage / assertions / edge cases]
   - Recommendation: [specific action]

2. **[file2]** - [X]% mutation score
   - [Number] surviving mutants
   - Primary issues: [coverage / assertions / edge cases]
   - Recommendation: [specific action]

### Well-Tested Areas

Files with highest mutation scores (good coverage):

1. **[file1]** - [X]% mutation score
2. **[file2]** - [X]% mutation score

### Test Suite Weaknesses

**Common patterns identified:**
- [ ] Insufficient boundary testing
- [ ] Weak assertions (checking types instead of values)
- [ ] Missing null/empty checks
- [ ] Incomplete error handling tests
- [ ] Missing side effect verification
- [ ] Inadequate boolean logic testing

---

## Mutation Tool Configuration

### Current Configuration

```[config format]
[current mutation tool configuration]
```

### Recommended Configuration Changes

**Exclude equivalent mutants:**
```[config format]
[configuration to exclude identified equivalent mutants]
```

**Adjust timeouts:**
```[config format]
[timeout configuration if needed]
```

**Focus on high-value mutators:**
```[config format]
[mutator selection configuration]
```

---

## Metrics and Trends

### Mutation Score by Package/Module

| Package/Module | Mutation Score | Trend |
|----------------|----------------|-------|
| [package1] | [X]% | [↑/↓/→] |
| [package2] | [X]% | [↑/↓/→] |

### Mutant Distribution by Operator

| Mutation Operator | Total | Killed | Survived | Kill Rate |
|-------------------|-------|--------|----------|-----------|
| [operator1] | [count] | [count] | [count] | [%] |
| [operator2] | [count] | [count] | [count] | [%] |

### Test Effectiveness

| Test File | Mutants Killed | Effectiveness |
|-----------|----------------|---------------|
| [test1] | [count] | [High/Medium/Low] |
| [test2] | [count] | [High/Medium/Low] |

---

## Implementation Guide

### Step 1: Apply Generated Tests

1. Review generated tests in this report
2. Add tests to appropriate test files
3. Run tests to verify they pass
4. Run mutation testing to confirm mutants are killed

### Step 2: Enhance Existing Tests

1. Identify tests marked for enhancement
2. Apply suggested improvements
3. Verify enhanced tests still pass
4. Confirm improved mutation detection

### Step 3: Configure Mutation Tool

1. Update mutation tool configuration
2. Exclude identified equivalent mutants
3. Adjust settings based on recommendations

### Step 4: Verify Improvements

```bash
# Re-run mutation testing
[command to run mutation testing]

# Expected improvement: [X]% → [Y]%
```

---

## Appendix

### A. All Surviving Mutants

Complete list of all surviving mutants with IDs:

| ID | File | Line | Operator | Category | Priority |
|----|------|------|----------|----------|----------|
| [ID] | [file] | [line] | [op] | [cat] | [pri] |

### B. Equivalent Mutant Registry

Documented equivalent mutants for future reference:

| ID | Location | Reason | Configuration |
|----|----------|--------|---------------|
| [ID] | [file:line] | [reason] | [config] |

### C. Test Coverage Report

[Link to or summary of code coverage report]

### D. Mutation Testing Raw Output

[Link to full mutation testing report]

---

## Conclusion

[Summary paragraph synthesizing findings and providing clear next steps]

**Expected Outcome:**
After implementing recommendations, mutation score should improve from [current]% to approximately [target]%.

**Next Review:**
Schedule next mutation analysis after implementing high-priority improvements.

---

**Report Generated:** [Timestamp]
**Analysis Duration:** [Time taken]
**Contact:** [For questions about this report]
