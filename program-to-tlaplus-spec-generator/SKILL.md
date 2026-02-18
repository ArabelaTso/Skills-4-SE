---
name: program-to-tlaplus-spec-generator
description: Automatically generate TLA+ specifications from program code, repositories, or system implementations. Use when asked to generate TLA+ spec, create TLA+ specification from code, convert program to TLA+, formalize system in TLA+, extract TLA+ model from code, or when working with formal specification of concurrent systems, distributed systems, protocols, algorithms, or state machines that need to be verified.
---

# Program to TLA+ Spec Generator

## Overview

This skill enables automatic generation of TLA+ specifications from source code. It analyzes program structure, identifies state variables and transitions, and produces well-formed TLA+ modules with proper syntax and semantics.

## Generation Workflow

Follow this sequential process to generate TLA+ specifications from code:

### 1. Analyze Input Program

Read and understand the source code:

- **Identify scope**: Determine which components/modules to formalize
- **Understand purpose**: What does the system do? What properties matter?
- **Detect patterns**: Is it concurrent? Distributed? Sequential? State machine?
- **Note language**: Adapt analysis to language-specific constructs

Ask clarifying questions if needed:
- Which components should be included in the spec?
- Are there specific properties or invariants to capture?
- What level of abstraction is desired?

### 2. Extract State Variables

Identify variables that represent system state:

**Look for:**
- Global variables and shared state
- Object fields that persist across operations
- Database/storage state
- Message queues or buffers
- Locks, semaphores, and synchronization primitives
- Process/thread state (running, waiting, etc.)

**Determine types:**
- Booleans, integers, sets, sequences, records
- Map program types to TLA+ types
- Identify bounded vs unbounded values

**Output**: List of state variables with TLA+ type declarations

### 3. Identify System Actions

Extract operations that modify state:

**Look for:**
- Functions/methods that change state
- Event handlers and callbacks
- Message send/receive operations
- Lock acquire/release
- State transitions in state machines
- Concurrent operations

**For each action, identify:**
- Preconditions (when can it execute?)
- State changes (what variables are modified?)
- Postconditions (what must be true after?)
- Parameters and return values

**Output**: List of actions with their effects

### 4. Determine Initial State

Identify how the system starts:

- Variable initialization
- Constructor logic
- Setup/bootstrap code
- Default values

**Output**: Initial state predicate (Init)

### 5. Analyze Control Flow

Understand execution patterns:

- Sequential vs concurrent execution
- Synchronization points
- Branching and conditionals
- Loops and iteration
- Process spawning/termination

**Output**: Understanding of how actions compose

### 6. Extract Invariants and Properties

Identify correctness conditions:

**Safety properties** (something bad never happens):
- Type invariants
- Consistency constraints
- Mutual exclusion
- Assertions in code

**Liveness properties** (something good eventually happens):
- Progress guarantees
- Fairness requirements
- Termination conditions

**Output**: List of properties to specify

### 7. Generate TLA+ Module

Construct the specification following TLA+ syntax:

**Module structure:**
```tla
---- MODULE ModuleName ----
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS [constants]

VARIABLES [state variables]

vars == <<var1, var2, ...>>

Init == [initial state predicate]

Action1 == [action definition]
Action2 == [action definition]
...

Next == Action1 \/ Action2 \/ ...

Spec == Init /\ [][Next]_vars

TypeInvariant == [type constraints]
SafetyProperty == [safety properties]

====
```

**Key elements:**
- Use proper TLA+ operators and syntax
- Include EXTENDS for standard modules
- Define CONSTANTS for parameters
- Declare all VARIABLES
- Write clear Init predicate
- Define each action separately
- Combine actions in Next with disjunction
- Add Spec with stuttering
- Include invariants and properties

See [references/tlaplus_syntax.md](references/tlaplus_syntax.md) for detailed syntax guide.

### 8. Create Abstraction Mapping

Document how program maps to TLA+:

