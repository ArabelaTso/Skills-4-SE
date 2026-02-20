# Specification Types Reference

Common specification types and how to interpret counterexamples against them.

## Formal Specifications

### Temporal Logic (LTL/CTL)

**Linear Temporal Logic (LTL):**

Operators:
- `G p` - Globally: p holds at all future states
- `F p` - Finally: p holds at some future state
- `X p` - Next: p holds in the next state
- `p U q` - Until: p holds until q becomes true
- `p → q` - Implies: if p then q

**Examples:**

```
G (request → F grant)
"Every request is eventually granted"

Counterexample: request=true at t=0, grant never becomes true
Violation: Grant never occurs after request
```

```
G (locked → X locked)
"If locked, stays locked in next state"

Counterexample: locked=true at t=3, locked=false at t=4
Violation: Lock was released without proper unlock operation
```

**Computation Tree Logic (CTL):**

Path quantifiers:
- `A` - All paths
- `E` - Exists a path

State formulas:
- `AG p` - p holds on all paths globally
- `EF p` - p holds on some path eventually
- `AF p` - p holds on all paths eventually

**Example:**

```
AG (error → AF recovery)
"From any error state, all paths lead to recovery"

Counterexample: error=true at state S5, path exists where recovery never occurs
Violation: System can get stuck in error state
```

### Invariants

**Definition:** Properties that must hold in all reachable states.

**Types:**

**Safety invariants:**
```
balance >= 0
"Account balance is always non-negative"

Counterexample:
  Initial: balance = 100
  withdraw(150)
  Result: balance = -50
Violation: Withdrawal allowed despite insufficient funds
```

**Type invariants:**
```python
isinstance(user_id, int) and user_id > 0
"User ID is always a positive integer"

Counterexample:
  user_id = -5
Violation: Negative user ID assigned
```

**Relationship invariants:**
```
len(active_users) <= max_capacity
"Active users never exceed capacity"

Counterexample:
  max_capacity = 100
  active_users has 101 elements
Violation: User added when already at capacity
```

### Pre/Postconditions

**Preconditions:** Must hold before function execution

```python
@requires(len(array) > 0)
def get_first(array):
    return array[0]

Counterexample:
  Input: array = []
  Result: IndexError
Violation: Precondition violated - empty array passed
```

**Postconditions:** Must hold after function execution

```python
@ensures(lambda result: result >= 0)
def absolute_value(x):
    return x  # BUG: should be abs(x)

Counterexample:
  Input: x = -5
  Output: -5
Violation: Postcondition failed - result is negative
```

## Informal Requirements

### User Stories

```
As a user, I want to reset my password so that I can regain access to my account.

Acceptance Criteria:
- Password reset link expires after 24 hours
- User receives email with reset link
- New password must be different from old password

Counterexample:
  Scenario: User clicks reset link after 25 hours
  Expected: Link expired error
  Actual: Password reset allowed
Violation: Expiration time not enforced
```

### Functional Requirements

```
REQ-001: System shall log all failed login attempts

Counterexample:
  Action: Failed login with wrong password
  Expected: Entry in audit log
  Actual: No log entry created
Violation: Failed login not logged
```

## Test Specifications

### Assertion Failures

```python
def test_sort_ascending():
    result = sort([3, 1, 2])
    assert result == [1, 2, 3]

Counterexample:
  Input: [3, 1, 2]
  Expected: [1, 2, 3]
  Actual: [3, 2, 1]  # Sorted descending instead
Violation: Elements not in ascending order
```

### Property-Based Tests

```python
@given(st.integers())
def test_reverse_twice_is_identity(lst):
    assert reverse(reverse(lst)) == lst

Counterexample:
  Input: lst = [1, 2, 3]
  reverse(lst) = [3, 2, 1]
  reverse(reverse(lst)) = [1, 3, 2]  # BUG in implementation
Violation: Double reversal doesn't restore original
```

## Code Contracts

### Type Constraints

```python
def add_user(name: str, age: int) -> User:
    pass

Counterexample:
  Input: name = "Alice", age = "25"  # String instead of int
  Error: TypeError
Violation: Type constraint violated - age must be int
```

### API Contracts

