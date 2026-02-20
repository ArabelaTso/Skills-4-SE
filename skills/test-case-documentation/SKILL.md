---
name: test-case-documentation
description: Generate comprehensive test case documentation from test code, test framework output, existing test docs, and source code context. Use when documenting test suites, creating test specifications, generating test coverage reports, onboarding developers to testing practices, or preparing QA documentation. Analyzes test functions (pytest, unittest) to extract test names, docstrings, assertions, and organization, then produces structured markdown with both overview-level summaries and detailed test case specifications including purpose, preconditions, steps, expected results, and test data. Triggers when users ask to document tests, generate test specifications, create test reports, summarize test coverage, or explain what tests do.
---

# Test Case Documentation

## Overview

Generate comprehensive, structured documentation for test suites by analyzing test code, framework output, and source context to produce both overview summaries and detailed test case specifications.

## Workflow

### 1. Understand Documentation Needs

Determine what documentation is needed:

**Questions to ask:**
- What test suites need documentation?
- Is this for developers, QA, or stakeholders?
- Focus on overview or detailed specifications?
- Include coverage analysis?

**Identify test location:**
```bash
# Find test files
find . -name "test_*.py" -o -name "*_test.py"

# Count test files
find . -name "test_*.py" | wc -l

# Check test framework
grep -r "import pytest\|import unittest" tests/
```

### 2. Extract Test Information

Gather test data from multiple sources.

#### Source 1: Test Code Analysis

Use the bundled script to extract test metadata:

```bash
# Extract tests from directory
python scripts/extract_tests.py /path/to/tests

# Exclude specific directories
python scripts/extract_tests.py /path/to/tests venv,.venv,__pycache__
```

**What it extracts:**
- Test function names
- Test classes and organization
- Docstrings
- Test types (unit, integration, e2e)
- Pytest markers/tags
- File locations and line numbers

**Manual extraction:**

Read test files to understand:

```python
def test_user_registration_with_valid_data():
    """
    Test successful user registration with valid input.

    Given: Valid email, username, and password
    When: User submits registration form
    Then: User account is created and welcome email sent
    """
    # Extract: purpose, preconditions, expected behavior
    user_data = {"email": "test@example.com", ...}  # Extract: test data
    result = service.register(user_data)  # Extract: operation
    assert result.success  # Extract: assertions/expected results
    assert result.user_id > 0
```

**Key information to extract:**
- Test purpose (from name and docstring)
- Test data (sample inputs)
- Operations performed
- Assertions (expected outcomes)
- Setup and teardown (fixtures)

#### Source 2: Test Framework Output

Capture test execution results:

```bash
# Run tests with verbose output
pytest tests/ -v > test_output.txt

# Run with detailed output
pytest tests/ -v --tb=short > test_results.txt

# Generate coverage report
pytest tests/ --cov=src --cov-report=term-missing > coverage.txt
```

**Extract from output:**
- Which tests passed/failed
- Execution time
- Coverage percentages
- Missing coverage areas

#### Source 3: Existing Test Documentation

Check for existing docs:

```bash
# Look for test documentation
find . -name "*test*.md" -o -name "TEST*.md"

# Check for test plans
find . -name "*test*plan*.md"

# Look for docstrings in conftest.py
cat tests/conftest.py
```

#### Source 4: Source Code Context

Understand what's being tested:

```bash
# Find source files related to tests
# test_user_service.py -> user_service.py
ls src/user_service.py

# Read source to understand functionality
cat src/user_service.py
```

### 3. Organize Test Information

Structure tests hierarchically.

See [documentation-templates.md](references/documentation-templates.md) for detailed templates.

**Organization structure:**

```
Test Suite Overview
├── Summary Statistics
├── Test Organization (directory structure)
├── Coverage Summary
└── Test Files
    ├── File 1: test_user_service.py
    │   ├── TestUserRegistration (class)
    │   │   ├── test_valid_registration (unit)
    │   │   ├── test_duplicate_email (unit)
    │   │   └── test_weak_password (unit)
    │   └── TestUserAuthentication (class)
    │       ├── test_login_success (unit)
    │       └── test_login_failure (unit)
    └── File 2: test_api.py
        └── test_full_workflow (integration)
```

