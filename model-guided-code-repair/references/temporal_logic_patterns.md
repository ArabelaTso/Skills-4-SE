# Temporal Logic Patterns and Repair Strategies

## LTL (Linear Temporal Logic) Operators

### Basic Operators

- **G φ** (Globally): φ holds at all future states
  - Example: `G(x > 0)` - x is always positive

- **F φ** (Finally/Eventually): φ holds at some future state
  - Example: `F(done == true)` - eventually done becomes true

- **X φ** (Next): φ holds in the next state
  - Example: `X(state == READY)` - next state is READY

- **φ U ψ** (Until): φ holds until ψ becomes true
  - Example: `(waiting) U (granted)` - waiting until granted

### Common LTL Patterns

**Safety Properties** (something bad never happens):
- `G(!error)` - never enter error state
- `G(request -> F(response))` - every request gets a response
- `G(locked -> !access)` - no access when locked

**Liveness Properties** (something good eventually happens):
- `G(request -> F(grant))` - every request eventually granted
- `GF(checkpoint)` - infinitely often reach checkpoint
- `FG(stable)` - eventually always stable

**Response Properties**:
- `G(p -> F(q))` - p always eventually followed by q
- `G(p -> X(q))` - p always immediately followed by q

## CTL (Computation Tree Logic) Operators

### Path Quantifiers

- **A** (All paths): property holds on all paths
- **E** (Exists path): property holds on at least one path

### Temporal Operators

- **G φ**: globally φ
- **F φ**: eventually φ
- **X φ**: next φ
- **φ U ψ**: φ until ψ

### Common CTL Patterns

- `AG(φ)` - φ holds on all paths globally
- `EF(φ)` - there exists a path where φ eventually holds
- `AG(p -> EF(q))` - whenever p, there's a path to q
- `EG(φ)` - there exists a path where φ always holds

## Common Violation Patterns and Repairs

### Pattern 1: Missing Guard Condition

**Violation**: Safety property violated due to missing precondition check

**Counterexample**: Direct transition to error state without validation

**Repair Strategy**:
```
// Before
void process(int x) {
    result = 100 / x;  // Violation: division by zero possible
}

// After
void process(int x) {
    if (x == 0) return;  // Added guard
    result = 100 / x;
}
```

### Pattern 2: Incorrect Ordering

**Violation**: Operations executed in wrong sequence

**Counterexample**: Resource used before initialization

**Repair Strategy**:
```
// Before
void setup() {
    use_resource();      // Violation: used before init
    init_resource();
}

// After
void setup() {
    init_resource();     // Reordered
    use_resource();
}
```

### Pattern 3: Missing Synchronization

**Violation**: Race condition in concurrent access

**Counterexample**: Two threads modify shared variable simultaneously

**Repair Strategy**:
```
// Before
void increment() {
    counter++;  // Violation: race condition
}

// After
void increment() {
    lock.acquire();      // Added synchronization
    counter++;
    lock.release();
}
```

### Pattern 4: Missing State Update

**Violation**: State variable not updated correctly

**Counterexample**: State remains in old value after transition

**Repair Strategy**:
```
// Before
void transition() {
    perform_action();
    // Violation: forgot to update state
}

// After
void transition() {
    perform_action();
    state = NEXT_STATE;  // Added state update
}
```

### Pattern 5: Deadlock

**Violation**: Liveness property violated due to circular wait

**Counterexample**: Thread A waits for B, B waits for A

**Repair Strategy**:
```
// Before
Thread A: lock(L1); lock(L2);
Thread B: lock(L2); lock(L1);  // Violation: deadlock

// After (consistent lock ordering)
Thread A: lock(L1); lock(L2);
Thread B: lock(L1); lock(L2);  // Fixed ordering
```

### Pattern 6: Infinite Loop

**Violation**: Liveness property violated due to non-terminating loop

**Counterexample**: Loop condition never becomes false

**Repair Strategy**:
```
// Before
while (waiting) {
    check_status();
    // Violation: waiting never set to false
}

// After
while (waiting) {
    if (check_status()) {
        waiting = false;  // Added exit condition
    }
}
```

## Repair Heuristics

### Minimality Principles

1. **Single point of change**: Prefer repairs that modify one location
2. **Smallest scope**: Change the narrowest scope possible (expression < statement < function)
3. **Preserve structure**: Keep original control flow when possible
4. **No refactoring**: Don't restructure code beyond what's needed

### Semantic Justification

1. **Direct causality**: Repair should directly address the root cause
2. **No side effects**: Avoid changes that affect unrelated behavior
3. **Maintain invariants**: Preserve existing program invariants
4. **Type safety**: Ensure repairs are type-correct

### Validation Strategies

**For Safety Properties**:
- Add assertions at violation points
- Generate test cases covering the counterexample path
- Re-run model checker with same property

**For Liveness Properties**:
- Add progress monitors or timeouts
- Check for deadlock freedom
- Verify fairness assumptions

**For Concurrent Systems**:
- Use thread sanitizers (TSan)
- Run stress tests with multiple threads
- Verify with model checker supporting concurrency

## Tool-Specific Counterexample Formats

### SPIN Counterexample

```
State 1: [line 10] x = 0
State 2: [line 15] y = 5
State 3: [line 20] z = y/x  <- violation
```

**Translation**: Execution reaches line 20 with x=0, causing division by zero

### NuSMV Counterexample

```
-> State 1.1 <-
  state = INIT
-> State 1.2 <-
  state = PROCESSING
-> State 1.3 <-
  state = ERROR  <- violation of AG(!ERROR)
```

**Translation**: System transitions from INIT to PROCESSING to ERROR, violating "never ERROR"

### CBMC Counterexample

```
[main.c:25] x = 10
[main.c:30] y = x - 10
[main.c:35] assert(y > 0) FAILED
```

**Translation**: Assertion fails when x=10 leads to y=0
