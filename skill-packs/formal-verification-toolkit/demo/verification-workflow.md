# Formal Verification Workflow Guide

This guide walks you through a complete formal verification workflow using the Formal Verification Toolkit.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Workflow](#step-by-step-workflow)
4. [Example: Concurrent Counter](#example-concurrent-counter)
5. [Tips and Best Practices](#tips-and-best-practices)

## Overview

The formal verification workflow consists of these main stages:

```
Source Code → Specification → Property Definition → Model Checking → Repair → Testing
```

Each stage uses specific skills from the toolkit to automate the verification process.

## Prerequisites

- Formal Verification Toolkit installed
- Basic understanding of temporal logic (optional but helpful)
- Source code to verify

## Step-by-Step Workflow

### Step 1: Generate Formal Specification

**Goal:** Convert your source code into a formal TLA+ specification.

**Skill:** `program-to-tlaplus-spec-generator`

**Input:**
- Your source code (any language: Python, Java, C, etc.)
- Optional: Specific components to focus on

**Action:**
```
Use the program-to-tlaplus-spec-generator skill with your source code.
```

**Output:**
- TLA+ specification (.tla file)
- Mapping document (program constructs → TLA+ elements)

**Example:**
```python
# Input: Python code
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def get(self):
        return self.value
```

```tla
---- MODULE Counter ----
EXTENDS Naturals

VARIABLE value

Init == value = 0

Increment == value' = value + 1

Get == UNCHANGED value

Next == Increment \/ Get

Spec == Init /\ [][Next]_value
====
```

### Step 2: Formalize Requirements as Properties

**Goal:** Convert natural language requirements into formal temporal logic properties.

**Skill:** `requirement-to-tlaplus-property-generator`

**Input:**
- Natural language requirements
- The TLA+ specification from Step 1

**Action:**
```
Use the requirement-to-tlaplus-property-generator skill with your requirements.
```

**Output:**
- Formal TLA+ properties
- Safety and liveness properties

**Example:**
```
Requirement: "The counter value should never be negative"

TLA+ Property:
SafetyProperty == value >= 0

Requirement: "The counter should eventually reach 10"

TLA+ Property:
LivenessProperty == <>(value = 10)
```

### Step 3: Model Checking (External Tool)

**Goal:** Verify that your specification satisfies the properties.

**Tool:** TLC (TLA+ model checker) or nuXmv

**Action:**
```bash
# Using TLC
tlc Counter.tla -config Counter.cfg

# Or using nuXmv (if using SMV model)
nuXmv -int model.smv
```

**Possible Outcomes:**

#### ✅ No Violations Found
Congratulations! Your code satisfies all properties. You're done!

#### ❌ Counterexample Found
The model checker found a violation. Proceed to Step 4.

### Step 4: Analyze Counterexample

**Goal:** Understand why the property was violated.

**Skill:** Built into `model-guided-code-repair`

**Input:**
- The counterexample trace from the model checker
- Your original code
- The violated property

**Action:**
```
The model-guided-code-repair skill will automatically analyze the counterexample.
```

**Output:**
- Root cause analysis
- Execution trace showing the violation
- Suggested repair strategy

**Example Counterexample:**
```
State 1: value = 0
State 2: value = 1
State 3: value = 2
State 4: value = -1  ← Violation! (concurrent decrement not in spec)
```

### Step 5: Repair Code

**Goal:** Fix the code to satisfy the violated property.

**Skill:** `model-guided-code-repair` or `tlaplus-guided-code-repair`

**Input:**
- Original code
- Violated property
- Counterexample

**Action:**
```
Use the model-guided-code-repair skill to automatically generate a fix.
```

**Output:**
- Repaired code
- Explanation of changes
- Validation results

**Example:**
```python
# Original (buggy) code
def increment(self):
    temp = self.value
    # Bug: race condition here
    self.value = temp + 1

# Repaired code
def increment(self):
    with self.lock:  # Added synchronization
        self.value += 1
```

### Step 6: Generate Regression Tests

**Goal:** Create tests to prevent the bug from reoccurring.

**Skill:** `counterexample-to-test-generator`

**Input:**
- The counterexample from Step 4
- Your programming language/test framework

**Action:**
```
Use the counterexample-to-test-generator skill to create test cases.
```

**Output:**
- Executable test cases
- Test that reproduces the original bug
- Test that verifies the fix

**Example:**
```python
def test_concurrent_increment():
    """Test that concurrent increments are safe"""
    counter = Counter()
    threads = [Thread(target=counter.increment) for _ in range(10)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert counter.get() == 10  # Should be exactly 10
```

### Step 7: Re-verify (Loop back to Step 3)

Run the model checker again with the repaired code to ensure:
- The original violation is fixed
- No new violations were introduced

## Example: Concurrent Counter

Let's walk through a complete example.

### Scenario
You have a concurrent counter that multiple threads can increment. You want to verify it's thread-safe.

### Step-by-Step

**1. Generate Specification**
```
Input: Counter class with increment() method
Skill: program-to-tlaplus-spec-generator
Output: TLA+ spec modeling the counter and concurrent operations
```

**2. Define Properties**
```
Requirement: "Counter increments should be atomic"
Skill: requirement-to-tlaplus-property-generator
Output: AtomicIncrement == [](increment => value' = value + 1)
```

**3. Model Check**
```
Tool: TLC
Result: ❌ Counterexample found - race condition detected
```

**4. Analyze & Repair**
```
Skill: model-guided-code-repair
Analysis: Missing synchronization in increment()
Fix: Add lock around increment operation
```

**5. Generate Tests**
```
Skill: counterexample-to-test-generator
Output: Test with 10 concurrent threads incrementing
```

**6. Re-verify**
```
Tool: TLC
Result: ✅ No violations - counter is now thread-safe!
```

## Tips and Best Practices

### 1. Start Simple
- Begin with a small subset of your code
- Verify core functionality first
- Gradually add complexity

### 2. Choose the Right Abstraction Level
- Too detailed: state space explosion
- Too abstract: miss real bugs
- Use `tlaplus-model-reduction` to optimize

### 3. Prioritize Properties
- Safety properties first (something bad never happens)
- Then liveness properties (something good eventually happens)
- Focus on critical properties

### 4. Iterate Quickly
- Don't try to verify everything at once
- Fix one violation at a time
- Re-verify after each fix

### 5. Leverage Invariant Inference
- Use `abstract-invariant-generator` to discover invariants
- Use `invariant-inference` for loop invariants
- These can strengthen your specifications

### 6. Document Assumptions
- Make environmental assumptions explicit
- Document what's verified vs. assumed
- Keep track of verification boundaries

### 7. Combine with Testing
- Use `counterexample-to-test-generator` for every violation
- Build a regression test suite
- Formal verification + testing = high confidence

## Common Patterns

### Pattern 1: Concurrent System
```
1. Model each thread/process
2. Model shared resources
3. Verify mutual exclusion
4. Verify progress (no deadlock)
```

### Pattern 2: Distributed Protocol
```
1. Model each node
2. Model message passing
3. Verify safety (consistency)
4. Verify liveness (termination)
```

### Pattern 3: State Machine
```
1. Extract state machine from code
2. Verify state coverage
3. Verify transition validity
4. Verify reachability
```

## Troubleshooting

### Issue: State Space Too Large
**Solution:** Use `tlaplus-model-reduction` to reduce model complexity

### Issue: Property Too Weak
**Solution:** Use `abstract-invariant-generator` to discover stronger invariants

### Issue: Counterexample Hard to Understand
**Solution:** Use `counterexample-to-test-generator` to create a runnable test

### Issue: Repair Breaks Other Properties
**Solution:** Verify all properties together, not one at a time

## Next Steps

- Try the [Concurrent Counter Example](../examples/concurrent-counter)
- Explore [Distributed Consensus Example](../examples/distributed-consensus)
- Read about [TLA+ Basics](../../../skills/program-to-tlaplus-spec-generator/references/tlaplus_syntax.md)
- Learn [Temporal Logic Patterns](../../../skills/model-guided-code-repair/references/temporal_logic_patterns.md)

## Resources

- [TLA+ Homepage](https://lamport.azurewebsites.net/tla/tla.html)
- [Learn TLA+](https://learntla.com/)
- [TLA+ Examples](https://github.com/tlaplus/Examples)

---

**Need Help?** Open an issue in the main repository or check the FAQ.
