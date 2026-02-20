# Issue Report Generation Patterns

This reference provides patterns and templates for generating clear, actionable issue reports from failing tests.

## Table of Contents

1. [Report Structure](#report-structure)
2. [Analysis Patterns](#analysis-patterns)
3. [Report Templates](#report-templates)
4. [Language Guidelines](#language-guidelines)
5. [Common Failure Patterns](#common-failure-patterns)

## Report Structure

### Essential Components

Every issue report must include:

1. **Title**
   - Concise (50-80 characters)
   - Descriptive of the problem
   - Includes affected component
   - Example: "NullPointerException in UserService.authenticate()"

2. **Bug Description**
   - Clear summary of the issue
   - Context about when it occurs
   - Impact on functionality

3. **Steps to Reproduce**
   - Exact test case or commands
   - Minimal reproduction steps
   - Environment details if relevant

4. **Expected Behavior**
   - What should happen
   - Based on test assertions or documentation

5. **Actual Behavior**
   - What actually happens
   - Include error messages
   - Include stack traces

6. **Affected Code**
   - File paths
   - Class/method names
   - Line numbers if available

7. **Additional Context** (optional)
   - Suspected root cause
   - Related issues
   - Workarounds

### Optional Components

- **Environment:** OS, language version, dependencies
- **Severity:** Critical, High, Medium, Low
- **Labels:** bug, regression, performance, etc.
- **Assignee suggestions:** Based on code ownership

## Analysis Patterns

### Pattern 1: Assertion Failure Analysis

**Input:**
```
Test: test_user_authentication
Assertion: expected 'authenticated' but got 'failed'
```

**Analysis Steps:**
1. Identify the assertion: `expected 'authenticated' but got 'failed'`
2. Find the test code making this assertion
3. Trace back to the method being tested
4. Identify the code path that returns 'failed'
5. Look for conditions that trigger this path

**Report Focus:**
- Expected vs. actual values
- The condition that caused the unexpected value
- The code location returning the wrong value

### Pattern 2: Exception Analysis

**Input:**
```
NullPointerException at UserService.java:45
  at UserService.authenticate(UserService.java:45)
  at AuthController.login(AuthController.java:23)
```

**Analysis Steps:**
1. Identify exception type: `NullPointerException`
2. Find the exact line: `UserService.java:45`
3. Examine the code at that line
4. Identify which variable is null
5. Trace back to where it should be initialized

**Report Focus:**
- Exception type and location
- The null variable
- Where it should have been initialized
- Why initialization failed

### Pattern 3: Timeout/Performance Analysis

**Input:**
```
Test: test_large_dataset_processing
Error: Test timeout after 30s
```

**Analysis Steps:**
1. Identify the operation that timed out
2. Look for loops or recursive calls
3. Check for inefficient algorithms (O(n²), etc.)
4. Look for blocking operations

**Report Focus:**
- The slow operation
- Expected vs. actual performance
- Algorithmic complexity issues
- Potential optimizations

### Pattern 4: Integration Test Failure

**Input:**
```
Test: test_api_endpoint_returns_user_data
Error: Expected status 200, got 500
Response: {"error": "Database connection failed"}
```

**Analysis Steps:**
1. Identify the integration point (API, database, etc.)
2. Check the error response
3. Find the code handling this integration
4. Look for configuration or connection issues

**Report Focus:**
- The integration point
- The error from the external system
- Configuration requirements
- Connection handling code

### Pattern 5: Regression Analysis

**Input:**
```
Test: test_feature_X (previously passing)
Recent changes: commit abc123 modified FeatureX.java
```

**Analysis Steps:**
1. Identify when test started failing
2. Find recent commits affecting related code
3. Compare old vs. new implementation
4. Identify the breaking change

**Report Focus:**
- When it broke (commit/PR)
- What changed
- Why the change broke the test
- The specific breaking code

## Report Templates

### Template 1: Exception-Based Bug

```markdown
# [Exception Type] in [Component].[Method]

## Description
A `[ExceptionType]` is thrown when [condition/scenario]. This causes [impact].

## Steps to Reproduce
1. Run test: `[test command]`
2. Or execute: `[code snippet]`

## Expected Behavior
[What should happen - no exception, or different behavior]

## Actual Behavior
```
[Exception Type]: [Exception message]
  at [Class].[Method]([File]:[Line])
  at [Class].[Method]([File]:[Line])
  ...
```

## Affected Code
- **File:** `[path/to/file]`
- **Method:** `[ClassName.methodName]`
- **Line:** [line number]

## Analysis
[Brief analysis of why this happens, if determinable]

The exception occurs because [reason]. The variable `[varName]` is null/invalid when [condition].

## Additional Context
- Test file: `[path/to/test]`
- Test method: `[testMethodName]`
```

### Template 2: Assertion Failure Bug

```markdown
# [Feature] returns incorrect [value/result]

## Description
The `[method/feature]` returns `[actual]` instead of the expected `[expected]` when [condition].

## Steps to Reproduce
1. Run test: `[test command]`
2. Test case: `[test name]`

## Expected Behavior
```
[Expected output/value]
```

## Actual Behavior
```
[Actual output/value]
```

**Assertion:**
```
[Assertion code from test]
```

## Affected Code
- **File:** `[path/to/file]`
- **Method:** `[ClassName.methodName]`
- **Lines:** [line range]

## Analysis
The method returns `[actual]` because [reason]. The expected value `[expected]` should be returned when [condition].

**Suspected cause:** [Brief explanation of likely root cause]

## Test Details
- Test file: `[path/to/test]`
- Test method: `[testMethodName]`
```

### Template 3: Performance/Timeout Bug

```markdown
# Performance issue: [Operation] exceeds timeout

## Description
The `[operation/method]` takes longer than expected, causing test timeout after [duration].

## Steps to Reproduce
1. Run test: `[test command]`
2. Test case: `[test name]`
3. Input size: [size/scale]

## Expected Behavior
Operation should complete within [expected time].

## Actual Behavior
Operation times out after [actual time].

## Affected Code
- **File:** `[path/to/file]`
- **Method:** `[ClassName.methodName]`
- **Lines:** [line range]

## Analysis
The performance issue appears to be caused by [reason]:
- [Specific inefficiency, e.g., O(n²) loop]
- [Blocking operation]
- [Resource contention]

**Suspected bottleneck:** [Code section or operation]

## Test Details
- Test file: `[path/to/test]`
- Test method: `[testMethodName]`
- Input size: [size]
```

### Template 4: Integration Failure Bug

```markdown
# [Integration Point] failure: [Error]

## Description
Integration with `[external system/API/database]` fails with error: `[error message]`.

## Steps to Reproduce
1. Run test: `[test command]`
2. Test case: `[test name]`

## Expected Behavior
[Expected response/behavior from integration]

## Actual Behavior
```
Error: [error message]
Status: [status code if applicable]
Response: [error response if applicable]
```

## Affected Code
- **File:** `[path/to/file]`
- **Method:** `[ClassName.methodName]`
- **Lines:** [line range]

## Analysis
The integration fails because [reason]:
- [Configuration issue]
- [Connection problem]
- [Authentication failure]
- [API contract mismatch]

## Environment
- [Relevant environment details]
- [Configuration requirements]

## Test Details
- Test file: `[path/to/test]`
- Test method: `[testMethodName]`
```

### Template 5: Regression Bug

```markdown
# Regression: [Feature] broken by recent changes

## Description
The `[feature/method]` was working correctly but now fails after recent changes.

## Steps to Reproduce
1. Run test: `[test command]`
2. Test case: `[test name]` (previously passing)

## Expected Behavior
[What used to work]

## Actual Behavior
[What now fails]

## Affected Code
- **File:** `[path/to/file]`
- **Method:** `[ClassName.methodName]`

## Regression Analysis
**Breaking commit:** [commit hash] - [commit message]
**Changed files:** [list of files]

The regression was introduced by [specific change]. The change [what it did] which breaks [what it breaks].

## Test Details
- Test file: `[path/to/test]`
- Test method: `[testMethodName]`
- Last passing: [commit/date]
- First failing: [commit/date]
```

## Language Guidelines

### Clarity Principles

1. **Be specific:**
   - ❌ "The code doesn't work"
   - ✅ "UserService.authenticate() throws NullPointerException"

2. **Use precise terminology:**
   - ❌ "Something is wrong with the database"
   - ✅ "Database connection fails with 'Connection refused' error"

3. **State facts, not opinions:**
   - ❌ "The code is badly written"
   - ✅ "The method has O(n²) complexity causing timeout"

4. **Indicate uncertainty:**
   - ❌ "The bug is in line 45"
   - ✅ "The bug appears to be in line 45" or "Suspected location: line 45"

### Developer-Friendly Language

**Good Examples:**
- "NullPointerException at UserService.java:45 when user parameter is null"
- "Assertion failed: expected 200 OK, got 500 Internal Server Error"
- "Method returns empty list instead of filtered results"
- "Test timeout: operation takes >30s with 10,000 items"

**Bad Examples:**
- "It crashes" (too vague)
- "The system is broken" (not specific)
- "Fix the bug in the code" (not actionable)
- "This is obviously wrong" (judgmental, not helpful)

### Uncertainty Indicators

When root cause is unclear, use:
- "Suspected cause:"
- "Likely related to:"
- "Appears to be caused by:"
- "Possibly due to:"
- "Further investigation needed:"

**Example:**
```markdown
## Analysis
The NullPointerException occurs at line 45 when accessing `user.getProfile()`.

**Suspected cause:** The `user` object is null, possibly because:
1. User lookup failed (line 42)
2. User was not properly initialized
3. Database query returned null

Further investigation needed to determine which condition triggers the null user.
```

## Common Failure Patterns

### Pattern: Null Pointer

**Indicators:**
- `NullPointerException`
- `AttributeError: 'NoneType' object has no attribute`
- Accessing member of null/None object

**Report Focus:**
- Which variable is null
- Where it should be initialized
- Why initialization failed

**Example Title:**
"NullPointerException in UserService.authenticate() when user not found"

### Pattern: Assertion Mismatch

**Indicators:**
- `AssertionError`
- `expected X but got Y`
- Test assertion failure

**Report Focus:**
- Expected vs. actual values
- The code producing the wrong value
- Conditions causing the mismatch

**Example Title:**
"UserService.authenticate() returns 'failed' instead of 'authenticated'"

### Pattern: Index Out of Bounds

**Indicators:**
- `IndexError`
- `ArrayIndexOutOfBoundsException`
- Accessing invalid array index

**Report Focus:**
- The invalid index
- Array/list size
- Loop or access logic

**Example Title:**
"IndexError in processItems() when list is empty"

### Pattern: Type Mismatch

**Indicators:**
- `TypeError`
- `ClassCastException`
- Type conversion errors

**Report Focus:**
- Expected vs. actual types
- Where type mismatch occurs
- Why wrong type is provided

**Example Title:**
"TypeError: expected int, got string in calculateTotal()"

### Pattern: Resource Not Found

**Indicators:**
- `FileNotFoundException`
- `ResourceNotFoundError`
- Missing file/resource errors

**Report Focus:**
- Expected resource location
- Actual search path
- Configuration issues

**Example Title:**
"FileNotFoundException: config.json not found in expected location"

### Pattern: Timeout

**Indicators:**
- Test timeout
- Operation exceeds time limit
- Hanging/blocking

**Report Focus:**
- The slow operation
- Expected vs. actual duration
- Performance bottleneck

**Example Title:**
"Test timeout: processLargeDataset() exceeds 30s limit"

### Pattern: Connection Failure

**Indicators:**
- `ConnectionError`
- `Connection refused`
- Network/database connection issues

**Report Focus:**
- Connection target
- Error message
- Configuration requirements

**Example Title:**
"Database connection failed: Connection refused on localhost:5432"

## Best Practices

### DO:
- ✅ Include exact error messages
- ✅ Provide stack traces
- ✅ Reference specific code locations
- ✅ Include test commands
- ✅ State expected vs. actual behavior
- ✅ Indicate uncertainty when appropriate
- ✅ Use code formatting for code snippets
- ✅ Link to relevant files/commits

### DON'T:
- ❌ Invent behavior not in the test
- ❌ Claim fixes without evidence
- ❌ Use vague language
- ❌ Blame developers
- ❌ Include irrelevant information
- ❌ Make assumptions without stating them
- ❌ Omit error messages or stack traces
- ❌ Write overly long descriptions

## Quality Checklist

Before finalizing a report, verify:

- [ ] Title is concise and descriptive
- [ ] Bug description is clear
- [ ] Steps to reproduce are provided
- [ ] Expected behavior is stated
- [ ] Actual behavior is documented
- [ ] Error messages/stack traces included
- [ ] Affected code locations specified
- [ ] Uncertainty is clearly indicated
- [ ] Language is developer-friendly
- [ ] Report is ready to post to issue tracker

## Example: Complete Issue Report

```markdown
# NullPointerException in UserService.authenticate() when user not found

## Description
A `NullPointerException` is thrown in `UserService.authenticate()` when attempting to authenticate a user that doesn't exist in the database. This causes the authentication endpoint to return a 500 error instead of properly handling the missing user case.

## Steps to Reproduce
1. Run test: `mvn test -Dtest=UserServiceTest#testAuthenticateNonExistentUser`
2. Or call: `userService.authenticate("nonexistent@example.com", "password")`

## Expected Behavior
The method should return an authentication failure result (e.g., `AuthResult.FAILED`) or throw a specific `UserNotFoundException`, not a `NullPointerException`.

## Actual Behavior
```
java.lang.NullPointerException
  at com.example.UserService.authenticate(UserService.java:45)
  at com.example.AuthController.login(AuthController.java:23)
  at com.example.UserServiceTest.testAuthenticateNonExistentUser(UserServiceTest.java:67)
```

## Affected Code
- **File:** `src/main/java/com/example/UserService.java`
- **Method:** `UserService.authenticate`
- **Line:** 45

**Code at line 45:**
```java
String hashedPassword = user.getPassword(); // user is null here
```

## Analysis
The exception occurs because the `user` object is null when the user lookup fails (line 42). The code attempts to call `user.getPassword()` without checking if the user exists.

**Suspected cause:** Missing null check after user lookup.

**Suggested fix:** Add null check:
```java
User user = userRepository.findByEmail(email);
if (user == null) {
    return AuthResult.USER_NOT_FOUND;
}
String hashedPassword = user.getPassword();
```

## Test Details
- Test file: `src/test/java/com/example/UserServiceTest.java`
- Test method: `testAuthenticateNonExistentUser`
- Test assertion: Expected `AuthResult.USER_NOT_FOUND`, got `NullPointerException`

## Labels
`bug`, `authentication`, `null-pointer`

## Severity
High - Causes 500 errors in production
```
