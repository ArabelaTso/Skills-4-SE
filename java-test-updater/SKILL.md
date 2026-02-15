---
name: java-test-updater
description: Update Java test classes and methods to work with new code versions after refactoring or modifications. Use when code changes break existing tests due to signature changes, refactoring, or behavior modifications. Takes old and new code versions plus old tests as input, and outputs updated tests that compile and pass against the new code. Handles method signature changes, class refactoring, assertion updates, and mock modifications.
---

# Java Test Updater

## Overview

Automatically update Java test code to align with changes in production code, ensuring tests compile and pass after refactoring, signature changes, or behavior modifications.

## Workflow

### 1. Analyze Code Changes

Compare old and new versions of the production code to identify changes:

**Read both versions**:
- Old code version (before changes)
- New code version (after changes)
- Identify the specific class and methods that changed

**Categorize changes**:
- **Signature changes**: Parameter types, parameter order, return type, method name
- **Refactoring**: Class renamed, method moved, package changed
- **Behavior changes**: Logic modified, new exceptions, different return values
- **API changes**: New methods added, old methods removed

**Example change analysis**:
```java
// Old version
public double calculateDiscount(double price) {
    return price * 0.1;
}

// New version
public double calculateDiscount(double price, double discountRate) {
    if (discountRate < 0 || discountRate > 1) {
        throw new IllegalArgumentException("Invalid discount rate");
    }
    return price * discountRate;
}
```

**Identified changes**:
- Added parameter: `discountRate`
- Added validation with exception
- Changed calculation logic

### 2. Analyze Existing Tests

Read and understand the old test code:

**Identify test structure**:
- Test class name and package
- Test methods and their purposes
- Setup and teardown methods (`@Before`, `@BeforeEach`, `@After`, `@AfterEach`)
- Test data and fixtures
- Mocks and stubs used

**Map tests to code changes**:
- Which tests call the changed methods
- Which assertions depend on changed behavior
- Which mocks need updating

**Example old test**:
```java
@Test
public void testCalculateDiscount() {
    double price = 100.0;
    double result = calculator.calculateDiscount(price);
    assertEquals(10.0, result, 0.01);
}
```

### 3. Update Method Calls

Modify test code to match new method signatures:

**For added parameters**:
```java
// Old call
calculator.calculateDiscount(price)

// Updated call
calculator.calculateDiscount(price, 0.1)  // Use appropriate default or test value
```

**For removed parameters**:
```java
// Old call
calculator.calculateDiscount(price, taxRate, shippingCost)

// Updated call (if taxRate removed)
calculator.calculateDiscount(price, shippingCost)
```

**For parameter type changes**:
```java
// Old call
calculator.process(userId)  // userId was int

// Updated call (if userId changed to Long)
calculator.process(Long.valueOf(userId))
```

**For renamed methods**:
```java
// Old call
calculator.computeTotal()

// Updated call (if renamed to calculateTotal)
calculator.calculateTotal()
```

**For moved methods**:
```java
// Old call
calculator.validateInput(data)

// Updated call (if moved to validator class)
validator.validateInput(data)
```

### 4. Update Assertions

Adjust test assertions to match new behavior:

**For changed return values**:
```java
// Old assertion (10% fixed discount)
assertEquals(10.0, result, 0.01);

// Updated assertion (variable discount rate)
assertEquals(8.0, calculator.calculateDiscount(100.0, 0.08), 0.01);
```

**For new exceptions**:
```java
// Add new test for exception
@Test
public void testInvalidDiscountRate() {
    assertThrows(IllegalArgumentException.class, () -> {
        calculator.calculateDiscount(100.0, -0.1);
    });
}
```

**For changed behavior**:
```java
// Old assertion
assertTrue(result.isEmpty());

// Updated assertion (if behavior changed to return null instead)
assertNull(result);
```

**For modified object state**:
```java
// Old assertion
assertEquals(1, cart.getItemCount());

// Updated assertion (if implementation changed)
assertEquals(1, cart.getItems().size());
```

### 5. Update Mocks and Stubs

Modify mock objects to match new interfaces:

**For Mockito mocks with signature changes**:
```java
// Old mock setup
when(repository.findById(userId)).thenReturn(user);

// Updated mock setup (if return type changed to Optional)
when(repository.findById(userId)).thenReturn(Optional.of(user));
```

**For added parameters in mocked methods**:
```java
// Old mock
when(service.process(data)).thenReturn(result);

// Updated mock (if parameter added)
when(service.process(data, context)).thenReturn(result);
// Or use argument matchers
when(service.process(eq(data), any(Context.class))).thenReturn(result);
```

**For changed mock behavior**:
```java
// Old mock (method returned boolean)
when(validator.isValid(input)).thenReturn(true);

// Updated mock (method now throws exception instead)
doNothing().when(validator).validate(input);
// Or for invalid case:
doThrow(new ValidationException()).when(validator).validate(invalidInput);
```

### 6. Add New Test Cases

Create additional tests for new functionality or edge cases:

**For new parameters**:
```java
@Test
public void testCalculateDiscountWithZeroRate() {
    double result = calculator.calculateDiscount(100.0, 0.0);
    assertEquals(0.0, result, 0.01);
}

@Test
public void testCalculateDiscountWithMaxRate() {
    double result = calculator.calculateDiscount(100.0, 1.0);
    assertEquals(100.0, result, 0.01);
}
```

**For new exceptions**:
```java
@Test
public void testNegativeDiscountRate() {
    assertThrows(IllegalArgumentException.class, () -> {
        calculator.calculateDiscount(100.0, -0.5);
    });
}

@Test
public void testDiscountRateAboveOne() {
    assertThrows(IllegalArgumentException.class, () -> {
        calculator.calculateDiscount(100.0, 1.5);
    });
}
```

