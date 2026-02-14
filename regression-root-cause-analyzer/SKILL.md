---
name: regression-root-cause-analyzer
description: Locate root causes of failing regression tests by analyzing code changes, error messages, and test dependencies. Use when regression tests start failing after code changes, investigating test failures in CI/CD, debugging flaky tests, or understanding why previously passing tests now fail. Analyzes git diffs, stack traces, test output, and dependency changes to produce structured markdown reports ranking likely causes. Triggers when users ask to find why tests are failing, debug regression failures, investigate test breakage, or analyze failing test suites.
---

# Regression Root Cause Analyzer

## Overview

Systematically investigate failing regression tests to identify root causes by analyzing code changes, error messages, test dependencies, and common failure patterns.

## Workflow

### 1. Gather Initial Information

Collect essential details about the test failure:

**Test failure details:**
- Which test(s) are failing?
- Error message and stack trace
- When did tests start failing? (commit, PR, date)
- Do tests fail consistently or intermittently?
- Do tests fail locally, in CI, or both?

**Quick commands to gather info:**
```bash
# Run the failing test
pytest path/to/test_file.py::test_name -v

# Get recent commits
git log --oneline -10

# Check current branch and status
git status
git branch

# See what changed recently
git log --since="1 week ago" --oneline

# Check for uncommitted changes
git diff
```

### 2. Analyze Error Messages

Parse the error message and stack trace for clues. See [failure-patterns.md](references/failure-patterns.md) for common patterns.

**Error type indicators:**

**ImportError / ModuleNotFoundError:**
```
ImportError: cannot import name 'UserService' from 'app.services'
```
- **Likely cause**: Module or class renamed/moved
- **Investigation**: Check recent commits to `app/services/`

**AttributeError:**
```
AttributeError: 'User' object has no attribute 'email_address'
```
- **Likely cause**: Property renamed or removed
- **Investigation**: Check `User` class definition changes

**TypeError (arguments):**
```
TypeError: process_data() got an unexpected keyword argument 'format'
```
- **Likely cause**: Function signature changed
- **Investigation**: Find `process_data` definition and recent changes

**AssertionError:**
```
AssertionError: assert 3 == 2
```
- **Likely cause**: Logic change or test data change
- **Investigation**: Understand what the assertion checks

**KeyError / IndexError:**
```
KeyError: 'status'
```
- **Likely cause**: Data structure changed
- **Investigation**: Check response/data format changes

### 3. Identify Code Changes

Use git to find what changed since tests last passed.

#### Find When Tests Broke

```bash
# If you know the last good commit
git diff <last-good-commit> <current-commit>

# Check specific file changes
git log -p path/to/file.py

# See what changed in last N commits
git log -p -n 5

# Find commits that touched specific function
git log -S "function_name" -p
```

#### Analyze Relevant Changes

**Priority order for investigation:**
1. **Direct changes to tested code** - Changes to the file/class being tested
2. **Changes to imported dependencies** - Files imported by tested code
3. **Changes to test fixtures/mocks** - Test setup code
4. **Changes to test infrastructure** - pytest config, test runners
5. **Dependency version changes** - requirements.txt, package.json

**Commands to find changes:**
```bash
# What files changed recently?
git diff --name-only HEAD~5..HEAD

# Changes to specific file
git diff HEAD~5..HEAD path/to/file.py

# Changes to test file
git diff HEAD~5..HEAD path/to/test_file.py

# Changes to requirements
git diff HEAD~5..HEAD requirements.txt package.json
```

### 4. Investigate Specific Failure Patterns

Match the error to common patterns:

#### Pattern: API Signature Change

**Symptoms:**
- `TypeError: missing required argument`
- `TypeError: got unexpected keyword argument`

**Investigation steps:**
1. Find function definition: `grep -r "def function_name" .`
2. Check git history: `git log -p -S "def function_name"`
3. Compare signatures before/after
4. Update test calls to match new signature

#### Pattern: Return Type Change

**Symptoms:**
- `AttributeError` when accessing return value
- `TypeError: 'NoneType' object is not iterable`

**Investigation steps:**
1. Check function return statements
2. Look for changes from `return []` to `return None`
3. Check if error handling changed
4. Update test to handle new return type

#### Pattern: Dependency Version Change

