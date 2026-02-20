# TLA+ Syntax Reference

## Module Structure

```tla
---- MODULE ModuleName ----
EXTENDS StandardModules
CONSTANTS ConstantDeclarations
VARIABLES VariableDeclarations

Definitions

====
```

## Standard Modules

Common modules to extend:

- **Naturals**: Natural numbers (0, 1, 2, ...), operators: +, -, *, /, %, ^, .., \div, \leq, \geq
- **Integers**: All integers, includes Naturals
- **Reals**: Real numbers
- **Sequences**: Sequence operations (Seq, Len, Append, Head, Tail, SubSeq)
- **FiniteSets**: Finite set operations (Cardinality, IsFiniteSet)
- **TLC**: TLC-specific operators (Print, Assert, JavaTime)

## Variable Declarations

```tla
VARIABLES x, y, z

\* Group variables for convenience
vars == <<x, y, z>>
```

## Constants

```tla
CONSTANTS MaxValue, NumProcesses, Data
```

Constants are parameters that remain fixed during execution.

## Operators

### Boolean Operators

- `/\` - AND (conjunction)
- `\/` - OR (disjunction)
- `~` - NOT (negation)
- `=>` - Implies
- `<=>` - Equivalence (if and only if)

### Comparison Operators

- `=` - Equality
- `#` or `/=` - Inequality
- `<`, `>`, `\leq`, `\geq` - Ordering

### Set Operators

- `\in` - Element of
- `\notin` - Not element of
- `\subseteq` - Subset or equal
- `\cup` - Union
- `\cap` - Intersection
- `\` - Set difference
- `SUBSET S` - Set of all subsets of S
- `UNION S` - Union of all sets in S

### Set Construction

```tla
{1, 2, 3}                    \* Explicit set
{x \in S : P(x)}             \* Set filter
{e(x) : x \in S}             \* Set map
```

### Sequence Operators

```tla
<<1, 2, 3>>                  \* Sequence literal
Len(seq)                     \* Length
seq[i]                       \* Index (1-based)
Append(seq, elem)            \* Append element
Head(seq)                    \* First element
Tail(seq)                    \* All but first
SubSeq(seq, m, n)            \* Subsequence from m to n
seq1 \o seq2                 \* Concatenation
```

### Record Operators

```tla
[field1 |-> value1, field2 |-> value2]    \* Record literal
record.field                               \* Field access
[record EXCEPT !.field = newValue]         \* Update field
```

### Function Operators

```tla
[x \in S |-> e(x)]                        \* Function definition
f[x]                                       \* Function application
DOMAIN f                                   \* Domain of function
[f EXCEPT ![x] = newValue]                 \* Update function
```

## Temporal Operators

### Action Operators

- `[A]_v` - A or variables v unchanged (stuttering)
- `<<A>>_v` - A and variables v changed (non-stuttering)
- `ENABLED A` - Action A is enabled
- `UNCHANGED v` - Variables v remain unchanged
- `v'` - Next-state value of v

### Temporal Logic Operators

- `[]P` - Always P (globally)
- `<>P` - Eventually P (finally)
- `P ~> Q` - P leads to Q (P implies eventually Q)
- `[][A]_v` - Always A or v unchanged
- `WF_v(A)` - Weak fairness of A with respect to v
- `SF_v(A)` - Strong fairness of A with respect to v

## Common Patterns

### Initial State Predicate

```tla
Init ==
    /\ x = 0
    /\ y = {}
    /\ z = <<>>
```

### Action Definition

```tla
Action ==
    /\ Precondition          \* Guard/enabling condition
    /\ x' = x + 1            \* State update
    /\ UNCHANGED <<y, z>>    \* Other variables unchanged
```

### Next State Relation

```tla
Next ==
    \/ Action1
    \/ Action2
    \/ Action3
```

### Specification

```tla
Spec == Init /\ [][Next]_vars
```

With fairness:
```tla
Spec == Init /\ [][Next]_vars /\ WF_vars(Action1)
```

### Type Invariant

```tla
TypeInvariant ==
    /\ x \in Nat
    /\ y \in SUBSET Data
    /\ z \in Seq(Data)
```

### Safety Property

```tla
SafetyProperty ==
    /\ x \leq MaxValue
    /\ Cardinality(y) \leq 10
```

### Liveness Property

```tla
LivenessProperty ==
    <>(x = MaxValue)         \* Eventually x reaches MaxValue
```

## Quantifiers

```tla
\A x \in S : P(x)            \* For all x in S, P(x) holds
\E x \in S : P(x)            \* There exists x in S such that P(x)
```

## Conditional Expressions

```tla
IF condition THEN expr1 ELSE expr2

CASE p1 -> e1
  [] p2 -> e2
  [] OTHER -> e3
```

## LET Definitions

```tla
LET
    helper(x) == x + 1
    constant == 42
IN
    helper(constant)
```

## CHOOSE Operator

```tla
CHOOSE x \in S : P(x)        \* Arbitrarily choose x from S satisfying P
```

## Common Idioms

### Nondeterministic Choice

```tla
\E x \in S :
    /\ Condition(x)
    /\ var' = x
    /\ UNCHANGED other_vars
```

### Parameterized Action

```tla
Action(param) ==
    /\ param \in ValidParams
    /\ var' = f(param)
    /\ UNCHANGED other_vars

Next == \E p \in Params : Action(p)
```

### Multiple Process Model

```tla
VARIABLES pc, data

Process(i) ==
    /\ pc[i] = "ready"
    /\ pc' = [pc EXCEPT ![i] = "running"]
    /\ data' = data \cup {i}

Next == \E i \in Processes : Process(i)
```

### Message Passing

```tla
VARIABLES messages

Send(msg) ==
    messages' = messages \cup {msg}

Receive(msg) ==
    /\ msg \in messages
    /\ messages' = messages \ {msg}
```

### Mutex Lock

```tla
VARIABLES lock, owner

Acquire(proc) ==
    /\ lock = FALSE
    /\ lock' = TRUE
    /\ owner' = proc

Release(proc) ==
    /\ lock = TRUE
    /\ owner = proc
    /\ lock' = FALSE
    /\ owner' = NULL
```

## Comments

```tla
\* Single line comment

(* Multi-line
   comment *)
```

## Operator Precedence (highest to lowest)

1. Function application: `f[x]`, record access: `r.field`
2. Prefix operators: `~`, `DOMAIN`, `SUBSET`, `UNION`, `ENABLED`, `UNCHANGED`
3. Postfix operators: `'` (prime)
4. Infix operators (left to right within same level):
   - `^` (exponentiation)
   - `*`, `/`, `\div`, `%`
   - `+`, `-`, `\o` (concatenation)
   - `..` (range)
   - Set operators: `\cap`, `\cup`, `\`
   - Comparison: `=`, `#`, `/=`, `<`, `>`, `\leq`, `\geq`, `\in`, `\notin`, `\subseteq`
   - `/\` (AND)
   - `\/` (OR)
   - `=>` (implies)
   - `<=>` (equivalence)
5. Temporal operators: `[]`, `<>`, `~>`
6. Quantifiers: `\A`, `\E`

Use parentheses to clarify precedence when in doubt.
