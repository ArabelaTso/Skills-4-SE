---
name: counterexample-to-test-generator
description: Automatically generates executable test cases from model checking counterexample traces. Translates abstract counterexample states and transitions into concrete test inputs, execution steps, and assertions that reproduce property violations. Use when working with model checker outputs (SPIN, CBMC, NuSMV, TLA+, Java PathFinder, etc.) and needing to create regression tests, validate bug fixes, or reproduce verification failures in executable test suites.
---

# Counterexample To Test Generator

## Overview

This skill transforms counterexample traces from model checkers into executable test cases that reliably reproduce property violations. It bridges formal verification and testing by mapping abstract states to concrete values and generating runnable tests with clear traceability from counterexample steps to test logic.

## Workflow

### Step 1: Analyze Inputs

Gather and understand the counterexample trace and program:

1. **Identify the model checker format**: Determine which tool produced the counterexample (SPIN, CBMC, NuSMV, TLA+, JPF, etc.). See [references/model_checker_formats.md](references/model_checker_formats.md) for format details.

2. **Extract key information**:
   - Initial state values
   - Sequence of transitions/steps
   - Variable values at each step
   - Property violation point
   - Error condition or assertion failure

3. **Understand the program structure**:
   - Entry points and function signatures
   - Input parameters and their types
   - State variables involved in the trace
   - Control flow relevant to the counterexample

### Step 2: Map Abstract States to Concrete Values

Translate the counterexample's abstract representation into concrete test inputs:

1. **Determine concrete values** for abstract state variables:
   - Map symbolic values to concrete instances
   - Resolve non-deterministic choices to specific values
   - Handle ranges and constraints from the model

2. **Identify input sequences**:
   - Extract the sequence of function calls or operations
   - Determine parameter values for each call
   - Identify timing or ordering constraints

3. **Handle environment assumptions**:
   - External inputs or system calls
   - Concurrency or scheduling decisions
   - Resource states (files, network, memory)

### Step 3: Generate Test Structure

Create the test case framework in the target language:

1. **Choose test framework** based on the program language:
   - C/C++: Google Test, CUnit, Check
   - Java: JUnit, TestNG
   - Python: pytest, unittest
   - C#: NUnit, xUnit

2. **Structure the test**:
   - Setup phase: Initialize state to match counterexample start
   - Execution phase: Replay the counterexample sequence
   - Assertion phase: Verify the property violation occurs

3. **Add traceability comments**: Map each test step to counterexample steps for debugging and maintenance.

### Step 4: Implement Test Logic

Write the executable test code:

1. **Setup code**:
   ```
   // Initialize variables to counterexample initial state
   // Set up test fixtures or mocks
   // Configure environment (if needed)
   ```

2. **Execution sequence**:
   ```
   // Step 1 (CE line X): [description]
   // Execute operation with concrete values

   // Step 2 (CE line Y): [description]
   // Execute next operation
   ```

3. **Assertions**:
   ```
   // Verify property violation (CE line Z)
   // Assert expected failure condition
   // Check final state matches counterexample
   ```

### Step 5: Generate Output

Produce the complete test case with documentation:

1. **Test file**: Complete, compilable/runnable test code
2. **Mapping document**: Table linking counterexample steps to test lines
3. **Execution instructions**: How to compile and run the test
4. **Expected behavior**: What the test should demonstrate (failure reproduction)

## Example Workflow

**Input**: SPIN counterexample showing a deadlock in a concurrent system

**Output**:
```c
// test_deadlock.c - Reproduces deadlock from SPIN counterexample trail
#include <pthread.h>
#include <assert.h>

// Counterexample mapping:
// CE Step 1-2: Thread 1 acquires lock A
// CE Step 3-4: Thread 2 acquires lock B
// CE Step 5: Thread 1 waits for lock B (blocks)
// CE Step 6: Thread 2 waits for lock A (deadlock)

void* thread1_func(void* arg) {
    pthread_mutex_lock(&lock_a);  // CE Step 1
    sleep(1);                      // CE Step 2 (timing)
    pthread_mutex_lock(&lock_b);  // CE Step 5 (blocks)
    // ... rest of test
}

void test_deadlock_scenario() {
    // Setup: Initialize locks (CE initial state)
    pthread_mutex_init(&lock_a, NULL);
    pthread_mutex_init(&lock_b, NULL);

    // Execute: Create threads in counterexample order
    pthread_create(&t1, NULL, thread1_func, NULL);
    pthread_create(&t2, NULL, thread2_func, NULL);

    // This test will hang, demonstrating the deadlock
    pthread_join(t1, NULL);  // Will timeout
}
```

## Best Practices

1. **Minimize test complexity**: Generate the simplest test that reproduces the violation
2. **Preserve causality**: Maintain the exact sequence from the counterexample
3. **Make violations obvious**: Use clear assertions and error messages
4. **Add context**: Include comments explaining the property being violated
5. **Handle non-determinism**: Document any assumptions made when concretizing values
6. **Test the test**: Verify the generated test actually fails as expected

## Common Challenges

**Challenge**: Counterexample uses symbolic values without concrete bounds
**Solution**: Use representative values from the domain, document the choice

**Challenge**: Trace involves complex timing or scheduling
**Solution**: Use synchronization primitives or explicit delays to enforce ordering

**Challenge**: Program state is partially specified in counterexample
**Solution**: Initialize unspecified variables to default/neutral values

**Challenge**: Counterexample is very long
**Solution**: Identify the minimal prefix that still triggers the violation

## References

- [references/model_checker_formats.md](references/model_checker_formats.md): Detailed format specifications for common model checkers
- [assets/test_templates/](assets/test_templates/): Test framework templates for various languages
