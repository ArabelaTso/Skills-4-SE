# Model Checker Counterexample Formats

This document describes common counterexample formats from popular model checkers.

## Table of Contents

1. [SPIN](#spin)
2. [CBMC](#cbmc)
3. [NuSMV](#nusmv)
4. [TLA+](#tla)
5. [Java PathFinder (JPF)](#java-pathfinder-jpf)
6. [DIVINE](#divine)
7. [UPPAAL](#uppaal)

---

## SPIN

**Format**: Trail file (.trail) with state transitions

**Structure**:
```
-2:3:-2
-4:-4:-4
1:0:1234:0
2:1:1235:1
...
```

**Key Elements**:
- Each line represents a state transition
- Format: `process_id:statement:state_id:transition_type`
- Negative numbers indicate special states (initial, accept, etc.)
- Trail ends at property violation

**Parsing Strategy**:
1. Use `spin -t -p model.pml` to get readable trace
2. Extract variable values at each step
3. Identify the assertion or LTL property violated
4. Map process IDs to concurrent threads

**Example Output**:
```
  1: proc  0 (init) line  12 "model.pml" (state 1) [x = 0]
  2: proc  1 (P) line  5 "model.pml" (state 2) [y = x + 1]
  3: proc  0 (init) line  13 "model.pml" (state 3) [assert(y < 10)]
spin: trail ends after 3 steps
```

---

## CBMC

**Format**: XML or text trace with program execution

**Structure**:
```xml
<result>
  <program>program.c</program>
  <property>assertion</property>
  <status>FAILURE</status>
  <trace>
    <assignment>
      <location file="program.c" line="10"/>
      <lhs>x</lhs>
      <value>5</value>
    </assignment>
    <assignment>
      <location file="program.c" line="11"/>
      <lhs>y</lhs>
      <value>10</value>
    </assignment>
    <failure>
      <location file="program.c" line="15"/>
      <property>assertion x + y < 20</property>
    </failure>
  </trace>
</result>
```

**Key Elements**:
- Variable assignments with source locations
- Function calls and returns
- Assertion failures with exact line numbers
- Memory operations (malloc, free, array access)

**Parsing Strategy**:
1. Extract initial variable values
2. Follow assignment sequence
3. Identify branch decisions (if/while conditions)
4. Locate the failing assertion or property

---

## NuSMV

**Format**: State sequence with variable valuations

**Structure**:
```
Trace Type: Counterexample
  -> State: 1.1 <-
    x = 0
    y = FALSE
    state = idle
  -> State: 1.2 <-
    x = 1
    y = FALSE
    state = active
  -> State: 1.3 <-
    x = 2
    y = TRUE
    state = error
-- specification AG (state != error) is false
```

**Key Elements**:
- Explicit state numbering
- Complete variable valuations at each state
- Transition labels (if present)
- Property specification that failed

**Parsing Strategy**:
1. Extract state sequence
2. Record variable values at each state
3. Identify state transitions and their triggers
4. Map to program control flow

---

## TLA+

**Format**: TLC error trace with state predicates

**Structure**:
```
Error: Invariant Inv is violated.
The behavior up to this point is:
State 1: <Initial predicate>
/\ x = 0
/\ y = 0
/\ pc = "Start"

State 2: <Action Next>
/\ x = 1
/\ y = 0
/\ pc = "Step1"

State 3: <Action Next>
/\ x = 1
/\ y = 2
/\ pc = "Error"
```

**Key Elements**:
- State predicates (conjunctions of variable values)
- Action names (which transition was taken)
- Invariant or temporal property violated
- Variable bindings at each state

**Parsing Strategy**:
1. Parse state predicates to extract variable values
2. Identify action sequence
3. Map TLA+ variables to program variables
4. Reconstruct the execution path

---

## Java PathFinder (JPF)

**Format**: Java stack trace with choice points

**Structure**:
```
====================================================== error 1
gov.nasa.jpf.vm.NoUncaughtExceptionsProperty
java.lang.AssertionError: x should be less than 10
        at Example.method(Example.java:25)
        at Example.main(Example.java:15)

====================================================== trace
transition #0 thread: 0
  Example.main(Example.java:10)  : x = 0;

transition #1 thread: 0
  Example.main(Example.java:11)  : y = getInput();
  choice: y = 5

transition #2 thread: 0
  Example.main(Example.java:12)  : x = x + y;

transition #3 thread: 0
  Example.main(Example.java:25)  : assert x < 10;
```

**Key Elements**:
- Java stack traces
- Thread IDs for concurrent programs
- Choice points (non-deterministic values)
- Source line numbers

**Parsing Strategy**:
1. Extract thread execution sequence
2. Identify choice points and selected values
3. Map to Java method calls and field accesses
4. Handle thread interleavings for concurrent tests

---

## DIVINE

**Format**: LLVM-level trace with memory states

**Structure**:
```
Counterexample:
[0] __boot:
    _VM_Frame: { pc: 0, ... }
[1] main:
    x: i32 = 0
    y: i32 = 0
[2] main+4:
    x: i32 = 5
    y: i32 = 0
[3] main+8:
    x: i32 = 5
    y: i32 = 10
[4] ERROR: assertion failed at main+12
```

**Key Elements**:
- LLVM instruction addresses
- Memory state (variables and heap)
- Function call stack
- Error location in LLVM IR

**Parsing Strategy**:
1. Map LLVM IR back to source code (use debug info)
2. Extract variable values from memory state
3. Reconstruct high-level operations from IR
4. Generate test at source level

---

## UPPAAL

**Format**: Timed automata trace with clock valuations

**Structure**:
```
State [0]: P.loc0 Q.loc0
  x=0 y=0 clock=0

Transition: P.loc0 -> P.loc1 { guard: x < 5, sync: a!, assign: x := x+1 }

State [1]: P.loc1 Q.loc0
  x=1 y=0 clock=0

Delay: 2.5

State [2]: P.loc1 Q.loc0
  x=1 y=0 clock=2.5

Transition: Q.loc0 -> Q.error { guard: clock > 2 }

State [3]: P.loc1 Q.error
  x=1 y=0 clock=2.5
  ERROR: Query 'A[] not Q.error' is not satisfied
```

**Key Elements**:
- Automaton locations
- Clock valuations
- Delays (time passage)
- Synchronization events
- Guards and assignments

**Parsing Strategy**:
1. Extract location sequence for each automaton
2. Record clock values and delays
3. Identify synchronization points
4. Generate test with timing constraints (sleep/wait)

---

## General Parsing Tips

1. **Identify the format**: Look for characteristic markers (XML tags, state numbers, etc.)
2. **Extract initial state**: First state or explicit initialization
3. **Build state sequence**: Ordered list of states with variable values
4. **Find the violation**: Last state or explicit error marker
5. **Handle concurrency**: Track thread/process IDs and interleavings
6. **Preserve causality**: Maintain exact order of operations
7. **Map to source**: Use line numbers or debug info to link to original code
