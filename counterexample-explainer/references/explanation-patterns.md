# Explanation Patterns

Effective patterns for explaining why counterexamples violate specifications.

## Step-by-Step Trace Pattern

Show the execution path that leads to violation.

### Template

```markdown
## Counterexample Trace

**Initial State:**
- [Variable1]: [Value]
- [Variable2]: [Value]

**Step 1:** [Action/Event]
- State changes:
  - [Variable1]: [Old Value] → [New Value]
  - [Variable2]: [Old Value] → [New Value]
- **Why this matters:** [Explanation]

**Step 2:** [Action/Event]
- State changes:
  - [Variable]: [Old Value] → [New Value]
- **Violation Point:** [Which specification property is violated]
- **Why it violates:** [Detailed explanation]

**Final State:**
- [Variable1]: [Value]
- [Variable2]: [Value]
- **Status:** ❌ Violates specification
```

### Example: Invariant Violation

```markdown
## Counterexample: Balance Invariant Violation

**Specification:** `balance >= 0` (Account balance must always be non-negative)

### Trace

**Initial State:**
- account.balance: 100
- Status: ✅ Satisfies invariant (100 >= 0)

**Step 1:** User calls `withdraw(150)`
- Withdrawal amount: 150
- Available balance: 100
- **Why this matters:** Withdrawal exceeds available funds

**Step 2:** System processes withdrawal
- State changes:
  - account.balance: 100 → -50
- **Violation Point:** balance becomes negative
- **Why it violates:** balance = -50, which is NOT >= 0

**Final State:**
- account.balance: -50
- Status: ❌ Violates invariant `balance >= 0`

### Root Cause

The `withdraw` method failed to check if the withdrawal amount exceeds the available
balance before deducting funds.

**Missing Check:**
```python
if amount > balance:
    raise InsufficientFundsError()
```
```

## Compare Expected vs Actual Pattern

Side-by-side comparison of what should happen vs what actually happened.

### Template

```markdown
## Specification vs Reality

| Aspect | Expected (Specification) | Actual (Counterexample) | Violation? |
|--------|-------------------------|-------------------------|------------|
| [Property 1] | [Expected value/behavior] | [Actual value/behavior] | ✅/❌ |
| [Property 2] | [Expected value/behavior] | [Actual value/behavior] | ✅/❌ |

**Key Violation:** [Property that failed]

**Why it matters:** [Impact of violation]
```

### Example: Test Assertion Failure

```markdown
## Test Failure Analysis

**Test:** `test_sort_numbers_ascending()`
**Specification:** Sort function should arrange numbers in ascending order

### Expected vs Actual

| Aspect | Expected | Actual | Match? |
|--------|----------|--------|--------|
| Input | [3, 1, 4, 1, 5] | [3, 1, 4, 1, 5] | ✅ |
| Output | [1, 1, 3, 4, 5] | [5, 4, 3, 1, 1] | ❌ |
| Order | Ascending | Descending | ❌ |
| Length | 5 | 5 | ✅ |
| Elements | Same elements | Same elements | ✅ |

**Key Violation:** Output order is descending instead of ascending

**Root Cause:**
The sort function uses `>` instead of `<` in comparison:
```python
# Actual (wrong)
if arr[i] > arr[j]:  # Should be <

# Expected (correct)
if arr[i] < arr[j]:
```

**Impact:** All sorted outputs are reversed, making the function produce
descending order instead of the specified ascending order.
```

## State Diagram Pattern

Visual representation of state transitions showing where violation occurs.

### Template

```markdown
## State Transition Analysis

```
[State A] --event--> [State B] --event--> [State C (VIOLATION)]
                                              ↑
                                              Specification says this is illegal
```

**Path Taken:**
1. State A: [Description]
2. → Event: [What happened]
3. State B: [Description]
4. → Event: [What happened]
5. State C: ❌ **ILLEGAL STATE** (Violates: [Specification])

**Why C is illegal:** [Explanation]
```

### Example: State Machine Violation

```markdown
## Invalid State Transition

**Specification:** A stopped task cannot be resumed; it must be restarted.

### State Diagram

```
IDLE --start()--> RUNNING --pause()--> PAUSED --resume()--> RUNNING
                     ↓                                         ↑
                  stop()                                       |
                     ↓                                         |
                  STOPPED --resume()--> (ILLEGAL TRANSITION) --┘
                              ❌
