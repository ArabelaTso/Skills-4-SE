---
name: requirement-to-tlaplus-property-generator
description: Automatically derives TLA+ properties (invariants, safety, liveness) from natural-language requirements or structured requirement documents. Resolves ambiguities, asks clarifying questions for underspecified requirements, and outputs TLA+-compatible property definitions with semantic explanations. Use when translating system requirements, specifications, or behavioral constraints into formal TLA+ temporal logic properties for verification with TLC model checker.
---

# Requirement to TLA+ Property Generator

## Overview

This skill transforms natural-language requirements into formal TLA+ properties, enabling rigorous verification of system specifications. It handles invariants, safety properties, and liveness properties, resolving ambiguities and seeking clarification when needed.

## Workflow

### Step 1: Analyze the Requirement

Parse and understand the input requirement:

1. **Identify requirement type**:
   - Invariant: "The system always maintains property P"
   - Safety: "Bad thing X never happens"
   - Liveness: "Good thing Y eventually happens"
   - Fairness: "Process Z gets a fair chance"

2. **Extract key elements**:
   - State variables involved
   - Conditions and constraints
   - Temporal aspects (always, eventually, until, etc.)
   - Quantifiers (for all, exists)

3. **Detect ambiguities**:
   - Undefined terms or variables
   - Unclear temporal scope
   - Missing boundary conditions
   - Implicit assumptions

### Step 2: Resolve Ambiguities

When ambiguities are detected, use one of these strategies:

**Strategy A: Reasonable Interpretation**
If the ambiguity has a standard interpretation in the domain, resolve it automatically and document the assumption.

Example:
- Requirement: "The buffer never overflows"
- Interpretation: "buffer_size <= MAX_BUFFER_SIZE" (assuming MAX_BUFFER_SIZE is defined)

**Strategy B: Ask Clarifying Questions**
For critical or non-obvious ambiguities, ask the user:

- "Does 'eventually' mean within a bounded time or unbounded?"
- "Should this property hold for all processes or just specific ones?"
- "What is the initial state assumption?"

See [references/clarification_patterns.md](references/clarification_patterns.md) for common question templates.

### Step 3: Map to TLA+ Constructs

Translate the requirement into TLA+ syntax:

**Invariants** (Type Invariant or State Predicate):
```tla
TypeOK == /\ var1 \in ValidSet1
          /\ var2 \in ValidSet2
          /\ condition

StateInvariant == predicate_over_state_variables
```

**Safety Properties** (Always):
```tla
Safety == []P  \* P holds in all reachable states
```

**Liveness Properties** (Eventually):
```tla
Liveness == <>P  \* P eventually holds
Liveness2 == [](P => <>Q)  \* If P holds, Q eventually holds
```

**Fairness**:
```tla
Fairness == WF_vars(Action)  \* Weak fairness
Fairness2 == SF_vars(Action)  \* Strong fairness
```

See [references/tlaplus_syntax.md](references/tlaplus_syntax.md) for comprehensive syntax reference.

### Step 4: Generate TLA+ Property Definition

Create the complete property definition:

1. **Choose appropriate name**: Descriptive and follows TLA+ conventions
2. **Write the formula**: Use correct TLA+ temporal operators
3. **Add comments**: Explain the property's intent
4. **Include in spec**: Show where to place it in the TLA+ module

Example output:
```tla
\* Property: Buffer never overflows
\* Requirement: "The system must ensure the buffer size never exceeds capacity"
\* Type: Safety (Invariant)
BufferSafety == buffer_size <= MAX_BUFFER_SIZE

\* Add to specification:
\* Spec == Init /\ [][Next]_vars /\ BufferSafety
```

### Step 5: Provide Semantic Explanation

Explain what the property means:

1. **Plain English**: Restate in clear, unambiguous language
2. **Violation scenario**: Describe what would violate this property
3. **Verification approach**: How TLC will check it
4. **Related properties**: Mention dependencies or related properties

## Common Requirement Patterns

### Pattern 1: Mutual Exclusion
**Requirement**: "At most one process can be in the critical section"

**TLA+ Property**:
```tla
MutualExclusion ==
    \A p1, p2 \in Processes :
        (p1 # p2) => ~(pc[p1] = "critical" /\ pc[p2] = "critical")
```

### Pattern 2: Eventual Progress
**Requirement**: "Every request is eventually served"

**TLA+ Property**:
```tla
EventualService ==
    \A req \in Requests :
        (req.status = "pending") ~> (req.status = "completed")
```

### Pattern 3: Bounded Response
**Requirement**: "The system responds within N steps"

**TLA+ Property**:
```tla
\* Note: TLA+ doesn't directly express bounded liveness
\* Use auxiliary counter variable
BoundedResponse ==
    [](request_made => <>(response_sent \/ timeout_counter > N))
```

### Pattern 4: Ordering Constraint
**Requirement**: "Event A must occur before event B"

**TLA+ Property**:
```tla
OrderingConstraint ==
    [](event_B_occurred => event_A_occurred_before)
```

See [references/requirement_patterns.md](references/requirement_patterns.md) for more patterns.

## Handling Complex Requirements

### Compound Requirements
Break down complex requirements into multiple properties:

**Requirement**: "The system must process requests in FIFO order and complete each within 10 steps"

**Decomposition**:
1. FIFO ordering property
2. Bounded completion property
3. Conjunction of both

### Conditional Requirements
Use implication for conditional properties:

**Requirement**: "If the system is in safe mode, no writes are allowed"

**TLA+ Property**:
```tla
SafeModeConstraint == [](safe_mode => ~write_enabled)
```

### Quantified Requirements
Use TLA+ quantifiers appropriately:

**Requirement**: "All active processes eventually terminate"

**TLA+ Property**:
```tla
AllTerminate ==
    \A p \in Processes :
        (status[p] = "active") ~> (status[p] = "terminated")
```

## Best Practices

1. **Start simple**: Begin with basic invariants before complex temporal properties
2. **Be explicit**: Document all assumptions and interpretations
3. **Use meaningful names**: Property names should reflect their purpose
4. **Test incrementally**: Verify simple properties first
5. **Consider negation**: Sometimes it's easier to express "bad thing never happens"
6. **Check consistency**: Ensure properties don't contradict each other

## Common Pitfalls

**Pitfall 1**: Confusing safety and liveness
- Safety: "Nothing bad happens" ([]P)
- Liveness: "Something good happens" (<>P)

**Pitfall 2**: Unbounded liveness without fairness
- Liveness properties often require fairness assumptions

**Pitfall 3**: Over-specification
- Too many constraints may make the spec unrealizable

**Pitfall 4**: Implicit state assumptions
- Always make initial state assumptions explicit

## Output Format

For each requirement, provide:

1. **Original Requirement**: Quote the input
2. **Property Type**: Invariant/Safety/Liveness/Fairness
3. **TLA+ Definition**: Complete, syntactically correct property
4. **Semantic Explanation**: What it means in plain language
5. **Assumptions**: Any assumptions made during translation
6. **Integration**: How to add it to the TLA+ specification
7. **Verification Notes**: Tips for checking with TLC

## References

- [references/tlaplus_syntax.md](references/tlaplus_syntax.md): Complete TLA+ temporal logic syntax
- [references/requirement_patterns.md](references/requirement_patterns.md): Common requirement-to-property mappings
- [references/clarification_patterns.md](references/clarification_patterns.md): Question templates for ambiguous requirements
