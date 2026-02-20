# Common Requirement Patterns

This document maps common natural-language requirement patterns to TLA+ property definitions.

## Table of Contents

1. [State Invariants](#state-invariants)
2. [Safety Properties](#safety-properties)
3. [Liveness Properties](#liveness-properties)
4. [Ordering Properties](#ordering-properties)
5. [Resource Management](#resource-management)
6. [Concurrency Properties](#concurrency-properties)
7. [Temporal Constraints](#temporal-constraints)

---

## State Invariants

### Pattern: Value Range Constraint

**Requirement**: "Variable X must always be between MIN and MAX"

**TLA+ Property**:
```tla
RangeInvariant == /\ X >= MIN
                  /\ X <= MAX
```

**Alternative**:
```tla
RangeInvariant == X \in MIN..MAX
```

---

### Pattern: Set Membership

**Requirement**: "The status must always be one of: idle, running, or done"

**TLA+ Property**:
```tla
ValidStatus == status \in {"idle", "running", "done"}
```

---

### Pattern: Non-Negative Constraint

**Requirement**: "The counter can never be negative"

**TLA+ Property**:
```tla
NonNegative == counter >= 0
```

**Alternative**:
```tla
NonNegative == counter \in Nat
```

---

## Safety Properties

### Pattern: Mutual Exclusion

**Requirement**: "At most one process can be in the critical section at any time"

**TLA+ Property**:
```tla
MutualExclusion ==
    \A p1, p2 \in Processes :
        (p1 # p2) => ~(pc[p1] = "critical" /\ pc[p2] = "critical")
```

**Alternative (counting)**:
```tla
MutualExclusion ==
    Cardinality({p \in Processes : pc[p] = "critical"}) <= 1
```

---

### Pattern: Buffer Overflow Prevention

**Requirement**: "The buffer must never exceed its capacity"

**TLA+ Property**:
```tla
NoOverflow == Len(buffer) <= CAPACITY
```

---

### Pattern: Resource Bounds

**Requirement**: "The total allocated resources must not exceed the available resources"

**TLA+ Property**:
```tla
ResourceBound ==
    (\A r \in Resources : allocated[r]) <= available
```

---

### Pattern: Deadlock Freedom

**Requirement**: "The system must never deadlock"

**TLA+ Property**:
```tla
NoDeadlock ==
    [](\E p \in Processes : ENABLED Action(p))
```

---

### Pattern: Data Consistency

**Requirement**: "All replicas must have consistent data"

**TLA+ Property**:
```tla
Consistency ==
    \A r1, r2 \in Replicas : data[r1] = data[r2]
```

---

## Liveness Properties

### Pattern: Eventual Completion

**Requirement**: "Every started task eventually completes"

**TLA+ Property**:
```tla
EventualCompletion ==
    \A task \in Tasks :
        (task.status = "started") ~> (task.status = "completed")
```

---

### Pattern: Guaranteed Response

**Requirement**: "Every request eventually receives a response"

**TLA+ Property**:
```tla
GuaranteedResponse ==
    \A req \in Requests :
        (req.sent) ~> (req.responded)
```

---

### Pattern: Termination

**Requirement**: "The algorithm eventually terminates"

**TLA+ Property**:
```tla
Termination == <>(terminated = TRUE)
```

**Alternative (all processes done)**:
```tla
Termination ==
    <>(\A p \in Processes : pc[p] = "done")
```

---

### Pattern: Progress

**Requirement**: "The system makes progress (doesn't get stuck)"

**TLA+ Property**:
```tla
Progress == []<>(state_changed)
```

**Alternative (with fairness)**:
```tla
Progress == WF_vars(Next)
```

---

### Pattern: Eventual Stability

**Requirement**: "The system eventually reaches a stable state and stays there"

**TLA+ Property**:
```tla
EventualStability == <>[](stable)
```

---

## Ordering Properties

### Pattern: Happens-Before

**Requirement**: "Event A must happen before event B"

**TLA+ Property**:
```tla
HappensBefore ==
    [](event_B_occurred => event_A_occurred_before)
```

**With timestamps**:
```tla
HappensBefore ==
    [](event_B.occurred => event_A.timestamp < event_B.timestamp)
```

---

### Pattern: FIFO Ordering

**Requirement**: "Requests are processed in first-in-first-out order"

**TLA+ Property**:
```tla
FIFOOrder ==
    \A req1, req2 \in Requests :
        (req1.arrival_time < req2.arrival_time /\
         req2.status = "completed")
            => (req1.status = "completed")
```

---

### Pattern: Causal Ordering

**Requirement**: "If operation A causally precedes B, A must be applied before B"

**TLA+ Property**:
```tla
CausalOrder ==
    \A a, b \in Operations :
        (CausallyPrecedes(a, b) /\ Applied(b))
            => Applied(a)
```

---

## Resource Management

### Pattern: Resource Acquisition

**Requirement**: "A process can only use a resource if it has acquired it"

**TLA+ Property**:
```tla
ProperAcquisition ==
    \A p \in Processes, r \in Resources :
        (Using(p, r)) => (Holds(p, r))
```

---

### Pattern: No Resource Leaks

**Requirement**: "Every acquired resource is eventually released"

**TLA+ Property**:
```tla
NoLeaks ==
    \A p \in Processes, r \in Resources :
        (Acquired(p, r)) ~> (Released(p, r))
```

---

### Pattern: Bounded Resources

**Requirement**: "At most N processes can hold resource R simultaneously"

**TLA+ Property**:
```tla
BoundedAccess ==
    Cardinality({p \in Processes : Holds(p, R)}) <= N
```

---

## Concurrency Properties

### Pattern: Atomicity

**Requirement**: "Operation X executes atomically (no interleaving)"

**TLA+ Property**:
```tla
Atomicity ==
    [](OperationStarted(X) => <>OperationCompleted(X))
    /\ ~(\E p1, p2 \in Processes :
            p1 # p2 /\ InOperation(p1, X) /\ InOperation(p2, X))
```

---

### Pattern: No Starvation

**Requirement**: "Every waiting process eventually gets access"

**TLA+ Property**:
```tla
NoStarvation ==
    \A p \in Processes :
        (Waiting(p)) ~> (Granted(p))
```

---

### Pattern: Bounded Waiting

**Requirement**: "A waiting process gets access within N steps"

**TLA+ Property**:
```tla
\* Requires auxiliary counter variable
BoundedWaiting ==
    \A p \in Processes :
        [](Waiting(p) => <>(Granted(p) \/ wait_count[p] > N))
```

---

### Pattern: Fair Scheduling

**Requirement**: "All processes get fair access to the CPU"

**TLA+ Property**:
```tla
FairScheduling ==
    \A p \in Processes :
        WF_vars(Schedule(p))
```

---

## Temporal Constraints

### Pattern: Conditional Execution

**Requirement**: "If condition C holds, action A must eventually execute"

**TLA+ Property**:
```tla
ConditionalExecution ==
    [](C => <>A)
```

---

### Pattern: Persistent Condition

**Requirement**: "Once condition C becomes true, it stays true"

**TLA+ Property**:
```tla
Persistent ==
    [](C => []C)
```

**Alternative (stability)**:
```tla
Stable == <>[](C)
```

---

### Pattern: Recurrence

**Requirement**: "Condition C holds infinitely often"

**TLA+ Property**:
```tla
Recurrence == []<>C
```

---

### Pattern: Response Time

**Requirement**: "If event E occurs, response R happens within T time units"

**TLA+ Property**:
```tla
\* Requires clock variable
ResponseTime ==
    \A e \in Events :
        [](e.occurred => <>(e.responded /\ clock - e.time <= T))
```

---

## Complex Patterns

### Pattern: Two-Phase Commit

**Requirement**: "All participants must agree before commit"

**TLA+ Property**:
```tla
TwoPhaseCommit ==
    /\ [](Committed => (\A p \in Participants : Prepared(p)))
    /\ \A p \in Participants : (Prepared(p)) ~> (Committed \/ Aborted)
```

---

### Pattern: Leader Election

**Requirement**: "Eventually exactly one leader is elected"

**TLA+ Property**:
```tla
LeaderElection ==
    /\ <>(\E p \in Processes : IsLeader(p))
    /\ [](\A p1, p2 \in Processes :
            (IsLeader(p1) /\ IsLeader(p2)) => (p1 = p2))
```

---

### Pattern: Consensus

**Requirement**: "All correct processes eventually agree on the same value"

**TLA+ Property**:
```tla
Consensus ==
    /\ <>(\A p \in CorrectProcesses : Decided(p))
    /\ [](\A p1, p2 \in CorrectProcesses :
            (Decided(p1) /\ Decided(p2)) => (decision[p1] = decision[p2]))
```

---

### Pattern: Eventual Consistency

**Requirement**: "After updates stop, all replicas converge to the same state"

**TLA+ Property**:
```tla
EventualConsistency ==
    ([]<>(~UpdateOccurred))
        => <>[](\A r1, r2 \in Replicas : state[r1] = state[r2])
```

---

## Requirement Keywords to TLA+ Mapping

| Requirement Keyword | TLA+ Operator | Example |
|---------------------|---------------|---------|
| "always" | `[]` | `[](x > 0)` |
| "never" | `[]~` | `[]~(deadlock)` |
| "eventually" | `<>` | `<>(terminated)` |
| "until" | `~>` | `P ~> Q` |
| "for all" | `\A` | `\A p \in Processes : ...` |
| "there exists" | `\E` | `\E p \in Processes : ...` |
| "at most one" | Cardinality | `Cardinality(S) <= 1` |
| "exactly one" | Cardinality | `Cardinality(S) = 1` |
| "infinitely often" | `[]<>` | `[]<>(event)` |
| "eventually forever" | `<>[]` | `<>[](stable)` |
| "if...then" | `=>` | `P => Q` |
| "if and only if" | `<=>` | `P <=> Q` |