**Categorize by:**
- Test type (unit, integration, e2e)
- Module/feature tested
- Priority/criticality
- Test status (passing, failing, skipped)

### 4. Generate Documentation

Create structured markdown documentation.

#### Level 1: Overview Documentation

High-level summary for project understanding:

```markdown
# Test Suite: User Management

**Last Updated:** 2026-02-15
**Total Tests:** 42
**Coverage:** 87%
**Status:** ✅ 40 passing, ❌ 2 failing

## Summary

Comprehensive test suite for user management functionality including registration,
authentication, profile management, and user data export.

## Test Statistics

- **Unit Tests:** 28 (67%)
- **Integration Tests:** 12 (28%)
- **End-to-End Tests:** 2 (5%)

## Test Organization

```
tests/
├── unit/
│   ├── test_user_service.py (15 tests)
│   ├── test_auth_service.py (8 tests)
│   └── test_validators.py (5 tests)
├── integration/
│   ├── test_api.py (10 tests)
│   └── test_workflows.py (2 tests)
└── e2e/
    └── test_complete_flows.py (2 tests)
```

## Coverage by Module

| Module | Coverage | Tests | Priority |
|--------|----------|-------|----------|
| user_service.py | 95% | 15 | High |
| auth_service.py | 88% | 8 | High |
| validators.py | 94% | 5 | Medium |

## Quick Start

```bash
# Run all tests
pytest tests/

# Run unit tests only
pytest tests/unit/

# Run with coverage
pytest --cov=src tests/
```
```

#### Level 2: Detailed Test Documentation

Detailed specifications for each test:

```markdown
## Test File: test_user_service.py

**Path:** `tests/unit/test_user_service.py`
**Tests:** 15
**Coverage:** 95%

---

### Class: TestUserRegistration

Tests for user registration functionality.

---

#### Test: test_user_registration_with_valid_data

**Type:** Unit Test
**Line:** 45
**Status:** ✅ Passing
**Tags:** user, authentication

**Purpose:**
Verify that a new user can successfully register with valid email, username, and password.

**Preconditions:**
- Database is empty (no existing users)
- Email validation service is mocked

**Test Data:**
```python
user_data = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "SecurePass123!"
}
```

**Test Steps:**
1. Create user data dictionary with valid fields
2. Call `UserService.register(user_data)`
3. Verify user record is created in database
4. Verify user ID is returned
5. Verify password is hashed (not plain text)

**Assertions:**
- `assert result.success == True`
- `assert result.user_id > 0`
- `assert User.query.count() == 1`
- `assert created_user.password != "SecurePass123!"`

**Expected Result:**
- User created with status "active"
- User ID returned (positive integer)
- Password stored as hash
- No errors raised

**Actual Result:** ✅ Pass (0.12s)

**Related Tests:**
- `test_user_registration_with_duplicate_email` - Tests duplicate handling
- `test_user_registration_with_weak_password` - Tests password validation

**Source Code Tested:**
`src/user_service.py:67-89` - `UserService.register()`

---

#### Test: test_user_registration_with_duplicate_email

**Type:** Unit Test
**Line:** 78
**Status:** ✅ Passing

**Purpose:**
Verify that registration fails when email already exists.

**Preconditions:**
- User with email "test@example.com" already exists in database

**Test Data:**
```python
existing_user = User(email="test@example.com", username="existing")
duplicate_data = {
    "email": "test@example.com",  # Duplicate
    "username": "newuser",
    "password": "ValidPass123"
}
```

**Expected Result:**
- `DuplicateEmailError` exception raised
- Error message: "Email already registered"
- No new user record created

**Actual Result:** ✅ Pass (0.08s)

---

### Class: TestUserAuthentication

Tests for user login and authentication.

[Continue with more tests...]
```

### 5. Include Coverage Analysis

Identify tested and untested areas.

