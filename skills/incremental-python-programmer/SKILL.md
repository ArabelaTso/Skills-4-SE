---
name: incremental-python-programmer
description: "Takes a Python repository and natural language feature description as input, implements the feature with proper code placement, generates comprehensive tests, and ensures all tests pass. Use when Claude needs to: (1) Add new features to existing Python projects, (2) Implement functions, classes, or modules based on requirements, (3) Modify existing code to add functionality, (4) Generate unit and integration tests for new code, (5) Fix failing tests after implementation, (6) Ensure code follows existing patterns and conventions."
---

# Incremental Python Programmer

Implement new features in Python repositories with automated testing and validation.

## Workflow

### 1. Understand the Feature Request

**Parse the request:**
- Identify what functionality is being requested
- Determine scope (function, class, module, or modification)
- Understand expected behavior and inputs/outputs
- Note any specific requirements or constraints

**Clarify if needed:**
- Ask about edge cases
- Confirm integration points
- Verify expected behavior
- Check for dependencies

### 2. Analyze Repository Structure

**Automated analysis:**
```bash
python scripts/analyze_repo_structure.py <repo_path>
```

**Manual analysis:**
- Identify relevant modules and files
- Understand existing code organization
- Find similar existing implementations
- Locate test directory structure
- Check coding conventions and patterns

**Key questions:**
- Where should the new code be placed?
- What existing code needs modification?
- What dependencies are needed?
- What patterns should be followed?

See [implementation-patterns.md](references/implementation-patterns.md) for common patterns.

### 3. Plan Implementation

**Determine implementation approach:**

**For new functions:**
- Identify appropriate module
- Determine function signature
- Plan implementation logic
- Identify dependencies

**For new classes:**
- Identify appropriate module or create new one
- Design class structure and methods
- Plan initialization and attributes
- Consider inheritance if applicable

**For new modules:**
- Determine module name and location
- Plan module structure
- Identify exports and public API
- Plan integration with existing code

**For modifications:**
- Identify code to modify
- Plan backward compatibility
- Determine parameter additions
- Plan integration with existing logic

### 4. Implement the Feature

Follow this order:

**Step 1: Add necessary imports**
```python
# Standard library
import os
from typing import List, Dict, Optional

# Third-party (add to requirements.txt if new)
import requests

# Local imports
from .existing_module import helper_function
```

**Step 2: Implement core functionality**
- Follow existing code style and conventions
- Use type hints consistently
- Add docstrings for all public functions/classes
- Include error handling
- Follow patterns from similar code

**Step 3: Integrate with existing code**
- Update relevant functions/classes
- Add new module to `__init__.py` if needed
- Update configuration if required
- Ensure backward compatibility

**Example: Adding a new function**
```python
def new_feature_function(param1: str, param2: int = 10) -> dict:
    """
    Brief description of what the function does.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)

    Returns:
        Dictionary containing results

    Raises:
        ValueError: If param1 is empty
        TypeError: If param2 is not an integer
    """
    # Validate inputs
    if not param1:
        raise ValueError("param1 cannot be empty")

    # Implementation
    result = {
        "input": param1,
        "multiplier": param2,
        "output": len(param1) * param2
    }

    return result
```

**Example: Adding a new class**
```python
class NewFeatureClass:
    """
    Class for handling new feature functionality.

    Attributes:
        attribute1: Description of attribute1
        attribute2: Description of attribute2
    """

    def __init__(self, param1: str, param2: int = 10):
        """
        Initialize NewFeatureClass.

        Args:
            param1: Description
            param2: Description (default: 10)
        """
        self.attribute1 = param1
        self.attribute2 = param2

    def method1(self) -> str:
        """Method description."""
        return f"{self.attribute1}_{self.attribute2}"

    def method2(self, value: int) -> int:
        """Method description."""
        return value * self.attribute2
```

**Example: Modifying existing code**
```python
# Before
def existing_function(param: str) -> str:
    return param.upper()

# After - adding new parameter with default
def existing_function(param: str, enable_new_feature: bool = False) -> str:
    result = param.upper()
    if enable_new_feature:
        result = apply_new_transformation(result)
    return result

def apply_new_transformation(text: str) -> str:
    """New feature logic."""
    return f"[TRANSFORMED] {text}"
```

