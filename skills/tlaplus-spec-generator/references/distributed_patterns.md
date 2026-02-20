# Distributed Systems Patterns in TLA+

Common patterns for specifying distributed systems in TLA+.

## Pattern 1: Message Passing

### Basic Message Passing

```tla
CONSTANTS Procs, Messages

VARIABLES
  network,    \* Messages in transit
  state       \* Process states

TypeOK ==
  /\ network \in SUBSET Messages
  /\ state \in [Procs -> States]

Init ==
  /\ network = {}
  /\ state = [p \in Procs |-> "Init"]

Send(p, msg) ==
  /\ network' = network \cup {msg}
  /\ UNCHANGED state

Receive(p, msg) ==
  /\ msg \in network
  /\ network' = network \ {msg}
  /\ state' = [state EXCEPT ![p] = ProcessMessage(msg)]
```

### Reliable FIFO Channels

```tla
VARIABLES channels  \* channels[p][q] is queue from p to q

TypeOK == channels \in [Procs -> [Procs -> Seq(Messages)]]

Init == channels = [p \in Procs |-> [q \in Procs |-> <<>>]]

Send(p, q, msg) ==
  /\ channels' = [channels EXCEPT ![p][q] = Append(@, msg)]

Receive(p, q) ==
  /\ channels[q][p] /= <<>>
  /\ LET msg == Head(channels[q][p])
     IN /\ channels' = [channels EXCEPT ![q][p] = Tail(@)]
        /\ ProcessMessage(p, msg)
```

## Pattern 2: Consensus Protocols

### Two-Phase Commit

```tla
CONSTANTS
  RM,           \* Resource managers
  Coordinator

VARIABLES
  rmState,      \* State of each RM: "working", "prepared", "committed", "aborted"
  tmState,      \* State of coordinator: "init", "preparing", "committed", "aborted"
  tmPrepared,   \* Set of RMs that have prepared
  msgs          \* Messages in transit

TypeOK ==
  /\ rmState \in [RM -> {"working", "prepared", "committed", "aborted"}]
  /\ tmState \in {"init", "preparing", "committed", "aborted"}
  /\ tmPrepared \subseteq RM
  /\ msgs \subseteq Messages

Init ==
  /\ rmState = [r \in RM |-> "working"]
  /\ tmState = "init"
  /\ tmPrepared = {}
  /\ msgs = {}

TMPrepare ==
  /\ tmState = "init"
  /\ tmState' = "preparing"
  /\ msgs' = msgs \cup {[type |-> "Prepare", dest |-> r] : r \in RM}
  /\ UNCHANGED <<rmState, tmPrepared>>

RMPrepare(r) ==
  /\ rmState[r] = "working"
  /\ [type |-> "Prepare", dest |-> r] \in msgs
  /\ rmState' = [rmState EXCEPT ![r] = "prepared"]
  /\ msgs' = msgs \cup {[type |-> "Prepared", src |-> r]}
  /\ UNCHANGED <<tmState, tmPrepared>>

TMCommit ==
  /\ tmState = "preparing"
  /\ tmPrepared = RM
  /\ tmState' = "committed"
  /\ msgs' = msgs \cup {[type |-> "Commit", dest |-> r] : r \in RM}
  /\ UNCHANGED <<rmState, tmPrepared>>

RMCommit(r) ==
  /\ [type |-> "Commit", dest |-> r] \in msgs
  /\ rmState' = [rmState EXCEPT ![r] = "committed"]
  /\ UNCHANGED <<tmState, tmPrepared, msgs>>

\* Safety: All RMs reach the same decision
Consistency == \A r1, r2 \in RM :
  /\ rmState[r1] = "committed" => rmState[r2] /= "aborted"
  /\ rmState[r1] = "aborted" => rmState[r2] /= "committed"
```

### Paxos (Simplified)