```markdown
## Test Coverage Analysis

**Overall Coverage:** 87%

### High Coverage Areas

**user_service.py** - 95% coverage
- ✅ User registration (all paths tested)
- ✅ User update (all paths tested)
- ✅ User deletion (all paths tested)
- ⚠️ Uncovered: External API error handling (lines 145-150)

**Recommendation:** Add test case `test_user_registration_with_api_failure`

### Medium Coverage Areas

**payment_service.py** - 85% coverage
- ✅ Payment processing (happy path tested)
- ✅ Payment validation (tested)
- ⚠️ Uncovered: Timeout handling (lines 67-72)
- ⚠️ Uncovered: Retry logic (lines 89-95)

**Recommendations:**
- Add `test_payment_processing_timeout`
- Add `test_payment_retry_on_failure`

### Low Coverage Areas

**export_service.py** - 78% coverage
- ✅ Basic export (tested)
- ❌ Large dataset handling (not tested)
- ❌ Memory overflow scenarios (not tested)

**Recommendations:**
- Add `test_export_large_dataset`
- Add `test_export_memory_limit`
```

### 6. Document Test Execution

Include how to run tests:

```markdown
## Test Execution Guide

### Running All Tests

```bash
# Run entire test suite
pytest tests/

# Run with coverage report
pytest --cov=src --cov-report=html tests/

# Run with detailed output
pytest tests/ -v
```

### Running Specific Tests

```bash
# Run tests in specific file
pytest tests/unit/test_user_service.py

# Run specific test class
pytest tests/unit/test_user_service.py::TestUserRegistration

# Run specific test
pytest tests/unit/test_user_service.py::TestUserRegistration::test_valid_registration

# Run tests with specific marker
pytest -m "unit" tests/
pytest -m "integration" tests/
```

### Test Configuration

**pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

### Continuous Integration

Tests run automatically on:
- Pull requests to main branch
- Daily at 2am UTC
- Before deployment

**CI Command:**
```bash
pytest tests/ --cov=src --cov-report=xml --junitxml=test-results.xml
```
```

### 7. Present Documentation

Finalize and share the documentation.

**Documentation structure:**

```
docs/testing/
├── README.md (overview + quick start)
├── test-suite-overview.md (high-level summary)
├── test-specifications/
│   ├── user-management-tests.md
│   ├── payment-tests.md
│   └── api-tests.md
├── test-coverage-report.md
└── test-execution-guide.md
```

**Present to stakeholders:**
- Developers: Detailed specs + coverage
- QA: Test execution + expected results
- Management: Overview + statistics
- New team members: Overview + execution guide

## Tips for Effective Test Documentation

**Focus on clarity:**
- Use clear, descriptive test names
- Document the "why" not just the "what"
- Include expected vs actual behavior
- Show test data examples

**Keep it current:**
- Update docs when tests change
- Include last updated date
- Link to source code line numbers
- Note test status (passing/failing)

**Make it actionable:**
- Include reproduction steps
- Provide test execution commands
- Show configuration requirements
- Link related tests

**Organize logically:**
- Group by feature/module
- Order by priority or type
- Use consistent formatting
- Include table of contents for long docs

**Include context:**
- Explain preconditions
- Document test data
- Note dependencies
- Link to requirements or tickets

## Common Documentation Patterns

**Given-When-Then format:**
```python
def test_user_registration():
    """
    Given: A new user with valid email and password
    When: They submit the registration form
    Then: Their account is created and activated
    """
```

**Arrange-Act-Assert pattern:**
```python
def test_calculate_total():
    """Test order total calculation with tax."""
    # Arrange
    order = Order(items=[Item(price=100)])

    # Act
    total = order.calculate_total(tax_rate=0.1)

    # Assert
    assert total == 110
```

**Test matrices for combinatorial tests:**

| Input A | Input B | Expected |
|---------|---------|----------|
| Valid   | Valid   | Success  |
| Valid   | Invalid | Error A  |
| Invalid | Valid   | Error B  |
| Invalid | Invalid | Error C  |

## Automation Opportunities

**Auto-generate from CI:**
```bash
# Run tests and generate documentation
pytest tests/ --json-report --json-report-file=test-report.json

# Parse JSON and generate markdown
python generate_test_docs.py test-report.json > docs/test-report.md
```

**Keep docs in sync:**
- Git hooks to update docs when tests change
- CI checks for undocumented tests
- Automated coverage reports
- Test status badges in README

## Reference

For documentation templates and examples, see [documentation-templates.md](references/documentation-templates.md).
