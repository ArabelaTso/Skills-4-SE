---
name: unit-test-generator
description: Automatically generates comprehensive unit tests for functions, classes, and modules. Use when you need to create tests for Python (pytest, unittest) or Java (JUnit, TestNG) code. Generates tests with comprehensive coverage including happy paths, edge cases, and error conditions. Analyzes existing test patterns in the codebase to match style and conventions. Supports mocking, parameterized tests, fixtures, and follows best practices for each framework.
---

# Unit Test Generator

Automatically generate comprehensive unit tests for your code.

## Core Capabilities

This skill helps you generate high-quality unit tests by:

1. **Analyzing source code** - Understanding function/class behavior and contracts
2. **Identifying test cases** - Determining happy paths, edge cases, and error conditions
3. **Matching style** - Following existing test patterns and conventions in your codebase
4. **Generating tests** - Creating complete, runnable test code
5. **Explaining coverage** - Documenting what each test validates

## Test Generation Workflow

### Step 1: Analyze the Code to Test

Examine the source code to understand:

**Function Signature:**
- Parameters and their types
- Return type
- Exceptions raised

**Function Behavior:**
- What the function does
- Preconditions and postconditions
- Side effects (DB writes, API calls, file I/O)
- Dependencies on other code

**Example Analysis:**

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price.

    Args:
        price: Original price (must be positive)
        discount_percent: Discount percentage (0-100)

    Returns:
        Discounted price

    Raises:
        ValueError: If price is negative or discount is invalid
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")

    return price * (1 - discount_percent / 100)
```

**Analysis:**
- Takes two floats, returns float
- Validates price >= 0
- Validates discount in [0, 100]
- Raises ValueError for invalid inputs
- Pure function (no side effects)

### Step 2: Identify Test Cases

Determine all test scenarios using the **Comprehensive Coverage** approach:

**1. Happy Path Tests** - Normal, expected usage
- Valid inputs that should succeed
- Typical use cases

**2. Edge Case Tests** - Boundary conditions
- Zero values
- Maximum/minimum values
- Empty inputs
- Single element inputs

**3. Error Condition Tests** - Invalid inputs
- Null/None values
- Negative numbers (when positive expected)
- Out-of-range values
- Type mismatches (if applicable)
- Invalid states

**4. Special Cases** - Domain-specific scenarios
- Floating point precision
- String encoding issues
- Date/time edge cases (leap years, time zones)
- Concurrency issues

**Example Test Cases for `calculate_discount`:**

| Category | Test Case | Input | Expected |
|----------|-----------|-------|----------|
| Happy path | Normal discount | price=100, discount=20 | 80.0 |
| Happy path | No discount | price=100, discount=0 | 100.0 |
| Happy path | Full discount | price=100, discount=100 | 0.0 |
| Edge case | Zero price | price=0, discount=50 | 0.0 |
| Edge case | Small discount | price=100, discount=0.01 | 99.99 |
| Error | Negative price | price=-10, discount=20 | ValueError |
| Error | Discount too high | price=100, discount=101 | ValueError |
| Error | Negative discount | price=100, discount=-5 | ValueError |

### Step 3: Examine Existing Test Patterns

Before generating tests, analyze existing tests in the codebase to match style:

**Look for:**
- Test file naming convention (`test_*.py`, `*_test.py`, `*Test.java`)
- Test class structure (if used)
- Assertion style (`assert`, `self.assertEqual`, `assertThat`)
- Fixture/setup patterns
- Mocking patterns
- Test organization (Arrange-Act-Assert, Given-When-Then)
- Naming conventions (`test_function_does_something`, `testFunctionDoesSomething`)

**Python Example - Analyze Existing Tests:**

```python
# If existing tests use this pattern:
class TestUserService:
    @pytest.fixture
    def user_service(self):
        return UserService()

    def test_create_user_with_valid_data_succeeds(self, user_service):
        # Arrange
        user_data = {"name": "Alice", "email": "alice@example.com"}

        # Act
        user = user_service.create_user(user_data)

        # Assert
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
```

**Pattern Identified:**
- Class-based test organization
- pytest fixtures
- Descriptive test names with underscores
- Arrange-Act-Assert comments
- Direct assertions using `assert`

**Java Example - Analyze Existing Tests:**

```java
// If existing tests use this pattern:
public class UserServiceTest {
    private UserService userService;

    @Before
    public void setUp() {
        userService = new UserService();
    }

    @Test
    public void testCreateUserWithValidData() {
        // given
        UserData data = new UserData("Alice", "alice@example.com");

        // when
        User user = userService.createUser(data);

        // then
        assertEquals("Alice", user.getName());
        assertEquals("alice@example.com", user.getEmail());
    }
}
```

**Pattern Identified:**
- JUnit 4 style with `@Before` setup
- Given-When-Then comments
- `assertEquals` assertions
- Test method prefix `test`

### Step 4: Generate Test Code

Create complete, runnable tests following the identified patterns.

**Test Structure Template:**

```
1. Test file/class setup
2. Fixtures/setup methods (if needed)
3. Happy path tests
4. Edge case tests
5. Error condition tests
6. Cleanup/teardown (if needed)
```

**Python Example - Generated Tests:**

See `references/test_patterns.md` for full example with 9 comprehensive tests covering happy paths, edge cases, and error conditions.

**Java Example - Generated Tests:**

See `references/test_patterns.md` for full JUnit example with comprehensive coverage.

### Step 5: Handle Dependencies and Mocking

When the code under test has dependencies (databases, APIs, external services), generate tests with appropriate mocks.

**Identify Dependencies:**
- External API calls
- Database queries
- File system operations
- Time/date dependencies
- Random number generation
- Other service classes

**Python Mocking Pattern:**

```python
@pytest.fixture
def mock_dependency():
    return Mock()

