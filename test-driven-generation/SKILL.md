---
name: test-driven-generation
description: Generate implementation code that passes existing unit tests. Use when the user provides test files (Python pytest/unittest, Java JUnit/TestNG) and asks Claude to implement the code to make those tests pass. Supports full TDD workflow - analyzing tests, generating implementation, running tests, debugging failures, and iterating until all tests pass.
---

# Test-Driven Generation

Generate implementation code that satisfies existing unit tests through an iterative test-driven development workflow.

## Workflow

### 1. Analyze Tests

Read and understand the provided test file(s):

- Identify what functions/classes/methods need to be implemented
- Extract input/output expectations from assertions
- Note edge cases, error conditions, and special behaviors
- Understand dependencies and imports

### 2. Generate Implementation

Create implementation code that should satisfy the tests:

**For Python:**
- Match the exact function/class signatures expected by tests
- Implement logic to satisfy assertions
- Handle all tested edge cases
- Add necessary imports and dependencies

**For Java:**
- Match exact method signatures and return types
- Implement logic within the correct class structure
- Handle exceptions as tested
- Add required imports and annotations

### 3. Run Tests

Execute the test suite to verify the implementation:

**Python:**
```bash
pytest <test_file>.py -v
# or
python -m unittest <test_file>.py -v
```

**Java:**
```bash
mvn test
# or
gradle test
# or for single test file
javac <TestFile>.java && java org.junit.runner.JUnitCore <TestFile>
```

### 4. Debug Failures

If tests fail, analyze the failure output:

- Read the assertion error messages carefully
- Identify which specific test cases are failing
- Understand what the test expected vs. what was returned
- Locate the bug in the implementation

### 5. Iterate

Fix the implementation based on failure analysis:

- Update the code to handle the failing case
- Re-run tests to verify the fix
- Repeat until all tests pass

## Best Practices

### Code Quality
- Write clean, readable implementation code
- Use descriptive variable names
- Add comments for complex logic
- Follow language conventions (PEP 8 for Python, Java naming conventions)

### Test Understanding
- Read ALL test cases before implementing
- Don't assume - verify exact expected behavior from assertions
- Pay attention to parametrized tests and edge cases
- Check test fixtures and setup methods for context

### Debugging Strategy
- Start with the first failing test
- Fix one test at a time when possible
- After each fix, run the full suite to catch regressions
- If stuck, re-read the test to verify understanding

### Common Pitfalls
- **Type mismatches**: Ensure return types match exactly (e.g., int vs float, List vs array)
- **Off-by-one errors**: Carefully check boundary conditions
- **Null/None handling**: Implement null checks if tests verify null behavior
- **Exception types**: Raise/throw the exact exception type the test expects
- **Mutable state**: Reset state between test runs if using class-level variables

## Example Session

User provides `test_calculator.py`:
```python
import pytest
from calculator import Calculator

def test_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0

def test_divide():
    calc = Calculator()
    assert calc.divide(10, 2) == 5
    with pytest.raises(ValueError):
        calc.divide(10, 0)
```

**Step 1**: Analyze - need `Calculator` class with `add()` and `divide()` methods, divide should raise ValueError on zero

**Step 2**: Generate `calculator.py`:
```python
class Calculator:
    def add(self, a, b):
        return a + b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
```

**Step 3**: Run `pytest test_calculator.py -v`

**Step 4**: If failure occurs, read error and identify issue

**Step 5**: Fix and re-run until passing

## Language-Specific Notes

### Python
- Use type hints when test imports suggest them
- Match pytest vs unittest assertion styles
- Check for `setUp`/`tearDown` or fixtures that provide context
- Watch for `@pytest.mark.parametrize` for multiple test cases

### Java
- Match access modifiers (public/private/protected)
- Implement interfaces if tests verify interface compliance
- Use correct exception handling (throws vs try-catch)
- Check for `@Before`/`@After` setup methods
- Watch for `@ParameterizedTest` annotations
