---
name: error-explanation-generator
description: Explains test failures and provides actionable debugging guidance. Use when tests fail (unit, integration, E2E), builds fail, or code throws errors. Analyzes error messages, stack traces, and test output to identify root causes and suggest concrete fixes. Handles pytest, jest, junit, mocha, vitest, selenium, cypress, playwright, and other testing frameworks across Python, JavaScript/TypeScript, Java, Go, and other languages.
---

# Error Explanation Generator

Analyze test failures and provide clear explanations with actionable fixes.

## Core Capabilities

This skill helps debug failed tests by:

1. **Parsing error messages** - Extract key information from test output
2. **Identifying root causes** - Determine why tests fail
3. **Explaining clearly** - Translate technical errors into understandable language
4. **Providing fixes** - Suggest concrete, actionable solutions
5. **Recognizing patterns** - Detect common error categories across frameworks

## Error Analysis Workflow

### Step 1: Gather Error Context

Collect all relevant information:

**Essential Information:**
- Complete error message and stack trace
- Test framework being used (pytest, jest, junit, etc.)
- Test code that failed
- Code being tested (if accessible)
- Programming language

**Additional Context (if available):**
- Recent code changes
- Environment details (OS, language version, dependencies)
- Test configuration files

**How to gather:**
```bash
# Python pytest
pytest -v --tb=long

# JavaScript/TypeScript jest
npm test -- --verbose

# Java junit
mvn test -X

# Go tests
go test -v
```

### Step 2: Parse and Categorize the Error

Identify the error category using `references/error_patterns.md`:

**Common Categories:**

1. **Assertion Failures** - Expected vs actual value mismatch
2. **Exceptions/Errors** - Runtime errors during test execution
3. **Timeout Errors** - Tests taking too long
4. **Setup/Teardown Failures** - Fixture or initialization issues
5. **Import/Dependency Errors** - Missing modules or broken imports
6. **Type Errors** - Type mismatches in typed languages
7. **Mock/Stub Issues** - Problems with test doubles
8. **Configuration Errors** - Test framework or build config issues
9. **Compilation Errors** - Syntax or build failures
10. **Flaky Test Issues** - Intermittent failures

### Step 3: Extract Key Information

Pull out critical details:

**From Error Message:**
- Error type (AssertionError, TypeError, NullPointerException, etc.)
- Expected vs actual values
- Error description
- Line numbers where error occurred

**From Stack Trace:**
- Failure point in test code
- Failure point in source code
- Call chain leading to error

**Example Extraction:**

```
FAILED tests/test_user.py::test_create_user - AssertionError: assert 201 == 200
```

**Extracted:**
- Test file: `tests/test_user.py`
- Test name: `test_create_user`
- Error type: `AssertionError`
- Expected: `200`
- Actual: `201`

### Step 4: Identify Root Cause

Analyze why the error occurred:

**Questions to Ask:**
- What was the test expecting?
- What actually happened?
- Why did the actual behavior differ from expected?
- Is this a test bug or a code bug?

**Common Root Causes:**
- Logic error in implementation
- Incorrect test expectations
- Missing or wrong test data
- Race conditions or timing issues
- Environmental differences
- Outdated mocks or fixtures
- Dependency version conflicts

### Step 5: Provide Explanation

Structure the explanation clearly:

```markdown
## Error Summary

[One-sentence description of what went wrong]

## What Happened

[Explain the error in plain language]

**Expected:** [What the test expected to happen]
**Actual:** [What actually happened]

## Root Cause

[Explain why this happened - the underlying issue]

## How to Fix

### Option 1: [Most likely fix] ⭐

[Specific code change or action to take]

```[language]
// Before
[problematic code]

// After
[fixed code]
```

**Why this works:** [Brief explanation]

### Option 2: [Alternative fix]

[Another possible solution if Option 1 doesn't apply]

## Verification

[How to verify the fix works]

```bash
[command to run test]
```

## Prevention

[How to avoid this error in the future]
```

### Step 6: Suggest Next Steps

Provide actionable guidance:

**If fix is clear:**
- Show exact code change
- Provide test command to verify
- Mention related tests to check

**If diagnosis needs more info:**
- Suggest debugging steps
- Recommend logging/print statements to add
- Propose code to inspect

**If issue is environmental:**
- Suggest dependency checks
- Recommend configuration verification
- Propose environment comparison

## Error Pattern Examples

### Example 1: Assertion Failure (Python/pytest)

**Error Output:**
```
FAILED tests/test_calculator.py::test_divide - AssertionError: assert 2.5 == 2
```

**Analysis:**

