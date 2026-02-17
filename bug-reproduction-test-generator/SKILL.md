---
name: bug-reproduction-test-generator
description: "Automatically generates executable tests that reproduce reported bugs from issue reports and code repositories. Use when users need to: (1) Create a test that reproduces a bug described in an issue report, (2) Generate failing tests from bug descriptions, stack traces, or error messages, (3) Validate bug reports by creating reproducible test cases, (4) Convert issue reports into executable regression tests. Takes a repository and issue report as input and produces test code that reliably triggers the reported bug."
---

# Bug Reproduction Test Generator

Generate executable tests that reproduce reported bugs based on issue reports and code repositories.

## Workflow

Follow these steps to generate a bug reproduction test:

### 1. Analyze the Issue Report

Extract key information from the issue report:

- **Symptoms**: What goes wrong? (incorrect output, exception, crash, assertion failure, unexpected behavior)
- **Affected components**: Which modules, classes, or functions are involved?
- **Triggering conditions**: What inputs, states, or sequences trigger the bug?
- **Stack traces**: If provided, identify the call chain and failure point
- **Expected vs. actual behavior**: What should happen vs. what actually happens?

### 2. Inspect the Repository

Identify relevant code and context:

- Locate the affected components mentioned in the issue
- Find entry points (public APIs, main functions, test fixtures)
- Understand dependencies and required setup
- Identify the test framework used (pytest, unittest, JUnit, Jest, etc.)
- Check existing test patterns for consistency

### 3. Generate the Reproduction Test

Create a minimal, focused test that:

**Test structure:**
- Uses the repository's existing test framework and conventions
- Sets up minimal preconditions needed to trigger the bug
- Executes the code path that triggers the bug
- Asserts the symptom described in the issue report

**Assertions:**
- For exceptions: Assert the exception type and message match the report
- For incorrect output: Assert actual output matches the reported incorrect behavior
- For crashes: Assert the crash occurs at the expected point
- For assertion failures: Reproduce the failing assertion

**Documentation:**
- Add inline comments explaining the reproduction logic
- Reference the issue number/URL in the test name or docstring
- Document any assumptions made due to underspecified details

### 4. Output Format

Provide:

1. **Executable test code** in the appropriate language and framework
2. **Inline comments** explaining how the test reproduces the bug
3. **Markdown summary** including:
   - How the test reproduces the issue
   - Which symptoms it validates
   - Any assumptions made
   - Instructions for running the test

## Example Workflow

**Issue Report:**
```
Title: Division by zero in calculate_average()
Description: When calling calculate_average([]) with an empty list,
the function crashes with ZeroDivisionError instead of returning 0.

Stack trace:
  File "stats.py", line 15, in calculate_average
    return sum(values) / len(values)
ZeroDivisionError: division by zero
```

**Generated Test (Python/pytest):**
```python
import pytest
from stats import calculate_average

def test_calculate_average_empty_list_reproduction():
    """
    Reproduces bug: calculate_average([]) raises ZeroDivisionError
    Issue: #123

    Expected: Should return 0 for empty list
    Actual: Raises ZeroDivisionError
    """
    # Trigger the bug with empty list input
    with pytest.raises(ZeroDivisionError):
        result = calculate_average([])

    # This test currently passes (reproduces the bug)
    # After fix, change to: assert calculate_average([]) == 0
```

**Summary:**
```markdown
## Bug Reproduction Test

**Issue**: Division by zero in calculate_average()

**How it reproduces the bug:**
- Calls `calculate_average([])` with an empty list
- Asserts that ZeroDivisionError is raised (the buggy behavior)

**Symptoms validated:**
- Exception type: ZeroDivisionError
- Location: stats.py line 15

**Assumptions:**
- The function should return 0 for empty lists (common convention)

**Running the test:**
```bash
pytest test_stats.py::test_calculate_average_empty_list_reproduction
```

**After the bug is fixed:**
Replace the `pytest.raises` assertion with:
```python
assert calculate_average([]) == 0
```
```

## Language-Specific Patterns

### Python (pytest/unittest)

```python
import pytest

def test_bug_reproduction_issue_123():
    """Reproduces bug #123: [brief description]"""
    # Setup: Create conditions that trigger the bug

    # Execute: Run the code that exhibits the bug

    # Assert: Verify the buggy behavior occurs
    with pytest.raises(ExpectedException):
        buggy_function()
```

### Java (JUnit)

```java
@Test
public void testBugReproduction_Issue123() {
    // Reproduces bug #123: [brief description]

    // Setup: Create conditions that trigger the bug

    // Execute and Assert: Verify the buggy behavior
    assertThrows(ExpectedException.class, () -> {
        buggyMethod();
    });
}
```

### JavaScript (Jest)

```javascript
test('reproduces bug #123: [brief description]', () => {
  // Setup: Create conditions that trigger the bug

  // Execute and Assert: Verify the buggy behavior
  expect(() => {
    buggyFunction();
  }).toThrow(ExpectedException);
});
```

## Constraints

- **Do not modify production code** - Only create test code
- **Do not assume fixes** - Test the buggy behavior, not the expected correct behavior (unless explicitly stated in the issue)
- **Document assumptions** - If the issue is underspecified, state assumptions clearly
- **Prefer minimal tests** - Focus on isolating the bug, avoid unnecessary setup
- **Match existing patterns** - Follow the repository's test conventions and style

## Handling Underspecified Issues

When the issue report lacks details:

1. **State assumptions explicitly** in test comments
2. **Document what's unclear** in the summary
3. **Provide multiple test variants** if multiple interpretations are possible
4. **Ask clarifying questions** if critical information is missing

Example:
```python
def test_bug_reproduction_issue_456():
    """
    Reproduces bug #456: Null pointer exception in processData()

    ASSUMPTION: The bug occurs when input is null (not specified in issue)
    ASSUMPTION: Using default configuration (not specified in issue)
    """
    # Test with null input (assumed trigger)
    with pytest.raises(NullPointerException):
        processData(None)
```

## Tips for Effective Reproduction Tests

1. **Start simple** - Begin with the most direct path to trigger the bug
2. **Isolate the bug** - Remove unrelated setup and assertions
3. **Make it deterministic** - Avoid flaky conditions (timing, randomness)
4. **Reference the issue** - Include issue number in test name and comments
5. **Verify it fails** - Run the test to confirm it reproduces the bug
6. **Plan for the fix** - Comment on how the test should change after the bug is fixed