**Symptoms:**
- Tests fail after `pip install` or `npm install`
- Different behavior in CI vs local

**Investigation steps:**
1. Check dependency files: `git diff HEAD~5..HEAD requirements.txt`
2. Review changelogs for updated packages
3. Look for deprecation warnings in test output
4. Pin to previous version to confirm

#### Pattern: Test Isolation Issue

**Symptoms:**
- Tests pass individually but fail when run together
- Order-dependent failures

**Investigation steps:**
1. Run tests individually: `pytest test_file.py::test_one`
2. Run in different orders
3. Check for shared state (global variables, database, files)
4. Look for missing cleanup in teardown

### 5. Generate Root Cause Report

Produce a structured markdown report:

## Root Cause Analysis: [Test Name]

### Summary
- **Test**: `test_user_registration`
- **Status**: Failing since commit abc123
- **Error**: `TypeError: process_user() got an unexpected keyword argument 'email_format'`

### Root Cause
The `process_user()` function signature changed in commit abc123. The parameter `email_format` was renamed to `email_type`.

**Evidence:**
- Commit abc123 modified `app/users.py`
- Function signature before: `def process_user(data, email_format="html")`
- Function signature after: `def process_user(data, email_type="html")`
- Test still calls: `process_user(user_data, email_format="html")`

### Likelihood: **High (95%)**

This is the direct cause of the TypeError.

### Fix Required
Update test to use new parameter name:

```python
# Before
result = process_user(user_data, email_format="html")

# After
result = process_user(user_data, email_type="html")
```

### Related Changes
- Commit abc123: Renamed email_format to email_type throughout codebase
- 5 other test files also need updates

### Additional Notes
The function behavior is otherwise unchanged. Only the parameter name differs.

---

## Alternative Hypotheses

### Hypothesis 2: Test Data Changed
**Likelihood**: Low (10%)

The test fixture might have changed, but review shows fixtures are unchanged.

### Hypothesis 3: Environment Difference
**Likelihood**: Very Low (5%)

Could be environment-related, but error is consistent locally and in CI.

---

## Reproduction Steps
1. Checkout commit abc123
2. Run: `pytest tests/test_users.py::test_user_registration`
3. Observe TypeError

## Verification Steps
1. Apply suggested fix
2. Run test: `pytest tests/test_users.py::test_user_registration`
3. Verify test passes

---

### 6. Verify the Root Cause

Before finalizing the analysis:

**Test the hypothesis:**
1. Apply the proposed fix
2. Run the test to confirm it passes
3. Run related tests to ensure no new breaks

**If fix doesn't work:**
1. Review alternative hypotheses
2. Gather more information
3. Expand investigation to related areas

**Commands to verify:**
```bash
# Run the specific failing test
pytest path/to/test.py::test_name -v

# Run all related tests
pytest path/to/test.py -v

# Run with verbose output
pytest path/to/test.py::test_name -vv

# Run with print statements visible
pytest path/to/test.py::test_name -s
```

## Investigation Strategies

### Strategy 1: Binary Search Through Commits

Find exact commit that broke tests:

```bash
# Start bisect
git bisect start

# Mark current (broken) commit
git bisect bad

# Mark last known good commit
git bisect good <commit-hash>

# Git will checkout middle commit
# Run tests, then mark good or bad
pytest tests/

# If tests pass
git bisect good

# If tests fail
git bisect bad

# Repeat until git finds the breaking commit
```

### Strategy 2: Compare Working vs Broken

**Diff approach:**
```bash
# Compare file between commits
git diff <good-commit>:<path> <bad-commit>:<path>

# Show file at specific commit
git show <commit>:path/to/file.py
```

**Checkout approach:**
```bash
# Temporarily checkout old version
git checkout <good-commit> path/to/file.py

# Run tests
pytest tests/

# Restore current version
git checkout HEAD path/to/file.py
```

### Strategy 3: Isolate the Problem

**Minimal reproduction:**
1. Create minimal test case that reproduces failure
2. Remove unrelated code
3. Identify exact line causing issue

**Example:**
```python
# Simplified test
def test_minimal_repro():
    # Reproduce just the failing assertion
    result = function_under_test(input)
    assert result == expected  # This fails
```

### Strategy 4: Check Test Dependencies

