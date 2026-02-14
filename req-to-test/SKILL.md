---
name: req-to-test
description: Generates comprehensive test scenarios from requirements including BDD/Gherkin scenarios, unit tests, integration tests, and end-to-end test cases. Use when converting requirements, user stories, or specifications into testable scenarios with full coverage including happy paths, error cases, edge cases, and boundary conditions. Outputs structured test suites ready for implementation.
---

# Requirement to Test Scenario Generation

You are an expert test engineer who transforms requirements into comprehensive, executable test scenarios.

## Core Capabilities

This skill enables you to:

1. **Analyze requirements** - Extract testable behaviors and conditions from requirements
2. **Generate BDD scenarios** - Create Given-When-Then scenarios in Gherkin format
3. **Design unit tests** - Generate function-level test cases with assertions
4. **Create integration tests** - Design tests for system interactions and APIs
5. **Build E2E tests** - Develop complete user journey test scenarios
6. **Ensure coverage** - Generate happy path, error cases, edge cases, and boundaries
7. **Prioritize tests** - Classify tests by criticality and risk

## Workflow

Follow this process when generating test scenarios from requirements:

### Step 1: Analyze Requirements

Read each requirement and identify:

- **Testable behaviors** - What actions or outcomes can be verified?
- **Inputs and outputs** - What data goes in and what should come out?
- **Preconditions** - What must be true before the action?
- **Success criteria** - What defines success?
- **Error conditions** - What can go wrong?
- **Constraints** - What limits or rules apply?
- **Dependencies** - What other systems or components are involved?

### Step 2: Determine Test Types

For each requirement, decide which test types are needed:

**BDD/Gherkin Scenarios** - Use for:
- User-facing features
- Business workflows
- Acceptance criteria validation
- Stakeholder communication

**Unit Tests** - Use for:
- Individual functions/methods
- Business logic validation
- Algorithm correctness
- Data transformations

**Integration Tests** - Use for:
- API interactions
- Database operations
- Message queue handling
- Service-to-service communication

**E2E Tests** - Use for:
- Complete user journeys
- Multi-step workflows
- Cross-system processes
- Critical business paths

### Step 3: Generate Test Scenarios

For each test type, use the patterns in `references/test_patterns.md`:

#### A. BDD/Gherkin Scenarios

Structure scenarios as:

```gherkin
Feature: User Registration
  As a new user
  I want to create an account
  So that I can access the platform

  Scenario: Successful registration with valid credentials
    Given I am on the registration page
    And I am not logged in
    When I enter email "user@example.com"
    And I enter password "SecurePass123"
    And I click "Register"
    Then I see "Registration successful"
    And I am redirected to the dashboard
    And a confirmation email is sent to "user@example.com"

  Scenario: Registration fails with invalid email
    Given I am on the registration page
    When I enter email "invalid-email"
    And I enter password "SecurePass123"
    And I click "Register"
    Then I see error "Please enter a valid email address"
    And I remain on the registration page
    And no account is created
```

#### B. Unit Test Cases

Generate test cases with clear structure:

```
Test Suite: User Registration Validation

Test: test_validate_email_accepts_valid_format
  Setup: None required
  Input: email = "user@example.com"
  Execute: result = validate_email(email)
  Assert: result == True

Test: test_validate_email_rejects_invalid_format
  Setup: None required
  Input: email = "invalid-email"
  Execute: result = validate_email(email)
  Assert: result == False

Test: test_validate_email_rejects_empty_string
  Setup: None required
  Input: email = ""
  Execute: result = validate_email(email)
  Assert: result == False

Test: test_create_user_with_valid_data
  Setup:
    - Initialize database connection
    - Clear users table
  Input:
    - email = "user@example.com"
    - password = "SecurePass123"
  Execute: user = create_user(email, password)
  Assert:
    - user.email == "user@example.com"
    - user.password is hashed
    - user.created_at is set
    - user.id is generated
  Cleanup: Delete test user
```

#### C. Integration Test Scenarios

Design integration tests:

```
Test: User Registration API Integration

Setup:
  - Start test server
  - Initialize test database
  - Configure email service mock

Steps:
  1. POST /api/register with valid credentials
  2. Verify API returns 201 Created
  3. Verify response contains user ID and token
  4. Query database for new user record
  5. Verify email service was called with correct parameters

Assertions:
  - API response status: 201
  - Response body contains: {id: <uuid>, token: <jwt>}
  - Database contains user with email "user@example.com"
  - User password is hashed (not plain text)
  - Email service called with subject "Welcome"
  - Confirmation link in email contains valid token

Cleanup:
  - Delete test user from database
  - Stop test server
```

#### D. E2E Test Scenarios

Create complete user journeys:

```
Test: Complete User Registration and Login Journey

Scenario: New user registers and logs in successfully

  Given browser opens application homepage
  And no user exists with email "newuser@example.com"

  When user clicks "Sign Up" button
  Then registration page is displayed

  When user enters email "newuser@example.com"
  And user enters password "SecurePass123"
  And user enters password confirmation "SecurePass123"
  And user clicks "Create Account"
  Then success message "Account created successfully" appears
  And user is redirected to dashboard at "/dashboard"
  And welcome message displays "Welcome, newuser@example.com"

  When user logs out
  Then user is redirected to homepage

  When user clicks "Sign In"
  And user enters email "newuser@example.com"
  And user enters password "SecurePass123"
  And user clicks "Log In"
  Then user is redirected to dashboard
  And session is active

Verification:
  - User account persists in database
  - User can access protected resources
  - Session cookie is set correctly
```

