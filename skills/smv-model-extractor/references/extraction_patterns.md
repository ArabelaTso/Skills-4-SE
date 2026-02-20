# Extraction Patterns and Best Practices

Guidelines for extracting effective SMV models from source code.

## Abstraction Strategies

### Medium Abstraction (Recommended)

Balance between detail and tractability:

**Data abstraction:**
- Boolean variables → keep as boolean
- Integer counters → bound to small range (e.g., 0..3)
- Pointers/references → abstract to null/valid
- Arrays → abstract to size or key properties
- Strings → abstract to empty/non-empty or length categories

**Control flow:**
- Preserve branching structure (if/else)
- Preserve loop structure (while/for)
- Merge sequential statements without branches
- Keep function call boundaries

**Example:**
```c
// Original C code
int buffer[100];
int count = 0;

void add_item(int item) {
    if (count < 100) {
        buffer[count] = item;
        count++;
    }
}
```

```smv
-- Abstracted SMV model
VAR
  count : 0..3;  -- bounded counter
  buffer_full : boolean;

ASSIGN
  init(count) := 0;
  init(buffer_full) := FALSE;

  next(count) := case
    !buffer_full & count < 3 : count + 1;
    TRUE : count;
  esac;

  next(buffer_full) := (count = 3);
```

## Protocol Implementation Patterns

### Pattern 1: Client-Server Protocol

**Source characteristics:**
- State machine with connection states
- Request/response cycles
- Timeout handling

**Extraction approach:**
1. Identify protocol states (disconnected, connecting, connected, etc.)
2. Extract state transitions based on events
3. Abstract message contents to types
4. Model timeouts as non-deterministic events

**Example mapping:**
```
Program State          → SMV State
--------------           ----------
DISCONNECTED          → disconnected
CONNECTING            → connecting
CONNECTED             → connected
DISCONNECTING         → disconnecting

Events                → Transitions
------                   -----------
connect()             → disconnected -> connecting
on_connect_success()  → connecting -> connected
on_connect_fail()     → connecting -> disconnected
disconnect()          → connected -> disconnecting
```

### Pattern 2: Mutual Exclusion Protocol

**Source characteristics:**
- Shared resources
- Lock/unlock operations
- Critical sections

**Extraction approach:**
1. Identify critical sections
2. Track lock states
3. Model each process/thread as separate state
4. Verify mutual exclusion property

**SMV pattern:**
```smv
VAR
  process1 : {idle, trying, critical};
  process2 : {idle, trying, critical};
  lock : boolean;

ASSIGN
  init(lock) := FALSE;

  next(process1) := case
    process1 = idle : {idle, trying};
    process1 = trying & !lock : critical;
    process1 = critical : idle;
    TRUE : process1;
  esac;

-- Mutual exclusion property
SPEC AG !(process1 = critical & process2 = critical)
```

### Pattern 3: Producer-Consumer

**Source characteristics:**
- Buffer management
- Producer adds items
- Consumer removes items
- Synchronization

**Extraction approach:**
1. Abstract buffer to count or full/empty flags
2. Model producer and consumer states
3. Track buffer occupancy
4. Verify no overflow/underflow

### Pattern 4: State Machine Protocol

**Source characteristics:**
- Explicit state variable
- Switch/case or if-else chains
- State transitions based on inputs

**Extraction approach:**
1. Direct mapping of states
2. Extract transition conditions
3. Identify inputs that trigger transitions
4. Model as SMV case statement

## Common Pitfalls and Solutions

### Pitfall 1: State Explosion

**Problem:** Too many variables or large domains cause state explosion.

**Solutions:**
- Increase abstraction level
- Bound integer ranges tightly
- Use symmetry reduction
- Focus on specific functions/modules

### Pitfall 2: Over-Abstraction

**Problem:** Model is too abstract to verify meaningful properties.

**Solutions:**
- Keep variables relevant to properties of interest
- Preserve control flow structure
- Don't merge states that affect verification
- Use medium abstraction as starting point

### Pitfall 3: Missing Transitions

**Problem:** Incomplete transition coverage leads to deadlocks in model.

**Solutions:**
- Always include default case: `TRUE : state;`
- Check for all possible conditions
- Handle error/exception paths
- Model external events as non-deterministic

### Pitfall 4: Incorrect Initial States

**Problem:** Model starts in unreachable or invalid state.

**Solutions:**
- Carefully analyze program initialization
- Set realistic initial values
- Consider multiple entry points
- Verify initial state is reachable

## Variable Selection Heuristics

### Automatically Track These Variables:

1. **State variables** - explicit state enums or flags
2. **Counters** - loop counters, buffer sizes, retry counts
3. **Flags** - boolean conditions used in branches
4. **Lock variables** - mutexes, semaphores
5. **Status codes** - return values, error codes

### Usually Ignore These Variables:

1. **Temporary variables** - used only within single function
2. **Constants** - don't change during execution
3. **Derived values** - can be computed from other variables
4. **Performance metrics** - timing, profiling data
5. **Debug information** - logging, trace data

## Verification Properties

### Safety Properties (AG)

Things that should never happen:
```smv
-- No buffer overflow
SPEC AG (count <= MAX_SIZE)

-- No null pointer dereference
SPEC AG (ptr != null | !accessing_ptr)

-- Mutual exclusion
SPEC AG !(proc1_critical & proc2_critical)
```

### Liveness Properties (AF)

Things that should eventually happen:
```smv
-- Request eventually granted
SPEC AG (request -> AF grant)

-- Process eventually terminates
SPEC AF (state = terminated)

-- Deadlock freedom
SPEC AG EF (state = idle)
```

### Response Properties

Stimulus-response patterns:
```smv
-- Every request gets response
SPEC AG (request -> AF response)

-- Bounded response time (abstract)
SPEC AG (request -> AX (response | AX response))
```

## Tips for Protocol Implementations

1. **Identify protocol phases** - handshake, data transfer, teardown
2. **Model timeouts** - use non-deterministic transitions
3. **Abstract message contents** - focus on message types, not data
4. **Track sequence numbers** - bound to small range (0..3)
5. **Model retransmissions** - as state transitions
6. **Consider error conditions** - network failures, invalid messages
7. **Verify protocol properties** - ordering, completeness, no deadlock
