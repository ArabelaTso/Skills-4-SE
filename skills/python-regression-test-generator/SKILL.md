---
name: python-regression-test-generator
description: Automatically generates regression tests for Python codebases by analyzing changes between old and new code versions and their existing tests. Migrates tests to work with new code, generates tests for new functionality, and creates mocks for external dependencies. Supports unittest and pytest frameworks. Use when refactoring code, adding features, or ensuring backward compatibility.
---

# Python Regression Test Generator

## Overview

This skill automatically generates regression tests for Python code by analyzing differences between old and new versions, migrating existing tests, and creating new tests for modified or added functionality. It ensures previously tested behavior still works while covering new code paths.

## Test Generation Workflow

Follow these steps to generate regression tests:

### 1. Analyze Code Changes

**Compare old and new versions to identify:**

**Function Signature Changes:**
- Added parameters (with or without defaults)
- Removed parameters
- Changed parameter types or names
- Changed return types

**Logic Changes:**
- Modified implementation
- New validation rules
- Changed error handling
- Algorithm improvements

**Structural Changes:**
- Added functions/classes/methods
- Removed functions/classes/methods
- Renamed functions/classes/methods
- Moved code between modules

**Example Analysis:**
```python
# Old version
def calculate_total(items):
    return sum(item.price for item in items)

# New version
def calculate_total(items, tax_rate=0.0):
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)
```

**Changes identified:**
- Added parameter: `tax_rate` with default value 0.0
- Modified logic: now applies tax calculation
- Backward compatible: old calls still work

### 2. Analyze Existing Tests

**Review old tests to understand:**
- Test structure (unittest vs pytest)
- Test coverage (which functions/paths are tested)
- Test patterns (fixtures, mocks, parametrization)
- Dependencies and setup requirements

**Example Existing Test:**
```python
def test_calculate_total():
    items = [Item(price=10), Item(price=20)]
    assert calculate_total(items) == 30
```

**Analysis:**
- Uses pytest style
- Tests basic functionality
- No mocking needed
- Simple assertion

### 3. Migrate Existing Tests

**Update tests to work with new code:**

**For backward-compatible changes:**
- Keep original test (ensures backward compatibility)
- Add new tests for new functionality

**For breaking changes:**
- Update test to match new signature/behavior
- Document what changed in test docstring

**Migrated Tests:**
```python
def test_calculate_total_no_tax():
    """Regression: ensure backward compatibility with no tax"""
    items = [Item(price=10), Item(price=20)]
    assert calculate_total(items) == 30  # Uses default tax_rate=0.0

def test_calculate_total_with_tax():
    """New: test tax calculation functionality"""
    items = [Item(price=10), Item(price=20)]
    assert calculate_total(items, tax_rate=0.1) == 33.0
```

### 4. Generate Tests for New Functionality

**Create tests for:**
- New parameters and their effects
- New functions/methods
- New code paths
- Edge cases and boundaries
- Error conditions

**Generated Tests:**
```python
def test_calculate_total_zero_tax():
    """Test explicit zero tax rate"""
    items = [Item(price=100)]
    assert calculate_total(items, tax_rate=0.0) == 100

def test_calculate_total_high_tax():
    """Test high tax rate"""
    items = [Item(price=100)]
    assert calculate_total(items, tax_rate=0.5) == 150

def test_calculate_total_empty_items():
    """Edge case: empty items list"""
    assert calculate_total([], tax_rate=0.1) == 0

def test_calculate_total_negative_tax():
    """Edge case: negative tax (discount)"""
    items = [Item(price=100)]
    assert calculate_total(items, tax_rate=-0.1) == 90
```

### 5. Create Mocks for Dependencies

**Identify dependencies that need mocking:**
- External APIs and HTTP requests
- Database operations
- File I/O operations
- Email/notification services
- Time-dependent operations
- Random number generation

**Example with External Dependency:**

**New Code:**
```python
def send_notification(user_id, message):
    user = database.get_user(user_id)
    email_service.send_email(
        to=user.email,
        subject='Notification',
        body=message
    )
    return True
```

**Generated Test with Mocks:**
```python
from unittest.mock import Mock, patch

def test_send_notification():
    """Test notification sending with mocked dependencies"""
    # Mock database
    mock_db = Mock()
    mock_user = Mock()
    mock_user.email = 'user@example.com'
    mock_db.get_user.return_value = mock_user

    # Mock email service
    with patch('myapp.email_service.send_email') as mock_send:
        mock_send.return_value = True

        with patch('myapp.database', mock_db):
            result = send_notification(user_id=123, message="Hello")

            assert result is True
            mock_db.get_user.assert_called_once_with(123)
            mock_send.assert_called_once_with(
                to='user@example.com',
                subject='Notification',
                body='Hello'
            )
```

### 6. Add Setup and Teardown

**Determine if tests need:**
- Shared fixtures
- Database setup/cleanup
- File creation/deletion
- State initialization