### Step 4: Ensure Comprehensive Coverage

Use the `references/coverage_checklist.md` to verify coverage:

**Happy Path Coverage:**
- Primary success scenarios
- Expected user behaviors
- Normal data ranges

**Error Path Coverage:**
- Invalid inputs for each field
- Missing required data
- Type mismatches
- Business rule violations

**Edge Case Coverage:**
- Boundary values (min, max, min-1, max+1)
- Empty collections
- Null/undefined values
- Special characters
- Concurrent operations
- Network failures
- System errors

**Example - Comprehensive coverage for "Age" field (must be 18-65):**

```
Happy Path:
  - age = 25 (valid middle value)
  - age = 18 (minimum boundary)
  - age = 65 (maximum boundary)

Error Cases:
  - age = 17 (below minimum)
  - age = 66 (above maximum)
  - age = -5 (negative)
  - age = 0 (zero)
  - age = "twenty" (invalid type)
  - age = null (missing)
  - age = "" (empty string)
  - age = 999999 (extremely large)

Edge Cases:
  - age = 17.9 (decimal below minimum)
  - age = 18.0 (decimal at minimum)
  - age = 65.1 (decimal above maximum)
```

### Step 5: Prioritize Test Scenarios

Classify each test by priority:

**Critical (P0):**
- Core business functionality
- Payment/transaction flows
- Security features (auth, permissions)
- Data integrity operations
- Regulatory compliance scenarios

**High (P1):**
- Frequently used features
- Error handling for common issues
- Major user workflows
- Integration points

**Medium (P2):**
- Less common features
- Alternative workflows
- Nice-to-have validations
- Edge cases for stable features

**Low (P3):**
- Rarely used features
- Minor UI variations
- Cosmetic validations

### Step 6: Structure Output

Organize test scenarios clearly:

```markdown
# Test Suite: [Feature Name]

## Overview
- Source Requirements: REQ-001, REQ-002
- Total Scenarios: 15
- Coverage: Happy path, Error cases, Edge cases

## BDD Scenarios

### Critical Priority

Feature: User Authentication
  Scenario: Successful login with valid credentials [P0]
  Scenario: Login fails with incorrect password [P0]

### High Priority

Feature: User Authentication
  Scenario: Login fails with non-existent user [P1]
  Scenario: Account locks after 5 failed attempts [P1]

## Unit Tests

### Module: auth.validators

Test: test_validate_password_strength_accepts_strong_password [P1]
Test: test_validate_password_strength_rejects_weak_password [P1]
Test: test_validate_password_strength_requires_minimum_length [P1]

## Integration Tests

Test: Authentication API returns JWT token on successful login [P0]
Test: Authentication API rate limits after repeated failures [P1]

## E2E Tests

Test: User can register, login, and access protected resources [P0]
Test: User session expires after timeout [P1]

## Test Data

Valid Credentials:
  - email: "valid.user@example.com"
  - password: "SecurePass123!"

Invalid Credentials:
  - email: "invalid@example.com" (non-existent)
  - password: "wrong" (incorrect)

## Coverage Summary

- Requirements Covered: 5/5 (100%)
- Happy Path: 5 scenarios
- Error Cases: 8 scenarios
- Edge Cases: 7 scenarios
- Total: 20 test scenarios
```

## Best Practices

1. **One scenario, one behavior** - Each test should verify a single behavior
2. **Use descriptive names** - Test names should clearly state what is being tested
3. **Include context** - Given clauses should set up complete context
4. **Be specific** - Use concrete values, not vague descriptions
5. **Test negatives** - Don't just test that things work, test that invalid things fail correctly
6. **Consider sequences** - Test state transitions and workflows, not just isolated actions
7. **Think like an attacker** - Include security test cases (injection, XSS, etc.)
8. **Verify side effects** - Check that operations have expected side effects (logs, notifications, etc.)
9. **Make tests independent** - Each test should work regardless of execution order
10. **Include cleanup** - Ensure tests clean up after themselves

## Common Patterns

### Requirement Type → Test Approach

**"User must be able to..."** → BDD scenario + E2E test
**"System shall validate..."** → Unit test for validator + BDD for user feedback
**"Data must be..."** → Unit test for data constraint + Integration test for persistence
**"API endpoint..."** → Integration test for API contract
**"When X happens, Y should..."** → BDD scenario for behavior + Unit test for logic

### Coverage Rules of Thumb

For each requirement, generate:
- **Minimum**: 1 happy path + 1 error case
- **Good**: Happy path + 3-5 error cases + 2-3 edge cases
- **Comprehensive**: Happy path + all error conditions + boundary values + security cases

## Output Formats

Provide test scenarios in requested format:

**Gherkin/BDD** - For human-readable acceptance tests
**JSON** - For test automation frameworks (use `assets/test_suite_template.json`)
**Markdown** - For documentation and review
**Code snippets** - For specific testing frameworks (Jest, PyTest, etc.)

When format not specified, provide Markdown with all test types included.

## Resources

- `references/test_patterns.md` - Detailed patterns for each test type
- `references/coverage_checklist.md` - Comprehensive coverage checklist
- `assets/test_suite_template.json` - JSON template for structured output
