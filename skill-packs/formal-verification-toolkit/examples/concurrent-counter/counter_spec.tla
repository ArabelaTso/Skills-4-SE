---- MODULE ConcurrentCounter ----
(*
TLA+ Specification for Concurrent Counter

This specification models a counter that can be incremented by multiple threads.
It captures the race condition in the buggy implementation.
*)

EXTENDS Naturals, Sequences

CONSTANTS
    NumThreads,     \* Number of concurrent threads
    MaxValue        \* Maximum counter value (for bounded model checking)

VARIABLES
    value,          \* The counter value
    pc,             \* Program counter for each thread
    temp            \* Temporary variable for each thread (models local state)

vars == <<value, pc, temp>>

\* Type invariant
TypeInvariant ==
    /\ value \in Nat
    /\ pc \in [1..NumThreads -> {"idle", "read", "compute", "write", "done"}]
    /\ temp \in [1..NumThreads -> Nat]

\* Initial state
Init ==
    /\ value = 0
    /\ pc = [i \in 1..NumThreads |-> "idle"]
    /\ temp = [i \in 1..NumThreads |-> 0]

\* Thread i starts incrementing
StartIncrement(i) ==
    /\ pc[i] = "idle"
    /\ pc' = [pc EXCEPT ![i] = "read"]
    /\ UNCHANGED <<value, temp>>

\* Thread i reads the counter value (BUGGY: not atomic with write)
ReadValue(i) ==
    /\ pc[i] = "read"
    /\ temp' = [temp EXCEPT ![i] = value]
    /\ pc' = [pc EXCEPT ![i] = "compute"]
    /\ UNCHANGED value

\* Thread i computes new value
Compute(i) ==
    /\ pc[i] = "compute"
    /\ temp' = [temp EXCEPT ![i] = temp[i] + 1]
    /\ pc' = [pc EXCEPT ![i] = "write"]
    /\ UNCHANGED value

\* Thread i writes the new value (BUGGY: not atomic with read)
WriteValue(i) ==
    /\ pc[i] = "write"
    /\ value' = temp[i]
    /\ pc' = [pc EXCEPT ![i] = "done"]
    /\ UNCHANGED temp

\* Next state relation
Next ==
    \E i \in 1..NumThreads :
        \/ StartIncrement(i)
        \/ ReadValue(i)
        \/ Compute(i)
        \/ WriteValue(i)

\* Specification
Spec == Init /\ [][Next]_vars

\* PROPERTIES TO VERIFY

\* Safety: Counter never decreases
CounterNeverDecreases ==
    [][value' >= value]_vars

\* Safety: Counter is bounded
CounterBounded ==
    value <= MaxValue

\* Correctness: If all threads complete, value should equal NumThreads
\* This property will be VIOLATED due to the race condition!
CorrectFinalValue ==
    (\A i \in 1..NumThreads : pc[i] = "done") => (value = NumThreads)

\* Atomicity: Increment should be atomic (this is violated in buggy version)
\* If a thread is between read and write, no other thread should modify value
AtomicIncrement ==
    \A i \in 1..NumThreads :
        (pc[i] \in {"compute", "write"}) =>
            (\A j \in 1..NumThreads :
                (i /= j) => (pc[j] \notin {"write"}))

====
