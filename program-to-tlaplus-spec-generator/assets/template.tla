---- MODULE Template ----
EXTENDS Naturals, Sequences, FiniteSets

\* Constants define parameters of the system
CONSTANTS
    MaxValue,        \* Maximum value for bounded variables
    NumProcesses,    \* Number of concurrent processes
    Data             \* Set of data values

\* Variables define the state space
VARIABLES
    state,           \* Current system state
    counter,         \* Example counter variable
    buffer,          \* Example buffer (sequence)
    processes        \* Process states

\* Convenience definition for all variables
vars == <<state, counter, buffer, processes>>

\* Type invariant defines the types of all variables
TypeInvariant ==
    /\ state \in {"Init", "Running", "Done"}
    /\ counter \in Nat
    /\ buffer \in Seq(Data)
    /\ processes \in [1..NumProcesses -> {"Ready", "Running", "Waiting", "Done"}]

\* Initial state predicate
Init ==
    /\ state = "Init"
    /\ counter = 0
    /\ buffer = <<>>
    /\ processes = [i \in 1..NumProcesses |-> "Ready"]

\* Example action: Increment counter
Increment ==
    /\ state = "Running"
    /\ counter < MaxValue
    /\ counter' = counter + 1
    /\ UNCHANGED <<state, buffer, processes>>

\* Example action: Add to buffer
AddToBuffer(value) ==
    /\ state = "Running"
    /\ value \in Data
    /\ Len(buffer) < MaxValue
    /\ buffer' = Append(buffer, value)
    /\ UNCHANGED <<state, counter, processes>>

\* Example action: Process starts
ProcessStart(i) ==
    /\ i \in 1..NumProcesses
    /\ processes[i] = "Ready"
    /\ processes' = [processes EXCEPT ![i] = "Running"]
    /\ UNCHANGED <<state, counter, buffer>>

\* Example action: Process completes
ProcessComplete(i) ==
    /\ i \in 1..NumProcesses
    /\ processes[i] = "Running"
    /\ processes' = [processes EXCEPT ![i] = "Done"]
    /\ UNCHANGED <<state, counter, buffer>>

\* Transition to running state
Start ==
    /\ state = "Init"
    /\ state' = "Running"
    /\ UNCHANGED <<counter, buffer, processes>>

\* Transition to done state
Finish ==
    /\ state = "Running"
    /\ counter = MaxValue
    /\ state' = "Done"
    /\ UNCHANGED <<counter, buffer, processes>>

\* Next-state relation: disjunction of all actions
Next ==
    \/ Start
    \/ Increment
    \/ \E v \in Data : AddToBuffer(v)
    \/ \E i \in 1..NumProcesses : ProcessStart(i)
    \/ \E i \in 1..NumProcesses : ProcessComplete(i)
    \/ Finish

\* Specification with stuttering
Spec == Init /\ [][Next]_vars

\* Optional: Specification with fairness
FairSpec ==
    /\ Init
    /\ [][Next]_vars
    /\ WF_vars(Increment)           \* Weak fairness for Increment
    /\ WF_vars(Finish)               \* Weak fairness for Finish

\* Safety property: counter never exceeds maximum
SafetyProperty ==
    counter \leq MaxValue

\* Safety property: buffer size is bounded
BufferBounded ==
    Len(buffer) \leq MaxValue

\* Liveness property: eventually reach done state
LivenessProperty ==
    <>(state = "Done")

\* Invariant: all processes eventually complete
AllProcessesComplete ==
    state = "Done" => \A i \in 1..NumProcesses : processes[i] = "Done"

====
