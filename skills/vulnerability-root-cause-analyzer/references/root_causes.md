# Common Root Causes of Vulnerabilities

## 1. Violated Assumptions

### Trust Boundary Violations
- **Assumption**: External input is validated before use
- **Reality**: Input validation is missing, incomplete, or bypassable
- **Example**: SQL injection when assuming user input is safe

### Implicit Contracts
- **Assumption**: Caller provides valid data within expected ranges
- **Reality**: No enforcement of preconditions
- **Example**: Buffer overflow when assuming string length < buffer size

### Environmental Assumptions
- **Assumption**: System resources are always available
- **Reality**: Resource exhaustion or race conditions occur
- **Example**: TOCTOU bugs when assuming file state persists

## 2. Missing Checks

### Boundary Checks
- Missing array bounds validation
- No string length verification
- Unchecked pointer arithmetic
- Integer overflow/underflow without detection

### Null/Validity Checks
- Dereferencing pointers without null checks
- Using uninitialized variables
- Accessing freed memory
- Missing error code validation

### Authorization Checks
- Missing access control verification
- Inadequate privilege separation
- Confused deputy problems

## 3. Incorrect Invariants

### Loop Invariants
- **Broken**: Buffer index stays within bounds
- **Reality**: Off-by-one errors or incorrect termination
- **Example**: `for(i=0; i<=n; i++)` when array has n elements

### Data Structure Invariants
- **Broken**: Linked list is acyclic
- **Reality**: Circular references created
- **Example**: Use-after-free in doubly-linked list removal

### State Machine Invariants
- **Broken**: Authentication required before privileged operations
- **Reality**: State transitions allow bypassing authentication
- **Example**: Session fixation vulnerabilities

## 4. Unsafe Interactions

### Component Composition
- Mismatched assumptions between components
- Incorrect API usage patterns
- Semantic gaps in interfaces

### Concurrency Issues
- Race conditions on shared state
- Missing synchronization primitives
- Atomicity violations

### Type Confusion
- Implicit type conversions causing data loss
- Mixing signed/unsigned integers
- Pointer type mismatches

## 5. Design Flaws

### Insufficient Isolation
- Lack of privilege separation
- Shared mutable state across trust boundaries
- Missing sandboxing or compartmentalization

### Cryptographic Misuse
- Weak or broken algorithms
- Improper key management
- Incorrect protocol implementation

### Logic Errors
- Flawed authentication/authorization logic
- Incorrect business rule implementation
- Time-of-check to time-of-use gaps

## 6. Implementation Defects

### Memory Management
- Manual memory management errors
- Dangling pointers
- Double-free vulnerabilities
- Memory leaks enabling DoS

### Error Handling
- Ignoring error returns
- Incorrect exception handling
- Information leakage in error messages

### Input Processing
- Insufficient input sanitization
- Incorrect parsing logic
- Format string vulnerabilities

## Root Cause Analysis Framework

### Questions to Ask

1. **What assumption was violated?**
   - What did the developer assume about inputs, state, or environment?
   - Where is this assumption documented or implicit?

2. **What check is missing?**
   - What validation should have occurred but didn't?
   - Where should the check be placed?

3. **What invariant was broken?**
   - What property should always hold?
   - When and how does it get violated?

4. **What interaction is unsafe?**
   - How do components interact incorrectly?
   - What semantic mismatch exists?

5. **What is the exploitation chain?**
   - How does the attacker trigger the root cause?
   - What capabilities does this provide?
   - What is the security impact?
