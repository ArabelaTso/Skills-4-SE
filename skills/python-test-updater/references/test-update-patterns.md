# Test Update Patterns

## Common Test Update Scenarios

### 1. Function Signature Changes

#### Adding Parameters

**Old Code:**
```python
def calculate_total(items):
    return sum(item.price for item in items)
```

**New Code:**
```python
def calculate_total(items, tax_rate=0.0):
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)
```

**Old Test:**
```python
def test_calculate_total():
    items = [Item(price=10), Item(price=20)]
    result = calculate_total(items)
    assert result == 30
```

**Updated Test:**
```python
def test_calculate_total():
    items = [Item(price=10), Item(price=20)]
    result = calculate_total(items)
    assert result == 30

def test_calculate_total_with_tax():
    items = [Item(price=10), Item(price=20)]
    result = calculate_total(items, tax_rate=0.1)
    assert result == 33  # 30 * 1.1
```

#### Removing Parameters

**Old Code:**
```python
def get_user(user_id, include_deleted=False):
    # implementation
```

**New Code:**
```python
def get_user(user_id):
    # implementation (no longer supports deleted users)
```

**Old Test:**
```python
def test_get_user():
    user = get_user(123, include_deleted=False)
    assert user.id == 123
```

**Updated Test:**
```python
def test_get_user():
    user = get_user(123)
    assert user.id == 123
```

#### Renaming Parameters

**Old Code:**
```python
def search(query, max_results=10):
    # implementation
```

**New Code:**
```python
def search(query, limit=10):
    # implementation
```

**Old Test:**
```python
def test_search():
    results = search("test", max_results=5)
    assert len(results) <= 5
```

**Updated Test:**
```python
def test_search():
    results = search("test", limit=5)
    assert len(results) <= 5
```

### 2. Return Value Changes

#### Changed Return Type

**Old Code:**
```python
def get_users():
    return [user1, user2, user3]
```

**New Code:**
```python
def get_users():
    return {"users": [user1, user2, user3], "total": 3}
```

**Old Test:**
```python
def test_get_users():
    users = get_users()
    assert len(users) == 3
```

**Updated Test:**
```python
def test_get_users():
    result = get_users()
    assert len(result["users"]) == 3
    assert result["total"] == 3
```

#### Changed Return Structure

**Old Code:**
```python
def get_user_info(user_id):
    return user.name, user.email
```

**New Code:**
```python
def get_user_info(user_id):
    return {"name": user.name, "email": user.email, "created_at": user.created_at}
```

**Old Test:**
```python
def test_get_user_info():
    name, email = get_user_info(123)
    assert name == "John"
    assert email == "john@example.com"
```

**Updated Test:**
```python
def test_get_user_info():
    info = get_user_info(123)
    assert info["name"] == "John"
    assert info["email"] == "john@example.com"
    assert "created_at" in info
```

### 3. Behavior Changes

#### Modified Logic

**Old Code:**
```python
def validate_password(password):
    return len(password) >= 6
```

**New Code:**
```python
def validate_password(password):
    return len(password) >= 8 and any(c.isdigit() for c in password)
```

**Old Test:**
```python
def test_validate_password():
    assert validate_password("abc123") == True
    assert validate_password("abc") == False
```

**Updated Test:**
```python
def test_validate_password():
    assert validate_password("abc12345") == True  # 8+ chars with digit
    assert validate_password("abc123") == False   # Only 6 chars
    assert validate_password("abcdefgh") == False # No digit
    assert validate_password("abc") == False
```

#### Changed Error Handling

**Old Code:**
```python
def divide(a, b):
    return a / b  # Raises ZeroDivisionError
```

**New Code:**
```python
def divide(a, b):
    if b == 0:
        return None
    return a / b
```

**Old Test:**
```python
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

**Updated Test:**
```python
def test_divide_by_zero():
    result = divide(10, 0)
    assert result is None
```

### 4. Class Changes

#### Added Methods

**Old Code:**
```python
class User:
    def __init__(self, name):
        self.name = name
```

**New Code:**
```python
class User:
    def __init__(self, name):
        self.name = name

    def get_display_name(self):
        return f"User: {self.name}"