```markdown
## Error Summary
Test expected integer division but got float division result.

## What Happened

**Expected:** `2` (integer)
**Actual:** `2.5` (float)

The test `test_divide` called a divide function with arguments that produce
a decimal result (e.g., 5 / 2 = 2.5) but expected an integer result.

## Root Cause

The implementation uses true division (`/`) which returns floats in Python 3,
but the test expects integer division behavior.

## How to Fix

### Option 1: Update implementation to use integer division ⭐

```python
# Before
def divide(a, b):
    return a / b

# After
def divide(a, b):
    return a // b  # Integer division
```

**Why this works:** The `//` operator performs floor division, returning
integers when both operands are integers.

### Option 2: Update test to expect float result

```python
# Before
assert divide(5, 2) == 2

# After
assert divide(5, 2) == 2.5
```

Use this if float division is the intended behavior.

## Verification

```bash
pytest tests/test_calculator.py::test_divide -v
```

## Prevention

- Clarify division requirements in function documentation
- Use type hints: `def divide(a: int, b: int) -> int:`
- Add test cases for both integer and float division scenarios
```

### Example 2: TypeError (JavaScript/Jest)

**Error Output:**
```
TypeError: Cannot read property 'name' of undefined
    at getUserName (src/user.js:5:20)
    at Object.<anonymous> (tests/user.test.js:10:22)
```

**Analysis:**

```markdown
## Error Summary
Attempted to access property 'name' on undefined user object.

## What Happened

**Expected:** User object with 'name' property
**Actual:** `undefined`

Function `getUserName()` tried to access `.name` property on a value that
was undefined, causing a runtime error.

## Root Cause

The user object passed to `getUserName()` was undefined. This commonly
happens when:
- Function called without argument
- Async data not yet loaded
- Database/API query returned no result

## How to Fix

### Option 1: Add null/undefined check ⭐

```javascript
// Before
function getUserName(user) {
    return user.name;
}

// After
function getUserName(user) {
    if (!user) {
        return null; // or throw error, or return default
    }
    return user.name;
}
```

**Why this works:** Defensively handles cases where user might be undefined.

### Option 2: Fix the test to provide valid user object

```javascript
// Before
const name = getUserName(); // Called without argument

// After
const name = getUserName({ name: 'Alice', id: 1 });
```

### Option 3: Use optional chaining (modern JS)

```javascript
function getUserName(user) {
    return user?.name ?? 'Unknown';
}
```

## Verification

```bash
npm test -- user.test.js
```

## Prevention

- Add input validation to functions
- Use TypeScript for type safety
- Define clear function contracts
- Use optional chaining for property access
```

### Example 3: Timeout Error (E2E/Cypress)

**Error Output:**
```
Timed out retrying after 4000ms: Expected to find element: [data-testid="submit-btn"],
but never found it.
```

**Analysis:**

```markdown
## Error Summary
Test couldn't find submit button within timeout period.

## What Happened

**Expected:** Element with `data-testid="submit-btn"` to appear on page
**Actual:** Element never appeared within 4 seconds

## Root Cause

Possible reasons:
1. Element takes longer than 4s to render
2. Element has different selector/ID
3. Element only appears under certain conditions
4. JavaScript error preventing element from rendering

## How to Fix

### Option 1: Increase timeout for slow-loading elements ⭐

```javascript
// Before
cy.get('[data-testid="submit-btn"]').click();

// After
cy.get('[data-testid="submit-btn"]', { timeout: 10000 }).click();
```

### Option 2: Wait for prerequisite conditions

```javascript
// Wait for page to fully load first
cy.get('[data-testid="form-container"]').should('be.visible');
cy.get('[data-testid="submit-btn"]').click();
```

### Option 3: Check selector is correct

Inspect the page to verify:
```javascript
// Verify element exists with different selector
cy.get('button[type="submit"]').click();
```

## Verification

```bash
npx cypress run --spec "cypress/e2e/form.cy.js"
```

## Debugging Steps

1. **Add screenshot on failure:**
   ```javascript
   cy.screenshot('before-submit-btn');
   cy.get('[data-testid="submit-btn"]').click();
   ```

2. **Check browser console:**
   ```javascript
   cy.window().then((win) => {
       console.log(win.document.body.innerHTML);
   });
   ```

3. **Verify element in browser:**
   Run test in headed mode: `npx cypress open`

## Prevention

- Use appropriate timeouts for async operations
- Add explicit waits for dynamic content
- Verify selectors match actual DOM
- Test with network throttling to catch timing issues
```

### Example 4: Mock Issue (Python/pytest)

**Error Output:**
```
E   AssertionError: Expected call: send_email('user@example.com', 'Welcome')
E   Actual calls: []
```

**Analysis:**

```markdown
## Error Summary
Mock expected a function call that never happened.

## What Happened

**Expected:** `send_email()` to be called with specific arguments
**Actual:** `send_email()` was never called

## Root Cause

