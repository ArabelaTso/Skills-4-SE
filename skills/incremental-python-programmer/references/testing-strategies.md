# Testing Strategies

## Test Generation Principles

### Test Coverage Goals
- Test all public functions and methods
- Test edge cases and boundary conditions
- Test error handling and exceptions
- Test integration points
- Aim for >80% code coverage

### Test Organization
```
tests/
├── __init__.py
├── test_module1.py
├── test_module2.py
├── integration/
│   ├── __init__.py
│   └── test_integration.py
└── conftest.py  # pytest fixtures
```

## Unit Test Patterns

### Basic Function Test

```python
import pytest
from module import function_to_test

def test_function_basic():
    """Test basic functionality."""
    result = function_to_test("input")
    assert result == "expected_output"

def test_function_with_different_input():
    """Test with different input."""
    result = function_to_test("other_input")
    assert result == "other_expected_output"
```

### Testing with Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {"key": "value", "number": 42}

def test_with_fixture(sample_data):
    """Test using fixture."""
    result = process_data(sample_data)
    assert result["key"] == "value"
    assert result["number"] == 42
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("input_value,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_uppercase(input_value, expected):
    """Test uppercase conversion with multiple inputs."""
    result = to_uppercase(input_value)
    assert result == expected
```

### Testing Exceptions

```python
import pytest

def test_function_raises_value_error():
    """Test that function raises ValueError for invalid input."""
    with pytest.raises(ValueError, match="Invalid input"):
        function_with_validation("")

def test_function_raises_type_error():
    """Test that function raises TypeError for wrong type."""
    with pytest.raises(TypeError):
        function_with_validation(123)
```

### Testing Class Methods

```python
import pytest

class TestMyClass:
    """Test suite for MyClass."""

    @pytest.fixture
    def instance(self):
        """Create instance for testing."""
        return MyClass(param="value")

    def test_initialization(self, instance):
        """Test class initialization."""
        assert instance.param == "value"

    def test_method(self, instance):
        """Test class method."""
        result = instance.method()
        assert result is not None
```

## Integration Test Patterns

### Testing Component Interactions

```python
import pytest

def test_end_to_end_workflow():
    """Test complete workflow from input to output."""
    # Setup
    data = load_test_data()

    # Execute workflow
    processed = process_data(data)
    result = save_data(processed)

    # Verify
    assert result["status"] == "success"
    assert result["records_processed"] > 0
```

### Testing with External Dependencies

```python
import pytest
from unittest.mock import Mock, patch

@patch('module.external_api_call')
def test_with_mocked_api(mock_api):
    """Test function that calls external API."""
    # Setup mock
    mock_api.return_value = {"data": "mocked_response"}

    # Execute
    result = function_that_calls_api()

    # Verify
    assert result["data"] == "mocked_response"
    mock_api.assert_called_once()
```

### Testing Database Operations

```python
import pytest

@pytest.fixture
def db_session():
    """Create test database session."""
    # Setup test database
    session = create_test_session()
    yield session
    # Teardown
    session.rollback()
    session.close()

def test_database_insert(db_session):
    """Test inserting data into database."""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    # Verify
    retrieved = db_session.query(User).filter_by(email="test@example.com").first()
    assert retrieved is not None
    assert retrieved.name == "Test User"
```

## Test Fixing Strategies

### Common Test Failures

**1. Assertion Failures**
```python
# Failing test
def test_calculation():
    result = calculate(5, 3)
    assert result == 15  # Expected 8, got 15

# Fix: Update assertion or fix implementation
def test_calculation():
    result = calculate(5, 3)
    assert result == 8  # Corrected expectation
```

**2. Import Errors**
```python
# Failing test
from module import new_function  # ImportError

# Fix: Check module path and function name
from module.submodule import new_function  # Corrected import
```

**3. Missing Fixtures**
```python
# Failing test
def test_with_data(sample_data):  # Fixture not found
    pass

# Fix: Add fixture
@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_with_data(sample_data):
    pass
```

**4. Type Errors**
```python
# Failing test
def test_function():
    result = function("string")  # TypeError: expected int
    assert result == "output"

# Fix: Use correct type
def test_function():
    result = function(123)  # Corrected type
    assert result == "output"
```

### Debugging Test Failures

**Steps:**
1. Read error message carefully
2. Check test expectations vs actual behavior
3. Verify test setup and fixtures
4. Check for side effects from other tests
5. Run test in isolation
6. Add print statements or use debugger

**Example debugging:**
```python
def test_complex_function():
    """Test with debugging."""
    input_data = {"key": "value"}
    print(f"Input: {input_data}")  # Debug print

    result = complex_function(input_data)
    print(f"Result: {result}")  # Debug print

    assert result["status"] == "success"
```

## Test Running Strategies

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_module.py

# Run specific test
pytest tests/test_module.py::test_function

# Run with coverage
pytest --cov=module --cov-report=html

# Run with verbose output
pytest -v

# Run and stop at first failure
pytest -x
```

### Test Markers

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    """Test that takes a long time."""
    pass

@pytest.mark.integration
def test_integration():
    """Integration test."""
    pass

# Run only marked tests
# pytest -m slow
# pytest -m "not slow"
```

## Coverage Analysis

### Identifying Uncovered Code

```bash
# Generate coverage report
pytest --cov=module --cov-report=term-missing

# Output shows:
# module.py    85%   45-47, 52
# Lines 45-47 and 52 are not covered
```

### Writing Tests for Uncovered Code

```python
# Uncovered code
def function_with_branches(value):
    if value > 10:
        return "high"  # Covered
    else:
        return "low"   # Not covered

# Add test for uncovered branch
def test_function_low_value():
    """Test function with low value."""
    result = function_with_branches(5)
    assert result == "low"
```

## Test Quality Guidelines

### Good Test Characteristics

**1. Independent**
- Tests don't depend on each other
- Can run in any order
- Clean setup and teardown

**2. Readable**
- Clear test names
- Descriptive assertions
- Well-organized

**3. Fast**
- Run quickly
- Use mocks for slow operations
- Minimize I/O

**4. Reliable**
- Consistent results
- No flaky behavior
- Deterministic

### Test Naming Conventions

```python
# Good test names
def test_user_creation_with_valid_email():
    """Test creating user with valid email."""
    pass

def test_user_creation_raises_error_for_invalid_email():
    """Test that user creation raises error for invalid email."""
    pass

def test_calculate_returns_sum_of_two_numbers():
    """Test that calculate returns sum of two numbers."""
    pass
```

### Assertion Best Practices

```python
# Good: Specific assertions
assert result == expected_value
assert len(items) == 3
assert "key" in dictionary

# Good: Descriptive messages
assert result == expected, f"Expected {expected}, got {result}"

# Avoid: Multiple unrelated assertions in one test
# Split into separate tests instead
```

## Test-Driven Development (TDD) Approach

### TDD Workflow

1. **Write failing test**
```python
def test_new_feature():
    """Test new feature that doesn't exist yet."""
    result = new_feature("input")
    assert result == "expected"
```

2. **Implement minimal code to pass**
```python
def new_feature(input_value):
    """Minimal implementation."""
    return "expected"
```

3. **Refactor and improve**
```python
def new_feature(input_value):
    """Improved implementation."""
    # Proper logic here
    return process(input_value)
```

4. **Repeat for next feature**

### Benefits of TDD
- Tests written before code
- Ensures testability
- Clear requirements
- Immediate feedback
- Better design
