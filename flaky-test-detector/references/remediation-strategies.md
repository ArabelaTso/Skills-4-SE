# Remediation Strategies

## Quick Reference

| Issue Type | Detection | Fix Strategy |
|------------|-----------|--------------|
| Sleep/Wait | `time.sleep()`, `Thread.sleep()` | Use explicit waits with conditions |
| Race Conditions | Shared state, threading | Add synchronization, use locks |
| Random Data | `random.`, `UUID.randomUUID()` | Seed random, use fixed test data |
| Time Dependencies | `datetime.now()`, `System.currentTimeMillis()` | Mock time, use fixed timestamps |
| Network Calls | `requests.`, `http.` | Mock external calls |
| Shared State | Class/global variables | Use fixtures, setUp/tearDown |
| Resource Leaks | Missing close/cleanup | Use context managers, try-finally |
| Test Order | Tests depend on each other | Make tests independent |

## Timing Issues

### Replace Fixed Sleeps with Explicit Waits

**Python (pytest)**
```python
# Before
import time
def test_element_appears():
    click_button()
    time.sleep(2)
    assert element.is_visible()

# After
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_element_appears():
    click_button()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "element"))
    )
    assert element.is_visible()
```

**Java (JUnit)**
```java
// Before
@Test
public void testElementAppears() {
    clickButton();
    Thread.sleep(2000);
    assertTrue(element.isVisible());
}

// After
@Test
public void testElementAppears() {
    clickButton();
    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("element")));
    assertTrue(element.isVisible());
}
```

### Fix Race Conditions

**Python**
```python
# Before
def test_concurrent_updates():
    thread1 = Thread(target=update_counter)
    thread2 = Thread(target=update_counter)
    thread1.start()
    thread2.start()
    assert counter == 2  # Flaky due to race condition

# After
def test_concurrent_updates():
    lock = threading.Lock()
    thread1 = Thread(target=update_counter, args=(lock,))
    thread2 = Thread(target=update_counter, args=(lock,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    assert counter == 2
```

## State Management

### Isolate Test State

**Python (pytest)**
```python
# Before - shared state
class TestUserService:
    users = []  # Shared across tests

    def test_create_user(self):
        user = create_user("test@example.com")
        self.users.append(user)
        assert len(self.users) == 1

# After - isolated state
class TestUserService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.users = []
        yield
        self.users.clear()

    def test_create_user(self):
        user = create_user("test@example.com")
        self.users.append(user)
        assert len(self.users) == 1
```

**Java (JUnit)**
```java
// Before - shared state
public class UserServiceTest {
    private static List<User> users = new ArrayList<>();  // Shared

    @Test
    public void testCreateUser() {
        User user = createUser("test@example.com");
        users.add(user);
        assertEquals(1, users.size());
    }
}

// After - isolated state
public class UserServiceTest {
    private List<User> users;

    @Before
    public void setUp() {
        users = new ArrayList<>();
    }

    @After
    public void tearDown() {
        users.clear();
    }

    @Test
    public void testCreateUser() {
        User user = createUser("test@example.com");
        users.add(user);
        assertEquals(1, users.size());
    }
}
```

### Database State Management

**Python (pytest with transactions)**
```python
# Before
def test_create_user():
    user = User.objects.create(email="test@example.com")
    assert user.id is not None
    # No cleanup

# After - use pytest-django with transaction rollback
@pytest.mark.django_db(transaction=True)
def test_create_user():
    user = User.objects.create(email="test@example.com")
    assert user.id is not None
    # Automatically rolled back
```

**Java (JUnit with Spring)**
```java
// Before
@Test
public void testCreateUser() {
    User user = userRepository.save(new User("test@example.com"));
    assertNotNull(user.getId());
    // No cleanup
}

// After - use @Transactional for automatic rollback
@Test
@Transactional
public void testCreateUser() {
    User user = userRepository.save(new User("test@example.com"));
    assertNotNull(user.getId());
    // Automatically rolled back
}
```

## External Dependencies

### Mock Network Calls

**Python (pytest with unittest.mock)**
```python
# Before
def test_fetch_data():
    response = requests.get("https://api.example.com/data")
    assert response.status_code == 200

# After
def test_fetch_data(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    mocker.patch('requests.get', return_value=mock_response)

    response = requests.get("https://api.example.com/data")
    assert response.status_code == 200
```

