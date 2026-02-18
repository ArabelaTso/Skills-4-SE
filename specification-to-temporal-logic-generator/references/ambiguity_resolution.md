# Ambiguity Resolution Guidelines

## Common Ambiguities in Requirements

### 1. Temporal Scope Ambiguity

**Ambiguous**: "The system responds to requests"

**Clarifications needed**:
- Does EVERY request get a response? → `G(request -> F response)`
- Or can SOME requests go unanswered? → `G(request -> EF response)` (CTL)
- Is there a time bound? → `G(request -> F[0,t] response)`

**Resolution strategy**: Ask "Does this apply to all cases or just some cases?"

### 2. Ordering Ambiguity

**Ambiguous**: "Authentication before access"

**Clarifications needed**:
- Must authentication happen IMMEDIATELY before? → `G(access -> X authenticated)`
- Or just SOMETIME before? → `(!access) U authenticated`
- Can access happen without authentication? → Determines if it's `->` or `<->`

**Resolution strategy**: Ask "Must X happen immediately before Y, or just at some earlier point?"

### 3. Duration Ambiguity

**Ambiguous**: "The alarm stays on"

**Clarifications needed**:
- Forever once triggered? → `G(alarm_on -> G alarm_on)`
- Until some condition? → `G(alarm_on -> (alarm_on U acknowledged))`
- For a specific duration? → `G(alarm_on -> (alarm_on U[t,t] !alarm_on))`

**Resolution strategy**: Ask "How long should this condition persist?"

### 4. Frequency Ambiguity

**Ambiguous**: "The system performs maintenance"

**Clarifications needed**:
- At least once? → `F maintenance`
- Infinitely often? → `G F maintenance`
- Periodically with bounds? → `G(maintenance -> F[t1,t2] maintenance)`

**Resolution strategy**: Ask "How often should this occur?"

### 5. Quantification Ambiguity

**Ambiguous**: "Requests are processed"

**Clarifications needed**:
- ALL requests? → `G(request -> F processed)`
- SOME requests? → `EF(request && F processed)`
- AT LEAST ONE request? → `F(request && F processed)`

**Resolution strategy**: Ask "Does this apply to all instances or just some?"

### 6. Causality Ambiguity

**Ambiguous**: "When the button is pressed, the light turns on"

**Clarifications needed**:
- EVERY press causes light on? → `G(press -> F light_on)`
- Press is NECESSARY for light? → `G(light_on -> press)`
- Press is SUFFICIENT for light? → `G(press -> light_on)`
- Both necessary and sufficient? → `G(press <-> light_on)`

**Resolution strategy**: Ask "Is X necessary, sufficient, or both for Y?"

### 7. Negation Scope Ambiguity

**Ambiguous**: "The system doesn't always respond"

**Clarifications needed**:
- Sometimes doesn't respond? → `F(!response)` or `!(G response)`
- Never responds? → `G(!response)`

**Resolution strategy**: Ask "Does 'not always' mean 'sometimes not' or 'never'?"

### 8. Conditional Ambiguity

**Ambiguous**: "If the sensor fails, the system shuts down"

**Clarifications needed**:
- Immediate shutdown? → `G(sensor_fail -> X shutdown)`
- Eventually shuts down? → `G(sensor_fail -> F shutdown)`
- Shuts down only if sensor fails? → `G(shutdown -> sensor_fail)`

**Resolution strategy**: Ask "Is this an immediate or eventual consequence?"

## Disambiguation Questions to Ask

### For Safety Properties:
1. "Should this NEVER happen, or just not happen USUALLY?"
2. "Are there any exceptions to this rule?"
3. "What should happen if this condition is violated?"

### For Liveness Properties:
1. "Must this ALWAYS eventually happen, or just SOMETIMES?"
2. "Is there a time limit for when this should occur?"
3. "Can this be delayed indefinitely under certain conditions?"

### For Response Properties:
1. "Must EVERY occurrence of X lead to Y?"
2. "Should Y happen IMMEDIATELY after X, or just EVENTUALLY?"
3. "Can Y happen without X occurring first?"

### For Ordering Properties:
1. "Must X happen DIRECTLY before Y, or just SOMETIME before?"
2. "Can Y ever happen without X?"
3. "Can X happen multiple times before Y?"

## Resolution Strategies

### Strategy 1: Provide Options
When ambiguous, present multiple interpretations:
```
"The system responds to requests" could mean:
1. Every request gets a response: G(request -> F response)
2. Requests eventually get responses: F(request -> response)
3. Some requests get responses: EF(request && response)
Which interpretation matches your intent?
```

### Strategy 2: Use Domain Knowledge
Apply common patterns from the domain:
- Safety-critical systems: Assume universal quantification (all, always)
- Real-time systems: Assume bounded time constraints
- Concurrent systems: Consider fairness assumptions

### Strategy 3: Conservative Interpretation
When in doubt, choose the stronger (more restrictive) property:
- "Eventually" → Assume "always eventually" (G F) rather than "sometime" (F)
- "Before" → Assume "immediately before" (X) rather than "sometime before" (U)

### Strategy 4: Explicit Assumptions
State assumptions clearly in the output:
```
Formula: G(request -> F response)
Assumption: "Every request" means all requests, not just some
Assumption: "Responds" means eventually, with no time bound
If these assumptions are incorrect, please clarify.
```

## Common Requirement Patterns and Their Clarifications

| Ambiguous Requirement | Clarification Needed | Possible Formulas |
|----------------------|---------------------|-------------------|
| "X happens before Y" | Immediately or eventually? | `X U Y` or `G(Y -> X)` |
| "X leads to Y" | Always or sometimes? | `G(X -> F Y)` or `EF(X && F Y)` |
| "X is always true" | Globally or eventually forever? | `G X` or `F G X` |
| "X never happens" | On all paths or some path? | `AG(!X)` or `!EF X` |
| "X happens infinitely often" | Required or possible? | `G F X` or `EG F X` |
| "X until Y" | Strong or weak until? | `X U Y` or `X W Y` |

## Handling Implicit Requirements

Some requirements have implicit temporal aspects:

**"The door is locked"**
- Implicit: Always locked? → `G locked`
- Or: Currently locked? → `locked` (state assertion)
- Or: Eventually locked? → `F locked`

**"The system is safe"**
- Implicit: Always safe? → `G safe`
- Or: Can reach safe state? → `EF safe`
- Or: Eventually safe forever? → `F G safe`

**Resolution**: Ask "Is this a current state, a persistent property, or an eventual goal?"
