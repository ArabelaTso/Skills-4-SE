# Test Case Documentation Templates

Templates and examples for test case documentation.

## Test Suite Overview Template

```markdown
# Test Suite: [Module/Feature Name]

**Last Updated:** [Date]
**Coverage:** [X%]
**Total Tests:** [N]

## Summary

[Brief description of what this test suite covers]

## Test Statistics

- **Unit Tests:** X
- **Integration Tests:** Y
- **End-to-End Tests:** Z
- **Total:** N

## Test Organization

```
tests/
├── unit/
│   ├── test_module_a.py (12 tests)
│   └── test_module_b.py (8 tests)
├── integration/
│   └── test_api.py (15 tests)
└── e2e/
    └── test_workflows.py (6 tests)
```

## Coverage Summary

| Module | Coverage | Tests |
|--------|----------|-------|
| module_a | 95% | 12 |
| module_b | 87% | 8 |
| api | 92% | 15 |

## Test Execution

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run with coverage
pytest --cov=src tests/
```
```

## Individual Test Case Template

```markdown
### Test: test_user_registration_with_valid_data

**Type:** Unit Test
**File:** `tests/unit/test_user_service.py:45`
**Tags:** user, authentication

**Purpose:**
Verify that a new user can successfully register with valid email, username, and password.

**Preconditions:**
- Database is empty (no existing users)
- Email validation service is available

**Test Steps:**
1. Create user data with valid email, username, and password
2. Call `UserService.register(user_data)`
3. Verify user is created in database
4. Verify welcome email is sent
5. Verify user ID is returned

**Test Data:**
```python
user_data = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "SecurePass123!"
}
```

**Expected Result:**
- User record created with status "active"
- User ID returned (integer > 0)
- Welcome email sent to provided email address
- Password is hashed (not stored in plain text)

**Actual Behavior:** ✅ Pass

**Related Tests:**
- `test_user_registration_with_duplicate_email` - Duplicate email handling
- `test_user_registration_with_weak_password` - Password validation
```

## Test Matrix Template

```markdown
# Test Matrix: User Authentication

| Test Case | Valid Email | Valid Password | Account Active | Expected Result |
|-----------|-------------|----------------|----------------|-----------------|
| test_login_success | ✓ | ✓ | ✓ | Login successful |
| test_login_invalid_email | ✗ | ✓ | ✓ | Error: Invalid email |
| test_login_invalid_password | ✓ | ✗ | ✓ | Error: Wrong password |
| test_login_inactive_account | ✓ | ✓ | ✗ | Error: Account inactive |
| test_login_missing_email | - | ✓ | ✓ | Error: Email required |
| test_login_missing_password | ✓ | - | ✓ | Error: Password required |
```

## Test Coverage Report Template

```markdown
# Test Coverage Report

**Generated:** 2026-02-15
**Project:** Example Project
**Overall Coverage:** 87%

## Coverage by Module

### Core Modules (High Priority)

| Module | Statements | Missing | Coverage |
|--------|------------|---------|----------|
| user_service.py | 150 | 8 | 95% |
| auth_service.py | 120 | 15 | 88% |
| payment_service.py | 200 | 30 | 85% |

### Utility Modules (Medium Priority)

| Module | Statements | Missing | Coverage |
|--------|------------|---------|----------|
| validators.py | 80 | 5 | 94% |
| formatters.py | 60 | 12 | 80% |

## Uncovered Code

### Critical Uncovered Areas

**user_service.py:145-150**
```python
# UNCOVERED: Error handling for external API failure
try:
    result = external_api.call()
except ExternalAPIError:
    # This error path is not tested
    logger.error("API failed")
    return None
```

**Recommendation:** Add test case `test_user_registration_with_api_failure`

### Low Priority Uncovered Areas

**formatters.py:34-38**
```python
# UNCOVERED: Edge case for empty input
if not data:
    return ""
```

**Recommendation:** Add test case `test_format_with_empty_input`

## Recommendations

1. **Immediate:** Add tests for error handling in user_service.py
2. **Short-term:** Increase coverage of payment_service.py to 90%+
3. **Long-term:** Add integration tests for payment workflows
```

## Test Specification Template

```markdown
# Test Specification: [Feature Name]

## TS-001: User Registration Flow

### Description
Comprehensive test of user registration functionality from form submission to account activation.

### Test Cases

#### TC-001: Valid Registration

**Priority:** High
**Type:** Integration Test

**Preconditions:**
- Application is running
- Database is accessible
- Email service is configured

**Input:**
- Email: valid email format
- Username: 3-20 alphanumeric characters
- Password: 8+ characters with mixed case and numbers

**Steps:**
1. Navigate to registration page
2. Fill in registration form with valid data
3. Submit form
4. Check email inbox
5. Click activation link
6. Verify redirect to login page

