# Error Pattern Catalog

Comprehensive catalog of common test error patterns organized by framework and language.

## Table of Contents

1. [Python (pytest, unittest)](#python-pytest-unittest)
2. [JavaScript/TypeScript (Jest, Mocha, Vitest)](#javascripttypescript-jest-mocha-vitest)
3. [Java (JUnit, TestNG)](#java-junit-testng)
4. [Go (testing package)](#go-testing-package)
5. [Cross-Framework Patterns](#cross-framework-patterns)

---

## Python (pytest, unittest)

### AssertionError

**Pattern:**
```
AssertionError: assert [actual] == [expected]
```

**Variations:**
- `assert 5 == 10` - Simple value mismatch
- `assert 'hello' in 'world'` - Membership test failure
- `assert len(items) == 3` - Length mismatch
- `assert response.status_code == 200` - Attribute comparison

**Common Causes:**
- Logic errors in implementation
- Incorrect test expectations
- Off-by-one errors
- Wrong comparison operators

**Quick Fix Pattern:**
```python
# Check if assertion logic is correct
assert actual == expected  # Is 'expected' value correct?

# Use pytest's detailed assertion rewriting
assert actual == expected, f"Expected {expected}, got {actual}"

# For floating point, use approx
from pytest import approx
assert 0.1 + 0.2 == approx(0.3)
```

### AttributeError

**Pattern:**
```
AttributeError: 'NoneType' object has no attribute 'method_name'
AttributeError: module 'X' has no attribute 'Y'
```

**Common Causes:**
- Accessing attribute on None
- Typo in attribute name
- Wrong import (importing module instead of class)
- Missing initialization

**Quick Fix Pattern:**
```python
# Add None check
if obj is not None:
    result = obj.method_name()

# Fix import
from module import ClassName  # Not just 'import module'

# Check initialization
def __init__(self):
    self.attribute = initial_value  # Don't forget to initialize
```

### ImportError / ModuleNotFoundError

**Pattern:**
```
ModuleNotFoundError: No module named 'package_name'
ImportError: cannot import name 'ClassName' from 'module'
```

**Common Causes:**
- Package not installed
- Circular imports
- Wrong module path
- Missing `__init__.py` (Python 2.x)

**Quick Fix Pattern:**
```bash
# Install missing package
pip install package_name

# Check if in requirements.txt
grep package_name requirements.txt

# Verify package installation
pip list | grep package_name
```

### FixtureNotFoundError (pytest)

**Pattern:**
```
fixture 'fixture_name' not found
```

**Common Causes:**
- Fixture not defined in test file or conftest.py
- Typo in fixture name
- Fixture in wrong scope
- Missing conftest.py import

**Quick Fix Pattern:**
```python
# Define fixture in conftest.py
@pytest.fixture
def fixture_name():
    return value

# Or in test file
@pytest.fixture
def fixture_name():
    return value

# Check fixture scope
@pytest.fixture(scope="session")  # session, module, class, function
```

### TypeError

**Pattern:**
```
TypeError: unsupported operand type(s) for +: 'int' and 'str'
TypeError: function() takes 2 positional arguments but 3 were given
TypeError: 'NoneType' object is not iterable
```

**Common Causes:**
- Type mismatch in operations
- Wrong number of arguments
- Trying to iterate over None
- Missing type conversion

**Quick Fix Pattern:**
```python
# Fix type conversion
result = int(string_value) + 5

# Check argument count
def function(arg1, arg2):  # Match signature

# Handle None for iteration
for item in (items or []):  # Provide default empty list
```

---

## JavaScript/TypeScript (Jest, Mocha, Vitest)

### TypeError: Cannot read property 'X' of undefined

**Pattern:**
```
TypeError: Cannot read property 'name' of undefined
TypeError: Cannot read properties of null (reading 'id')
```

**Common Causes:**
- Accessing property on undefined/null
- Async data not loaded
- API returned null
- Object not initialized

**Quick Fix Pattern:**
```javascript
// Option 1: Optional chaining
const name = user?.name;

// Option 2: Null check
if (user) {
    const name = user.name;
}

// Option 3: Default value
const name = user?.name ?? 'Default';

// Option 4: Ensure object exists
const user = await fetchUser() || {};
```

### ReferenceError: X is not defined

**Pattern:**
```
ReferenceError: variableName is not defined
ReferenceError: functionName is not defined
```

**Common Causes:**
- Variable used before declaration
- Typo in variable name
- Missing import
- Scope issues

**Quick Fix Pattern:**
```javascript
// Import missing module
import { functionName } from './module';

// Declare variable
const variableName = value;

// Check variable scope
function outer() {
    const variable = 'value';
    function inner() {
        console.log(variable);  // OK - closure
    }
}
```

### Test timeout errors

**Pattern:**
```
Timeout - Async callback was not invoked within the 5000ms timeout
Error: Timeout of 2000ms exceeded
```

**Common Causes:**
- Async operation not completing
- Missing done() callback
- Missing await
- Infinite loop

**Quick Fix Pattern:**
```javascript
// Jest: Increase timeout
jest.setTimeout(10000);

test('async test', async () => {
    await asyncOperation();  // Don't forget await
}, 10000);  // Or per-test timeout

// Mocha: Increase timeout
it('async test', async function() {
    this.timeout(5000);
    await asyncOperation();
});

// Ensure promise resolves
await expect(promise).resolves.toBeDefined();
```

### Cannot find module

**Pattern:**
```
Cannot find module './moduleName'
Cannot find module 'package-name'
```

**Common Causes:**
- Module path incorrect
- Package not installed
- Missing file extension in import
- TypeScript path mapping issue

**Quick Fix Pattern:**
```bash
# Install package
npm install package-name

# Check import path
import { func } from './correct/path';  // Check relative path

# For TypeScript, check tsconfig.json paths
{
    "compilerOptions": {
        "baseUrl": ".",
        "paths": {
            "@/*": ["src/*"]
        }
    }
}
```

### Async/Promise errors

**Pattern:**
```
UnhandledPromiseRejectionWarning
Error: Promise rejection was handled asynchronously
```

**Common Causes:**
- Promise rejection not caught
- Missing .catch()
- Missing try/catch in async function

**Quick Fix Pattern:**
```javascript
// Option 1: Use try/catch
async function test() {
    try {
        await operation();
    } catch (error) {
        // Handle error
    }
}

// Option 2: Use .catch()
promise
    .then(result => {})
    .catch(error => {});

// Option 3: Test error with Jest
await expect(promise).rejects.toThrow();
```

---

## Java (JUnit, TestNG)

### AssertionFailedError

**Pattern:**
```
org.opentest4j.AssertionFailedError: expected: <200> but was: <404>
AssertionError: Expected 5 but was 3
```

**Common Causes:**
- Value mismatch
- Wrong expected value
- Logic error

**Quick Fix Pattern:**
```java
// Use proper assertion
assertEquals(expected, actual);  // JUnit 4
assertThat(actual).isEqualTo(expected);  // AssertJ

// Add message for clarity
assertEquals("User should be created", 200, response.getStatus());

// For floating point
assertEquals(expected, actual, 0.001);  // delta
```

### NullPointerException

**Pattern:**
```
java.lang.NullPointerException
java.lang.NullPointerException: Cannot invoke "Object.method()" because "object" is null
```

**Common Causes:**
- Accessing method/field on null reference
- Uninitialized field
- Method returning null unexpectedly

**Quick Fix Pattern:**
```java
// Option 1: Null check
if (object != null) {
    object.method();
}

// Option 2: Optional (Java 8+)
Optional<String> optional = Optional.ofNullable(value);
optional.ifPresent(v -> process(v));

// Option 3: Objects.requireNonNull
Objects.requireNonNull(object, "Object must not be null");

// Option 4: Use @NonNull annotations
public void method(@NonNull Object param) { }
```

### ClassNotFoundException / NoClassDefFoundError

**Pattern:**
```
java.lang.ClassNotFoundException: com.example.ClassName
java.lang.NoClassDefFoundError: com/example/ClassName
```

**Common Causes:**
- Class not in classpath
- Missing dependency
- Wrong package name
- Build issue

**Quick Fix Pattern:**
```xml
<!-- Maven: Add dependency -->
<dependency>
    <groupId>com.example</groupId>
    <artifactId>artifact</artifactId>
    <version>1.0.0</version>
    <scope>test</scope>
</dependency>
```

```gradle
// Gradle: Add dependency
testImplementation 'com.example:artifact:1.0.0'
```

### ComparisonFailure

**Pattern:**
```
org.junit.ComparisonFailure: expected:<hello [world]> but was:<hello [there]>
```

**Common Causes:**
- String content mismatch
- Whitespace differences
- Line ending differences

**Quick Fix Pattern:**
```java
// Normalize strings before comparison
String expected = "hello world".trim().replaceAll("\\s+", " ");
String actual = result.trim().replaceAll("\\s+", " ");
assertEquals(expected, actual);

// Or use contains/matches
assertTrue(result.contains("expected substring"));
assertTrue(result.matches("regex pattern"));
```

---

## Go (testing package)

### Test Panics

**Pattern:**
```
panic: runtime error: invalid memory address or nil pointer dereference
panic: index out of range [5] with length 3
```

**Common Causes:**
- Nil pointer dereference
- Index out of bounds
- Type assertion failure

**Quick Fix Pattern:**
```go
// Check for nil
if ptr != nil {
    value := *ptr
}

// Check slice bounds
if i < len(slice) {
    value := slice[i]
}

// Safe type assertion
if val, ok := interfaceValue.(Type); ok {
    // Use val
}

// Recover from panic in test
defer func() {
    if r := recover(); r != nil {
        t.Errorf("Test panicked: %v", r)
    }
}()
```

### Comparison Failures

**Pattern:**
```
got 5, want 10
got "hello", want "world"
```

**Common Causes:**
- Value mismatch
- Pointer vs value comparison
- Deep equality not used for structs/slices

**Quick Fix Pattern:**
```go
// Basic comparison
if got != want {
    t.Errorf("got %v, want %v", got, want)
}

// Deep equality for complex types
if !reflect.DeepEqual(got, want) {
    t.Errorf("got %+v, want %+v", got, want)
}

// Use testify for better assertions
assert.Equal(t, want, got)
assert.ElementsMatch(t, wantSlice, gotSlice)
```

### Race Conditions

**Pattern:**
```
WARNING: DATA RACE
Read at 0x00c000124080 by goroutine 8
Previous write at 0x00c000124080 by goroutine 7
```

**Common Causes:**
- Concurrent access to shared variable
- Missing mutex
- Channel misuse

**Quick Fix Pattern:**
```go
// Use mutex
var mu sync.Mutex
mu.Lock()
sharedVar = value
mu.Unlock()

// Or RWMutex
var mu sync.RWMutex
mu.RLock()
val := sharedVar
mu.RUnlock()

// Or use channels
ch := make(chan int)
go func() {
    ch <- value
}()
result := <-ch

// Run tests with race detector
go test -race
```

---

## Cross-Framework Patterns

### Mock/Stub Not Called

**Common across:** pytest-mock, Jest, Mockito, gomock

**Pattern:**
- Python: `AssertionError: Expected call not found`
- JS: `Expected mock function to have been called`
- Java: `Wanted but not invoked`

**Common Causes:**
- Wrong code path executed
- Mock patched in wrong location
- Conditional logic preventing call
- Wrong mock instance

**Quick Fix:**
```
1. Verify code path reaches mock
2. Check mock is patched where used, not defined
3. Print/log to confirm execution
4. Relax assertion to check any call first
```

### Async/Timing Issues

**Common across:** All frameworks

**Symptoms:**
- Intermittent failures
- Works locally, fails in CI
- Depends on system speed

**Common Causes:**
- Race conditions
- Insufficient wait times
- Order of execution assumptions

**Quick Fix:**
```
1. Add explicit waits/timeouts
2. Use retry logic for flaky operations
3. Avoid sleep() - use event/condition waits
4. Mock time-dependent code
```

### Configuration/Setup Errors

**Common across:** All frameworks

**Symptoms:**
- Tests fail before running
- Framework can't find tests
- Import/module resolution fails

**Files to check:**
- Python: `pytest.ini`, `setup.py`, `conftest.py`
- JS: `jest.config.js`, `package.json`, `tsconfig.json`
- Java: `pom.xml`, `build.gradle`
- Go: `go.mod`

**Quick Fix:**
```
1. Verify test discovery patterns
2. Check dependency versions
3. Ensure test files match naming conventions
4. Validate configuration syntax
```
