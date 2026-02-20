# Python Regression Test Generation Reference

This reference provides comprehensive patterns and techniques for generating regression tests for Python codebases.

## Table of Contents

1. [Change Analysis Patterns](#change-analysis-patterns)
2. [Test Generation Strategies](#test-generation-strategies)
3. [Testing Framework Support](#testing-framework-support)
4. [Mocking and Stubbing](#mocking-and-stubbing)
5. [Test Structure Patterns](#test-structure-patterns)
6. [Coverage Strategies](#coverage-strategies)
7. [Test Migration Patterns](#test-migration-patterns)

## Change Analysis Patterns

### Types of Code Changes

**1. Function Signature Changes**

**Added Parameters:**
```python
# Old version
def calculate_total(items):
    return sum(item.price for item in items)

# New version
def calculate_total(items, tax_rate=0.0):
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)
```

**Analysis:**
- New parameter `tax_rate` with default value
- Backward compatible (old calls still work)
- Need tests for new parameter

**2. Removed Parameters:**
```python
# Old version
def send_email(to, subject, body, cc=None):
    # implementation

# New version
def send_email(to, subject, body):
    # cc removed
```

**Analysis:**
- Breaking change
- Old tests using `cc` will fail
- Need to update existing tests

**3. Return Type Changes:**
```python
# Old version
def get_user(user_id):
    return user_dict  # Returns dict or None

# New version
def get_user(user_id):
    return User(user_dict) if user_dict else None  # Returns User object or None
```

**Analysis:**
- Return type changed from dict to User object
- Tests accessing dict keys need updating
- Need tests for new object interface

**4. Logic Changes:**
```python
# Old version
def is_valid_email(email):
    return '@' in email

# New version
def is_valid_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

**Analysis:**
- Implementation changed (more strict validation)
- Some previously valid inputs may now be invalid
- Need tests for new validation rules

**5. Added Functions:**
```python
# New version only
def calculate_discount(price, discount_percent):
    return price * (1 - discount_percent / 100)
```

**Analysis:**
- New functionality
- No existing tests to migrate
- Need comprehensive tests for new function

**6. Removed Functions:**
```python
# Old version
def legacy_format(data):
    # implementation
```

**Analysis:**
- Function removed
- Existing tests become obsolete
- Mark tests as obsolete or remove

### Change Detection Techniques

**AST Comparison:**
- Parse both versions into Abstract Syntax Trees
- Compare function definitions, signatures, bodies
- Identify added/removed/modified nodes

**Diff Analysis:**
- Line-by-line comparison
- Identify changed regions
- Map changes to functions/classes

**Semantic Analysis:**
- Analyze behavior changes
- Identify breaking vs non-breaking changes
- Determine test impact

## Test Generation Strategies

### Strategy 1: Test Migration

**Migrate existing tests to work with new code:**

**Old Test:**
```python
def test_calculate_total():
    items = [Item(price=10), Item(price=20)]
    assert calculate_total(items) == 30
```

**New Code:** Added `tax_rate` parameter

**Migrated Test:**
```python
def test_calculate_total_no_tax():
    """Regression: ensure backward compatibility with no tax"""
    items = [Item(price=10), Item(price=20)]
    assert calculate_total(items) == 30  # Uses default tax_rate=0.0

def test_calculate_total_with_tax():
    """New: test new tax functionality"""
    items = [Item(price=10), Item(price=20)]
    assert calculate_total(items, tax_rate=0.1) == 33.0
```

### Strategy 2: Behavior Preservation

**Ensure old behavior still works:**

**Old Code:**
```python
def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')
```

**New Code:** Added format parameter
```python
def parse_date(date_str, format='%Y-%m-%d'):
    return datetime.strptime(date_str, format)
```

**Regression Tests:**
```python
def test_parse_date_default_format():
    """Regression: default format should work as before"""
    result = parse_date('2024-01-15')
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 15

def test_parse_date_custom_format():
    """New: test custom format support"""
    result = parse_date('15/01/2024', format='%d/%m/%Y')
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 15
```

### Strategy 3: Edge Case Coverage

**Generate tests for boundary conditions:**

```python
def test_calculate_total_empty_list():
    """Edge case: empty items list"""
    assert calculate_total([]) == 0

def test_calculate_total_negative_tax():
    """Edge case: negative tax rate (discount)"""
    items = [Item(price=100)]
    assert calculate_total(items, tax_rate=-0.1) == 90.0

def test_calculate_total_zero_prices():
    """Edge case: all items have zero price"""
    items = [Item(price=0), Item(price=0)]
    assert calculate_total(items, tax_rate=0.1) == 0
```

### Strategy 4: Exception Handling

**Test error conditions:**

```python
def test_calculate_total_invalid_tax_rate():
    """Test validation of tax rate"""
    items = [Item(price=100)]
    with pytest.raises(ValueError):
        calculate_total(items, tax_rate=2.0)  # Tax rate > 100%

def test_parse_date_invalid_format():
    """Test error handling for invalid date format"""
    with pytest.raises(ValueError):
        parse_date('invalid-date')
```

## Testing Framework Support

### unittest Framework

**Basic Test Structure:**
```python
import unittest

class TestCalculateTotal(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.items = [Item(price=10), Item(price=20)]

    def tearDown(self):
        """Clean up after tests"""
        pass

    def test_no_tax(self):
        """Test calculation without tax"""
        result = calculate_total(self.items)
        self.assertEqual(result, 30)

    def test_with_tax(self):
        """Test calculation with tax"""
        result = calculate_total(self.items, tax_rate=0.1)
        self.assertAlmostEqual(result, 33.0)

if __name__ == '__main__':
    unittest.main()
```

**Assertions:**
- `assertEqual(a, b)`: a == b
- `assertNotEqual(a, b)`: a != b
- `assertTrue(x)`: bool(x) is True
- `assertFalse(x)`: bool(x) is False
- `assertIs(a, b)`: a is b
- `assertIsNone(x)`: x is None
- `assertIn(a, b)`: a in b
- `assertIsInstance(a, b)`: isinstance(a, b)
- `assertRaises(exc)`: context manager for exceptions
- `assertAlmostEqual(a, b)`: for floating point comparison

### pytest Framework

**Basic Test Structure:**
```python
import pytest

@pytest.fixture
def items():
    """Fixture providing test items"""
    return [Item(price=10), Item(price=20)]

def test_no_tax(items):
    """Test calculation without tax"""
    result = calculate_total(items)
    assert result == 30

def test_with_tax(items):
    """Test calculation with tax"""
    result = calculate_total(items, tax_rate=0.1)
    assert result == pytest.approx(33.0)

def test_invalid_tax_rate(items):
    """Test error handling"""
    with pytest.raises(ValueError, match="Tax rate must be"):
        calculate_total(items, tax_rate=2.0)
```

**Parametrized Tests:**
```python
@pytest.mark.parametrize("tax_rate,expected", [
    (0.0, 30.0),
    (0.1, 33.0),
    (0.2, 36.0),
    (0.5, 45.0),
])
def test_calculate_total_various_rates(items, tax_rate, expected):
    result = calculate_total(items, tax_rate)
    assert result == pytest.approx(expected)
```

## Mocking and Stubbing

### unittest.mock

**Mocking External Dependencies:**

```python
from unittest.mock import Mock, patch, MagicMock

def test_send_notification_with_mock():
    """Test notification sending with mocked email service"""
    with patch('myapp.email.send_email') as mock_send:
        mock_send.return_value = True

        result = send_notification(user_id=123, message="Hello")

        assert result is True
        mock_send.assert_called_once_with(
            to='user@example.com',
            subject='Notification',
            body='Hello'
        )
```

**Mocking File I/O:**

```python
def test_read_config_with_mock():
    """Test config reading with mocked file"""
    mock_data = '{"setting": "value"}'

    with patch('builtins.open', unittest.mock.mock_open(read_data=mock_data)):
        config = read_config('config.json')
        assert config['setting'] == 'value'
```

**Mocking Database Calls:**

```python
def test_get_user_with_mock_db():
    """Test user retrieval with mocked database"""
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = {
        'id': 1,
        'name': 'Alice'
    }

    user = get_user(mock_db, user_id=1)

    assert user['name'] == 'Alice'
    mock_db.query.assert_called_once()
```

**Mocking HTTP Requests:**

```python
def test_fetch_data_with_mock_requests():
    """Test API call with mocked requests"""
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {'data': 'value'}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = fetch_data('https://api.example.com/data')

        assert result['data'] == 'value'
        mock_get.assert_called_once_with('https://api.example.com/data')
```

### pytest Mocking

**Using pytest-mock:**

```python
def test_send_notification_pytest(mocker):
    """Test with pytest-mock"""
    mock_send = mocker.patch('myapp.email.send_email')
    mock_send.return_value = True

    result = send_notification(user_id=123, message="Hello")

    assert result is True
    mock_send.assert_called_once()
```

**Mocking with Fixtures:**

```python
@pytest.fixture
def mock_database(mocker):
    """Fixture providing mocked database"""
    mock_db = mocker.Mock()
    mock_db.query.return_value.all.return_value = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ]
    return mock_db

def test_get_all_users(mock_database):
    users = get_all_users(mock_database)
    assert len(users) == 2
    assert users[0]['name'] == 'Alice'
```

### Stubbing Strategies

**Simple Stubs:**

```python
class StubEmailService:
    """Stub for email service"""
    def __init__(self):
        self.sent_emails = []

    def send_email(self, to, subject, body):
        self.sent_emails.append({
            'to': to,
            'subject': subject,
            'body': body
        })
        return True

def test_notification_with_stub():
    email_service = StubEmailService()
    send_notification(email_service, user_id=123, message="Hello")

    assert len(email_service.sent_emails) == 1
    assert email_service.sent_emails[0]['to'] == 'user@example.com'
```

**Fake Objects:**

```python
class FakeDatabase:
    """Fake in-memory database"""
    def __init__(self):
        self.data = {}

    def insert(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def delete(self, key):
        if key in self.data:
            del self.data[key]

def test_user_crud_with_fake_db():
    db = FakeDatabase()

    # Test insert
    db.insert('user:1', {'name': 'Alice'})
    assert db.get('user:1')['name'] == 'Alice'

    # Test delete
    db.delete('user:1')
    assert db.get('user:1') is None
```

## Test Structure Patterns

### Arrange-Act-Assert (AAA)

```python
def test_calculate_discount():
    # Arrange: Set up test data
    price = 100
    discount_percent = 20

    # Act: Execute the function
    result = calculate_discount(price, discount_percent)

    # Assert: Verify the result
    assert result == 80
```

### Given-When-Then (BDD Style)

```python
def test_user_login():
    # Given: a registered user
    user = User(username='alice', password='secret123')
    db.save(user)

    # When: the user attempts to login
    result = login(username='alice', password='secret123')

    # Then: login should succeed
    assert result.success is True
    assert result.user.username == 'alice'
```

### Setup and Teardown

**unittest:**
```python
class TestUserService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests in class"""
        cls.db = create_test_database()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests in class"""
        cls.db.close()

    def setUp(self):
        """Run before each test"""
        self.user = User(name='Test User')

    def tearDown(self):
        """Run after each test"""
        self.db.clear()
```

**pytest:**
```python
@pytest.fixture(scope='module')
def database():
    """Module-level fixture"""
    db = create_test_database()
    yield db
    db.close()

@pytest.fixture
def user():
    """Function-level fixture"""
    return User(name='Test User')

def test_user_creation(database, user):
    database.save(user)
    assert database.get(user.id) is not None
```

## Coverage Strategies

### Path Coverage

**Ensure all code paths are tested:**

```python
def process_payment(amount, payment_method):
    if amount <= 0:
        raise ValueError("Amount must be positive")

    if payment_method == 'credit_card':
        return process_credit_card(amount)
    elif payment_method == 'paypal':
        return process_paypal(amount)
    else:
        raise ValueError("Invalid payment method")

# Tests covering all paths:
def test_process_payment_negative_amount():
    """Path: amount <= 0"""
    with pytest.raises(ValueError, match="Amount must be positive"):
        process_payment(-10, 'credit_card')

def test_process_payment_credit_card():
    """Path: credit_card branch"""
    result = process_payment(100, 'credit_card')
    assert result.success is True

def test_process_payment_paypal():
    """Path: paypal branch"""
    result = process_payment(100, 'paypal')
    assert result.success is True

def test_process_payment_invalid_method():
    """Path: invalid payment method"""
    with pytest.raises(ValueError, match="Invalid payment method"):
        process_payment(100, 'bitcoin')
```

### Boundary Value Testing

```python
def test_age_validation_boundaries():
    """Test boundary values for age validation"""
    # Lower boundary
    assert is_valid_age(0) is False
    assert is_valid_age(1) is True

    # Upper boundary
    assert is_valid_age(120) is True
    assert is_valid_age(121) is False

    # Around typical values
    assert is_valid_age(17) is True
    assert is_valid_age(18) is True
    assert is_valid_age(65) is True
```

### State-Based Testing

```python
def test_order_state_transitions():
    """Test all valid state transitions"""
    order = Order()

    # Initial state
    assert order.state == 'pending'

    # pending -> confirmed
    order.confirm()
    assert order.state == 'confirmed'

    # confirmed -> shipped
    order.ship()
    assert order.state == 'shipped'

    # shipped -> delivered
    order.deliver()
    assert order.state == 'delivered'

def test_invalid_state_transitions():
    """Test invalid state transitions"""
    order = Order()

    # Cannot ship before confirming
    with pytest.raises(InvalidStateTransition):
        order.ship()

    # Cannot deliver before shipping
    order.confirm()
    with pytest.raises(InvalidStateTransition):
        order.deliver()
```

## Test Migration Patterns

### Pattern 1: Signature Change with Default Parameter

**Old Code:**
```python
def send_email(to, subject, body):
    # implementation
```

**Old Test:**
```python
def test_send_email():
    result = send_email('user@example.com', 'Hello', 'Message body')
    assert result is True
```

**New Code:**
```python
def send_email(to, subject, body, cc=None):
    # implementation with cc support
```

**Migrated Tests:**
```python
def test_send_email_without_cc():
    """Regression: ensure backward compatibility"""
    result = send_email('user@example.com', 'Hello', 'Message body')
    assert result is True

def test_send_email_with_cc():
    """New: test cc functionality"""
    result = send_email(
        'user@example.com',
        'Hello',
        'Message body',
        cc=['cc@example.com']
    )
    assert result is True
```

### Pattern 2: Return Type Change

**Old Code:**
```python
def get_user(user_id):
    return {'id': user_id, 'name': 'Alice'}  # Returns dict
```

**Old Test:**
```python
def test_get_user():
    user = get_user(1)
    assert user['name'] == 'Alice'
```

**New Code:**
```python
class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

def get_user(user_id):
    return User(user_id, 'Alice')  # Returns User object
```

**Migrated Test:**
```python
def test_get_user():
    """Updated: adapt to new User object return type"""
    user = get_user(1)
    assert user.name == 'Alice'  # Changed from user['name']
    assert user.id == 1
```

### Pattern 3: Exception Handling Changes

**Old Code:**
```python
def divide(a, b):
    return a / b  # Raises ZeroDivisionError
```

**Old Test:**
```python
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

**New Code:**
```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Migrated Test:**
```python
def test_divide_by_zero():
    """Updated: exception type changed to ValueError"""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
```

### Pattern 4: Async Conversion

**Old Code:**
```python
def fetch_data(url):
    response = requests.get(url)
    return response.json()
```

**Old Test:**
```python
def test_fetch_data():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'data': 'value'}
        result = fetch_data('https://api.example.com')
        assert result['data'] == 'value'
```

**New Code:**
```python
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

**Migrated Test:**
```python
@pytest.mark.asyncio
async def test_fetch_data():
    """Updated: converted to async test"""
    with patch('aiohttp.ClientSession') as mock_session:
        mock_response = AsyncMock()
        mock_response.json.return_value = {'data': 'value'}
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response

        result = await fetch_data('https://api.example.com')
        assert result['data'] == 'value'
```

### Pattern 5: Class Method to Static Method

**Old Code:**
```python
class Calculator:
    def add(self, a, b):
        return a + b
```

**Old Test:**
```python
def test_calculator_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5
```

**New Code:**
```python
class Calculator:
    @staticmethod
    def add(a, b):
        return a + b
```

**Migrated Test:**
```python
def test_calculator_add():
    """Updated: can call without instance"""
    assert Calculator.add(2, 3) == 5
    # Or still works with instance
    calc = Calculator()
    assert calc.add(2, 3) == 5
```

### Pattern 6: Dependency Injection

**Old Code:**
```python
def process_order(order_id):
    db = Database()  # Hard-coded dependency
    order = db.get_order(order_id)
    return order.process()
```

**Old Test:**
```python
def test_process_order():
    with patch('myapp.Database') as mock_db_class:
        mock_db = Mock()
        mock_db_class.return_value = mock_db
        mock_order = Mock()
        mock_order.process.return_value = True
        mock_db.get_order.return_value = mock_order

        result = process_order(123)
        assert result is True
```

**New Code:**
```python
def process_order(order_id, db=None):
    if db is None:
        db = Database()
    order = db.get_order(order_id)
    return order.process()
```

**Migrated Test:**
```python
def test_process_order():
    """Updated: use dependency injection for cleaner mocking"""
    mock_db = Mock()
    mock_order = Mock()
    mock_order.process.return_value = True
    mock_db.get_order.return_value = mock_order

    result = process_order(123, db=mock_db)
    assert result is True
    mock_db.get_order.assert_called_once_with(123)
```

