# Java Testing Patterns

## JUnit 5 Framework

### Basic Test Structure

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ClassNameTest {
    @Test
    void testMethodName() {
        // Arrange
        InputType input = setupTestData();

        // Act
        ResultType result = methodUnderTest(input);

        // Assert
        assertEquals(expected, result);
    }
}
```

### Common Assertions

```java
assertEquals(expected, actual);
assertNotEquals(unexpected, actual);
assertTrue(condition);
assertFalse(condition);
assertNull(object);
assertNotNull(object);
assertThrows(ExceptionType.class, () -> methodThatThrows());
assertArrayEquals(expectedArray, actualArray);
```

### Exception Testing

```java
@Test
void testExceptionThrown() {
    Exception exception = assertThrows(
        IllegalArgumentException.class,
        () -> methodThatShouldThrow(invalidInput)
    );
    assertTrue(exception.getMessage().contains("expected message"));
}
```

### Parametrized Tests

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

@ParameterizedTest
@CsvSource({
    "0, 0",
    "1, 1",
    "5, 120",
    "-1, -1"
})
void testFactorial(int input, int expected) {
    assertEquals(expected, factorial(input));
}
```

### Setup and Teardown

```java
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;

@BeforeEach
void setUp() {
    // Initialize test fixtures
}

@AfterEach
void tearDown() {
    // Clean up resources
}
```

### Edge Cases to Test

- Null inputs
- Empty collections
- Boundary values (Integer.MIN_VALUE, Integer.MAX_VALUE)
- Invalid inputs
- Concurrent access (if applicable)

### Test Organization

```java
class ClassNameTest {
    @Test
    void testNormalCase() { }

    @Test
    void testEdgeCase() { }

    @Test
    void testErrorCase() { }
}
```
