# TLA+ Property Violations and Repair Patterns

This reference guide documents common TLA+ property violations and corresponding repair strategies for C/C++ code.

## Common Violation Types

### 1. Invariant Violations

**What it means**: A safety property that should hold in all reachable states is violated.

**Common causes in C/C++ code**:
- Missing bounds checks
- Incorrect state transitions
- Race conditions in concurrent code
- Integer overflow/underflow
- Uninitialized variables

**Repair strategies**:
- Add guards/preconditions before state changes
- Add bounds checking
- Use atomic operations or locks for shared state
- Initialize variables properly
- Add assertions to catch violations early

**Example**:
```
TLA+ Invariant: balance >= 0
Violation: balance = -100 in some state
C++ Cause: withdraw() doesn't check if amount > balance
Repair: Add check: if (amount > balance) return false;
```

### 2. Deadlock Violations

**What it means**: The system reaches a state where no actions are enabled (stuck state).

**Common causes in C/C++ code**:
- Circular lock dependencies
- Missing unlock operations
- Waiting for conditions that never become true
- Resource exhaustion

**Repair strategies**:
- Establish lock ordering discipline
- Use RAII (lock_guard, unique_lock) to ensure unlocking
- Add timeout mechanisms
- Ensure all code paths release resources

**Example**:
```
TLA+ Deadlock: Thread1 holds lockA, waits for lockB; Thread2 holds lockB, waits for lockA
C++ Cause: Inconsistent lock acquisition order
Repair: Always acquire locks in same order (e.g., always lockA before lockB)
```

### 3. Temporal Property Violations (Liveness)

**What it means**: Something that should eventually happen never occurs.

**Common causes in C/C++ code**:
- Infinite loops without progress
- Starvation (some threads never get scheduled)
- Missing notifications (condition variables)
- Priority inversion

**Repair strategies**:
- Add fairness mechanisms
- Use condition variables with proper notifications
- Implement timeout and retry logic
- Ensure progress in loops

**Example**:
```
TLA+ Property: <>[] (request => <> response)  // Every request eventually gets response
Violation: Request sent but response never arrives
C++ Cause: Missing notify_all() after processing request
Repair: Add cv.notify_all() after setting response
```

## Mapping TLA+ States to Program States

### State Variables

TLA+ state variables typically map to:
- **Global variables** in the program
- **Object fields/members** in classes
- **Shared memory** in concurrent programs
- **File/database state** in I/O operations

### Actions

TLA+ actions map to:
- **Functions/methods** that modify state
- **Critical sections** protected by locks
- **Transactions** in database operations
- **Message handlers** in distributed systems

### Trace Analysis

When analyzing a counterexample trace:

1. **Identify the violated state**: Look at the final state where the invariant fails
2. **Work backwards**: Trace which action led to this state
3. **Find the program location**: Map the TLA+ action to the corresponding C/C++ function
4. **Analyze the transition**: Understand what values changed and why
5. **Identify the root cause**: Determine what condition was missing or incorrect

## Repair Principles

### Minimality

- Make the smallest change that fixes the violation
- Don't add unnecessary complexity
- Preserve existing functionality

### Semantic Justification

Every repair should have a clear reason:
- "This check ensures the invariant X holds"
- "This lock prevents the race condition on variable Y"
- "This initialization prevents undefined behavior"

### Verification

After repair:
1. Re-run TLC to verify the property now holds
2. Run existing tests to ensure no regressions
3. Add new tests that exercise the repaired code path

## Common Repair Patterns

### Pattern 1: Add Precondition Check

```cpp
// Before (violates invariant)
void withdraw(int amount) {
    balance -= amount;  // Can make balance negative
}

// After (enforces invariant: balance >= 0)
bool withdraw(int amount) {
    if (amount > balance) return false;  // Precondition check
    balance -= amount;
    return true;
}
```

### Pattern 2: Add Synchronization

```cpp
// Before (race condition)
void increment() {
    counter++;  // Not atomic
}

// After (thread-safe)
void increment() {
    std::lock_guard<std::mutex> lock(mtx);
    counter++;
}
```

### Pattern 3: Fix Lock Ordering

```cpp
// Before (potential deadlock)
void transfer(Account& from, Account& to, int amount) {
    std::lock_guard<std::mutex> lock1(from.mutex);
    std::lock_guard<std::mutex> lock2(to.mutex);
    from.balance -= amount;
    to.balance += amount;
}

// After (consistent ordering prevents deadlock)
void transfer(Account& from, Account& to, int amount) {
    // Always lock in consistent order based on address
    Account* first = &from < &to ? &from : &to;
    Account* second = &from < &to ? &to : &from;
    std::lock_guard<std::mutex> lock1(first->mutex);
    std::lock_guard<std::mutex> lock2(second->mutex);
    from.balance -= amount;
    to.balance += amount;
}
```

### Pattern 4: Add Missing Notification

```cpp
// Before (threads may wait forever)
void producer() {
    std::lock_guard<std::mutex> lock(mtx);
    queue.push(item);
    // Missing notification!
}

// After (proper signaling)
void producer() {
    std::lock_guard<std::mutex> lock(mtx);
    queue.push(item);
    cv.notify_one();  // Wake up waiting consumer
}
```

### Pattern 5: Initialize Variables

```cpp
// Before (undefined behavior)
class Counter {
    int count;  // Uninitialized
public:
    void increment() { count++; }
};

// After (well-defined)
class Counter {
    int count = 0;  // Initialized
public:
    void increment() { count++; }
};
```

## Validation Checklist

After generating a repair:

- [ ] Does the repair address the root cause identified in the trace?
- [ ] Is the repair minimal (no unnecessary changes)?
- [ ] Does the repair have semantic justification?
- [ ] Will TLC pass with this repair?
- [ ] Are there any potential side effects or regressions?
- [ ] Should new tests be added to prevent future violations?