```

**Actual Execution Path:**
1. State: IDLE
2. → Action: start()
3. State: RUNNING ✅
4. → Action: stop()
5. State: STOPPED ✅
6. → Action: resume()
7. State: RUNNING ❌ **ILLEGAL**

**Why this violates the specification:**

The specification explicitly states that once a task is STOPPED, it cannot
be resumed. The only valid transition from STOPPED is:
- STOPPED --restart()--> RUNNING

The counterexample shows a direct transition STOPPED → RUNNING via resume(),
which bypasses the required restart() operation.

**Consequence:** Skipping restart may leave the task in an inconsistent state
with partial cleanup from the previous execution.
```

## Cause and Effect Chain Pattern

Show causal chain from root cause to violation.

### Template

```markdown
## Violation Cause Chain

**Root Cause:**
[Initial problem or bug]
    ↓
**Leads to:**
[Intermediate consequence]
    ↓
**Which causes:**
[Another consequence]
    ↓
**Finally resulting in:**
❌ **Specification Violation:** [What specification is violated]

**Breaking the chain:** [Where to fix to prevent violation]
```

### Example: Concurrency Bug

```markdown
## Race Condition Analysis

**Specification:** Account balance must accurately reflect all transactions

### Cause Chain

**Root Cause:**
Balance update operations are not atomic
```python
# Non-atomic update
balance = get_balance()  # Read
balance += amount        # Modify
set_balance(balance)     # Write
```

    ↓

**Leads to:**
Two threads can read the same initial balance simultaneously

    ↓

**Which causes:**
Both threads compute new balance from the same starting point
- Thread 1: Reads balance=100, computes 100+50=150
- Thread 2: Reads balance=100, computes 100+30=130

    ↓

**Finally resulting in:**
❌ **Lost Update Violation**
- Expected final balance: 180 (100 + 50 + 30)
- Actual final balance: 130 or 150 (whichever writes last)
- **Missing transaction:** One deposit is lost

### Breaking the Chain

Fix at the root cause by making updates atomic:
```python
# Atomic update using lock
with lock:
    balance = get_balance()
    balance += amount
    set_balance(balance)
```
```

## Minimal Counterexample Pattern

Focus on the simplest input that exposes the violation.

### Template

```markdown
## Minimal Counterexample

**Specification:** [Specification statement]

**Simplest Input That Violates:**
```
[Minimal input data]
```

**Why this is minimal:**
- Removing any element → violation disappears
- Simplifying any value → violation disappears

**Execution with minimal input:**
1. [Step]
2. [Step]
3. ❌ Violation occurs: [What goes wrong]

**Generalization:**
This minimal case represents a whole class of violations:
[Pattern description]
```

### Example: Edge Case Bug

```markdown
## Minimal Counterexample: Empty Input Handling

**Specification:** `get_average(numbers)` returns the arithmetic mean

**Simplest Input That Violates:**
```python
numbers = []
```

**Why this is minimal:**
- Cannot simplify further - empty list is the smallest possible input
- Any non-empty list (e.g., [0]) does not trigger this violation

**Execution:**
```python
result = get_average([])
# Expected: Raise ValueError("Cannot compute average of empty list")
# Actual: Returns 0 (incorrect)
# or: Raises ZeroDivisionError (wrong error type)
```

**Why it violates:**
The specification doesn't define average for empty sets (mathematically undefined).
The implementation should reject this input, but instead:
- Returns 0 (nonsensical - 0 is not the average of nothing)
- Or crashes with unhelpful error

**Generalization:**
This represents the broader class of "empty input" bugs:
- Empty lists, strings, arrays
- Zero-length collections
- Null/None values

All require explicit handling when operations assume non-empty input.
```

## Assertion Chain Pattern

Show which assertions hold and which fail.

### Template

```markdown
## Assertion Analysis

**Specification consists of:**
1. ✅/❌ Assertion 1: [Statement]
2. ✅/❌ Assertion 2: [Statement]
3. ✅/❌ Assertion 3: [Statement]

**Violation Details:**

### ❌ Assertion [N]: [Failed assertion]

**Why it fails:**
- Expected: [What should be true]
- Actual: [What is actually true]
- Counterexample value: [Specific value that shows violation]
```

### Example: Postcondition Failure

