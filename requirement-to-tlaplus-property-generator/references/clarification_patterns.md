# Clarification Question Patterns

This document provides templates for asking clarifying questions when requirements are ambiguous or underspecified.

## Table of Contents

1. [Temporal Scope Questions](#temporal-scope-questions)
2. [Quantifier Questions](#quantifier-questions)
3. [Boundary Condition Questions](#boundary-condition-questions)
4. [State Variable Questions](#state-variable-questions)
5. [Fairness and Scheduling Questions](#fairness-and-scheduling-questions)
6. [Exception Handling Questions](#exception-handling-questions)

---

## Temporal Scope Questions

### Pattern: "Eventually" Ambiguity

**Requirement**: "The system eventually completes the task"

**Ambiguity**: Does "eventually" mean:
- Within a bounded time?
- Unbounded but guaranteed?
- Under certain fairness assumptions?

**Clarifying Questions**:
1. "Should the task complete within a specific time bound, or is unbounded eventual completion acceptable?"
2. "Are there any fairness assumptions (e.g., weak fairness, strong fairness) that should apply?"
3. "Can the system indefinitely postpone completion, or must it make progress?"

**Resolution Options**:
- **Unbounded liveness**: `<>(task_completed)`
- **With fairness**: `WF_vars(CompleteTask)` or `SF_vars(CompleteTask)`
- **Bounded (requires counter)**: `<>(task_completed \/ timeout)`

---

### Pattern: "Always" Scope

**Requirement**: "The buffer is always non-empty"

**Ambiguity**: Does "always" mean:
- In all reachable states?
- After initialization?
- During a specific phase?

**Clarifying Questions**:
1. "Should the buffer be non-empty from the initial state, or only after initialization completes?"
2. "Are there any phases where the buffer is allowed to be empty?"
3. "Does this apply to all execution paths or only under certain conditions?"

**Resolution Options**:
- **All states**: `[](Len(buffer) > 0)`
- **After init**: `[](initialized => Len(buffer) > 0)`
- **Conditional**: `[](active_phase => Len(buffer) > 0)`

---

### Pattern: "Until" Semantics

**Requirement**: "Property P holds until event E occurs"

**Ambiguity**: After E occurs:
- Can P become false?
- Must P remain true?
- Is there a guarantee E will occur?

**Clarifying Questions**:
1. "After event E occurs, can property P become false?"
2. "Is event E guaranteed to eventually occur?"
3. "What happens if E never occurs?"

**Resolution Options**:
- **Weak until**: `P \/ <>E` (P holds or E eventually occurs)
- **Strong until**: `P /\ <>E` (P holds AND E eventually occurs)
- **Leads-to**: `P ~> E` (P eventually leads to E)

---

## Quantifier Questions

### Pattern: Universal Quantifier Scope

**Requirement**: "All processes must complete"

**Ambiguity**: Does "all" mean:
- All processes that exist initially?
- All processes ever created?
- All currently active processes?

**Clarifying Questions**:
1. "Should this apply to all processes that exist at initialization, or all processes ever created during execution?"
2. "Are there any processes that are exempt from this requirement?"
3. "What about processes created dynamically?"

**Resolution Options**:
- **Fixed set**: `\A p \in InitialProcesses : completed[p]`
- **All ever created**: `\A p \in AllProcesses : completed[p]`
- **Currently active**: `\A p \in {p \in Processes : active[p]} : completed[p]`

---

### Pattern: Existential Quantifier

**Requirement**: "At least one server must be available"

**Ambiguity**: Does this mean:
- At every moment in time?
- Eventually?
- After some initialization period?

**Clarifying Questions**:
1. "Must at least one server be available at all times, or just eventually?"
2. "Is there an initialization period where no servers need to be available?"
3. "What happens during server restarts or maintenance?"

**Resolution Options**:
- **Always**: `[](\E s \in Servers : available[s])`
- **Eventually**: `<>(\E s \in Servers : available[s])`
- **After init**: `[](initialized => \E s \in Servers : available[s])`

---

## Boundary Condition Questions

### Pattern: Range Boundaries

**Requirement**: "The value must be between 0 and 100"

**Ambiguity**: Are the boundaries:
- Inclusive (0 ≤ value ≤ 100)?
- Exclusive (0 < value < 100)?
- Mixed (0 ≤ value < 100)?

**Clarifying Questions**:
1. "Should the boundaries be inclusive or exclusive?"
2. "Can the value be exactly 0 or exactly 100?"

**Resolution Options**:
- **Inclusive**: `value \in 0..100` or `value >= 0 /\ value <= 100`
- **Exclusive**: `value > 0 /\ value < 100`
- **Mixed**: `value >= 0 /\ value < 100`

---

### Pattern: Empty Set Handling

**Requirement**: "All elements in the set satisfy property P"

**Ambiguity**: If the set is empty:
- Is the property vacuously true?
- Is this an error condition?

**Clarifying Questions**:
1. "If the set is empty, should the property be considered satisfied (vacuously true)?"
2. "Should an empty set be treated as an error or invalid state?"

**Resolution Options**:
- **Vacuously true**: `\A x \in S : P(x)` (standard TLA+ semantics)
- **Require non-empty**: `S # {} /\ \A x \in S : P(x)`

---

## State Variable Questions

### Pattern: Undefined Variables

**Requirement**: "The counter increments when the button is pressed"

**Ambiguity**: Missing information:
- What is the initial value of counter?
- What is the type/range of counter?
- Can counter overflow?

**Clarifying Questions**:
1. "What is the initial value of the counter?"
2. "Is there a maximum value for the counter, or can it grow unbounded?"
3. "What happens if the counter reaches its maximum value?"

**Resolution Options**:
- **Natural numbers**: `counter \in Nat /\ counter' = counter + 1`
- **Bounded**: `counter \in 0..MAX /\ counter' = IF counter < MAX THEN counter + 1 ELSE counter`
- **Wrapping**: `counter' = (counter + 1) % MAX`

---

### Pattern: Implicit State

**Requirement**: "The system processes requests in order"

**Ambiguity**: What state is needed:
- Queue of pending requests?
- Timestamps for ordering?
- Request IDs?

**Clarifying Questions**:
1. "How are requests ordered? By arrival time, priority, or some other criterion?"
2. "Should the system maintain a queue, or just track ordering metadata?"
3. "What happens to completed requests?"

**Resolution Options**:
- **Queue-based**: `requests \in Seq(Request)`
- **Timestamp-based**: `\A r1, r2 \in Requests : r1.time < r2.time => ...`
- **ID-based**: `\A r1, r2 \in Requests : r1.id < r2.id => ...`

---

## Fairness and Scheduling Questions

### Pattern: Fair Access

**Requirement**: "All processes get fair access to the resource"

**Ambiguity**: What kind of fairness:
- Weak fairness (continuously enabled → eventually executed)?
- Strong fairness (infinitely often enabled → eventually executed)?
- Bounded fairness (access within N steps)?

**Clarifying Questions**:
1. "Should this be weak fairness (if continuously enabled, eventually executes) or strong fairness (if infinitely often enabled, eventually executes)?"
2. "Is there a bound on how long a process can wait?"
3. "Should all processes have equal priority, or are there priority levels?"

**Resolution Options**:
- **Weak fairness**: `WF_vars(Access(p))`
- **Strong fairness**: `SF_vars(Access(p))`
- **Bounded**: Requires auxiliary counter variable

---

### Pattern: Progress Guarantee

**Requirement**: "The system makes progress"

**Ambiguity**: What constitutes progress:
- Any state change?
- Specific meaningful actions?
- Completion of work units?

**Clarifying Questions**:
1. "What counts as progress? Any state change, or only specific actions?"
2. "Can the system make progress by performing internal actions, or must it complete external work?"
3. "Is stuttering (no state change) allowed indefinitely?"

**Resolution Options**:
- **Any change**: `[]<>(state_changed)`
- **Specific action**: `[]<>(MeaningfulAction)`
- **Work completion**: `[]<>(work_completed)`

---

## Exception Handling Questions

### Pattern: Error Conditions

**Requirement**: "The system handles errors gracefully"

**Ambiguity**: What does "gracefully" mean:
- Return to a safe state?
- Log the error and continue?
- Retry the operation?

**Clarifying Questions**:
1. "When an error occurs, should the system return to a safe state, retry, or continue with degraded functionality?"
2. "Are there different error handling strategies for different types of errors?"
3. "Should error recovery be guaranteed (liveness) or just possible (safety)?"

**Resolution Options**:
- **Safe state**: `[](error_occurred => <>safe_state)`
- **Retry**: `[](error_occurred => <>(retry \/ success))`
- **Continue**: `[](error_occurred => logged /\ operational)`

---

### Pattern: Timeout Behavior

**Requirement**: "Operations timeout after a period"

**Ambiguity**: After timeout:
- Is the operation cancelled?
- Can it still complete?
- What is the timeout value?

**Clarifying Questions**:
1. "After a timeout, is the operation cancelled, or can it still complete?"
2. "What is the specific timeout duration?"
3. "Should timeouts be modeled explicitly with a clock variable?"

**Resolution Options**:
- **Cancellation**: `[](timeout => cancelled)`
- **Best effort**: `[](timeout => (cancelled \/ completed))`
- **With clock**: `[](clock - start_time > TIMEOUT => timeout)`

---

## General Question Templates

### When Requirement is Vague

"I notice the requirement mentions [CONCEPT]. Could you clarify:
1. [SPECIFIC ASPECT 1]?
2. [SPECIFIC ASPECT 2]?
3. [SPECIFIC ASPECT 3]?"

### When Multiple Interpretations Exist

"The requirement '[REQUIREMENT]' could be interpreted as:
- Option A: [INTERPRETATION A]
- Option B: [INTERPRETATION B]

Which interpretation is correct, or is there a different meaning?"

### When Context is Missing

"To properly formalize this requirement, I need to know:
1. [MISSING CONTEXT 1]
2. [MISSING CONTEXT 2]

Could you provide this information?"

### When Assumptions are Needed

"I'm assuming [ASSUMPTION] based on the requirement. Is this correct?
If not, please clarify [SPECIFIC ASPECT]."

---

## Best Practices for Asking Questions

1. **Be specific**: Ask about concrete aspects, not general clarifications
2. **Offer options**: Provide 2-3 interpretations when possible
3. **Explain impact**: Briefly mention why the clarification matters
4. **Limit questions**: Ask 2-4 questions at a time, not overwhelming lists
5. **Suggest defaults**: Offer a reasonable default interpretation
6. **Use examples**: Illustrate ambiguities with concrete scenarios
