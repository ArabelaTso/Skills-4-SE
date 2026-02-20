# Common Flaky Test Patterns

## Timing and Concurrency Issues

### Sleep/Wait Statements
**Pattern:** Using fixed sleep/wait times
```python
# Flaky
time.sleep(2)  # Hope 2 seconds is enough
assert element.is_visible()

# Better
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "element"))
)
```

### Race Conditions
**Pattern:** Tests that depend on execution order or timing
```python
# Flaky - depends on thread timing
thread1.start()
thread2.start()
assert shared_state == expected  # May fail randomly

# Better
thread1.start()
thread2.start()
thread1.join()
thread2.join()
assert shared_state == expected
```

### Async/Await Issues
**Pattern:** Missing await or improper async handling
```python
# Flaky
async def test_api():
    result = api_call()  # Missing await
    assert result.status == 200

# Better
async def test_api():
    result = await api_call()
    assert result.status == 200
```

## State Management Issues

### Shared State Between Tests
**Pattern:** Tests that modify global or class-level state
```python
# Flaky - tests affect each other
class TestSuite:
    cache = {}  # Shared across tests

    def test_a(self):
        self.cache['key'] = 'value'
        assert self.cache['key'] == 'value'

    def test_b(self):
        assert 'key' not in self.cache  # May fail if test_a runs first

# Better - use fixtures or setUp/tearDown
class TestSuite:
    def setUp(self):
        self.cache = {}
```

### Database State
**Pattern:** Tests that don't clean up database state
```python
# Flaky
def test_create_user():
    user = User.create(email="test@example.com")
    assert user.id is not None
    # No cleanup - next run may fail on duplicate email

# Better
def test_create_user():
    user = User.create(email="test@example.com")
    assert user.id is not None
    user.delete()  # Or use transaction rollback
```

### File System State
**Pattern:** Tests that create files without cleanup
```python
# Flaky
def test_file_creation():
    with open('test.txt', 'w') as f:
        f.write('data')
    assert os.path.exists('test.txt')
    # No cleanup

# Better
def test_file_creation(tmp_path):
    file_path = tmp_path / 'test.txt'
    file_path.write_text('data')
    assert file_path.exists()
    # tmp_path automatically cleaned up
```

## External Dependencies

### Network Calls
**Pattern:** Tests that make real network requests
```python
# Flaky - depends on network and external service
def test_api():
    response = requests.get('https://api.example.com/data')
    assert response.status_code == 200

# Better - use mocking
def test_api(mocker):
    mocker.patch('requests.get', return_value=Mock(status_code=200))
    response = requests.get('https://api.example.com/data')
    assert response.status_code == 200
```

### Database Connections
**Pattern:** Tests that depend on external database availability
```python
# Flaky
def test_query():
    conn = psycopg2.connect("host=prod-db...")
    result = conn.execute("SELECT * FROM users")
    assert len(result) > 0

# Better - use test database or mocking
def test_query(test_db):
    result = test_db.execute("SELECT * FROM users")
    assert len(result) > 0
```

## Randomness and Non-Determinism

### Random Data Generation
**Pattern:** Using random values without seeding
```python
# Flaky
def test_sorting():
    data = [random.randint(1, 100) for _ in range(10)]
    sorted_data = sort(data)
    assert sorted_data[0] <= sorted_data[-1]  # May fail with duplicates

# Better
def test_sorting():
    random.seed(42)  # Or use fixed test data
    data = [random.randint(1, 100) for _ in range(10)]
    sorted_data = sort(data)
    assert sorted_data == sorted(data)
```

### UUID/ID Generation
**Pattern:** Tests that depend on specific generated IDs
```python
# Flaky
def test_create_entity():
    entity = Entity.create()
    assert entity.id == "expected-uuid"  # Will fail

# Better
def test_create_entity():
    entity = Entity.create()
    assert entity.id is not None
    assert isinstance(entity.id, str)
```

## Time Dependencies

### Current Time/Date
**Pattern:** Tests that depend on current time
```python
# Flaky
def test_is_business_hours():
    assert is_business_hours()  # Fails outside 9-5

# Better
def test_is_business_hours(mocker):
    mocker.patch('datetime.datetime.now', return_value=datetime(2024, 1, 1, 10, 0))
    assert is_business_hours()
```

### Timezone Issues
**Pattern:** Tests that assume specific timezone
```python
# Flaky
def test_date_formatting():
    date = datetime.now()
    assert format_date(date) == "2024-01-01 10:00:00"  # Fails in different TZ

# Better
def test_date_formatting():
    date = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    assert format_date(date) == "2024-01-01 10:00:00 UTC"
```

## Resource Issues

### Resource Leaks
**Pattern:** Not closing resources properly
```python
# Flaky - may run out of file handles
def test_file_reading():
    f = open('test.txt')
    data = f.read()
    assert len(data) > 0
    # File not closed

# Better
def test_file_reading():
    with open('test.txt') as f:
        data = f.read()
    assert len(data) > 0
```

### Memory Leaks
**Pattern:** Tests that accumulate memory
```python
# Flaky - may fail after many runs
class TestSuite:
    data = []  # Class variable accumulates

    def test_append(self):
        self.data.append(generate_large_object())
        assert len(self.data) > 0

# Better
class TestSuite:
    def setUp(self):
        self.data = []  # Fresh for each test
```

## Test Order Dependencies

### Implicit Ordering
**Pattern:** Tests that assume execution order
```python
# Flaky
def test_1_create():
    global user_id
    user_id = create_user()

def test_2_update():
    update_user(user_id)  # Fails if test_1 doesn't run first

# Better - make tests independent
def test_create():
    user_id = create_user()
    assert user_id is not None

def test_update():
    user_id = create_user()  # Create own test data
    update_user(user_id)
```

## Environment Dependencies

### Environment Variables
**Pattern:** Tests that depend on specific env vars
```python
# Flaky
def test_config():
    assert os.getenv('API_KEY') == 'expected-key'

# Better
def test_config(monkeypatch):
    monkeypatch.setenv('API_KEY', 'expected-key')
    assert os.getenv('API_KEY') == 'expected-key'
```

### File System Paths
**Pattern:** Tests with hardcoded paths
```python
# Flaky - path may not exist on all systems
def test_file_exists():
    assert os.path.exists('/tmp/test.txt')

# Better
def test_file_exists(tmp_path):
    test_file = tmp_path / 'test.txt'
    test_file.write_text('data')
    assert test_file.exists()
```