```markdown
## Postcondition Violation

**Function:** `sort_and_remove_duplicates(array)`

**Specification (Postconditions):**
1. ✅ Result contains all unique elements from input
2. ✅ Result has no duplicate elements
3. ❌ Result is sorted in ascending order
4. ✅ Result length ≤ input length

**Input:** [3, 1, 3, 2, 1]

**Output:** [1, 2, 3]

### Assertion Checks

**✅ Assertion 1: Contains all unique elements**
- Input unique elements: {1, 2, 3}
- Output elements: {1, 2, 3}
- Match: Yes

**✅ Assertion 2: No duplicates**
- Output: [1, 2, 3]
- Has duplicates: No

**❌ Assertion 3: Sorted in ascending order**
- Output: [1, 2, 3]
- Is sorted: Yes
- Order: Ascending
- **Wait, this passes...**

Let me try another input:

**Input:** [5, 2, 5, 1, 3]
**Output:** [5, 3, 2, 1]

**❌ Assertion 3 FAILS:**
- Expected order: [1, 2, 3, 5] (ascending)
- Actual order: [5, 3, 2, 1] (descending)
- Is sorted: No (not in ascending order)

**Root Cause:** The sort implementation uses descending order instead of ascending.
```

## Timeline Pattern

For temporal/sequential specifications, show when things happen.

### Template

```markdown
## Timeline Analysis

```
t=0: [Initial state]
     Spec requires: [What should be true]
     ✅ Status: OK

t=1: [Event/Action]
     State: [New state]
     Spec requires: [What should be true]
     ✅ Status: OK

t=2: [Event/Action]
     State: [New state]
     Spec requires: [What should be true]
     ❌ Status: VIOLATION
```

**Violation at t=2:**
[Detailed explanation]
```

### Example: Temporal Logic Violation

```markdown
## Temporal Property Violation

**Specification (LTL):** `G(request → F grant)`
"Every request is eventually granted"

### Timeline

```
t=0: Initial state
     request = false
     grant = false
     ✅ No pending requests

t=1: User makes request
     request = true
     grant = false
     ℹ️ Request pending - grant must eventually become true

t=2: System processes other requests
     request = true (still pending)
     grant = false
     ⚠️ Request still pending

t=3: System continues
     request = true
     grant = false
     ⚠️ Request still not granted

... [time passes] ...

t=100: Request still pending
       request = true
       grant = false
       ❌ VIOLATION: Grant never occurred

END: System terminates/enters infinite loop
     request = true
     grant = false
```

**Why this violates `G(request → F grant)`:**

At t=1, `request` becomes true. The specification requires that `F grant`
(eventually grant) must hold - meaning at some future time t > 1, grant must
become true.

However, the trace shows grant remains false through t=100 and beyond. The
"eventually" part of the specification is violated because grant never happens.

**Root Cause:** Request is added to queue but never processed:
```python
# Bug: request is queued but process_queue() is never called
queue.append(request)
# Missing: process_queue()
```
```

## Impact Analysis Pattern

Explain consequences of the violation.

### Template

```markdown
## Violation Impact

**What Went Wrong:**
[Description of violation]

**Immediate Impact:**
[Direct consequences]

**Downstream Effects:**
1. [Effect 1]
2. [Effect 2]
3. [Effect 3]

**Worst Case Scenario:**
[Most serious potential consequence]

**Real-World Impact:**
[What this means for users/system]
```

### Example: Security Violation

```markdown
## SQL Injection Vulnerability

**Specification:** All user input must be sanitized before database queries

**What Went Wrong:**
User input directly concatenated into SQL query:
```python
query = f"SELECT * FROM users WHERE username = '{user_input}'"
```

**Violation:** No input sanitization performed

**Immediate Impact:**
Attacker can inject SQL commands:
```python
user_input = "admin' OR '1'='1"
# Resulting query: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
# This returns all users instead of just 'admin'
```

**Downstream Effects:**
1. **Data Breach:** Attacker can read all user records
2. **Data Manipulation:** Attacker can modify/delete data
   ```sql
   user_input = "'; DROP TABLE users; --"
   ```
3. **Privilege Escalation:** Attacker can grant themselves admin rights
4. **Compliance Violation:** GDPR/HIPAA violations due to unauthorized access

**Worst Case Scenario:**
Complete database compromise:
- All user data stolen
- Tables dropped
- Malicious accounts created
- Production system taken offline

**Real-World Impact:**
- Users' personal information exposed
- Financial loss from data breach
- Legal liability and fines
- Reputation damage
- System downtime

**Fix:**
Use parameterized queries:
```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (user_input,))
```
```
