# Frama-C Integration Guide

Practical tips for using ACSL annotations with Frama-C verification tools.

## Table of Contents

1. [Overview](#overview)
2. [WP Plugin (Weakest Precondition)](#wp-plugin-weakest-precondition)
3. [RTE Plugin (Runtime Error Analysis)](#rte-plugin-runtime-error-analysis)
4. [Value Analysis Plugin](#value-analysis-plugin)
5. [Common Verification Patterns](#common-verification-patterns)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

## Overview

Frama-C is a framework for analyzing C programs with multiple plugins. The most common workflow combines:

1. **RTE plugin** - Generates assertions for runtime errors
2. **WP plugin** - Proves properties using weakest precondition calculus
3. **Value plugin** - Performs abstract interpretation for value ranges

## WP Plugin (Weakest Precondition)

### Basic Usage

```bash
frama-c -wp file.c
```

### Common WP Options

```bash
# Specify function to verify
frama-c -wp -wp-fct function_name file.c

# Choose prover (Alt-Ergo, Z3, CVC4, etc.)
frama-c -wp -wp-prover alt-ergo,z3 file.c

# Set timeout (in seconds)
frama-c -wp -wp-timeout 10 file.c

# Generate proof obligations report
frama-c -wp -wp-out report.txt file.c

# Verbose mode
frama-c -wp -wp-verbose 2 file.c
```

### WP-Specific Annotation Requirements

#### Frame Conditions (Assigns Clauses)

WP requires explicit `assigns` clauses to verify memory safety:

```c
/*@
  requires \valid(ptr);
  ensures *ptr == \old(*ptr) + 1;
  assigns *ptr;  // Required for WP!
*/
void increment(int *ptr) {
    (*ptr)++;
}
```

Without `assigns`, WP cannot prove the function doesn't modify other memory.

#### Loop Annotations

WP requires complete loop annotations:

```c
/*@
  loop invariant 0 <= i <= n;           // Required
  loop assigns i, sum;                   // Required
  loop variant n - i;                    // Required for termination
*/
for (int i = 0; i < n; i++) {
    sum += i;
}
```

### Proof Strategies

#### Strategy 1: Incremental Verification

Start with basic contracts, then add details:

```c
// Step 1: Basic contract
/*@
  requires n > 0;
  ensures \result >= 0;
*/

// Step 2: Add array validity
/*@
  requires \valid(array + (0..n-1));
  requires n > 0;
  ensures \result >= 0;
*/

// Step 3: Complete specification
/*@
  requires \valid(array + (0..n-1));
  requires n > 0;
  ensures \result >= 0 && \result < n;
  ensures \forall integer i; 0 <= i < n ==> array[\result] >= array[i];
  assigns \nothing;
*/
```

#### Strategy 2: Using Assertions as Hints

Add intermediate assertions to guide the prover:

```c
/*@
  requires \valid(array + (0..n-1));
  requires n > 0;
*/
void process(int *array, int n) {
    int mid = n / 2;

    //@ assert 0 <= mid < n;  // Hint for prover
    //@ assert \valid(array + mid);  // Explicit validity

    array[mid] = 0;
}
```

## RTE Plugin (Runtime Error Analysis)

### Basic Usage

RTE generates assertions for all potential runtime errors:

```bash
frama-c -rte file.c -then -wp
```

### Generated Assertions

RTE automatically adds assertions for:

- Division by zero
- Invalid pointer dereferences
- Array bounds violations
- Integer overflows
- Signed/unsigned conversions

Example:

```c
int divide(int a, int b) {
    return a / b;
}
```

RTE generates:

```c
int divide(int a, int b) {
    /*@ assert rte: division_by_zero: b ≠ 0; */
    return a / b;
}
```

### RTE Options

```bash
# Check only specific kinds of errors
frama-c -rte -rte-div file.c           # Division by zero only
frama-c -rte -rte-mem file.c           # Memory access only
frama-c -rte -rte-signed-overflow file.c  # Signed overflow only

# All runtime errors (default)
frama-c -rte -rte-all file.c
```

### Combining RTE with WP

Recommended workflow:

```bash
# Generate RTE assertions and verify with WP
frama-c -rte file.c -then -wp -then -report
```

## Value Analysis Plugin

### Basic Usage

```bash
frama-c -val file.c
```

### Value Analysis for Verification

Value analysis can help WP by narrowing value ranges:

```bash
frama-c -val file.c -then -wp
```

### Interpreting Value Results

Value plugin shows possible values for variables:

```c
int main() {
    int x;
    if (rand() % 2) {
        x = 10;
    } else {
        x = 20;
    }
    // Value plugin shows: x ∈ {10, 20}
    return x;
}
```

## Common Verification Patterns

### Pattern 1: Array Bounds Safety

Without ACSL, rely on RTE:

```bash
frama-c -rte file.c -then -wp
```

With ACSL, add explicit contracts:

```c
/*@
  requires \valid(array + (0..n-1));
  requires 0 <= index < n;
  assigns \nothing;
*/
int get(int *array, int n, int index) {
    return array[index];
}
```

### Pattern 2: Pointer Separation

When modifying multiple pointers:

```c
/*@
  requires \valid(a) && \valid(b);
  requires \separated(a, b);  // Critical for WP
  assigns *a, *b;
*/
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}
```

### Pattern 3: Loop Invariant Discovery

Use value analysis to discover invariants:

```bash
frama-c -val file.c -val-show-progress
```

Then formalize as loop invariants:

```c
/*@
  loop invariant 0 <= i <= n;  // From value analysis
  loop invariant 0 <= sum <= i * MAX_VALUE;  // From value analysis
*/
```

### Pattern 4: Function Pointers

```c
/*@
  requires \valid_function(func);
  requires \valid(array + (0..n-1));
  assigns array[0..n-1];
*/
void apply(void (*func)(int*), int *array, int n) {
    for (int i = 0; i < n; i++) {
        func(&array[i]);
    }
}
```

## Troubleshooting

### Problem: WP Timeout

**Symptom**: Prover times out on verification

**Solutions**:
1. Increase timeout: `-wp-timeout 30`
2. Try different provers: `-wp-prover z3,cvc4`
3. Add intermediate assertions as hints
4. Split complex properties into smaller ones
5. Simplify loop invariants

### Problem: Unknown Proof Result

**Symptom**: WP returns "Unknown" instead of "Valid" or "Invalid"

**Solutions**:
1. Add more precise invariants
2. Use RTE to catch missing preconditions
3. Add `assigns` clauses
4. Make implicit assumptions explicit

### Problem: Invalid Memory Access

**Symptom**: RTE reports potential invalid access

**Solutions**:
1. Add `\valid` preconditions
2. Add bounds checks to loop invariants
3. Verify pointer separation with `\separated`

### Problem: Loop Invariant Not Preserved

**Symptom**: WP fails to prove loop invariant preservation

**Solutions**:
1. Check invariant is true initially
2. Strengthen invariant with missing constraints
3. Add `loop assigns` clause
4. Verify loop variant is decreasing

### Problem: Assigns Clause Too Restrictive

**Symptom**: WP fails because function modifies more than specified

**Solutions**:
1. Review what the function actually modifies
2. Extend assigns clause: `assigns global, *ptr, array[0..n-1];`
3. Use `\nothing` only for pure functions

## Best Practices

### 1. Incremental Development

```bash
# Step 1: Start with RTE
frama-c -rte file.c

# Step 2: Add basic contracts
# (Edit file to add simple requires/ensures)

# Step 3: Verify with WP
frama-c -rte file.c -then -wp

# Step 4: Refine based on failures
# (Add missing preconditions, invariants, etc.)
```

### 2. Modular Verification

Verify functions one at a time:

```bash
frama-c -wp -wp-fct function1 file.c
frama-c -wp -wp-fct function2 file.c
```

### 3. Use Lemmas for Complex Properties

Define reusable lemmas:

```c
/*@
  lemma sum_bounds:
    \forall int *a, integer n;
      n > 0 && (\forall integer i; 0 <= i < n ==> 0 <= a[i] <= 100) ==>
      0 <= sum(a, 0, n) <= 100 * n;
*/
```

### 4. Document Verification Status

Add comments indicating verification status:

```c
// VERIFIED: Frama-C WP with Alt-Ergo (2024-01-15)
/*@
  requires \valid(array + (0..n-1));
  ensures sorted_array(array, n);
*/
void sort(int *array, int n);
```

### 5. Separate Concerns

- Use RTE for runtime safety
- Use WP for functional correctness
- Use Value for range analysis

### 6. GUI for Debugging

For complex proofs, use the Frama-C GUI:

```bash
frama-c-gui -wp file.c
```

The GUI provides:
- Visual proof obligation browser
- Inline annotation display
- Interactive prover results
- Source code navigation

### 7. Makefile Integration

Create a Makefile for verification:

```makefile
verify: file.c
	frama-c -rte $< -then -wp -then -report

verify-verbose: file.c
	frama-c -rte $< -then -wp -wp-verbose 2

verify-gui: file.c
	frama-c-gui -rte $< -then -wp
```

## Command Reference

### Complete Workflow Example

```bash
# Full verification pipeline
frama-c \
  -rte \                          # Generate runtime error checks
  -rte-all \                      # All error categories
  file.c \
  -then \
  -wp \                           # Weakest precondition
  -wp-rte \                       # Verify RTE assertions
  -wp-prover alt-ergo,z3 \        # Multiple provers
  -wp-timeout 10 \                # Timeout per proof
  -wp-fct main \                  # Verify specific function
  -then \
  -report                         # Generate report
```

### Quick Commands

```bash
# Quick check
frama-c -wp file.c

# With RTE
frama-c -rte file.c -then -wp

# Specific function
frama-c -wp -wp-fct foo file.c

# GUI mode
frama-c-gui -wp file.c

# Generate report
frama-c -wp file.c -then -report
```

## Verification Levels

### Level 1: Runtime Safety Only

```bash
frama-c -rte file.c -then -wp
```

Ensures no:
- Buffer overflows
- Null pointer dereferences
- Division by zero
- Arithmetic overflows

### Level 2: Partial Correctness

Add function contracts for intended behavior:

```c
/*@
  requires valid_input(x);
  ensures valid_output(\result);
*/
```

### Level 3: Full Functional Specification

Complete behavioral specification with:
- Full preconditions
- Complete postconditions
- Frame conditions (assigns)
- Loop invariants
- Termination proofs

```c
/*@
  requires \valid(array + (0..n-1));
  requires n > 0;
  ensures sorted_array(array, n);
  ensures is_permutation{Pre,Post}(array, array, n);
  assigns array[0..n-1];
  terminates \true;
*/
```
