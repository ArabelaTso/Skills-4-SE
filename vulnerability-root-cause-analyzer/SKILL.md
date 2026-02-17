---
name: vulnerability-root-cause-analyzer
description: Analyze vulnerable code to identify underlying root causes such as violated assumptions, incorrect invariants, missing validation checks, or unsafe component interactions. Use when investigating security vulnerabilities, CVEs, exploit code, or security audit findings. Infers why the vulnerability exists beyond surface symptoms, identifies systemic issues, and explains the chain of failures that enable exploitation.
---

# Vulnerability Root Cause Analyzer

Analyze vulnerable code to identify the underlying root causes that enable security vulnerabilities.

## Overview

Security vulnerabilities are symptoms of deeper issues in code design and implementation. This skill analyzes vulnerable code to identify:

1. **Violated assumptions** - What the code assumes but doesn't verify
2. **Incorrect invariants** - Properties that should hold but don't
3. **Missing checks** - Validation that should exist but is absent
4. **Unsafe interactions** - How components interact unsafely
5. **Design flaws** - Architectural issues that enable vulnerabilities

The goal is to understand WHY the vulnerability exists, not just WHAT it is.

## Root Cause Analysis Workflow

```
Vulnerable Code
    ↓
Identify Vulnerability Type
    ↓
Trace Attack Vector
    ↓
Analyze Assumptions
    ↓
Check Invariants
    ↓
Identify Missing Checks
    ↓
Examine Component Interactions
    ↓
Determine Root Cause
    ↓
Explain Exploitation Chain
```

## Analysis Process

### Step 1: Identify Vulnerability Type

Classify the vulnerability:

**Common types:**
- Buffer overflow
- SQL injection
- Cross-site scripting (XSS)
- Authentication bypass
- Privilege escalation
- Use-after-free
- Race condition
- Integer overflow

### Step 2: Trace Attack Vector

Understand how an attacker exploits the vulnerability:

**Questions:**
- What input triggers the vulnerability?
- What operations are performed?
- What security boundary is crossed?
- What is the impact?

### Step 3: Analyze Assumptions

Identify implicit assumptions in the code:

**Common assumptions:**
- Input is trusted
- Buffer is large enough
- Integer won't overflow
- Pointer is valid
- User is authenticated
- Data is sanitized

**Check:** Are these assumptions verified?

### Step 4: Check Invariants

Verify properties that should always hold:

**Common invariants:**
- Buffer bounds respected
- Pointers valid before dereference
- Authentication required for sensitive operations
- Data sanitized before use
- Resources properly released

**Check:** Do these invariants hold in all code paths?

### Step 5: Identify Missing Checks

Find validation that should exist:

**Common missing checks:**
- Input validation
- Bounds checking
- Null pointer checks
- Authentication checks
- Authorization checks
- Type validation
- Size limits

### Step 6: Examine Component Interactions

Analyze how components interact:

**Unsafe patterns:**
- Trusting data from untrusted source
- Passing unsanitized data between components
- Shared mutable state without synchronization
- Missing error propagation
- Inconsistent security policies

### Step 7: Determine Root Cause

Identify the fundamental issue:

**Root cause categories:**
- Design flaw
- Implementation error
- Missing security control
- Incorrect assumption
- Inadequate validation
- Unsafe API usage

## Root Cause Categories

For detailed root cause patterns, see [references/root_causes.md](references/root_causes.md).

Categories include:
- Trust boundary violations
- Input validation failures
- Memory safety violations
- Authentication/authorization flaws
- Race conditions and TOCTOU
- Cryptographic misuse

## Vulnerability Patterns

For common vulnerability patterns and their root causes, see [references/vulnerability_patterns.md](references/vulnerability_patterns.md).

Patterns include:
- Injection vulnerabilities
- Memory corruption
- Logic flaws
- Information disclosure
- Denial of service

## Example Analysis

**Input: Buffer overflow vulnerability**

```c
// Vulnerable code
void process_input(char *user_input) {
    char buffer[64];
    strcpy(buffer, user_input);  // VULNERABLE
    process(buffer);
}
```