**Java (JUnit with Mockito)**
```java
// Before
@Test
public void testFetchData() {
    Response response = httpClient.get("https://api.example.com/data");
    assertEquals(200, response.getStatusCode());
}

// After
@Test
public void testFetchData() {
    Response mockResponse = mock(Response.class);
    when(mockResponse.getStatusCode()).thenReturn(200);
    when(httpClient.get(anyString())).thenReturn(mockResponse);

    Response response = httpClient.get("https://api.example.com/data");
    assertEquals(200, response.getStatusCode());
}
```

## Randomness

### Seed Random Generators

**Python**
```python
# Before
def test_random_selection():
    items = [1, 2, 3, 4, 5]
    selected = random.choice(items)
    assert selected in items  # Always passes but not deterministic

# After
def test_random_selection():
    random.seed(42)
    items = [1, 2, 3, 4, 5]
    selected = random.choice(items)
    assert selected == 1  # Deterministic with seed
```

**Java**
```java
// Before
@Test
public void testRandomSelection() {
    List<Integer> items = Arrays.asList(1, 2, 3, 4, 5);
    Random random = new Random();
    int selected = items.get(random.nextInt(items.size()));
    assertTrue(items.contains(selected));
}

// After
@Test
public void testRandomSelection() {
    List<Integer> items = Arrays.asList(1, 2, 3, 4, 5);
    Random random = new Random(42);  // Seeded
    int selected = items.get(random.nextInt(items.size()));
    assertEquals(4, selected);  // Deterministic with seed
}
```

## Time Dependencies

### Mock Time

**Python (pytest with freezegun)**
```python
# Before
def test_is_expired():
    expiry = datetime.now() + timedelta(days=1)
    assert not is_expired(expiry)  # Flaky if test runs slowly

# After
from freezegun import freeze_time

@freeze_time("2024-01-01 12:00:00")
def test_is_expired():
    expiry = datetime(2024, 1, 2, 12, 0, 0)
    assert not is_expired(expiry)
```

**Java (JUnit with Mockito)**
```java
// Before
@Test
public void testIsExpired() {
    Date expiry = new Date(System.currentTimeMillis() + 86400000);
    assertFalse(isExpired(expiry));
}

// After
@Test
public void testIsExpired() {
    Clock fixedClock = Clock.fixed(
        Instant.parse("2024-01-01T12:00:00Z"),
        ZoneId.of("UTC")
    );
    when(clock.instant()).thenReturn(fixedClock.instant());

    Date expiry = Date.from(Instant.parse("2024-01-02T12:00:00Z"));
    assertFalse(isExpired(expiry));
}
```

## Resource Management

### Use Context Managers and Try-Finally

**Python**
```python
# Before
def test_file_operations():
    f = open('test.txt', 'w')
    f.write('data')
    assert os.path.exists('test.txt')
    # File not closed

# After
def test_file_operations(tmp_path):
    file_path = tmp_path / 'test.txt'
    with open(file_path, 'w') as f:
        f.write('data')
    assert file_path.exists()
```

**Java**
```java
// Before
@Test
public void testFileOperations() throws IOException {
    FileWriter writer = new FileWriter("test.txt");
    writer.write("data");
    assertTrue(new File("test.txt").exists());
    // File not closed
}

// After
@Test
public void testFileOperations() throws IOException {
    try (FileWriter writer = new FileWriter("test.txt")) {
        writer.write("data");
        assertTrue(new File("test.txt").exists());
    }
}
```

## Test Independence

### Remove Test Order Dependencies

**Python**
```python
# Before - tests depend on order
class TestUserWorkflow:
    user_id = None

    def test_1_create_user(self):
        TestUserWorkflow.user_id = create_user()
        assert TestUserWorkflow.user_id is not None

    def test_2_update_user(self):
        update_user(TestUserWorkflow.user_id)
        assert get_user(TestUserWorkflow.user_id).updated

# After - independent tests
class TestUserWorkflow:
    @pytest.fixture
    def user_id(self):
        user_id = create_user()
        yield user_id
        delete_user(user_id)

    def test_create_user(self):
        user_id = create_user()
        assert user_id is not None
        delete_user(user_id)

    def test_update_user(self, user_id):
        update_user(user_id)
        assert get_user(user_id).updated
```
