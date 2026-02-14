# Common Regression Failure Patterns

## Code Change Patterns

### Pattern 1: API Signature Change

**Symptom:** `TypeError: missing required argument`, `TypeError: got unexpected keyword argument`

**Common Causes:**
- Function parameters added/removed/renamed
- Default argument values changed
- Parameter order changed
- Type hints changed (may affect runtime in some cases)

**Example:**
```python
# Before
def process_data(data, format="json"):
    ...

# After
def process_data(data, output_format="json"):  # Parameter renamed
    ...

# Test still calls: process_data(data, format="json")
# Error: TypeError: process_data() got an unexpected keyword argument 'format'
```

### Pattern 2: Return Type Change

**Symptom:** `AttributeError`, `TypeError: 'NoneType' object is not iterable`

**Common Causes:**
- Function now returns None instead of empty collection
- Return type changed (dict → list, single value → tuple, etc.)
- Function returns error object instead of raising exception

**Example:**
```python
# Before
def get_users():
    return []  # Always returns list

# After
def get_users():
    return None  # Returns None when no users

# Test code: for user in get_users()
# Error: TypeError: 'NoneType' object is not iterable
```

### Pattern 3: Exception Changes

**Symptom:** Test expects exception but doesn't get one, or gets different exception

**Common Causes:**
- Exception type changed
- Code now handles error instead of raising
- New validation added that raises different exception

**Example:**
```python
# Before
def validate_email(email):
    if "@" not in email:
        raise ValueError("Invalid email")

# After
def validate_email(email):
    if "@" not in email:
        raise ValidationError("Invalid email")  # Different exception type

# Test: with pytest.raises(ValueError)
# Error: ValidationError raised instead
```

### Pattern 4: Side Effect Changes

**Symptom:** Assertions on mock calls fail, file operations fail, database state incorrect

**Common Causes:**
- Function no longer calls dependency
- Order of operations changed
- Caching introduced (reduces calls)
- Async behavior changed

**Example:**
```python
# Before
def save_user(user):
    db.insert(user)
    send_email(user.email)

# After
def save_user(user):
    send_email(user.email)  # Order changed
    db.insert(user)

# Test: mock.assert_has_calls([call.insert(), call.send_email()])
# Error: Calls in wrong order
```

## Environment/Dependency Patterns

### Pattern 5: Dependency Version Change

**Symptom:** Tests fail after dependency update

**Common Causes:**
- Breaking changes in minor/patch version
- Deprecated API removed
- Behavior change in library
- Transitive dependency updated

**Indicators:**
- Check `requirements.txt`, `package.json`, `pom.xml` for version changes
- Look for library upgrade commits

### Pattern 6: Test Data Changes

**Symptom:** Assertions fail with unexpected values

**Common Causes:**
- Fixture data modified
- Test database seeded differently
- Mock data structure changed
- External test data source changed

**Example:**
```python
# Before
@pytest.fixture
def sample_user():
    return {"name": "John", "age": 30}

# After
@pytest.fixture
def sample_user():
    return {"name": "John", "age": 30, "email": "john@example.com"}

# Test expecting 2 keys fails because now there are 3
```

### Pattern 7: Configuration Changes

**Symptom:** Tests fail in CI but pass locally, or vice versa

**Common Causes:**
- Environment variables changed
- Config file modified
- Feature flags toggled
- Different Python/Node/Java version

## Test Infrastructure Patterns

### Pattern 8: Test Isolation Issues

**Symptom:** Tests pass individually but fail when run together

**Common Causes:**
- Shared state not cleaned up
- Global variables modified
- Database not reset between tests
- File system state leaked

**Example:**
```python
# Test 1
def test_create_user():
    user = create_user("john")
    assert user.id == 1

# Test 2
def test_create_another_user():
    user = create_user("jane")
    assert user.id == 1  # Fails because ID is now 2 if test 1 ran first
```

### Pattern 9: Timing/Race Conditions

**Symptom:** Intermittent failures, flaky tests

**Common Causes:**
- Async operations not properly awaited
- Polling timeout too short
- Race condition in concurrent code
- System timing assumptions

**Example:**
```python
# Before
async def fetch_data():
    await asyncio.sleep(0.1)
    return data

# After (slower)
async def fetch_data():
    await asyncio.sleep(0.5)  # Takes longer now
    return data

# Test with 0.2s timeout now fails
```

### Pattern 10: Mock/Patch Issues

**Symptom:** `AttributeError` on mock, unexpected calls, wrong return values

**Common Causes:**
- Import path changed (mock patches wrong location)
- Function moved to different module
- Method renamed
- Mock setup doesn't match new code flow

**Example:**
```python
# Before: function in utils.py
from utils import process

# After: function moved to processors.py
from processors import process

# Test still mocks: @patch('utils.process')
# Error: Mock not called because it's patching wrong location
```

## Logic Change Patterns

### Pattern 11: Conditional Logic Changes

**Symptom:** Different code path executed than expected

**Common Causes:**
- If/else conditions modified
- Default values changed
- Validation logic updated
- Edge case handling added

**Example:**
```python
# Before
def get_discount(price):
    if price > 100:
        return price * 0.1

# After
def get_discount(price):
    if price >= 100:  # Changed > to >=
        return price * 0.1

# Test with price=100 now expects discount instead of None
```

### Pattern 12: Data Structure Changes

**Symptom:** `KeyError`, `IndexError`, wrong values extracted

**Common Causes:**
- Dict keys renamed
- List structure changed
- Nested structure flattened/deepened
- Field added/removed from class

**Example:**
```python
# Before
return {"status": "success", "data": results}

# After
return {"state": "success", "results": results}  # Keys renamed

# Test: response["status"]
# Error: KeyError: 'status'
```

## Common Root Cause Indicators

### Git History Indicators

1. **Recent commits to tested file** - Most likely cause
2. **Recent commits to dependencies** - Check imported modules
3. **Recent refactoring** - Check for moves/renames
4. **Recent dependency updates** - Check package.json, requirements.txt

### Error Message Indicators

1. **Import errors** - Module moved or renamed
2. **Attribute errors** - Method/property renamed or removed
3. **Type errors** - Signature change or type inconsistency
4. **Key/Index errors** - Data structure change

### Test Failure Pattern Indicators

1. **All tests in one file fail** - Change to tested module
2. **All tests for one class fail** - Change to that class
3. **Random subset fails** - Shared state/isolation issue
4. **Failures only in CI** - Environment difference
5. **Intermittent failures** - Race condition/timing issue
