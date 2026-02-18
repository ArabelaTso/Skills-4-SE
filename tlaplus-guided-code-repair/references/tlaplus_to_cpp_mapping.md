# Mapping TLA+ to C/C++ Code

This guide explains how to map TLA+ specifications and counterexamples to C/C++ program constructs.

## State Variable Mapping

### TLA+ Variables → C/C++ Constructs

| TLA+ Construct | C/C++ Equivalent | Example |
|----------------|------------------|---------|
| Simple variable | Global/member variable | `int balance` |
| Record | Struct/class | `struct Account { int id; int balance; }` |
| Set | `std::set`, `std::unordered_set` | `std::set<int> active_threads` |
| Sequence | `std::vector`, `std::deque` | `std::vector<Request> queue` |
| Function [domain -> range] | `std::map`, `std::unordered_map` | `std::map<int, Account> accounts` |
| Boolean | `bool` | `bool is_locked` |

### Example Mapping

**TLA+ Specification:**
```tla
VARIABLES
    balance,        \* Account balance
    pending,        \* Set of pending transactions
    history         \* Sequence of completed transactions
```

**C++ Code:**
```cpp
class BankAccount {
    int balance;                              // balance
    std::set<int> pending;                    // pending
    std::vector<Transaction> history;         // history
};
```

## Action Mapping

### TLA+ Actions → C/C++ Functions

TLA+ actions describe state transitions. Each action typically maps to a function or method.

**TLA+ Action:**
```tla
Withdraw(amount) ==
    /\ amount <= balance
    /\ balance' = balance - amount
    /\ UNCHANGED <<pending, history>>
```

**C++ Function:**
```cpp
bool withdraw(int amount) {
    if (amount > balance) return false;  // Precondition check
    balance -= amount;                   // State update
    // pending and history unchanged
    return true;
}
```

## Counterexample Trace Analysis

### Understanding TLC Trace Format

A typical TLC counterexample looks like:

```
Error: Invariant BalanceNonNegative is violated.

State 1: <Initial predicate>
/\ balance = 100
/\ pending = {}
/\ history = <<>>

State 2: <Withdraw line 45, col 12 to line 48, col 35>
/\ balance = 50
/\ pending = {}
/\ history = <<>>

State 3: <Withdraw line 45, col 12 to line 48, col 35>
/\ balance = -50
/\ pending = {}
/\ history = <<>>
```

### Trace Analysis Steps

1. **Identify the violation point**: State 3 shows `balance = -50`, violating the invariant

2. **Identify the action**: The action `Withdraw` (line 45-48) led to the violation

3. **Analyze the transition**:
   - State 2 → State 3: balance changed from 50 to -50
   - This means `Withdraw(100)` was called when balance was 50

4. **Find the C++ code**: Look for the `withdraw()` function around line 45-48 in the implementation

5. **Identify the bug**: The precondition check `amount <= balance` is missing or incorrect

### Mapping States to Program Execution

| TLA+ State | Program State | How to Find |
|------------|---------------|-------------|
| Initial state | Program startup, constructor | Look at initialization code |
| Intermediate states | After function calls | Trace function call sequence |
| Error state | When invariant violated | The bug location |

## Common Patterns

### Pattern 1: Concurrent Actions → Thread Functions

**TLA+ Spec:**
```tla
Process(i) ==
    /\ pc[i] = "start"
    /\ counter' = counter + 1
    /\ pc' = [pc EXCEPT ![i] = "done"]
```

**C++ Code:**
```cpp
void thread_function(int i) {
    // pc[i] = "start" is implicit (thread starts)
    counter++;  // counter' = counter + 1
    // pc[i] = "done" is implicit (thread ends)
}
```

### Pattern 2: Guarded Actions → Conditional Execution

**TLA+ Spec:**
```tla
Dequeue ==
    /\ queue # <<>>           \* Guard: queue not empty
    /\ queue' = Tail(queue)
    /\ result' = Head(queue)
```

**C++ Code:**
```cpp
bool dequeue(int& result) {
    if (queue.empty()) return false;  // Guard check
    result = queue.front();           // result' = Head(queue)
    queue.pop_front();                // queue' = Tail(queue)
    return true;
}
```

### Pattern 3: Atomic Actions → Critical Sections

**TLA+ Spec:**
```tla
Transfer(from, to, amount) ==
    /\ accounts[from] >= amount
    /\ accounts' = [accounts EXCEPT
                     ![from] = @ - amount,
                     ![to] = @ + amount]
```

**C++ Code:**
```cpp
bool transfer(int from, int to, int amount) {
    std::lock_guard<std::mutex> lock(mutex);  // Atomic action
    if (accounts[from] < amount) return false;
    accounts[from] -= amount;
    accounts[to] += amount;
    return true;
}
```

## Identifying Bug Locations

### Strategy 1: Line Number Mapping

If TLC reports `<Action line 45, col 12>`, look for:
1. The TLA+ action definition at that line
2. The corresponding C++ function (often same name)
3. The specific state update that caused the violation

### Strategy 2: Variable Change Analysis

Compare consecutive states in the trace:
- Which variables changed?
- What was the change? (increment, decrement, set to value)
- Which action could cause this change?

### Strategy 3: Precondition Analysis

For invariant violations:
1. Identify what invariant was violated
2. Look at the action that led to the violation
3. Check if the action's precondition is sufficient
4. The bug is often a missing or incorrect precondition check

## Example: Complete Mapping

**TLA+ Specification:**
```tla
VARIABLES balance, lock_held

Init == balance = 0 /\ lock_held = FALSE

Deposit(amount) ==
    /\ ~lock_held
    /\ lock_held' = TRUE
    /\ balance' = balance + amount
    /\ lock_held' = FALSE

TypeInvariant == balance >= 0
```

**Counterexample:**
```
State 1: balance = 0, lock_held = FALSE
State 2: balance = -100, lock_held = FALSE  [Invariant violated]
```

**C++ Code (buggy):**
```cpp
class Account {
    int balance = 0;
    std::mutex mtx;

    void deposit(int amount) {
        // BUG: No lock, and amount can be negative!
        balance += amount;
    }
};
```

**Analysis:**
- Violation: `balance = -100` violates `balance >= 0`
- Cause: `deposit(-100)` was called (amount should be positive)
- Missing checks:
  1. No precondition `amount > 0`
  2. No lock protection (though not shown in this trace)

**Repaired Code:**
```cpp
class Account {
    int balance = 0;
    std::mutex mtx;

    bool deposit(int amount) {
        if (amount <= 0) return false;  // Precondition check
        std::lock_guard<std::mutex> lock(mtx);  // Synchronization
        balance += amount;
        return true;
    }
};
```

## Tips for Effective Mapping

1. **Keep naming consistent**: Use same names in TLA+ and C++ when possible
2. **Document the mapping**: Add comments linking C++ code to TLA+ actions
3. **Preserve structure**: If TLA+ has multiple actions, have corresponding functions
4. **Match granularity**: TLA+ atomic actions should be C++ critical sections
5. **Validate assumptions**: TLA+ guards should be C++ precondition checks