```

**Old Test:**
```python
def test_user_creation():
    user = User("John")
    assert user.name == "John"
```

**Updated Test:**
```python
def test_user_creation():
    user = User("John")
    assert user.name == "John"

def test_user_display_name():
    user = User("John")
    assert user.get_display_name() == "User: John"
```

#### Modified Constructor

**Old Code:**
```python
class Database:
    def __init__(self, host, port):
        self.host = host
        self.port = port
```

**New Code:**
```python
class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string
```

**Old Test:**
```python
def test_database_init():
    db = Database("localhost", 5432)
    assert db.host == "localhost"
    assert db.port == 5432
```

**Updated Test:**
```python
def test_database_init():
    db = Database("postgresql://localhost:5432/db")
    assert db.connection_string == "postgresql://localhost:5432/db"
```

### 5. Exception Changes

#### New Exception Type

**Old Code:**
```python
def load_config(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config not found: {path}")
```

**New Code:**
```python
class ConfigError(Exception):
    pass

def load_config(path):
    if not os.path.exists(path):
        raise ConfigError(f"Config not found: {path}")
```

**Old Test:**
```python
def test_load_config_missing():
    with pytest.raises(FileNotFoundError):
        load_config("missing.yaml")
```

**Updated Test:**
```python
def test_load_config_missing():
    with pytest.raises(ConfigError):
        load_config("missing.yaml")
```

### 6. Async/Await Changes

#### Sync to Async

**Old Code:**
```python
def fetch_data(url):
    return requests.get(url).json()
```

**New Code:**
```python
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

**Old Test:**
```python
def test_fetch_data():
    data = fetch_data("http://api.example.com/data")
    assert "result" in data
```

**Updated Test:**
```python
@pytest.mark.asyncio
async def test_fetch_data():
    data = await fetch_data("http://api.example.com/data")
    assert "result" in data
```

## Test Update Strategies

### Strategy 1: Minimal Changes

Update only what's necessary to make tests pass:
- Fix broken assertions
- Update function calls
- Adjust expected values

### Strategy 2: Comprehensive Updates

Update tests to cover new functionality:
- Add new test cases
- Update existing tests
- Improve test coverage

### Strategy 3: Refactor Tests

Improve test quality while updating:
- Use fixtures for common setup
- Parametrize similar tests
- Improve test names and documentation

## Common Patterns

### Pattern: Update Assertion Values

```python
# Old
assert result == 10

# New (if behavior changed)
assert result == 15
```

### Pattern: Update Mock Calls

```python
# Old
mock_function.assert_called_with(arg1, arg2)

# New (if signature changed)
mock_function.assert_called_with(arg1, arg2, arg3)
```

### Pattern: Update Fixture Usage

```python
# Old
@pytest.fixture
def user():
    return User("John", "john@example.com")

# New (if constructor changed)
@pytest.fixture
def user():
    return User(name="John", email="john@example.com", role="user")
```

### Pattern: Add Parametrization

```python
# Old
def test_function():
    assert function(5) == 10

# New (add more test cases)
@pytest.mark.parametrize("input,expected", [
    (5, 10),
    (10, 20),
    (0, 0),
])
def test_function(input, expected):
    assert function(input) == expected
```

## Error Message Analysis

### Common Error Patterns

**TypeError: missing required positional argument**
→ Function signature changed, add missing argument

**AssertionError: assert X == Y**
→ Expected value changed, update assertion

**AttributeError: object has no attribute 'X'**
→ Attribute renamed or removed, update reference

**ImportError: cannot import name 'X'**
→ Import path changed, update import statement

**ValueError: too many values to unpack**
→ Return value structure changed, update unpacking

## Best Practices

### 1. Preserve Test Intent
- Keep the original purpose of the test
- Don't change what's being tested
- Only update how it's tested

### 2. Maintain Test Coverage
- Don't remove tests unless functionality removed
- Add tests for new functionality
- Keep edge case tests

### 3. Update Test Documentation
- Update docstrings if test purpose changed
- Update comments if implementation changed
- Keep test names descriptive

### 4. Verify Test Quality
- Tests should still be independent
- Tests should still be deterministic
- Tests should still be readable