**unittest Setup:**
```python
class TestCalculateTotal(unittest.TestCase):
    def setUp(self):
        """Run before each test"""
        self.items = [
            Item(price=10),
            Item(price=20),
            Item(price=30)
        ]

    def test_no_tax(self):
        result = calculate_total(self.items)
        self.assertEqual(result, 60)

    def test_with_tax(self):
        result = calculate_total(self.items, tax_rate=0.1)
        self.assertAlmostEqual(result, 66.0)
```

**pytest Fixtures:**
```python
@pytest.fixture
def items():
    """Fixture providing test items"""
    return [
        Item(price=10),
        Item(price=20),
        Item(price=30)
    ]

def test_no_tax(items):
    result = calculate_total(items)
    assert result == 60

def test_with_tax(items):
    result = calculate_total(items, tax_rate=0.1)
    assert result == pytest.approx(66.0)
```

### 7. Ensure Test Quality

**Verify generated tests are:**
- **Deterministic:** Same input always produces same output
- **Isolated:** Tests don't depend on each other
- **Readable:** Clear test names and docstrings
- **Maintainable:** Follow project conventions
- **Executable:** Can run without errors

## Complete Example

### Scenario: Adding Tax Calculation

**Old Code (calculator.py):**
```python
class Calculator:
    def calculate_total(self, items):
        """Calculate total price of items"""
        return sum(item.price for item in items)
```

**Old Test (test_calculator.py):**
```python
import unittest
from calculator import Calculator
from models import Item

class TestCalculator(unittest.TestCase):
    def test_calculate_total(self):
        calc = Calculator()
        items = [Item(price=10), Item(price=20)]
        result = calc.calculate_total(items)
        self.assertEqual(result, 30)
```

**New Code (calculator.py):**
```python
class Calculator:
    def calculate_total(self, items, tax_rate=0.0, discount=0.0):
        """Calculate total price with tax and discount"""
        if tax_rate < 0 or tax_rate > 1:
            raise ValueError("Tax rate must be between 0 and 1")
        if discount < 0 or discount > 1:
            raise ValueError("Discount must be between 0 and 1")

        subtotal = sum(item.price for item in items)
        after_discount = subtotal * (1 - discount)
        total = after_discount * (1 + tax_rate)
        return round(total, 2)
```

**Generated Regression Tests (test_calculator.py):**
```python
import unittest
from unittest.mock import Mock
from calculator import Calculator
from models import Item

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.calc = Calculator()
        self.items = [Item(price=10), Item(price=20)]

    def test_calculate_total_backward_compatibility(self):
        """Regression: ensure old behavior still works"""
        result = self.calc.calculate_total(self.items)
        self.assertEqual(result, 30)

    def test_calculate_total_with_tax(self):
        """New: test tax calculation"""
        result = self.calc.calculate_total(self.items, tax_rate=0.1)
        self.assertAlmostEqual(result, 33.0)

    def test_calculate_total_with_discount(self):
        """New: test discount calculation"""
        result = self.calc.calculate_total(self.items, discount=0.2)
        self.assertAlmostEqual(result, 24.0)

    def test_calculate_total_with_tax_and_discount(self):
        """New: test combined tax and discount"""
        result = self.calc.calculate_total(
            self.items,
            tax_rate=0.1,
            discount=0.2
        )
        self.assertAlmostEqual(result, 26.4)

    def test_calculate_total_empty_items(self):
        """Edge case: empty items list"""
        result = self.calc.calculate_total([])
        self.assertEqual(result, 0)

    def test_calculate_total_invalid_tax_rate_negative(self):
        """Error case: negative tax rate"""
        with self.assertRaises(ValueError) as context:
            self.calc.calculate_total(self.items, tax_rate=-0.1)
        self.assertIn("Tax rate must be between 0 and 1", str(context.exception))

    def test_calculate_total_invalid_tax_rate_too_high(self):
        """Error case: tax rate > 1"""
        with self.assertRaises(ValueError):
            self.calc.calculate_total(self.items, tax_rate=1.5)

    def test_calculate_total_invalid_discount_negative(self):
        """Error case: negative discount"""
        with self.assertRaises(ValueError):
            self.calc.calculate_total(self.items, discount=-0.1)

    def test_calculate_total_invalid_discount_too_high(self):
        """Error case: discount > 1"""
        with self.assertRaises(ValueError):
            self.calc.calculate_total(self.items, discount=1.5)

if __name__ == '__main__':
    unittest.main()
```

## Framework-Specific Examples

### pytest Example

**Old Code:**
```python
def fetch_user_data(user_id):
    response = requests.get(f'https://api.example.com/users/{user_id}')
    return response.json()
```

**Old Test:**
```python
def test_fetch_user_data():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'id': 1, 'name': 'Alice'}
        result = fetch_user_data(1)
        assert result['name'] == 'Alice'
```