The code being tested didn't call the mocked function. Common reasons:
- Different code path executed (conditional logic)
- Function called with different arguments
- Function called on different object instance
- Mock not properly configured

## How to Fix

### Option 1: Verify code path is reached ⭐

```python
# Add debug assertion to check if code executes
def test_registration_sends_email(mocker):
    mock_send = mocker.patch('app.email.send_email')

    result = register_user('user@example.com')

    # Check if registration succeeded
    assert result.success, "Registration failed, email won't be sent"

    mock_send.assert_called_once_with('user@example.com', 'Welcome')
```

### Option 2: Check mock target path

```python
# Ensure you're mocking where it's used, not where it's defined

# Wrong - mocking definition location
mocker.patch('app.email.send_email')

# Right - mocking where it's imported
mocker.patch('app.user.send_email')  # if user.py imports send_email
```

### Option 3: Relax assertion constraints

```python
# Instead of exact match
mock_send.assert_called_once_with('user@example.com', 'Welcome')

# Check if called at all
assert mock_send.called, "send_email was never called"

# Check call happened with first argument matching
mock_send.assert_called()
args = mock_send.call_args[0]
assert args[0] == 'user@example.com'
```

## Verification

```bash
pytest tests/test_registration.py::test_registration_sends_email -v
```

## Debugging Steps

Print actual calls to see what happened:
```python
print(f"Mock called: {mock_send.called}")
print(f"Call count: {mock_send.call_count}")
print(f"Call args: {mock_send.call_args_list}")
```

## Prevention

- Mock at the point of use, not definition
- Verify code paths with unit tests first
- Use `assert mock.called` before checking arguments
- Print mock call history when debugging
```

## Framework-Specific Notes

### Python (pytest, unittest)

**Common error patterns:**
- `AssertionError` - Failed assertions
- `AttributeError` - Missing attributes/methods
- `ImportError/ModuleNotFoundError` - Import issues
- `FixtureNotFoundError` - Missing pytest fixtures

**Key files to check:**
- `pytest.ini`, `setup.cfg` - Configuration
- `conftest.py` - Shared fixtures
- `requirements.txt` - Dependencies

### JavaScript/TypeScript (Jest, Mocha, Vitest)

**Common error patterns:**
- `TypeError` - Type-related errors
- `ReferenceError` - Undefined variables
- `Timeout exceeded` - Async operation timeouts
- `Cannot find module` - Import/require issues

**Key files to check:**
- `jest.config.js`, `vitest.config.js` - Test configuration
- `package.json` - Dependencies and scripts
- `tsconfig.json` - TypeScript settings

### Java (JUnit, TestNG)

**Common error patterns:**
- `AssertionFailedError` - Failed assertions
- `NullPointerException` - Null reference access
- `ClassNotFoundException` - Missing classes
- `ComparisonFailure` - Value comparison failures

**Key files to check:**
- `pom.xml` (Maven) or `build.gradle` (Gradle) - Dependencies
- Test configuration annotations

### Go (testing package)

**Common error patterns:**
- Test panics - Runtime panics
- Comparison failures - Expected vs actual mismatches
- Race conditions - Data race detector failures

**Key commands:**
```bash
go test -v              # Verbose output
go test -race           # Race detection
go test -cover          # Coverage
```

## Quick Reference: Error Categories

| Category | Keywords | Common Fix |
|----------|----------|------------|
| Assertion failure | `assert`, `expected`, `actual` | Fix test expectation or implementation |
| Null/undefined | `null`, `undefined`, `NullPointer` | Add null checks or fix data flow |
| Type error | `TypeError`, `type mismatch` | Fix types or add type conversion |
| Timeout | `timeout`, `exceeded` | Increase timeout or fix slow code |
| Import error | `ModuleNotFound`, `Cannot find` | Install dependency or fix import path |
| Mock issue | `assert_called`, `Expected call` | Fix mock configuration or code path |
| Async error | `Promise`, `await`, `async` | Properly handle async operations |
| Setup failure | `fixture`, `beforeEach`, `setUp` | Fix test initialization |

## Resources

- **`references/error_patterns.md`** - Comprehensive error pattern catalog with detailed examples for each framework and language
- **`references/debugging_strategies.md`** - Advanced debugging techniques, tools, and systematic approaches for complex failures

## Best Practices

1. **Read the full error** - Don't skip stack traces
2. **Identify the category** - Categorize before diagnosing
3. **Check recent changes** - Often related to recent code
4. **Reproduce consistently** - Ensure error is reproducible
5. **Isolate the problem** - Narrow down to minimal failing case
6. **Verify the fix** - Always run tests after fixing
7. **Add regression tests** - Prevent same error from recurring
8. **Keep tests simple** - Complex tests are harder to debug