```tla
CONSTANTS
  Acceptors,
  Values,
  Quorum

VARIABLES
  maxBal,       \* maxBal[a] is highest ballot seen by acceptor a
  maxVBal,      \* maxVBal[a] is ballot of highest vote by acceptor a
  maxVal,       \* maxVal[a] is value of highest vote by acceptor a
  msgs

TypeOK ==
  /\ maxBal \in [Acceptors -> Nat]
  /\ maxVBal \in [Acceptors -> Nat \cup {-1}]
  /\ maxVal \in [Acceptors -> Values \cup {None}]

Init ==
  /\ maxBal = [a \in Acceptors |-> 0]
  /\ maxVBal = [a \in Acceptors |-> -1]
  /\ maxVal = [a \in Acceptors |-> None]
  /\ msgs = {}

Phase1a(b) ==
  /\ msgs' = msgs \cup {[type |-> "1a", bal |-> b]}
  /\ UNCHANGED <<maxBal, maxVBal, maxVal>>

Phase1b(a, b) ==
  /\ [type |-> "1a", bal |-> b] \in msgs
  /\ b > maxBal[a]
  /\ maxBal' = [maxBal EXCEPT ![a] = b]
  /\ msgs' = msgs \cup {[type |-> "1b", acc |-> a, bal |-> b,
                         mbal |-> maxVBal[a], mval |-> maxVal[a]]}
  /\ UNCHANGED <<maxVBal, maxVal>>

Phase2a(b, v) ==
  /\ ~ \E m \in msgs : m.type = "2a" /\ m.bal = b
  /\ \E Q \in Quorum :
       LET Q1b == {m \in msgs : m.type = "1b" /\ m.bal = b /\ m.acc \in Q}
       IN /\ \A a \in Q : \E m \in Q1b : m.acc = a
          /\ \/ \A m \in Q1b : m.mbal = -1
             \/ \E m \in Q1b : /\ m.mval = v
                               /\ \A mm \in Q1b : m.mbal >= mm.mbal
  /\ msgs' = msgs \cup {[type |-> "2a", bal |-> b, val |-> v]}
  /\ UNCHANGED <<maxBal, maxVBal, maxVal>>

Phase2b(a, b, v) ==
  /\ [type |-> "2a", bal |-> b, val |-> v] \in msgs
  /\ b >= maxBal[a]
  /\ maxBal' = [maxBal EXCEPT ![a] = b]
  /\ maxVBal' = [maxVBal EXCEPT ![a] = b]
  /\ maxVal' = [maxVal EXCEPT ![a] = v]
  /\ msgs' = msgs \cup {[type |-> "2b", acc |-> a, bal |-> b, val |-> v]}

\* Safety: At most one value is chosen
Consistency ==
  \A v1, v2 \in Values :
    (\E Q \in Quorum : \A a \in Q : maxVal[a] = v1 /\ maxVBal[a] >= 0) /\
    (\E Q \in Quorum : \A a \in Q : maxVal[a] = v2 /\ maxVBal[a] >= 0)
    => v1 = v2
```

## Pattern 3: Leader Election

### Bully Algorithm

```tla
CONSTANTS Procs

VARIABLES
  state,        \* state[p]: "follower", "candidate", "leader"
  leader,       \* Current leader (or None)
  msgs

TypeOK ==
  /\ state \in [Procs -> {"follower", "candidate", "leader"}]
  /\ leader \in Procs \cup {None}

Init ==
  /\ state = [p \in Procs |-> "follower"]
  /\ leader = None
  /\ msgs = {}

StartElection(p) ==
  /\ state[p] = "follower"
  /\ state' = [state EXCEPT ![p] = "candidate"]
  /\ msgs' = msgs \cup {[type |-> "Election", from |-> p, to |-> q] : q \in Procs, q > p}
  /\ UNCHANGED leader

RespondToElection(p, q) ==
  /\ [type |-> "Election", from |-> q, to |-> p] \in msgs
  /\ p > q
  /\ msgs' = msgs \cup {[type |-> "OK", from |-> p, to |-> q]}
  /\ state' = [state EXCEPT ![p] = "candidate"]
  /\ UNCHANGED leader

BecomeLeader(p) ==
  /\ state[p] = "candidate"
  /\ ~ \E q \in Procs : q > p /\ [type |-> "OK", from |-> q, to |-> p] \in msgs
  /\ state' = [state EXCEPT ![p] = "leader"]
  /\ leader' = p
  /\ msgs' = msgs \cup {[type |-> "Coordinator", from |-> p, to |-> q] : q \in Procs}

\* Safety: At most one leader
LeaderUniqueness == \A p, q \in Procs :
  state[p] = "leader" /\ state[q] = "leader" => p = q
```

## Pattern 4: Replication