**Fixture issues:**
```python
# Check what fixtures provide
def test_debug_fixture(sample_user):
    print(f"Fixture data: {sample_user}")
    assert False  # Force test to show output
```

**Mock issues:**
```python
# Verify mock is called
@patch('module.function')
def test_with_mock(mock_func):
    mock_func.return_value = "test"
    result = code_that_uses_function()
    print(f"Mock called: {mock_func.called}")
    print(f"Call args: {mock_func.call_args}")
```

**Setup/teardown:**
```python
# Check state before/after
def test_check_state():
    print(f"Before: {get_current_state()}")
    run_test_code()
    print(f"After: {get_current_state()}")
```

## Common Investigation Commands

### Git Commands
```bash
# Show commits that changed a file
git log --follow path/to/file.py

# Show commits with specific content
git log -S "function_name" --source --all

# Show commits by author
git log --author="AuthorName" --since="1 week ago"

# Show detailed commit
git show <commit-hash>

# Compare branches
git diff main feature-branch
```

### Test Commands
```bash
# Run with maximum verbosity
pytest -vv

# Show print statements
pytest -s

# Stop at first failure
pytest -x

# Show local variables on failure
pytest -l

# Run last failed tests
pytest --lf

# Run tests that failed, then all
pytest --ff

# Collect tests without running
pytest --collect-only

# Show slowest tests
pytest --durations=10
```

### Python Debugging
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or in Python 3.7+
breakpoint()

# Print stack trace
import traceback
traceback.print_stack()

# Inspect object
import pprint
pprint.pprint(vars(obj))
```

## Example Workflows

### Example 1: Simple Function Signature Change

**User request:**
> "Tests started failing with TypeError about unexpected keyword argument"

**Investigation:**
1. Check error message: `TypeError: process() got unexpected keyword argument 'format'`
2. Find function: `grep -r "def process" .`
3. Check recent changes: `git log -p -S "def process"`
4. Find commit that changed parameter name
5. Verify: Apply fix and run test

**Report:**
```markdown
## Root Cause: Parameter Renamed

Function `process()` parameter `format` renamed to `output_format` in commit abc123.

**Fix**: Update test call from `process(data, format="json")` to `process(data, output_format="json")`

**Likelihood**: High (99%)
```

### Example 2: Flaky Test Investigation

**User request:**
> "Test passes sometimes but fails randomly"

**Investigation:**
1. Run test multiple times: `for i in {1..10}; do pytest test.py; done`
2. Check for timing issues, race conditions
3. Look for shared state between tests
4. Check for external dependencies (network, filesystem)

**Report:**
```markdown
## Root Cause: Race Condition

Test has race condition in async code. The async operation sometimes completes before assertion, sometimes after.

**Evidence**: Test fails ~30% of the time when run repeatedly.

**Fix**: Add proper await or increase timeout.

**Likelihood**: High (85%)
```

### Example 3: Dependency Update Breaking Tests

**User request:**
> "All tests started failing after pip install"

**Investigation:**
1. Check requirements: `git diff HEAD~1 requirements.txt`
2. Find updated package: `requests 2.28.0 → 2.31.0`
3. Review changelog for breaking changes
4. Test with old version: `pip install requests==2.28.0`

**Report:**
```markdown
## Root Cause: Breaking Change in requests 2.31.0

The `requests` library changed response encoding behavior in v2.31.0.

**Evidence**:
- Tests pass with requests==2.28.0
- Tests fail with requests==2.31.0
- Changelog mentions encoding changes

**Fix**: Update test expectations or pin requests version.

**Likelihood**: High (95%)
```

## Tips for Effective Analysis

**Start with the obvious:**
- What changed most recently?
- What does the error message say?
- What file is the test testing?

**Follow the stack trace:**
- Start from the innermost frame
- Identify which line in your code fails
- Work backwards to understand why

**Look for patterns:**
- Do multiple tests fail the same way?
- Are failures in related tests?
- Is there a common dependency?

**Use version control:**
- Git history is your friend
- Use `git bisect` for complex cases
- Compare working vs broken states

**Verify assumptions:**
- Don't assume—test your hypotheses
- Try potential fixes
- Check related code

**Document findings:**
- Record what you tried
- Note what worked and what didn't
- Build institutional knowledge

## Reference

For comprehensive failure patterns and their causes, see [failure-patterns.md](references/failure-patterns.md).
