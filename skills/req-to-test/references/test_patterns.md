# Test Scenario Patterns and Templates

This reference provides comprehensive patterns for generating test scenarios from requirements.

## Table of Contents

1. [BDD/Gherkin Scenarios](#bddgherkin-scenarios)
2. [Unit Test Cases](#unit-test-cases)
3. [Integration Test Scenarios](#integration-test-scenarios)
4. [E2E Test Scenarios](#e2e-test-scenarios)
5. [Coverage Patterns](#coverage-patterns)
6. [Edge Case Identification](#edge-case-identification)

---

## BDD/Gherkin Scenarios

### Basic Structure

```gherkin
Feature: [Feature Name]
  As a [role]
  I want to [action]
  So that [benefit]

  Scenario: [Scenario Name]
    Given [precondition/context]
    When [action/event]
    Then [expected outcome]
    And [additional expectation]

  Scenario Outline: [Parameterized Scenario Name]
    Given [precondition with <parameter>]
    When [action with <parameter>]
    Then [expected outcome with <parameter>]

    Examples:
      | parameter1 | parameter2 | expected_result |
      | value1     | value2     | result1         |
```

### Happy Path Pattern

```gherkin
Scenario: Successful [action] with valid inputs
  Given [system is in ready state]
  And [user has necessary permissions]
  When [user performs action with valid data]
  Then [action succeeds]
  And [system updates state correctly]
  And [user receives success confirmation]
```

### Error Path Pattern

```gherkin
Scenario: [Action] fails with [error condition]
  Given [system is in ready state]
  When [user performs action with invalid data]
  Then [action fails with appropriate error]
  And [system state remains unchanged]
  And [user receives helpful error message]
```

### Edge Case Pattern

```gherkin
Scenario: [Action] at boundary [condition]
  Given [boundary condition is set]
  When [user performs action at boundary]
  Then [system handles boundary correctly]
```

---

## Unit Test Cases

### Function Test Pattern

```
Test: test_[function_name]_[condition]_[expected_outcome]

Setup:
  - Initialize [dependencies/mocks]
  - Prepare [input data]

Execute:
  - Call [function] with [parameters]

Assert:
  - Result equals [expected value]
  - Side effects include [expected changes]
  - No exceptions raised

Cleanup:
  - Reset [state/mocks]
```

### Parameterized Test Pattern

```
Test Suite: [Function Name] with various inputs

Test Cases:
  | Input          | Expected Output | Description           |
  |----------------|----------------|-----------------------|
  | valid_value    | success        | Normal case           |
  | empty_string   | error          | Empty input           |
  | null           | error          | Null handling         |
  | max_value      | success        | Upper boundary        |
  | max_value + 1  | error          | Above upper boundary  |
```

### Exception Testing Pattern

```
Test: test_[function]_raises_[exception]_when_[condition]

Setup:
  - Prepare [invalid input/condition]

Execute & Assert:
  - Expect [SpecificException] when calling [function]
  - Verify exception message contains [expected text]
  - Verify exception details include [relevant info]
```

---

## Integration Test Scenarios

### API Integration Pattern

```
Scenario: [System A] integrates with [System B] for [purpose]

Setup:
  - Start [System A] in test mode
  - Mock/start [System B] endpoint
  - Configure authentication

Test Steps:
  1. [System A] sends [request type] to [System B]
  2. [System B] receives request with [expected data]
  3. [System B] responds with [response data]
  4. [System A] processes response correctly

Assertions:
  - Request format matches contract
  - Response is parsed correctly
  - Data is stored/processed as expected
  - Error handling works for failed requests

Cleanup:
  - Stop services
  - Clear test data
```

### Database Integration Pattern

```
Scenario: [Operation] persists data correctly

Setup:
  - Initialize test database
  - Seed with [initial data]

Test Steps:
  1. Perform [operation] with [test data]
  2. Commit transaction
  3. Query database for [affected records]

Assertions:
  - Records exist with correct values
  - Relationships are maintained
  - Constraints are enforced
  - Indexes are updated

Cleanup:
  - Rollback or delete test data
```

### Message Queue Integration Pattern

```
Scenario: [Service] publishes and consumes [message type]

Setup:
  - Start message broker
  - Configure test queue/topic

Test Steps:
  1. [Producer service] publishes [message]
  2. Wait for message delivery
  3. [Consumer service] receives message
  4. Consumer processes message

Assertions:
  - Message format is correct
  - Message is delivered exactly once
  - Processing completes successfully
  - Acknowledgment is sent

Cleanup:
  - Purge test queues
  - Stop broker
```

---

## E2E Test Scenarios

### User Journey Pattern

```
Feature: [User Journey Name]

Scenario: Complete [user goal] from start to finish
  Given user is on [starting page]
  And user is [authenticated/guest]

  When user navigates to [page]
  And user fills in [form field] with "[value]"
  And user clicks [button]

  Then user sees [success message]
  And user is redirected to [destination page]
  And [expected data] appears on the page

  When user performs [follow-up action]
  Then [final outcome] is achieved
```

### Multi-System Flow Pattern

```
Scenario: [Business process] across multiple systems

  Given user completes [action] in [System A]
  When [System A] triggers [event]
  Then [System B] receives [notification]

  When user navigates to [System B]
  Then user sees [updated data from System A]

  When user performs [action in System B]
  Then [System C] is notified
  And data flows to [System D]

  When user checks [final system]
  Then complete workflow is reflected
```

---

## Coverage Patterns

### Equivalence Partitioning

For requirement: "Age must be between 18 and 65"

```
Test Cases:
1. Valid partition: age = 25 (between 18 and 65)
2. Below minimum: age = 17 (< 18)
3. Minimum boundary: age = 18 (= 18)
4. Maximum boundary: age = 65 (= 65)
5. Above maximum: age = 66 (> 65)
6. Invalid type: age = "twenty" (non-numeric)
7. Null/missing: age = null
```

### State Transition Coverage

For stateful entities, test all valid and invalid transitions:

```
State Machine: Order Status
States: [Created, Pending, Processing, Shipped, Delivered, Cancelled]

Valid Transitions:
- Created → Pending ✓
- Pending → Processing ✓
- Processing → Shipped ✓
- Shipped → Delivered ✓
- Pending → Cancelled ✓

Invalid Transitions to Test:
- Delivered → Processing ✗
- Cancelled → Shipped ✗
- Shipped → Pending ✗
```

### Combination Testing

For features with multiple independent variables:

```
Feature: Search with filters
Variables:
- Category: [All, Electronics, Clothing]
- Price: [Any, <$50, $50-$100, >$100]
- Sort: [Relevance, Price, Rating]

Pairwise coverage (sample):
1. Category=All, Price=Any, Sort=Relevance
2. Category=Electronics, Price=<$50, Sort=Price
3. Category=Clothing, Price=$50-$100, Sort=Rating
4. Category=All, Price=>$100, Sort=Price
```

---

## Edge Case Identification

### Boundary Values

For any numeric constraint, test:
- Minimum value
- Minimum - 1
- Maximum value
- Maximum + 1
- Zero (if applicable)
- Negative values (if applicable)

### Special Values

**Strings:**
- Empty string ""
- Single character
- Very long string (exceeds expected limit)
- Special characters: <, >, &, ', ", \
- Unicode characters
- SQL injection attempts
- XSS attempts

**Collections:**
- Empty array/list []
- Single item
- Maximum allowed items
- Maximum + 1 items
- Null instead of collection
- Collection with null items
- Duplicates (if relevant)

**Dates/Times:**
- Current date/time
- Past dates
- Future dates
- Leap year dates (Feb 29)
- DST transition times
- Timezone edge cases
- Unix epoch (1970-01-01)
- Year 2038 problem dates

**Concurrent Operations:**
- Simultaneous reads
- Simultaneous writes to same resource
- Race conditions
- Deadlock scenarios

### Error Conditions

Test all possible error paths:

**Network Errors:**
- Timeout
- Connection refused
- DNS failure
- Partial response

**System Errors:**
- Out of memory
- Disk full
- Permission denied
- Resource unavailable

**Data Errors:**
- Malformed input
- Missing required fields
- Type mismatch
- Foreign key violation
- Unique constraint violation

---

## Test Prioritization

When generating test scenarios, prioritize:

1. **Critical path** - Core functionality users rely on
2. **High-risk areas** - Complex logic, frequent changes
3. **Frequently used features** - Common user workflows
4. **Security-sensitive** - Authentication, authorization, data access
5. **Regulatory requirements** - Compliance-mandated scenarios
6. **Edge cases** - Boundaries and error conditions
7. **Nice-to-have features** - Less critical functionality

---

## Test Data Patterns

### Realistic Test Data

Use realistic, production-like data:
- Real names (from public sources)
- Valid email formats
- Proper addresses
- Realistic dates and times
- Representative file sizes

### Negative Test Data

Include invalid data to test validation:
- Malformed emails: "notanemail", "@domain.com"
- Invalid dates: "2023-02-30", "13/45/2023"
- Out-of-range values
- SQL injection strings
- XSS payloads
- Extremely large inputs (buffer overflow attempts)

---

## Assertion Patterns

### Comprehensive Assertions

Don't just check success - verify:
- **Result value** - Is the returned value correct?
- **State changes** - Did the system state update as expected?
- **Side effects** - Were related records updated?
- **Messages** - Are user messages appropriate?
- **Logs** - Were events logged correctly?
- **Performance** - Did operation complete within SLA?

### Error Assertions

When testing error cases:
- Verify specific exception/error type
- Check error message is user-friendly
- Confirm error code is correct
- Ensure system state is unchanged or rolled back
- Validate error is logged appropriately
