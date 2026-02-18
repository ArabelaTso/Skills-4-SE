# TLA+ Temporal Logic Syntax Reference

This document provides a comprehensive reference for TLA+ temporal logic operators and property definitions.

## Table of Contents

1. [Basic Operators](#basic-operators)
2. [Temporal Operators](#temporal-operators)
3. [Action Operators](#action-operators)
4. [Quantifiers](#quantifiers)
5. [Property Types](#property-types)
6. [Common Patterns](#common-patterns)

---

## Basic Operators

### Logical Operators

```tla
/\    \* Conjunction (AND)
\/    \* Disjunction (OR)
~     \* Negation (NOT)
=>    \* Implication
<=>   \* Equivalence (if and only if)
#     \* Not equal
```

### Set Operators

```tla
\in       \* Element of
\notin    \* Not element of
\subseteq \* Subset or equal
\union    \* Set union
\cap      \* Set intersection
\         \* Set difference
```

### Comparison Operators

```tla
=     \* Equal
#     \* Not equal
<     \* Less than
>     \* Greater than
<=    \* Less than or equal
>=    \* Greater than or equal
```

---

## Temporal Operators

### Box (Always) - []

**Syntax**: `[]P`

**Meaning**: Property P holds in all states of the behavior

**Usage**:
```tla
\* Safety property: buffer never overflows
[]( buffer_size <= MAX_SIZE )

\* Type invariant always holds
[]TypeOK
```

### Diamond (Eventually) - <>

**Syntax**: `<>P`

**Meaning**: Property P holds in at least one state of the behavior

**Usage**:
```tla
\* Eventually the system terminates
<>(status = "terminated")

\* Some request eventually succeeds
<>(\E req \in Requests : req.status = "success")
```

### Leads-To (~>)

**Syntax**: `P ~> Q`

**Equivalent to**: `[](P => <>Q)`

**Meaning**: Whenever P holds, Q eventually holds

**Usage**:
```tla
\* Every request eventually gets a response
(request_sent) ~> (response_received)

\* If a process requests access, it eventually gets it
(pc[p] = "requesting") ~> (pc[p] = "critical")
```

### Enabled

**Syntax**: `ENABLED A`

**Meaning**: Action A is enabled in the current state

**Usage**:
```tla
\* The send action is enabled
ENABLED Send(msg)

\* At least one action is always enabled (non-blocking)
[](\E a \in Actions : ENABLED a)
```

---

## Action Operators

### Prime (')

**Syntax**: `var'`

**Meaning**: The value of var in the next state

**Usage**:
```tla
\* Counter increments
counter' = counter + 1

\* Variable doesn't change
UNCHANGED var  \* Equivalent to: var' = var
```

### Action Composition

**Syntax**: `[A]_vars`

**Meaning**: Action A occurs, or vars remain unchanged (stuttering step)

**Usage**:
```tla
\* Specification with stuttering
Spec == Init /\ [][Next]_vars

\* Next action or stutter
[Next]_<<x, y, z>>
```

### Strong Action

**Syntax**: `<A>_vars`

**Meaning**: Action A occurs and vars change

**Usage**:
```tla
\* Progress: Next action must change state
<>(<Next>_vars)
```

---

## Quantifiers

### Universal Quantifier (\A)

**Syntax**: `\A x \in S : P(x)`

**Meaning**: For all x in set S, property P(x) holds

**Usage**:
```tla
\* All processes are in valid states
\A p \in Processes : pc[p] \in {"idle", "active", "done"}

\* No two processes in critical section
\A p1, p2 \in Processes :
    (p1 # p2) => ~(pc[p1] = "critical" /\ pc[p2] = "critical")
```

### Existential Quantifier (\E)

**Syntax**: `\E x \in S : P(x)`

**Meaning**: There exists an x in set S such that property P(x) holds

**Usage**:
```tla
\* At least one process is active
\E p \in Processes : pc[p] = "active"

\* Some request is pending
\E req \in Requests : req.status = "pending"
```

### Choose Operator (CHOOSE)

**Syntax**: `CHOOSE x \in S : P(x)`

**Meaning**: Select an arbitrary x from S satisfying P(x)

**Usage**:
```tla
\* Pick any ready process
next_process == CHOOSE p \in Processes : pc[p] = "ready"
```

---

## Property Types

### Type Invariants

Check that variables have correct types:

```tla
TypeOK ==
    /\ counter \in Nat
    /\ status \in {"idle", "running", "done"}
    /\ buffer \in Seq(Messages)
    /\ pc \in [Processes -> {"idle", "active", "critical"}]
```

### State Invariants

Properties that must hold in every reachable state:

```tla
\* Invariant: System property
Invariant ==
    /\ buffer_size <= MAX_SIZE
    /\ \A p \in Processes : valid_state(pc[p])
    /\ resource_count >= 0
```

### Safety Properties

"Bad things never happen":

```tla
\* Safety: No deadlock
NoDeadlock ==
    [](\E p \in Processes : ENABLED Action(p))

\* Safety: Mutual exclusion
MutualExclusion ==
    [](\A p1, p2 \in Processes :
        (p1 # p2) => ~(InCS(p1) /\ InCS(p2)))
```

### Liveness Properties

"Good things eventually happen":

```tla
\* Liveness: Every request completes
RequestCompletion ==
    \A req \in Requests :
        (req.status = "pending") ~> (req.status = "done")

\* Liveness: System eventually stabilizes
EventualStability ==
    <>[](stable_state)
```

### Fairness Properties

Ensure actions get fair chances:

```tla
\* Weak fairness: If action continuously enabled, it eventually occurs
Fairness == WF_vars(Action)

\* Strong fairness: If action infinitely often enabled, it eventually occurs
StrongFairness == SF_vars(Action)

\* Fair specification
FairSpec == Spec /\ WF_vars(Next)
```

---

## Common Patterns

### Pattern 1: Bounded Property

```tla
\* Value stays within bounds
BoundedValue == [](min_val <= value /\ value <= max_val)
```

### Pattern 2: Monotonic Property

```tla
\* Counter never decreases
Monotonic == [][counter' >= counter]_vars
```

### Pattern 3: Conditional Liveness

```tla
\* If condition holds, goal eventually reached
ConditionalProgress == [](condition => <>goal)
```

### Pattern 4: Mutual Exclusion with Progress

```tla
\* At most one in CS, and requests eventually granted
MutexWithProgress ==
    /\ [](\A p1, p2 \in Processes :
            (p1 # p2) => ~(InCS(p1) /\ InCS(p2)))
    /\ \A p \in Processes :
            (Requesting(p)) ~> (InCS(p))
```

### Pattern 5: FIFO Ordering

```tla
\* Earlier requests served first
FIFOOrder ==
    \A req1, req2 \in Requests :
        (req1.timestamp < req2.timestamp /\ req1.status = "pending")
            => (req2.status # "completed")
```

### Pattern 6: Eventual Consistency

```tla
\* All replicas eventually agree
EventualConsistency ==
    <>[](\A r1, r2 \in Replicas : r1.value = r2.value)
```

### Pattern 7: No Starvation

```tla
\* Every waiting process eventually proceeds
NoStarvation ==
    \A p \in Processes :
        [](pc[p] = "waiting" => <>(pc[p] = "active"))
```

---

## Specification Structure

Complete TLA+ specification with properties:

```tla
---- MODULE Example ----
EXTENDS Naturals, Sequences

VARIABLES var1, var2, var3
vars == <<var1, var2, var3>>

\* Type invariant
TypeOK ==
    /\ var1 \in Nat
    /\ var2 \in BOOLEAN
    /\ var3 \in Seq(Messages)

\* Initial state
Init ==
    /\ var1 = 0
    /\ var2 = FALSE
    /\ var3 = <<>>

\* Next state actions
Action1 == ...
Action2 == ...

Next == Action1 \/ Action2

\* Specification
Spec == Init /\ [][Next]_vars

\* Properties to check
Safety == []SafetyCondition
Liveness == <>LivenessCondition
FairSpec == Spec /\ WF_vars(Next)

\* Theorems
THEOREM Spec => []TypeOK
THEOREM FairSpec => Liveness
====
```

---

## Operator Precedence

From highest to lowest:

1. `'` (prime), function application
2. `~` (negation)
3. `/\` (conjunction)
4. `\/` (disjunction)
5. `=>` (implication)
6. `<=>` (equivalence)
7. `[]`, `<>` (temporal operators)
8. `~>` (leads-to)

Use parentheses for clarity when in doubt.
