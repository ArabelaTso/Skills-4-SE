# Debugging Strategies

Advanced debugging techniques and systematic approaches for diagnosing complex test failures.

## Table of Contents

1. [Systematic Debugging Process](#systematic-debugging-process)
2. [Debugging Tools by Language](#debugging-tools-by-language)
3. [Common Debugging Techniques](#common-debugging-techniques)
4. [Debugging Flaky Tests](#debugging-flaky-tests)
5. [Performance Debugging](#performance-debugging)
6. [Integration Test Debugging](#integration-test-debugging)

---

## Systematic Debugging Process

### The Scientific Method for Debugging

1. **Observe** - Gather all error information
2. **Hypothesize** - Form theory about cause
3. **Predict** - What would happen if hypothesis is true?
4. **Test** - Run experiment to validate
5. **Analyze** - Evaluate results
6. **Iterate** - Refine hypothesis and repeat

### Binary Search Debugging

When failure point is unclear:

```
1. Identify working and broken states
2. Find midpoint between them
3. Test if midpoint works
4. Narrow to half with failure
5. Repeat until isolated
```

**Application:**
- Git bisect for regression hunting
- Commenting out half the code
- Removing half the test cases
- Testing with subset of data

### Rubber Duck Debugging

Explain the problem out loud (to a duck, colleague, or yourself):

1. What should happen
2. What actually happens
3. What code executes between them
4. Why each line should work

Often reveals the issue during explanation.

---

## Debugging Tools by Language

### Python

**Interactive Debugger (pdb):**
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Python 3.7+ built-in breakpoint
breakpoint()

# Common pdb commands:
# n - next line
# s - step into function
# c - continue
# l - list code
# p variable - print variable
# pp variable - pretty print
```

**pytest debugging:**
```bash
# Drop into pdb on failure
pytest --pdb

# Drop into pdb on first failure, then stop
pytest -x --pdb

# Show local variables on failure
pytest --showlocals

# Verbose output
pytest -vv

# Show print statements
pytest -s
```

**Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def function():
    logger.debug(f"Variable value: {variable}")
```

### JavaScript/TypeScript

**Debugger:**
```javascript
// Add breakpoint
debugger;

// Node.js debugging
node --inspect-brk test.js
# Then open chrome://inspect

// VS Code: Add launch configuration
{
    "type": "node",
    "request": "launch",
    "name": "Jest Debug",
    "program": "${workspaceFolder}/node_modules/.bin/jest",
    "args": ["--runInBand"],
    "console": "integratedTerminal"
}
```

**Jest debugging:**
```bash
# Run single test
npm test -- --testNamePattern="test name"

# Verbose output
npm test -- --verbose

# Show all output (disable mocking of console)
npm test -- --verbose --silent=false

# Run in band (one test at a time, easier to debug)
npm test -- --runInBand
```

**Console debugging:**
```javascript
// Structured logging
console.log('Value:', value);
console.table(arrayOfObjects);
console.trace(); // Show call stack
console.time('operation');
// ... code ...
console.timeEnd('operation'); // Measure duration
```

### Java

**IDE Debugger (IntelliJ/Eclipse):**
```
1. Click line number to set breakpoint
2. Right-click test → Debug
3. Use Step Over (F8), Step Into (F7), Resume (F9)
4. Evaluate expressions in debug console
```

**JUnit debugging:**
```java
// Add logging
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

private static final Logger log = LoggerFactory.getLogger(TestClass.class);

@Test
public void test() {
    log.debug("Variable: {}", variable);
}
```

**Maven debugging:**
```bash
# Run with debug logging
mvn test -X

# Run single test
mvn test -Dtest=TestClassName#testMethod

# Skip other tests
mvn test -Dtest=TestClassName
```

### Go

**Delve debugger:**
```bash
# Install
go install github.com/go-delve/delve/cmd/dlv@latest

# Debug test
dlv test -- -test.run TestName

# Common commands:
# break - set breakpoint
# continue - resume execution
# next - next line
# step - step into
# print var - print variable
```

**Test debugging:**
```bash
# Verbose
go test -v

# Run specific test
go test -run TestName

# Show test coverage
go test -cover

# Race detection
go test -race
```

**Print debugging:**
```go
import "fmt"

func test() {
    fmt.Printf("Variable: %+v\n", variable)  // %+v shows field names
    fmt.Printf("Type: %T\n", variable)       // Show type
}
```

---

## Common Debugging Techniques

### Add Strategic Logging

**Before/after critical operations:**
```python
logger.debug(f"Before operation: {state}")
result = operation(state)
logger.debug(f"After operation: {result}")
```

**Function entry/exit:**
```python
def function(arg):
    logger.debug(f"Called function with {arg}")
    result = process(arg)
    logger.debug(f"Returning {result}")
    return result
```

**Conditional logging:**
```python
if condition_that_causes_error:
    logger.debug(f"Error condition met: {details}")
```

### Simplify the Test

**Remove complexity:**
```python
# Complex test with many assertions
def test_complex():
    setup_database()
    create_users()
    create_posts()
    assert complex_query() == expected  # Fails here

# Simplified version
def test_simple():
    # Remove setup to isolate issue
    result = complex_query()
    print(f"Actual result: {result}")  # See what it actually returns
    assert result == expected
```

**Isolate the failure:**
```python
# Instead of testing everything
def test_all():
    assert step1() == expected1
    assert step2() == expected2  # Fails
    assert step3() == expected3

# Test each step separately
def test_step2_only():
    result = step2()
    assert result == expected2
```

### Compare Working vs Broken

**Side-by-side comparison:**
```python
def test_comparison():
    working_input = {...}
    broken_input = {...}

    working_result = function(working_input)
    broken_result = function(broken_input)

    print(f"Working: {working_result}")
    print(f"Broken: {broken_result}")
    print(f"Difference: {set(working_result) - set(broken_result)}")
```

### Check Assumptions

**Verify preconditions:**
```python
def test():
    # Don't assume, verify
    assert database.is_connected(), "DB not connected"
    assert user.exists(), "User doesn't exist"
    assert file.exists(), "File not found"

    # Now run actual test
    result = operation()
    assert result == expected
```

### Use Assertions Liberally

**Assert intermediate states:**
```python
def test():
    user = create_user()
    assert user.id is not None, "User ID should be set"

    post = create_post(user)
    assert post.author_id == user.id, "Author ID should match"

    result = get_posts(user)
    assert len(result) > 0, "Should have at least one post"
    assert result[0].id == post.id, "Should be the post we created"
```

---

## Debugging Flaky Tests

### Identify Flakiness Pattern

**Run test multiple times:**
```bash
# Run 100 times to see if flaky
for i in {1..100}; do pytest test_file.py::test_name || break; done

# Or use pytest-repeat
pip install pytest-repeat
pytest --count=100 test_file.py::test_name
```

**Check for timing dependencies:**
```python
# Bad - timing dependent
time.sleep(1)  # Hope 1 second is enough
assert element.is_visible()

# Good - wait for condition
wait_until(lambda: element.is_visible(), timeout=10)
```

### Common Flaky Test Causes

**1. Race Conditions:**
```python
# Bad
thread.start()
assert result == expected  # May not be ready yet

# Good
thread.start()
thread.join(timeout=5)  # Wait for completion
assert result == expected
```

**2. Non-deterministic Order:**
```python
# Bad
results = query_database()  # Order not guaranteed
assert results[0].name == "Alice"

# Good
results = sorted(query_database(), key=lambda x: x.name)
assert results[0].name == "Alice"
```

**3. Shared State:**
```python
# Bad - tests share state
class TestSuite:
    shared_data = []  # Class variable!

    def test_1(self):
        self.shared_data.append(1)
        assert len(self.shared_data) == 1

    def test_2(self):
        self.shared_data.append(2)
        assert len(self.shared_data) == 1  # Fails if test_1 ran first

# Good - isolate state
class TestSuite:
    def setup_method(self):
        self.data = []  # Instance variable, fresh each test

    def test_1(self):
        self.data.append(1)
        assert len(self.data) == 1
```

**4. External Dependencies:**
```python
# Bad - depends on external service
def test():
    response = requests.get("https://api.example.com")
    assert response.status_code == 200

# Good - mock external calls
def test(mocker):
    mock_response = mocker.Mock(status_code=200)
    mocker.patch('requests.get', return_value=mock_response)

    response = requests.get("https://api.example.com")
    assert response.status_code == 200
```

### Fix Flaky Tests

**Add explicit waits:**
```python
# Use polling wait
def wait_until(condition, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        if condition():
            return True
        time.sleep(0.1)
    return False

assert wait_until(lambda: element.is_visible())
```

**Isolate test state:**
```python
@pytest.fixture(autouse=True)
def reset_state():
    # Setup
    database.clear()
    cache.clear()
    yield
    # Teardown
    database.clear()
    cache.clear()
```

---

## Performance Debugging

### Profile Test Execution

**Python (pytest-profiling):**
```bash
pip install pytest-profiling
pytest --profile test_file.py

# Generate SVG graph
pytest --profile-svg test_file.py
```

**Identify slow tests:**
```bash
# Show slowest tests
pytest --durations=10

# With minimum duration
pytest --durations=0 --durations-min=1.0
```

### Find Performance Bottlenecks

**Add timing measurements:**
```python
import time

def test_performance():
    start = time.time()
    setup()
    print(f"Setup: {time.time() - start:.2f}s")

    start = time.time()
    operation()
    print(f"Operation: {time.time() - start:.2f}s")

    start = time.time()
    verification()
    print(f"Verification: {time.time() - start:.2f}s")
```

**Profile specific functions:**
```python
import cProfile
import pstats

def test():
    profiler = cProfile.Profile()
    profiler.enable()

    operation_under_test()

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 slowest functions
```

---

## Integration Test Debugging

### API Test Debugging

**Log full request/response:**
```python
import requests
import logging

# Enable request logging
logging.basicConfig(level=logging.DEBUG)

response = requests.get(url)
print(f"Request URL: {response.request.url}")
print(f"Request Headers: {response.request.headers}")
print(f"Response Status: {response.status_code}")
print(f"Response Headers: {response.headers}")
print(f"Response Body: {response.text}")
```

**Use network inspection:**
```bash
# Capture traffic with mitmproxy
mitmproxy -p 8080

# Configure test to use proxy
export HTTP_PROXY=http://localhost:8080
export HTTPS_PROXY=http://localhost:8080
pytest test_api.py
```

### Database Test Debugging

**Inspect database state:**
```python
def test_database():
    user = create_user("Alice")

    # Debug: Check what's actually in DB
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE name = 'Alice'")
    rows = cursor.fetchall()
    print(f"Database rows: {rows}")

    # Continue test
    assert user.exists()
```

**Log SQL queries:**
```python
# SQLAlchemy logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Will print all SQL queries
```

### E2E Test Debugging

**Take screenshots on failure:**
```python
# Selenium
def test_e2e(driver):
    try:
        driver.get(url)
        element = driver.find_element(By.ID, "submit")
        element.click()
    except Exception as e:
        driver.save_screenshot('failure.png')
        raise

# Cypress (automatic on failure)
```

**Use headed mode:**
```bash
# Cypress
npx cypress open  # Opens browser, can watch test execute

# Playwright
pytest --headed  # Shows browser

# Selenium
# Don't use headless option
```

**Slow down execution:**
```python
# Selenium
from selenium.webdriver.support.ui import WebDriverWait

# Add delays to watch what happens
driver.implicitly_wait(1)  # Wait 1s before each action

# Playwright
page.set_default_timeout(5000)  # 5 second timeout
```

**Save page source on failure:**
```python
def test_e2e(driver):
    try:
        # test code
    except Exception:
        with open('page_source.html', 'w') as f:
            f.write(driver.page_source)
        raise
```