See [implementation-patterns.md](references/implementation-patterns.md) for detailed patterns.

### 5. Generate Tests

**Identify test requirements:**
- What needs to be tested?
- What are the edge cases?
- What are the integration points?
- What error conditions exist?

**Generate unit tests:**

```python
import pytest
from module import new_feature_function, NewFeatureClass

class TestNewFeatureFunction:
    """Test suite for new_feature_function."""

    def test_basic_functionality(self):
        """Test basic functionality."""
        result = new_feature_function("test", 5)
        assert result["input"] == "test"
        assert result["multiplier"] == 5
        assert result["output"] == 20

    def test_default_parameter(self):
        """Test with default parameter."""
        result = new_feature_function("hello")
        assert result["multiplier"] == 10
        assert result["output"] == 50

    def test_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            new_feature_function("", 5)

    @pytest.mark.parametrize("input_str,multiplier,expected", [
        ("a", 1, 1),
        ("ab", 2, 4),
        ("abc", 3, 9),
    ])
    def test_various_inputs(self, input_str, multiplier, expected):
        """Test with various inputs."""
        result = new_feature_function(input_str, multiplier)
        assert result["output"] == expected


class TestNewFeatureClass:
    """Test suite for NewFeatureClass."""

    @pytest.fixture
    def instance(self):
        """Create instance for testing."""
        return NewFeatureClass("test", 5)

    def test_initialization(self, instance):
        """Test class initialization."""
        assert instance.attribute1 == "test"
        assert instance.attribute2 == 5

    def test_method1(self, instance):
        """Test method1."""
        result = instance.method1()
        assert result == "test_5"

    def test_method2(self, instance):
        """Test method2."""
        result = instance.method2(3)
        assert result == 15
```

**Generate integration tests if needed:**

```python
def test_integration_with_existing_code():
    """Test that new feature integrates with existing code."""
    # Setup
    data = prepare_test_data()

    # Execute workflow using new feature
    result = existing_workflow(data, use_new_feature=True)

    # Verify
    assert result["status"] == "success"
    assert "new_feature_output" in result
```

See [testing-strategies.md](references/testing-strategies.md) for comprehensive testing patterns.

### 6. Run Tests

**Execute test suite:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=module --cov-report=term-missing

# Run specific test file
pytest tests/test_new_feature.py

# Run with verbose output
pytest -v
```

**Check results:**
- All tests should pass
- Coverage should be adequate (>80% for new code)
- No regressions in existing tests

### 7. Fix Failing Tests

If tests fail, diagnose and fix:

**Common issues:**

**1. Assertion failures**
- Check expected vs actual values
- Verify test logic
- Fix implementation or test

**2. Import errors**
- Verify module paths
- Check `__init__.py` exports
- Ensure dependencies installed

**3. Type errors**
- Check function signatures
- Verify parameter types
- Update type hints if needed

**4. Logic errors**
- Debug implementation
- Add print statements
- Use pytest debugger: `pytest --pdb`

**Example fix:**
```python
# Failing test
def test_calculation():
    result = calculate(5, 3)
    assert result == 15  # AssertionError: assert 8 == 15

# Diagnosis: Expected value is wrong
# Fix: Update test expectation
def test_calculation():
    result = calculate(5, 3)
    assert result == 8  # Corrected
