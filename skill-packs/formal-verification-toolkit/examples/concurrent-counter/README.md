# Concurrent Counter Example

This example demonstrates how to use the Formal Verification Toolkit to verify and fix a concurrent counter implementation.

## 📋 Scenario

You have a simple counter that multiple threads can increment concurrently. The initial implementation has a race condition that causes lost updates.

## 🎯 Learning Objectives

- Generate TLA+ specification from code
- Define temporal properties
- Detect race conditions through model checking
- Automatically repair the code
- Generate regression tests

## 📁 Files

- `counter_buggy.py` - Original implementation with race condition
- `counter_fixed.py` - Repaired implementation
- `counter_spec.tla` - Generated TLA+ specification
- `properties.tla` - Temporal properties to verify
- `test_counter.py` - Generated regression tests
- `README.md` - This file

## 🚀 Step-by-Step Guide

### Step 1: Review the Buggy Code

```python
# counter_buggy.py
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        # Bug: This is not atomic!
        temp = self.value
        # Simulating some work
        temp = temp + 1
        self.value = temp

    def get(self):
        return self.value
```

**Problem:** The increment operation reads, modifies, and writes in separate steps, allowing race conditions.

### Step 2: Generate TLA+ Specification

**Use skill:** `program-to-tlaplus-spec-generator`

**Command:**
```
Generate TLA+ specification from counter_buggy.py
```

**Output:** `counter_spec.tla` (see file)

### Step 3: Define Properties

**Use skill:** `requirement-to-tlaplus-property-generator`

**Requirements:**
1. "The counter should never decrease"
2. "If N threads each increment once, the final value should be N"
3. "Increments should be atomic"

**Output:** `properties.tla` (see file)

### Step 4: Model Check

**Tool:** TLC (TLA+ model checker)

**Command:**
```bash
tlc counter_spec.tla -config counter.cfg
```

**Result:** ❌ Counterexample found!

```
Counterexample trace:
State 1: value = 0, thread1_temp = 0, thread2_temp = 0
State 2: value = 0, thread1_temp = 1, thread2_temp = 0  (thread1 reads)
State 3: value = 0, thread1_temp = 1, thread2_temp = 1  (thread2 reads)
State 4: value = 1, thread1_temp = 1, thread2_temp = 1  (thread1 writes)
State 5: value = 1, thread1_temp = 1, thread2_temp = 1  (thread2 writes)

Expected: value = 2
Actual: value = 1
Violation: Lost update!
```

### Step 5: Repair the Code

**Use skill:** `model-guided-code-repair`

**Input:**
- `counter_buggy.py`
- Counterexample trace
- Violated property

**Command:**
```
Repair counter_buggy.py using the counterexample
```

**Output:** `counter_fixed.py` (see file)

**Repair explanation:**
- Added a lock to ensure atomic increments
- All read-modify-write operations now protected

### Step 6: Generate Tests

**Use skill:** `counterexample-to-test-generator`

**Input:**
- Counterexample trace
- Test framework: pytest

**Command:**
```
Generate test from counterexample for Python/pytest
```

**Output:** `test_counter.py` (see file)

### Step 7: Verify the Fix

**Run the test:**
```bash
pytest test_counter.py -v
```

**Result:** ✅ All tests pass!

**Re-run model checker:**
```bash
tlc counter_fixed_spec.tla -config counter.cfg
```

**Result:** ✅ No violations found!

## 📊 Results

| Metric | Before | After |
|--------|--------|-------|
| Race conditions | 1 | 0 |
| Properties satisfied | 0/3 | 3/3 |
| Test coverage | 0% | 100% |
| Thread-safe | ❌ | ✅ |

## 🎓 Key Takeaways

1. **Formal verification catches subtle bugs** - The race condition might not show up in regular testing
2. **Counterexamples are valuable** - They show exactly how the bug manifests
3. **Automated repair works** - The tool correctly identified the need for synchronization
4. **Tests prevent regression** - Generated tests ensure the bug doesn't come back

## 🔄 Try It Yourself

1. Install the Formal Verification Toolkit
2. Run through each step with the provided files
3. Try modifying the code and see what happens
4. Experiment with different properties

## 📚 Related Examples

- [Distributed Consensus](../distributed-consensus) - More complex concurrent system
- [Mutex Protocol](../mutex-protocol) - Classic synchronization problem

## 💡 Variations to Try

1. **Add a decrement operation** - What properties need to change?
2. **Use atomic operations** - Compare with lock-based approach
3. **Add bounds checking** - Prevent overflow
4. **Multiple counters** - Verify independence

---

**Time to complete:** ~15 minutes
**Difficulty:** Beginner
**Prerequisites:** Basic Python, basic concurrency concepts