**State variable mapping:**
```
Program Variable -> TLA+ Variable
---------------------------------
counter (int)    -> counter \in Nat
buffer (array)   -> buffer \in Seq(Data)
lock (bool)      -> lock \in BOOLEAN
```

**Action mapping:**
```
Program Function -> TLA+ Action
--------------------------------
increment()      -> Increment
send(msg)        -> Send(msg)
acquire_lock()   -> AcquireLock
```

**Abstractions applied:**
- Unbounded integers -> bounded range
- Complex data structures -> simplified types
- Implementation details omitted
- Nondeterminism introduced

**Assumptions made:**
- Fairness assumptions
- Environment behavior
- Timing assumptions

### 9. Generate TLC Configuration (Optional)

Create model checking configuration:

```
SPECIFICATION Spec

CONSTANTS
  MaxValue = 10
  NumProcesses = 3

INVARIANTS
  TypeInvariant
  SafetyProperty

PROPERTIES
  LivenessProperty
```

## Output Format

Provide outputs in this structure:

### Generated TLA+ Specification

```tla
[Complete .tla file content]
```

### Program-to-Spec Mapping

**State Variables:**
- `program_var` → `tla_var`: [explanation]

**Actions:**
- `program_function()` → `TLAAction`: [explanation]

**Abstractions:**
- [List abstractions and simplifications]

**Assumptions:**
- [List assumptions made]

### TLC Configuration (if requested)

```
[.cfg file content]
```

### Verification Guidance

- Suggested invariants to check
- Properties to verify
- Model parameters to configure
- Expected verification results

## Common Patterns

### Sequential Program

**Program characteristics:**
- Single thread of execution
- No concurrency

**TLA+ approach:**
- Simple state machine
- Actions execute atomically
- Next is disjunction of all actions

### Concurrent Program

**Program characteristics:**
- Multiple threads/processes
- Shared state with synchronization

**TLA+ approach:**
- Model each thread as separate actions
- Use process variables for thread state
- Model locks/semaphores explicitly
- Consider fairness

### Distributed System

**Program characteristics:**
- Multiple nodes communicating
- Message passing
- Network delays/failures

**TLA+ approach:**
- Model each node's state
- Explicit message buffers
- Nondeterministic message delivery
- Model network failures if needed

### State Machine

**Program characteristics:**
- Explicit states and transitions
- Event-driven

**TLA+ approach:**
- Direct mapping of states to TLA+ values
- Each transition becomes an action
- Guards become preconditions

## Abstraction Guidelines

**What to abstract:**
- Implementation details (algorithms → effects)
- Concrete data structures (arrays → sequences/sets)
- Timing (delays → nondeterminism)
- Unbounded values (integers → bounded range)

**What to preserve:**
- State space structure
- Transition relationships
- Concurrency patterns
- Critical properties

**Abstraction levels:**
- **High**: Focus on protocol/algorithm logic only
- **Medium**: Include key data structures
- **Low**: Close to implementation details

Choose abstraction level based on verification goals.

## Tips for Effective Specs

- **Start simple**: Model core behavior first, add details later
- **Be explicit**: Make all state and transitions visible
- **Use symmetry**: Exploit symmetry to reduce state space
- **Bound carefully**: Choose bounds that expose bugs but keep verification tractable
- **Document well**: Add comments explaining non-obvious parts
- **Validate mapping**: Ensure TLA+ spec truly represents the program
- **Test incrementally**: Verify simple properties first

## Language-Specific Considerations

**C/C++:**
- Model pointers as references or indices
- Abstract memory management
- Model concurrency primitives (pthread, etc.)

**Java:**
- Model objects as records
- Abstract inheritance/polymorphism
- Model synchronized blocks and locks

**Go:**
- Model goroutines as processes
- Model channels explicitly
- Capture select statement nondeterminism

**Python:**
- Focus on high-level logic
- Abstract dynamic typing
- Model threading/asyncio patterns

**Rust:**
- Leverage ownership for safety properties
- Model borrowing as access control
- Abstract lifetimes

For detailed patterns, see [references/language_patterns.md](references/language_patterns.md).