```

See [testing-strategies.md](references/testing-strategies.md) for test fixing strategies.

### 8. Verify and Document

**Final verification:**
- All tests pass
- Code follows existing conventions
- Documentation is complete
- No regressions introduced
- Integration points work correctly

**Documentation checklist:**
- Docstrings for all public functions/classes
- Type hints for parameters and returns
- Examples in docstrings if complex
- Update README if needed
- Add comments for complex logic

**Summary to provide:**
1. **Files modified/created:**
   - List all changed files
   - Indicate new vs modified

2. **Implementation summary:**
   - What was implemented
   - Key design decisions
   - Integration points

3. **Tests added:**
   - Number of tests
   - Coverage achieved
   - Test types (unit/integration)

4. **Test results:**
   - All tests passing
   - Coverage percentage
   - Any notes or warnings

## Implementation Guidelines

### Code Placement

**Functions:**
- Add to existing module if related functionality exists
- Create new module if distinct feature area
- Place after imports and constants
- Group related functions together

**Classes:**
- Add to existing module if related
- Create new module for new feature areas
- Place after imports and before functions
- Follow existing class organization

**Modules:**
- Create in appropriate package directory
- Follow existing naming conventions
- Add to `__init__.py` for public API
- Include module docstring

### Code Style

**Follow existing conventions:**
- Indentation (spaces vs tabs)
- Line length limits
- Naming conventions (snake_case, PascalCase)
- Import organization
- Docstring style (Google, NumPy, etc.)

**Type hints:**
- Use for all function parameters
- Use for return values
- Import from `typing` module
- Be specific (List[str] not just List)

**Error handling:**
- Validate inputs
- Raise appropriate exceptions
- Include error messages
- Follow existing error patterns

### Testing Best Practices

**Test coverage:**
- Test all public functions/methods
- Test edge cases and boundaries
- Test error conditions
- Test integration points

**Test organization:**
- One test file per module
- Group related tests in classes
- Use descriptive test names
- Use fixtures for setup

**Test quality:**
- Tests should be independent
- Tests should be fast
- Tests should be deterministic
- Tests should be readable

## Common Scenarios

### Scenario 1: Add New Function to Existing Module

**Request:** "Add a function to validate email addresses"

**Steps:**
1. Analyze: Find appropriate module (e.g., `validators.py`)
2. Implement: Add `validate_email()` function
3. Test: Create `test_validate_email()` with various cases
4. Verify: Run tests, ensure all pass

### Scenario 2: Add New Class

**Request:** "Create a UserManager class to handle user operations"

**Steps:**
1. Analyze: Determine if new module needed or add to existing
2. Implement: Create `UserManager` class with methods
3. Test: Create `TestUserManager` class with method tests
4. Verify: Run tests, check integration

### Scenario 3: Modify Existing Function

**Request:** "Add optional caching to the data_loader function"

**Steps:**
1. Analyze: Understand current implementation
2. Implement: Add cache parameter and logic
3. Test: Add tests for cached and non-cached behavior
4. Verify: Run all tests including existing ones

### Scenario 4: Add New Module

**Request:** "Add a reporting module with PDF generation"

**Steps:**
1. Analyze: Plan module structure and dependencies
2. Implement: Create `reporting.py` with functions/classes
3. Test: Create `test_reporting.py` with comprehensive tests
4. Verify: Run tests, update `__init__.py`

## Troubleshooting

### Implementation Issues

**Problem: Don't know where to place code**
- Solution: Look for similar functionality in codebase
- Use repository analyzer script
- Follow existing module organization

**Problem: Unclear how to integrate with existing code**
- Solution: Find similar integration points
- Check how existing features are integrated
- Ask for clarification if needed

**Problem: Missing dependencies**
- Solution: Check requirements.txt
- Look at imports in similar modules
- Add to requirements.txt if new

### Testing Issues

**Problem: Tests fail after implementation**
- Solution: Read error messages carefully
- Check test expectations
- Debug implementation
- Fix code or tests as appropriate

**Problem: Low test coverage**
- Solution: Run coverage report
- Identify uncovered lines
- Add tests for uncovered code

**Problem: Tests are flaky**
- Solution: Check for timing issues
- Remove randomness
- Ensure test independence
- Use mocks for external dependencies

## Best Practices

### Implementation
- Start with simplest solution
- Follow existing patterns
- Write clean, readable code
- Add comprehensive documentation
- Consider edge cases

### Testing
- Write tests as you implement
- Test behavior, not implementation
- Use descriptive test names
- Keep tests simple and focused
- Aim for high coverage

### Integration
- Ensure backward compatibility
- Test integration points
- Update documentation
- Consider migration path if breaking changes

### Quality
- Run all tests before finishing
- Check code style consistency
- Review error handling
- Verify documentation completeness
- Test edge cases thoroughly
