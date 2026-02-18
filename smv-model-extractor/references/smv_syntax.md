# SMV/NuSMV Syntax Reference

Quick reference for NuSMV model syntax.

## Basic Structure

```smv
MODULE main
VAR
  -- state variables
ASSIGN
  -- initial values and transitions
DEFINE
  -- derived expressions
SPEC
  -- temporal logic specifications
```

## Variable Declarations

### Boolean Variables
```smv
VAR
  flag : boolean;
  ready : boolean;
```

### Enumerated Types
```smv
VAR
  state : {idle, running, stopped};
  color : {red, green, blue};
```

### Integer Ranges
```smv
VAR
  counter : 0..10;
  index : -5..5;
```

### Arrays
```smv
VAR
  buffer : array 0..9 of boolean;
```

## Assignments

### Initial Values
```smv
ASSIGN
  init(state) := idle;
  init(counter) := 0;
```

### Next-State Transitions

**Simple assignment:**
```smv
ASSIGN
  next(counter) := counter + 1;
```

**Conditional (case statement):**
```smv
ASSIGN
  next(state) := case
    state = idle & start : running;
    state = running & stop : stopped;
    state = stopped & reset : idle;
    TRUE : state;
  esac;
```

**Non-deterministic choice:**
```smv
ASSIGN
  next(value) := {0, 1, 2};  -- can be any of these
```

## Expressions

### Logical Operators
- `!` - NOT
- `&` - AND
- `|` - OR
- `->` - implication
- `<->` - equivalence

### Comparison Operators
- `=` - equality
- `!=` - inequality
- `<`, `<=`, `>`, `>=` - ordering

### Arithmetic Operators
- `+`, `-`, `*`, `/`, `mod`

## Temporal Logic Specifications

### CTL Operators

**Path quantifiers:**
- `AG` - for all paths, globally
- `EG` - exists a path, globally
- `AF` - for all paths, eventually
- `EF` - exists a path, eventually
- `AX` - for all paths, next state
- `EX` - exists a path, next state
- `AU` - for all paths, until
- `EU` - exists a path, until

**Examples:**
```smv
-- Safety: bad state never reached
SPEC AG (state != error)

-- Liveness: eventually reach goal
SPEC AF (state = goal)

-- Response: request always eventually granted
SPEC AG (request -> AF grant)

-- Mutual exclusion
SPEC AG !(process1 = critical & process2 = critical)
```

### LTL Operators

- `G` - globally (always)
- `F` - eventually (finally)
- `X` - next
- `U` - until
- `R` - releases

**Examples:**
```smv
LTLSPEC G (request -> F grant)
LTLSPEC G (critical -> X !critical)
```

## Common Patterns

### State Machine
```smv
VAR
  state : {s0, s1, s2, s3};

ASSIGN
  init(state) := s0;
  next(state) := case
    state = s0 & condition1 : s1;
    state = s1 & condition2 : s2;
    state = s2 : s3;
    state = s3 : s0;
    TRUE : state;
  esac;
```

### Counter
```smv
VAR
  count : 0..10;

ASSIGN
  init(count) := 0;
  next(count) := case
    count < 10 : count + 1;
    TRUE : count;
  esac;
```

### Flag with Set/Reset
```smv
VAR
  flag : boolean;
  set_signal : boolean;
  reset_signal : boolean;

ASSIGN
  init(flag) := FALSE;
  next(flag) := case
    set_signal : TRUE;
    reset_signal : FALSE;
    TRUE : flag;
  esac;
```

## Modules and Composition

### Defining Modules
```smv
MODULE counter(inc, reset)
VAR
  value : 0..10;
ASSIGN
  init(value) := 0;
  next(value) := case
    reset : 0;
    inc & value < 10 : value + 1;
    TRUE : value;
  esac;
```

### Using Modules
```smv
MODULE main
VAR
  c1 : counter(signal1, reset1);
  c2 : counter(signal2, reset2);
```

## Verification Commands

Run NuSMV:
```bash
NuSMV model.smv
```

Interactive mode:
```bash
NuSMV -int model.smv
```

Check specific property:
```bash
NuSMV -dcx model.smv
```