**For new behavior**:
```java
@Test
public void testNewFeature() {
    // Test newly added functionality
    Result result = service.newMethod(input);
    assertNotNull(result);
    assertEquals(expectedValue, result.getValue());
}
```

### 7. Update Test Setup and Teardown

Modify test fixtures if dependencies changed:

**For constructor changes**:
```java
// Old setup
@BeforeEach
void setUp() {
    calculator = new Calculator();
}

// Updated setup (if constructor now requires dependencies)
@BeforeEach
void setUp() {
    validator = new Validator();
    calculator = new Calculator(validator);
}
```

**For new dependencies**:
```java
// Old setup
@Mock
private Repository repository;

// Updated setup (if new dependency added)
@Mock
private Repository repository;

@Mock
private CacheService cacheService;

@BeforeEach
void setUp() {
    service = new Service(repository, cacheService);
}
```

### 8. Verify Compilation

Ensure updated tests compile without errors:

**Check for compilation issues**:
- Import statements are correct
- All types are resolved
- Method signatures match
- No syntax errors

**Common compilation fixes**:
```java
// Add missing imports
import java.util.Optional;
import static org.mockito.ArgumentMatchers.any;

// Fix type mismatches
Long userId = 123L;  // Instead of int userId = 123;

// Update generic types
List<String> items = new ArrayList<>();  // Instead of raw List
```

**Compile tests**:
```bash
# Maven
mvn test-compile

# Gradle
./gradlew testClasses
```

### 9. Run and Verify Tests

Execute tests to ensure they pass:

**Run all updated tests**:
```bash
# Maven
mvn test -Dtest=CalculatorTest

# Gradle
./gradlew test --tests CalculatorTest
```

**Analyze test results**:
- All tests should pass (green)
- No test failures
- No test errors
- Check test output for warnings

**If tests fail**:
1. Read failure message and stack trace
2. Identify the cause (assertion failure, exception, etc.)
3. Fix the test code or identify issues in production code
4. Re-run tests
5. Repeat until all tests pass

### 10. Validate Test Quality

Ensure updated tests maintain quality standards:

**Check test coverage**:
- New code paths are tested
- Edge cases are covered
- Exception handling is tested

**Verify test independence**:
- Tests don't depend on execution order
- Each test can run in isolation
- No shared mutable state between tests

**Review test clarity**:
- Test names are descriptive
- Test logic is clear
- Assertions are meaningful

## Update Patterns

### Pattern 1: Signature Change with Added Parameter

**Old code**:
```java
public String formatName(String firstName, String lastName) {
    return firstName + " " + lastName;
}
```

**New code**:
```java
public String formatName(String firstName, String lastName, String title) {
    return title + " " + firstName + " " + lastName;
}
```

**Old test**:
```java
@Test
public void testFormatName() {
    String result = formatter.formatName("John", "Doe");
    assertEquals("John Doe", result);
}
```

**Updated test**:
```java
@Test
public void testFormatName() {
    String result = formatter.formatName("John", "Doe", "Mr.");
    assertEquals("Mr. John Doe", result);
}

@Test
public void testFormatNameWithEmptyTitle() {
    String result = formatter.formatName("John", "Doe", "");
    assertEquals(" John Doe", result);
}
```

### Pattern 2: Method Refactored to Different Class

**Old code**:
```java
public class UserService {
    public boolean validateEmail(String email) {
        return email.contains("@");
    }
}
```

**New code**:
```java
public class UserService {
    private EmailValidator validator;
    // validateEmail moved to EmailValidator
}

public class EmailValidator {
    public boolean isValid(String email) {
        return email.contains("@");
    }
}
```

**Old test**:
```java
@Test
public void testValidateEmail() {
    assertTrue(userService.validateEmail("user@example.com"));
}
```

**Updated test**:
```java
@Mock
private EmailValidator emailValidator;

@BeforeEach
void setUp() {
    userService = new UserService(emailValidator);
}

@Test
public void testEmailValidation() {
    when(emailValidator.isValid("user@example.com")).thenReturn(true);
    // Test userService method that uses emailValidator
}

// Or create separate test for EmailValidator
@Test
public void testEmailValidatorIsValid() {
    EmailValidator validator = new EmailValidator();
    assertTrue(validator.isValid("user@example.com"));
}
```

### Pattern 3: Return Type Changed

**Old code**:
```java
public User findUser(Long id) {
    return repository.findById(id);  // Returns User or null
}
```

**New code**:
```java
public Optional<User> findUser(Long id) {
    return repository.findById(id);  // Returns Optional<User>
}
```

**Old test**:
```java
@Test
public void testFindUser() {
    User user = service.findUser(123L);
    assertNotNull(user);
    assertEquals("John", user.getName());
}
```

**Updated test**:
```java
@Test
public void testFindUser() {
    Optional<User> userOpt = service.findUser(123L);
    assertTrue(userOpt.isPresent());
    assertEquals("John", userOpt.get().getName());
}

@Test
public void testFindUserNotFound() {
    Optional<User> userOpt = service.findUser(999L);
    assertFalse(userOpt.isPresent());
}
```

## Tips

- Always read both old and new code versions completely
- Identify all affected test methods before making changes
- Update one test method at a time
- Compile frequently to catch errors early
- Run tests after each update to verify correctness
- Maintain test coverage - don't remove tests without replacement
- Add tests for new edge cases introduced by changes
- Keep test names descriptive and up-to-date
- Update test documentation/comments if behavior changed
- Use IDE refactoring tools when available for safe renames