def test_with_mock(mock_dependency):
    # Arrange
    mock_dependency.method.return_value = expected_value

    # Act
    result = code_under_test(mock_dependency)

    # Assert
    mock_dependency.method.assert_called_once()
    assert result == expected_value
```

**Java Mocking Pattern (Mockito):**

```java
@Mock
private Dependency dependency;

@Test
public void testWithMock() {
    // given
    when(dependency.method()).thenReturn(expectedValue);

    // when
    Result result = codeUnderTest(dependency);

    // then
    verify(dependency).method();
    assertEquals(expectedValue, result);
}
```

For detailed mocking examples, see `references/test_patterns.md`.

### Step 6: Add Documentation and Coverage Summary

Include comments explaining:
- What each test validates
- Why edge cases are important
- Coverage achieved

**Coverage Summary Example:**

```python
"""
Test coverage for calculate_discount function:

Happy Path (3 tests):
- Normal discount calculation
- Zero discount (no change)
- Full discount (price becomes 0)

Edge Cases (3 tests):
- Zero price
- Very small discount percentage
- Large price values

Error Conditions (3 tests):
- Negative price
- Discount > 100%
- Negative discount

Total: 9 tests covering all execution paths
"""
```

## Advanced Patterns

### Parameterized Tests

For testing multiple similar scenarios efficiently.

**Python (pytest):**

```python
@pytest.mark.parametrize("price,discount,expected", [
    (100, 20, 80),
    (100, 0, 100),
    (100, 100, 0),
    (50, 10, 45),
    (200, 25, 150),
])
def test_calculate_discount_various_inputs(price, discount, expected):
    result = calculate_discount(price, discount)
    assert result == expected
```

**Java (JUnit 5):**

```java
@ParameterizedTest
@CsvSource({
    "100.0, 20.0, 80.0",
    "100.0, 0.0, 100.0",
    "100.0, 100.0, 0.0"
})
void testCalculateDiscountVariousInputs(double price, double discount, double expected) {
    assertEquals(expected, calculator.calculateDiscount(price, discount), 0.001);
}
```

### Testing Classes with State

For classes that maintain state across method calls, see `references/test_patterns.md` for complete examples of:
- Fixture setup for stateful objects
- Testing state transitions
- Testing side effects
- Cleanup and teardown

## Framework-Specific Guidance

### Python (pytest)

**Key patterns:**
- Use `@pytest.fixture` for setup/teardown
- Use `@pytest.mark.parametrize` for data-driven tests
- Use `pytest.raises()` for exception testing
- Use `pytest.approx()` for floating point comparisons
- Use `mocker` fixture (pytest-mock) for mocking

**Test file naming:** `test_*.py` or `*_test.py`

### Python (unittest)

**Key patterns:**
- Inherit from `unittest.TestCase`
- Use `setUp()` and `tearDown()` methods
- Use `self.assertEqual()`, `self.assertTrue()`, etc.
- Use `self.assertRaises()` for exceptions
- Use `unittest.mock` for mocking

### Java (JUnit 4)

**Key patterns:**
- Use `@Before` and `@After` for setup/teardown
- Use `@Test` annotation on test methods
- Use `assertEquals()`, `assertTrue()`, etc.
- Use `@Test(expected = Exception.class)` for exceptions
- Use Mockito for mocking

### Java (JUnit 5)

**Key patterns:**
- Use `@BeforeEach` and `@AfterEach`
- Use `@Test` annotation
- Use `assertEquals()`, `assertThrows()`, etc.
- Use `@ParameterizedTest` for data-driven tests
- Use `@ExtendWith(MockitoExtension.class)` for Mockito

## Best Practices

1. **One assertion per test (generally)** - Makes failures clear
2. **Test behavior, not implementation** - Tests should survive refactoring
3. **Use descriptive test names** - Name should explain what and why
4. **Follow AAA pattern** - Arrange, Act, Assert (or Given-When-Then)
5. **Keep tests independent** - Tests shouldn't depend on each other
6. **Mock external dependencies** - Tests should be fast and reliable
7. **Test edge cases** - Don't just test the happy path
8. **Use fixtures/setup wisely** - Share setup but avoid complex fixtures
9. **Verify error messages** - Not just exception type
10. **Keep tests simple** - If test is complex, code might be too

## Resources

- **`references/test_patterns.md`** - Complete examples for common scenarios (mocking, stateful classes, async code, database operations, file I/O)
- **`references/assertion_guide.md`** - Framework-specific assertion reference and best practices

## Quick Reference

| Scenario | Python (pytest) | Java (JUnit) |
|----------|----------------|--------------|
| Basic test | `def test_name():` | `@Test public void testName()` |
| Setup | `@pytest.fixture` | `@Before` (JUnit 4) or `@BeforeEach` (JUnit 5) |
| Exception test | `with pytest.raises(Error):` | `@Test(expected = Error.class)` or `assertThrows()` |
| Parameterized | `@pytest.mark.parametrize` | `@ParameterizedTest` |
| Mocking | `mocker.patch()` or `Mock()` | `@Mock` with Mockito |
| Float comparison | `pytest.approx()` | `assertEquals(x, y, delta)` |