### Primary-Backup Replication

```tla
CONSTANTS
  Primary,
  Backups,
  Operations

VARIABLES
  primaryLog,   \* Log at primary
  backupLog,    \* Log at each backup
  committed,    \* Committed operations
  msgs

Replicas == {Primary} \cup Backups

TypeOK ==
  /\ primaryLog \in Seq(Operations)
  /\ backupLog \in [Backups -> Seq(Operations)]
  /\ committed \in SUBSET Operations

Init ==
  /\ primaryLog = <<>>
  /\ backupLog = [b \in Backups |-> <<>>]
  /\ committed = {}
  /\ msgs = {}

ClientRequest(op) ==
  /\ primaryLog' = Append(primaryLog, op)
  /\ msgs' = msgs \cup {[type |-> "Replicate", op |-> op, to |-> b] : b \in Backups}
  /\ UNCHANGED <<backupLog, committed>>

BackupAck(b, op) ==
  /\ [type |-> "Replicate", op |-> op, to |-> b] \in msgs
  /\ backupLog' = [backupLog EXCEPT ![b] = Append(@, op)]
  /\ msgs' = msgs \cup {[type |-> "Ack", op |-> op, from |-> b]}
  /\ UNCHANGED <<primaryLog, committed>>

Commit(op) ==
  /\ op \in DOMAIN primaryLog
  /\ \A b \in Backups : [type |-> "Ack", op |-> op, from |-> b] \in msgs
  /\ committed' = committed \cup {op}
  /\ UNCHANGED <<primaryLog, backupLog, msgs>>

\* Safety: All replicas have same committed operations
Consistency == \A b \in Backups :
  \A i \in DOMAIN backupLog[b] :
    backupLog[b][i] \in committed => backupLog[b][i] = primaryLog[i]
```

## Pattern 5: Distributed Transactions

### Snapshot Isolation

```tla
CONSTANTS
  Txns,         \* Transaction IDs
  Keys,         \* Data keys
  Values

VARIABLES
  store,        \* Versioned key-value store
  snapshots,    \* Snapshot for each transaction
  writeSet,     \* Write set for each transaction
  committed     \* Committed transactions

TypeOK ==
  /\ store \in [Keys -> Seq([val: Values, txn: Txns])]
  /\ snapshots \in [Txns -> [Keys -> Values]]
  /\ writeSet \in [Txns -> [Keys -> Values]]
  /\ committed \in SUBSET Txns

Init ==
  /\ store = [k \in Keys |-> <<>>]
  /\ snapshots = [t \in Txns |-> [k \in Keys |-> InitialValue]]
  /\ writeSet = [t \in Txns |-> [k \in Keys |-> NoValue]]
  /\ committed = {}

BeginTxn(t) ==
  /\ t \notin committed
  /\ snapshots' = [snapshots EXCEPT ![t] = [k \in Keys |-> LatestValue(store[k])]]
  /\ UNCHANGED <<store, writeSet, committed>>

Read(t, k) ==
  /\ t \notin committed
  /\ snapshots[t][k]  \* Returns snapshot value
  /\ UNCHANGED <<store, snapshots, writeSet, committed>>

Write(t, k, v) ==
  /\ t \notin committed
  /\ writeSet' = [writeSet EXCEPT ![t][k] = v]
  /\ UNCHANGED <<store, snapshots, committed>>

CommitTxn(t) ==
  /\ t \notin committed
  /\ NoConflicts(t, writeSet[t])
  /\ store' = ApplyWrites(store, t, writeSet[t])
  /\ committed' = committed \cup {t}
  /\ UNCHANGED <<snapshots, writeSet>>

\* Safety: Snapshot isolation guarantees
SnapshotIsolation ==
  \A t1, t2 \in committed :
    t1 /= t2 => NoWriteWriteConflict(t1, t2)
```

## Tips for Distributed Systems

1. **Model network explicitly** - Use message sets or channels
2. **Handle message loss** - Non-deterministically drop messages
3. **Model failures** - Process crashes, network partitions
4. **Use quorums** - For fault tolerance and consistency
5. **Check safety first** - Then add liveness properties
6. **Start with small models** - N=2 or N=3 processes
7. **Use symmetry** - Reduce state space for identical processes
8. **Abstract data** - Focus on protocol, not data values