**Expected Output:**
- Form submission successful (HTTP 200)
- Success message displayed
- Activation email received within 1 minute
- Account status = "pending" before activation
- Account status = "active" after activation
- User can log in after activation

**Postconditions:**
- User record exists in database
- User can authenticate with provided credentials

#### TC-002: Duplicate Email

**Priority:** High
**Type:** Unit Test

**Preconditions:**
- User with email "test@example.com" already exists

**Input:**
- Email: "test@example.com" (duplicate)
- Username: "newuser"
- Password: "ValidPass123"

**Steps:**
1. Attempt to register with duplicate email

**Expected Output:**
- HTTP 400 (Bad Request)
- Error message: "Email already registered"
- No new user record created

**Postconditions:**
- Only one user with that email exists

#### TC-003: Weak Password

**Priority:** Medium
**Type:** Unit Test

**Input:**
- Email: "test@example.com"
- Username: "testuser"
- Password: "123" (weak password)

**Expected Output:**
- Validation error
- Message: "Password must be at least 8 characters"

### Test Data

```python
VALID_USER = {
    "email": "valid@example.com",
    "username": "validuser",
    "password": "SecurePass123!"
}

INVALID_EMAILS = [
    "notanemail",
    "@example.com",
    "test@",
    ""
]

WEAK_PASSWORDS = [
    "123",
    "password",
    "12345678"
]
```

### Dependencies
- Database: PostgreSQL 14+
- Email service: SendGrid
- Python: 3.9+

### Execution
```bash
pytest tests/integration/test_user_registration.py -v
```
```

## Pytest Output Documentation Template

```markdown
# Test Execution Report

**Date:** 2026-02-15 14:30:00
**Environment:** Development
**Branch:** feature/user-auth

## Execution Summary

```
====================== test session starts ======================
platform linux -- Python 3.9.7, pytest-7.4.0
collected 42 items

tests/unit/test_user_service.py::test_create_user PASSED    [ 2%]
tests/unit/test_user_service.py::test_update_user PASSED    [ 4%]
tests/unit/test_user_service.py::test_delete_user PASSED    [ 7%]
...

===================== 40 passed, 2 failed in 12.34s =============
```

## Results

- **Total:** 42 tests
- **Passed:** 40 (95%)
- **Failed:** 2 (5%)
- **Skipped:** 0
- **Duration:** 12.34s

## Failures

### 1. test_payment_processing_timeout

**File:** `tests/integration/test_payment.py:67`

**Error:**
```
AssertionError: Payment should timeout after 30s
Expected: PaymentTimeout exception
Actual: Payment completed successfully after 35s
```

**Analysis:**
Timeout threshold may need adjustment or payment gateway is slower than expected.

**Action Required:** Review timeout settings

### 2. test_user_export_large_dataset

**File:** `tests/unit/test_export.py:89`

**Error:**
```
MemoryError: Unable to allocate 2.5GB for export
```

**Analysis:**
Memory limit exceeded when exporting 100k user records.

**Action Required:** Implement streaming export

## Slow Tests

| Test | Duration | Recommendation |
|------|----------|----------------|
| test_full_database_backup | 8.5s | Mock backup operation |
| test_generate_annual_report | 5.2s | Use smaller dataset |
| test_process_bulk_emails | 3.8s | Mock email sending |

## Coverage

**Overall:** 87%

| Module | Coverage |
|--------|----------|
| user_service | 95% |
| payment_service | 85% |
| export_service | 78% |
```

## Best Practices for Test Documentation

### Good Test Docstrings

```python
def test_user_registration_with_valid_data():
    """
    Test successful user registration with valid input.

    Given: Valid email, username, and password
    When: User submits registration form
    Then: User account is created with 'active' status
          Welcome email is sent
          User can log in with credentials
    """
    # Test implementation
```

### Test Organization

```python
class TestUserAuthentication:
    """Test suite for user authentication functionality."""

    def test_login_with_valid_credentials(self):
        """Verify successful login with correct username and password."""
        pass

    def test_login_with_invalid_password(self):
        """Verify login fails with incorrect password."""
        pass

    def test_login_with_nonexistent_user(self):
        """Verify login fails for user that doesn't exist."""
        pass

    def test_login_with_inactive_account(self):
        """Verify login fails for deactivated account."""
        pass
```

### Test Naming Conventions

**Good names:**
- `test_create_user_with_valid_email`
- `test_payment_fails_with_insufficient_funds`
- `test_order_cancellation_sends_notification`

**Bad names:**
- `test_1`
- `test_user`
- `test_it_works`

### Test Tags

```python
import pytest

@pytest.mark.slow
@pytest.mark.integration
def test_full_checkout_workflow():
    """Test complete checkout from cart to confirmation."""
    pass

@pytest.mark.unit
@pytest.mark.critical
def test_payment_validation():
    """Test payment data validation logic."""
    pass
```
