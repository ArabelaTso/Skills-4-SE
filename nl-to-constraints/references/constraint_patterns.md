# Constraint Patterns and Templates

This reference provides patterns for extracting and formalizing constraints from natural language.

## Common Constraint Categories

### 1. Data Constraints

**Pattern Recognition:**
- "must be", "should contain", "cannot exceed", "at least", "no more than"
- Data type specifications, format requirements, range limits

**Extraction Template:**
```
Field: [field_name]
Type: [data_type]
Constraints:
  - Format: [pattern/regex if applicable]
  - Range: [min-max if applicable]
  - Required: [true/false]
  - Default: [value if applicable]
  - Allowed Values: [enum if applicable]
```

**Example:**
Natural Language: "The user's email must be a valid email address and is required"
```
Field: email
Type: string
Constraints:
  - Format: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
  - Required: true
```

### 2. Business Rules

**Pattern Recognition:**
- "only if", "when", "unless", "requires", "depends on"
- Conditional logic, state-dependent behavior

**Extraction Template:**
```
Rule: [rule_name]
Condition: [precondition]
Action: [what must happen]
Exception: [edge cases]
```

**Example:**
Natural Language: "Users can only submit orders if their account balance is positive"
```
Rule: Order_Submission_Check
Condition: user.account_balance > 0
Action: Allow order submission
Exception: If user.account_balance <= 0, display "Insufficient funds" error
```

### 3. Temporal Constraints

**Pattern Recognition:**
- "before", "after", "within", "during", "between"
- Time-based conditions, deadlines, sequences

**Extraction Template:**
```
Event: [event_name]
Timing: [when it occurs]
Duration: [how long]
Sequence: [order relative to other events]
```

**Example:**
Natural Language: "Password reset links expire 24 hours after creation"
```
Event: Password_Reset_Link_Expiration
Timing: 24 hours after link creation
Action: Invalidate reset link
Validation: If current_time > (link_created_at + 24h), reject reset
```

### 4. State Constraints

**Pattern Recognition:**
- "status", "state", "when in", "while", "during"
- Valid states, state transitions, state-dependent behavior

**Extraction Template:**
```
Entity: [entity_name]
Valid States: [list of states]
Transitions:
  - From: [state] → To: [state] | Condition: [when allowed]
State Rules:
  - State: [state] | Allowed Actions: [list]
```

**Example:**
Natural Language: "An order can be cancelled only when it's in pending or processing status, but not when it's shipped"
```
Entity: Order
Valid States: [pending, processing, shipped, delivered, cancelled]
Transitions:
  - From: pending → To: cancelled | Condition: user_request OR timeout
  - From: processing → To: cancelled | Condition: user_request AND not_yet_shipped
  - From: shipped → To: cancelled | Condition: FORBIDDEN
```

### 5. Authorization/Permission Constraints

**Pattern Recognition:**
- "only", "authorized", "admin", "role", "permissions"
- Access control, role-based rules

**Extraction Template:**
```
Resource: [what is being accessed]
Action: [what operation]
Allowed Roles: [who can do it]
Conditions: [additional requirements]
```

**Example:**
Natural Language: "Only administrators can delete user accounts"
```
Resource: User Account
Action: DELETE
Allowed Roles: [administrator]
Conditions: user.role == 'administrator' AND target_user != self
```

### 6. Cardinality/Relationship Constraints

**Pattern Recognition:**
- "one", "many", "multiple", "each", "every", "at least one"
- Quantity relationships, multiplicities

**Extraction Template:**
```
Entity A: [first entity]
Relationship: [type of relationship]
Entity B: [second entity]
Cardinality: [A:B ratio]
```

**Example:**
Natural Language: "Each order must have at least one item and can have up to 100 items"
```
Entity A: Order
Relationship: contains
Entity B: OrderItem
Cardinality: 1:N where N >= 1 AND N <= 100
Constraint: COUNT(order.items) >= 1 AND COUNT(order.items) <= 100
```

### 7. Performance Constraints

**Pattern Recognition:**
- "within X seconds", "respond in", "no more than", "at least X per"
- Response times, throughput, latency

**Extraction Template:**
```
Operation: [what operation]
Performance Metric: [what to measure]
Threshold: [acceptable limit]
Measurement Context: [conditions]
```

**Example:**
Natural Language: "The search API must return results within 500ms for 95% of requests"
```
Operation: Search API
Performance Metric: Response time
Threshold: <= 500ms
Measurement Context: 95th percentile of all requests
```

## Signal Words and Phrases

### Mandatory Constraints
- **Must**, **shall**, **required**, **mandatory**, **necessary**
- Action: Create hard constraint with validation

### Optional/Desirable
- **Should**, **recommended**, **preferred**, **ideally**
- Action: Create soft constraint or guideline

### Prohibited
- **Must not**, **shall not**, **cannot**, **forbidden**, **prohibited**
- Action: Create negative constraint with rejection rule

### Conditional
- **If**, **when**, **unless**, **provided that**, **in case of**
- Action: Create conditional constraint with preconditions

### Quantitative
- **All**, **every**, **each**, **any**, **none**, **at least**, **no more than**, **exactly**
- Action: Create cardinality or range constraint

## Ambiguity Detection

Flag these patterns as needing clarification:

1. **Vague quantifiers**: "many", "few", "some", "often", "rarely"
2. **Unclear scope**: "the system", "users", "data" (which system? which users?)
3. **Missing edge cases**: No mention of error conditions or boundary cases
4. **Conflicting signals**: "should" with "required" in same requirement
5. **Undefined terms**: Domain-specific jargon without definition

When ambiguity detected:
- Flag the ambiguous element
- List possible interpretations
- Request clarification with specific questions