```
POST /api/users
Contract:
  - Must include "email" field
  - Email must be valid format
  - Returns 201 on success

Counterexample:
  Request: {"name": "Alice"}  # Missing email
  Expected: 400 Bad Request
  Actual: 500 Internal Server Error
Violation: Contract not enforced - missing field causes crash
```

### Algebraic Properties

**Commutativity:**
```
add(a, b) == add(b, a)

Counterexample:
  add(2, 3) = 5
  add(3, 2) = 6  # BUG: order matters
Violation: Addition is not commutative
```

**Associativity:**
```
concat(concat(a, b), c) == concat(a, concat(b, c))

Counterexample:
  concat(concat([1], [2]), [3]) = [1, 2, 3]
  concat([1], concat([2], [3])) = [1, [2, 3]]  # BUG: nested list
Violation: Concatenation is not associative
```

**Idempotence:**
```
delete(delete(x)) == delete(x)

Counterexample:
  delete(item) succeeds
  delete(item) raises ItemNotFoundError
Violation: Delete operation is not idempotent
```

## State Machine Specifications

```
States: [IDLE, RUNNING, PAUSED, STOPPED]
Transitions:
  IDLE → RUNNING (on start)
  RUNNING → PAUSED (on pause)
  PAUSED → RUNNING (on resume)
  RUNNING → STOPPED (on stop)

Invariant: Cannot go from STOPPED back to RUNNING

Counterexample:
  State sequence: IDLE → RUNNING → STOPPED → RUNNING
  Transition: STOPPED → RUNNING
Violation: Illegal state transition occurred
```

## Concurrency Specifications

### Race Conditions

```
Specification: balance updates are atomic

Counterexample:
  Thread 1: Read balance=100, add 50, write 150
  Thread 2: Read balance=100, add 30, write 130
  Final: balance=130 (should be 180)
Violation: Lost update - operations not atomic
```

### Deadlock Freedom

```
Specification: System never deadlocks

Counterexample:
  Thread 1: Holds lock A, waits for lock B
  Thread 2: Holds lock B, waits for lock A
  Result: Deadlock
Violation: Circular wait condition exists
```

### Linearizability

```
Specification: Concurrent operations appear sequential

Counterexample:
  Thread 1: enqueue(1) starts at t=0
  Thread 2: dequeue() returns null at t=1
  Thread 1: enqueue(1) completes at t=2

Violation: Dequeue returned empty while enqueue was in progress
```

## Security Specifications

### Access Control

```
Specification: Users can only access their own data

Counterexample:
  User A (id=1) requests /api/users/2/profile
  Expected: 403 Forbidden
  Actual: 200 OK with User B's data
Violation: Authorization check missing
```

### Data Integrity

```
Specification: Passwords must be hashed

Counterexample:
  User password: "secret123"
  Database: password column contains "secret123"
Violation: Password stored in plain text
```

## Performance Specifications

### Time Complexity

```
Specification: Search must be O(log n)

Counterexample:
  Input: Sorted array of 1000 elements
  Expected: ~10 comparisons (log₂ 1000)
  Actual: 500 comparisons (linear search used)
Violation: Algorithm is O(n) not O(log n)
```

### Resource Bounds

```
Specification: Memory usage must not exceed 1GB

Counterexample:
  Input: Process 10,000 records
  Memory: 2.5GB allocated
Violation: Memory limit exceeded
```

## Common Violation Patterns

### Boundary Violations

```
Specification: 0 ≤ index < length

Counterexample: index = -1 or index = length
Violation: Out of bounds access
```

### Off-by-One Errors

```
Specification: Loop processes all elements

Counterexample:
  Array: [1, 2, 3]
  for i in range(len(arr) - 1):  # BUG: should be range(len(arr))
  Processed: [1, 2]
Violation: Last element skipped
```

### Null/None Violations

```
Specification: Result is never null

Counterexample:
  Input: Empty list
  Result: None
Violation: Null returned for edge case
```

### Integer Overflow

```
Specification: Result fits in 32-bit integer

Counterexample:
  a = 2^31 - 1 (max int32)
  b = 1
  a + b = -2^31 (overflow wraps to negative)
Violation: Integer overflow not checked
```