**Output: Root cause analysis**

```markdown
# Vulnerability Root Cause Analysis

## Vulnerability Summary

**Type:** Buffer Overflow (CWE-120)
**Location:** process_input() function
**Severity:** Critical
**Impact:** Arbitrary code execution

## Vulnerability Description

The `strcpy` function copies user-controlled input into a fixed-size buffer
without checking the input length, allowing an attacker to overflow the buffer
and overwrite adjacent memory.

## Attack Vector

1. Attacker provides input longer than 64 bytes
2. `strcpy` copies entire input into 64-byte buffer
3. Excess bytes overflow into adjacent stack memory
4. Attacker can overwrite return address
5. Control flow hijacked to attacker-controlled code

## Root Cause Analysis

### Primary Root Cause: Violated Assumption

**Assumption:** Input length ≤ 64 bytes
**Reality:** Input length is unbounded and attacker-controlled
**Violation:** Code assumes input fits in buffer without verification

**Why this assumption exists:**
- Developer may have expected input from trusted source
- May have assumed earlier validation (that doesn't exist)
- May not have considered malicious input

**Why it's violated:**
- No length check before `strcpy`
- `strcpy` doesn't enforce bounds
- Input comes from untrusted source (user)

### Secondary Root Cause: Missing Security Control

**Missing Control:** Input length validation
**Should exist:** Before copying to fixed-size buffer
**Impact:** Allows unbounded copy operation

**What should be present:**
```c
if (strlen(user_input) >= sizeof(buffer)) {
    // Handle error
    return;
}
```

### Tertiary Root Cause: Unsafe API Usage

**Unsafe API:** `strcpy`
**Why unsafe:** No bounds checking
**Safe alternative:** `strncpy`, `strlcpy`, or `snprintf`

**API characteristics:**
- `strcpy` copies until null terminator
- No way to specify maximum length
- Inherently unsafe for untrusted input

## Invariant Violations

### Invariant 1: Buffer Bounds
**Expected:** `buffer[0]` through `buffer[63]` only
**Violated:** Writes beyond `buffer[63]`
**Consequence:** Stack corruption

### Invariant 2: Control Flow Integrity
**Expected:** Function returns to caller
**Violated:** Return address overwritten
**Consequence:** Arbitrary code execution

## Missing Checks

1. **Input length validation**
   - Location: Before `strcpy` call
   - Check: `strlen(user_input) < sizeof(buffer)`
   - Impact: Prevents overflow

2. **Buffer bounds enforcement**
   - Location: During copy operation
   - Check: Use bounded copy function
   - Impact: Limits copy to buffer size

3. **Input source validation**
   - Location: At trust boundary
   - Check: Verify input from trusted source
   - Impact: Reduces attack surface

## Component Interaction Analysis

### Trust Boundary Violation

```
[Untrusted Input] → [No Validation] → [Trusted Buffer]
```

**Issue:** Data crosses trust boundary without validation

**Components:**
- **User input:** Untrusted, attacker-controlled
- **process_input():** Assumes trusted input
- **buffer:** Expects bounded data

**Unsafe interaction:**
- Untrusted data used directly in memory operation
- No sanitization or validation at boundary
- Downstream code assumes data is safe

## Exploitation Chain

1. **Entry point:** User provides input
2. **Missing check:** No length validation
3. **Unsafe operation:** `strcpy` with unbounded input
4. **Memory corruption:** Buffer overflow
5. **Control flow hijack:** Return address overwritten
6. **Code execution:** Attacker code runs

**Each link in chain is necessary:**
- Remove any link → exploitation fails
- All links present → exploitation succeeds

## Systemic Issues

### Design Flaw
**Issue:** Fixed-size buffer for variable-length input
**Better design:** Dynamic allocation or streaming

### Implementation Error
**Issue:** Using unsafe `strcpy` function
**Better implementation:** Use safe alternatives

### Missing Security Layer
**Issue:** No input validation layer
**Better architecture:** Validate at trust boundary

## Recommended Fixes

### Fix 1: Input Validation (Immediate)
```c
void process_input(char *user_input) {
    char buffer[64];
    if (strlen(user_input) >= sizeof(buffer)) {
        // Log error and reject
        return;
    }
    strcpy(buffer, user_input);
    process(buffer);
}
```

**Addresses:** Missing check
**Limitation:** Still uses unsafe `strcpy`

### Fix 2: Safe API (Better)
```c
void process_input(char *user_input) {
    char buffer[64];
    strncpy(buffer, user_input, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';  // Ensure null termination
    process(buffer);
}
```

**Addresses:** Unsafe API usage
**Benefit:** Bounds enforced by API

### Fix 3: Dynamic Allocation (Best)
```c
void process_input(char *user_input) {
    size_t len = strlen(user_input);
    if (len > MAX_INPUT_SIZE) {
        return;  // Reject excessive input
    }
    char *buffer = malloc(len + 1);
    if (!buffer) {
        return;  // Handle allocation failure
    }
    strcpy(buffer, user_input);
    process(buffer);
    free(buffer);
}
```

**Addresses:** Design flaw
**Benefit:** No fixed-size limitation

## Prevention Strategies

### Code Level
- Use safe APIs (strncpy, snprintf)
- Validate all input
- Check buffer bounds
- Enable compiler protections (stack canaries, ASLR)

### Design Level
- Avoid fixed-size buffers for variable input
- Validate at trust boundaries
- Principle of least privilege
- Defense in depth

### Process Level
- Code review for unsafe functions
- Static analysis tools
- Fuzzing and testing
- Security training

## Related Vulnerabilities

This root cause pattern affects:
- All uses of `strcpy` with untrusted input
- Similar unsafe functions: `sprintf`, `gets`, `scanf`
- Any fixed-size buffer with variable input
- Other trust boundary violations in codebase
```

## Analysis Strategies

For detailed analysis strategies by vulnerability type, see [references/analysis_strategies.md](references/analysis_strategies.md).

Strategies include:
- Memory corruption vulnerabilities
- Injection vulnerabilities
- Authentication/authorization flaws
- Cryptographic vulnerabilities
- Race conditions

## Best Practices

1. **Look beyond symptoms** - Find the underlying cause
2. **Trace trust boundaries** - Where does untrusted data enter?
3. **Question assumptions** - What does code assume?
4. **Check invariants** - What should always be true?
5. **Examine interactions** - How do components interact?
6. **Consider systemic issues** - Is this a pattern?
7. **Explain exploitation** - How does attack succeed?

## Red Flags

Watch for these indicators of root causes:

**High-priority:**
- Untrusted input without validation
- Unsafe API usage (strcpy, sprintf, etc.)
- Missing bounds checks
- Unchecked return values
- Assumptions about input
- Trust boundary violations

**Medium-priority:**
- Complex conditionals
- Error handling gaps
- Implicit type conversions
- Global mutable state
- Privilege assumptions

## Report Template

```markdown
# Vulnerability Root Cause Analysis

## Vulnerability Summary
- Type and classification
- Location and severity
- Impact

## Attack Vector
- How exploitation works
- Required conditions
- Impact

## Root Cause Analysis
- Primary root cause
- Secondary causes
- Why they exist

## Invariant Violations
- What should hold
- What actually happens
- Consequences

## Missing Checks
- What validation is missing
- Where it should be
- Impact of absence

## Component Interactions
- How components interact
- Trust boundaries
- Unsafe patterns

## Exploitation Chain
- Step-by-step attack
- Necessary conditions
- Breaking points

## Systemic Issues
- Design flaws
- Implementation patterns
- Missing security layers

## Recommended Fixes
- Immediate fixes
- Better solutions
- Long-term improvements

## Prevention Strategies
- Code-level prevention
- Design-level prevention
- Process improvements

## Related Vulnerabilities
- Similar issues in codebase
- Pattern instances
```

## Additional Resources

For detailed guidance:
- [Root Causes](references/root_causes.md) - Common root cause patterns
- [Vulnerability Patterns](references/vulnerability_patterns.md) - Vulnerability types and causes
- [Analysis Strategies](references/analysis_strategies.md) - Analysis by vulnerability type
