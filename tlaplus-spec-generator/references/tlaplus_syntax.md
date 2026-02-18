# TLA+ Syntax Reference

Quick reference for TLA+ specification language.

## Module Structure

```tla
---- MODULE ModuleName ----
EXTENDS Naturals, Sequences

CONSTANTS N

VARIABLES x, y, z

Init == x = 0 /\ y = 0 /\ z = 0

Next == ...

Spec == Init /\ [][Next]_<<x,y,z>>
====
```

## Basic Syntax

### Comments
```tla
\* Single-line comment

(* Multi-line
   comment *)
```

### Logical Operators
- `/\` - AND (conjunction)
- `\/` - OR (disjunction)
- `~` - NOT (negation)
- `=>` - Implies
- `<=>` - Equivalence (if and only if)

### Comparison Operators
- `=` - Equality
- `/=` or `#` - Inequality
- `<`, `<=`, `>`, `>=` - Ordering

### Quantifiers
```tla
\A x \in S : P(x)    \* For all x in S, P(x) holds
\E x \in S : P(x)    \* There exists x in S such that P(x)
```

## Data Types

### Booleans
```tla
BOOLEAN          \* Set {TRUE, FALSE}
TRUE
FALSE
```

### Numbers
```tla
Nat              \* Natural numbers {0, 1, 2, ...}
0..10            \* Range from 0 to 10
x + y            \* Addition
x - y            \* Subtraction
x * y            \* Multiplication
x \div y         \* Integer division
x % y            \* Modulo
```

### Sets
```tla
{}               \* Empty set
{1, 2, 3}        \* Explicit set
{x \in S : P(x)} \* Set comprehension

x \in S          \* Set membership
S \subseteq T    \* Subset
S \cup T         \* Union
S \cap T         \* Intersection
S \ T            \* Set difference
SUBSET S         \* Power set (all subsets of S)
UNION S          \* Union of all sets in S
Cardinality(S)   \* Size of set S
```

### Sequences
```tla
<<>>             \* Empty sequence
<<1, 2, 3>>      \* Explicit sequence
Seq(S)           \* All sequences with elements from S

Head(seq)        \* First element
Tail(seq)        \* All but first element
Append(seq, x)   \* Add x to end
Len(seq)         \* Length of sequence
seq[i]           \* i-th element (1-indexed)
SubSeq(seq, m, n) \* Subsequence from m to n
```

### Records
```tla
[field1 |-> value1, field2 |-> value2]  \* Record literal
r.field          \* Field access
[r EXCEPT !.field = newValue]           \* Update field
```

### Functions
```tla
[x \in S |-> expr]                      \* Function definition
f[x]                                     \* Function application
DOMAIN f                                 \* Domain of function
[f EXCEPT ![x] = newValue]              \* Update function
```

## State and Actions

### Variables
```tla
VARIABLES x, y, z

vars == <<x, y, z>>  \* Tuple of all variables
```

### Primed Variables
```tla
x'               \* Value of x in next state
x' = x + 1       \* x increases by 1
```

### UNCHANGED
```tla
UNCHANGED x              \* x' = x
UNCHANGED <<x, y>>       \* x' = x /\ y' = y
```

### Initial State
```tla
Init ==
  /\ x = 0
  /\ y = 0
  /\ z = <<>>
```

### Actions
```tla
Action ==
  /\ x > 0              \* Precondition (enabling condition)
  /\ x' = x - 1         \* Effect on x
  /\ y' = y + 1         \* Effect on y
  /\ UNCHANGED z        \* z doesn't change
```

### Next-State Relation
```tla
Next ==
  \/ Action1
  \/ Action2
  \/ Action3
```

### Specification
```tla
Spec == Init /\ [][Next]_vars

\* With fairness
Spec == Init /\ [][Next]_vars /\ WF_vars(Action1)
```

## Temporal Operators

### Always and Eventually
```tla
[]P              \* Always P (P holds in all states)
<>P              \* Eventually P (P holds in some future state)
```

### Leads-to
```tla
P ~> Q           \* P leads to Q (if P holds, eventually Q holds)
                 \* Equivalent to: [](P => <>Q)
```

### Weak and Strong Fairness
```tla
WF_vars(Action)  \* Weak fairness: if Action is continuously enabled, it eventually happens
SF_vars(Action)  \* Strong fairness: if Action is infinitely often enabled, it eventually happens
```

## Common Patterns

### State Machine
```tla
VARIABLES state

States == {"Init", "Working", "Done"}

TypeOK == state \in States

Init == state = "Init"

StartWork ==
  /\ state = "Init"
  /\ state' = "Working"

FinishWork ==
  /\ state = "Working"
  /\ state' = "Done"

Next ==
  \/ StartWork
  \/ FinishWork

Spec == Init /\ [][Next]_state
```

### Counter
```tla
VARIABLES count

TypeOK == count \in Nat

Init == count = 0

Increment ==
  /\ count < 10
  /\ count' = count + 1

Decrement ==
  /\ count > 0
  /\ count' = count - 1

Next ==
  \/ Increment
  \/ Decrement
```

### Message Queue
```tla
VARIABLES queue

TypeOK == queue \in Seq(Messages)

Init == queue = <<>>

Send(msg) ==
  /\ queue' = Append(queue, msg)

Receive ==
  /\ queue /= <<>>
  /\ queue' = Tail(queue)

Next ==
  \/ \E msg \in Messages : Send(msg)
  \/ Receive
```

### Distributed System with Processes
```tla
CONSTANTS N      \* Number of processes

VARIABLES state  \* state[p] is state of process p

Procs == 1..N

TypeOK == state \in [Procs -> States]

Init == state = [p \in Procs |-> "Init"]

ProcessAction(p) ==
  /\ state[p] = "Init"
  /\ state' = [state EXCEPT ![p] = "Working"]

Next == \E p \in Procs : ProcessAction(p)
```

## Invariants and Properties

### Type Invariant
```tla
TypeOK ==
  /\ x \in Nat
  /\ y \in BOOLEAN
  /\ z \in Seq(Messages)
```

### Safety Property
```tla
Safety ==
  /\ x <= 100
  /\ y => (z /= <<>>)
```

### Liveness Property
```tla
\* Eventually reach done state
THEOREM Spec => <>[]( state = "Done" )

\* Every request is eventually granted
THEOREM Spec => [](request => <>grant)
```

## TLC Model Checker Directives

### Symmetry
```tla
SYMMETRY Permutations(Procs)
```

### State Constraints
```tla
StateConstraint == count <= 5
```

### Action Constraints
```tla
ActionConstraint == count' <= count + 1
```

## Tips

1. **Use meaningful names** - `state`, `queue`, `count` are clearer than `x`, `y`, `z`
2. **Factor out type invariants** - Define `TypeOK` separately
3. **Use UNCHANGED** - More concise than listing unchanged variables
4. **Quantify carefully** - `\E` can cause state explosion
5. **Start simple** - Add complexity incrementally
6. **Check TypeOK first** - Ensures basic correctness before checking properties