**New Code:**
```python
async def fetch_user_data(user_id, include_posts=False):
    async with aiohttp.ClientSession() as session:
        url = f'https://api.example.com/users/{user_id}'
        if include_posts:
            url += '?include=posts'
        async with session.get(url) as response:
            return await response.json()
```

**Generated Regression Tests:**
```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_fetch_user_data_backward_compatibility():
    """Regression: basic user fetch still works"""
    with patch('aiohttp.ClientSession') as mock_session:
        mock_response = AsyncMock()
        mock_response.json.return_value = {'id': 1, 'name': 'Alice'}
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response

        result = await fetch_user_data(1)
        assert result['name'] == 'Alice'

@pytest.mark.asyncio
async def test_fetch_user_data_with_posts():
    """New: test include_posts parameter"""
    with patch('aiohttp.ClientSession') as mock_session:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            'id': 1,
            'name': 'Alice',
            'posts': [{'id': 1, 'title': 'Post 1'}]
        }
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response

        result = await fetch_user_data(1, include_posts=True)
        assert 'posts' in result
        assert len(result['posts']) == 1

@pytest.mark.asyncio
@pytest.mark.parametrize("user_id,include_posts", [
    (1, False),
    (1, True),
    (999, False),
])
async def test_fetch_user_data_parametrized(user_id, include_posts):
    """Parametrized test for various inputs"""
    with patch('aiohttp.ClientSession') as mock_session:
        mock_response = AsyncMock()
        mock_response.json.return_value = {'id': user_id, 'name': 'User'}
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response

        result = await fetch_user_data(user_id, include_posts=include_posts)
        assert result['id'] == user_id
```

## Test Generation Guidelines

### When to Migrate vs Create New

**Migrate existing test when:**
- Function signature changed but is backward compatible
- Return type changed (update assertions)
- Exception type changed
- Implementation changed but interface is same

**Create new test when:**
- New parameters added
- New functionality added
- New code paths introduced
- New edge cases discovered

**Mark as obsolete when:**
- Function removed from codebase
- Functionality completely replaced
- Test no longer relevant

### Naming Conventions

**Regression tests:**
- `test_<function>_backward_compatibility`
- `test_<function>_<old_behavior>`
- Include "Regression:" in docstring

**New functionality tests:**
- `test_<function>_<new_feature>`
- `test_<function>_with_<parameter>`
- Include "New:" in docstring

**Edge case tests:**
- `test_<function>_empty_input`
- `test_<function>_boundary_<condition>`
- Include "Edge case:" in docstring

**Error tests:**
- `test_<function>_invalid_<parameter>`
- `test_<function>_raises_<exception>`
- Include "Error case:" in docstring

### Mock Generation Rules

**Always mock:**
- External API calls (requests, aiohttp)
- Database operations
- File system operations
- Email/SMS services
- Time-dependent functions (datetime.now, time.sleep)

**Consider mocking:**
- Complex object creation
- Expensive computations
- Non-deterministic operations

**Don't mock:**
- Simple data structures (lists, dicts)
- Pure functions without side effects
- The function under test
- Standard library functions (unless they have side effects)

## Constraints

**MUST:**
- Analyze both old and new code versions
- Preserve existing valid tests
- Generate tests for new functionality
- Create appropriate mocks for dependencies
- Follow existing test framework (unittest or pytest)
- Ensure tests are deterministic and isolated
- Include docstrings explaining test purpose
- Use proper setup/teardown or fixtures

**MUST NOT:**
- Remove valid tests without justification
- Generate redundant tests
- Create tests that depend on external state
- Mock the function being tested
- Generate non-executable test code
- Ignore breaking changes
- Create flaky or non-deterministic tests

## Output Format

**Complete test module structure:**

```python
"""
Regression tests for <module_name>

Generated tests ensure backward compatibility and cover new functionality
added in the latest version.
"""

import unittest  # or pytest
from unittest.mock import Mock, patch, MagicMock
# Other imports

class Test<ClassName>(unittest.TestCase):  # or pytest functions
    def setUp(self):
        """Set up test fixtures"""
        # Setup code

    def test_<name>_backward_compatibility(self):
        """Regression: <description of old behavior>"""
        # Test code

    def test_<name>_<new_feature>(self):
        """New: <description of new functionality>"""
        # Test code

    # More tests...

if __name__ == '__main__':
    unittest.main()
```

## Resources

### references/test_generation_patterns.md
Comprehensive patterns and techniques including:
- Change analysis patterns (signature changes, logic changes, structural changes)
- Test generation strategies (migration, behavior preservation, edge cases)
- Testing framework support (unittest and pytest)
- Mocking and stubbing patterns
- Test structure patterns (AAA, Given-When-Then, setup/teardown)
- Coverage strategies (path coverage, boundary testing, state-based testing)
- Test migration patterns with complete examples

