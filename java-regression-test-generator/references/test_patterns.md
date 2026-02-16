# Java Test Patterns

Common JUnit and TestNG patterns for regression test generation.

## Table of Contents
- [JUnit 5 Patterns](#junit-5-patterns)
- [TestNG Patterns](#testng-patterns)
- [Mocking Patterns](#mocking-patterns)
- [Parameterized Test Patterns](#parameterized-test-patterns)
- [Exception Testing Patterns](#exception-testing-patterns)
- [Setup and Teardown Patterns](#setup-and-teardown-patterns)

## JUnit 5 Patterns

### Basic Test Structure

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorTest {
    @Test
    public void testAddition() {
        Calculator calc = new Calculator();
        int result = calc.add(2, 3);
        assertEquals(5, result);
    }

    @Test
    public void testAddition_WithNegativeNumbers() {
        Calculator calc = new Calculator();
        assertEquals(-1, calc.add(-3, 2));
    }
}
```

### Test Lifecycle Hooks

```java
import org.junit.jupiter.api.*;

public class ServiceTest {
    private Service service;
    private Database database;

    @BeforeAll
    static void setupClass() {
        // Runs once before all tests
        System.setProperty("env", "test");
    }

    @BeforeEach
    void setup() {
        // Runs before each test
        database = new InMemoryDatabase();
        service = new Service(database);
    }

    @AfterEach
    void teardown() {
        // Runs after each test
        database.close();
    }

    @AfterAll
    static void teardownClass() {
        // Runs once after all tests
        System.clearProperty("env");
    }

    @Test
    void testServiceOperation() {
        service.performOperation();
        assertTrue(database.hasData());
    }
}
```

### Assertions

```java
import static org.junit.jupiter.api.Assertions.*;

@Test
void testAssertions() {
    // Equality
    assertEquals(expected, actual);
    assertEquals(expected, actual, "Custom failure message");
    assertEquals(3.14, actual, 0.01); // Delta for doubles

    // Boolean
    assertTrue(condition);
    assertFalse(condition);

    // Null checks
    assertNull(object);
    assertNotNull(object);

    // Reference equality
    assertSame(expected, actual);
    assertNotSame(expected, actual);

    // Array equality
    assertArrayEquals(expectedArray, actualArray);

    // Collection assertions
    List<String> list = Arrays.asList("a", "b", "c");
    assertEquals(3, list.size());
    assertTrue(list.contains("a"));

    // Multiple assertions (all executed even if some fail)
    assertAll("user",
        () -> assertEquals("John", user.getFirstName()),
        () -> assertEquals("Doe", user.getLastName()),
        () -> assertEquals(30, user.getAge())
    );
}
```

## TestNG Patterns

### Basic Test Structure

```java
import org.testng.annotations.Test;
import static org.testng.Assert.*;

public class CalculatorTest {
    @Test
    public void testAddition() {
        Calculator calc = new Calculator();
        int result = calc.add(2, 3);
        assertEquals(result, 5);
    }

    @Test(groups = {"fast", "unit"})
    public void testMultiplication() {
        Calculator calc = new Calculator();
        assertEquals(calc.multiply(3, 4), 12);
    }
}
```

### Test Dependencies

```java
import org.testng.annotations.Test;

public class DependentTest {
    @Test
    public void setupData() {
        // Setup test data
    }

    @Test(dependsOnMethods = {"setupData"})
    public void testWithData() {
        // This runs after setupData
    }

    @Test(dependsOnGroups = {"database"})
    public void testRequiringDatabase() {
        // Runs after all tests in "database" group
    }
}
```

### TestNG Lifecycle

```java
import org.testng.annotations.*;

public class ServiceTest {
    @BeforeSuite
    public void setupSuite() {
        // Runs once before entire test suite
    }

    @BeforeTest
    public void setupTest() {
        // Runs before each <test> tag in testng.xml
    }

    @BeforeClass
    public void setupClass() {
        // Runs once before all tests in this class
    }

    @BeforeMethod
    public void setupMethod() {
        // Runs before each test method
    }

    @Test
    public void testMethod() {
        // Test code
    }

    @AfterMethod
    public void teardownMethod() {
        // Runs after each test method
    }

    @AfterClass
    public void teardownClass() {
        // Runs once after all tests in this class
    }
}
```

## Mocking Patterns

### Mockito Basics

```java
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

public class UserServiceTest {
    @Test
    public void testGetUser() {
        // Create mock
        UserRepository mockRepo = mock(UserRepository.class);

        // Define behavior
        User expectedUser = new User("123", "John");
        when(mockRepo.findById("123")).thenReturn(expectedUser);

        // Use mock
        UserService service = new UserService(mockRepo);
        User actualUser = service.getUser("123");

        // Verify
        assertEquals(expectedUser, actualUser);
        verify(mockRepo).findById("123");
    }
}
```

### Mockito Annotations

```java
import org.mockito.Mock;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.extension.ExtendWith;

@ExtendWith(MockitoExtension.class)
public class OrderServiceTest {
    @Mock
    private PaymentProcessor paymentProcessor;

    @Mock
    private InventoryService inventoryService;

    @InjectMocks
    private OrderService orderService;

    @Test
    public void testProcessOrder() {
        Order order = new Order("ORD-123", 99.99);

        when(inventoryService.isAvailable(order.getProductId()))
            .thenReturn(true);
        when(paymentProcessor.process(99.99))
            .thenReturn(new PaymentResult(true, "TXN-456"));

        orderService.processOrder(order);

        verify(inventoryService).isAvailable(order.getProductId());
        verify(paymentProcessor).process(99.99);
    }
}
```

### Argument Matchers

```java
import static org.mockito.ArgumentMatchers.*;

@Test
public void testWithMatchers() {
    UserRepository mockRepo = mock(UserRepository.class);

    // Any argument
    when(mockRepo.findById(anyString())).thenReturn(new User());

    // Specific type
    when(mockRepo.save(any(User.class))).thenReturn(true);

    // Null argument
    when(mockRepo.findById(isNull())).thenThrow(new IllegalArgumentException());

    // Custom matcher
    when(mockRepo.findById(argThat(id -> id.startsWith("USR-"))))
        .thenReturn(new User());

    // Verify with matchers
    verify(mockRepo).findById(eq("123"));
    verify(mockRepo, times(2)).save(any(User.class));
    verify(mockRepo, never()).delete(any());
}
```

### Spy Objects

```java
@Test
public void testWithSpy() {
    // Spy wraps a real object
    List<String> list = new ArrayList<>();
    List<String> spyList = spy(list);

    // Real method is called
    spyList.add("one");
    assertEquals(1, spyList.size());

    // Can stub specific methods
    when(spyList.size()).thenReturn(100);
    assertEquals(100, spyList.size());

    // Can verify interactions
    verify(spyList).add("one");
}
```

## Parameterized Test Patterns

### JUnit 5 Parameterized Tests

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;

public class ParameterizedTests {
    @ParameterizedTest
    @ValueSource(ints = {1, 3, 5, 7, 9})
    void testOddNumbers(int number) {
        assertTrue(number % 2 != 0);
    }

    @ParameterizedTest
    @CsvSource({
        "1, 1, 2",
        "2, 3, 5",
        "5, 5, 10"
    })
    void testAddition(int a, int b, int expected) {
        assertEquals(expected, calculator.add(a, b));
    }

    @ParameterizedTest
    @MethodSource("provideStringsForIsBlank")
    void testIsBlank(String input, boolean expected) {
        assertEquals(expected, StringUtils.isBlank(input));
    }

    static Stream<Arguments> provideStringsForIsBlank() {
        return Stream.of(
            Arguments.of(null, true),
            Arguments.of("", true),
            Arguments.of("  ", true),
            Arguments.of("not blank", false)
        );
    }

    @ParameterizedTest
    @EnumSource(TimeUnit.class)
    void testTimeUnits(TimeUnit unit) {
        assertNotNull(unit);
    }
}
```

### TestNG Data Providers

```java
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

public class DataProviderTest {
    @DataProvider(name = "additionData")
    public Object[][] createData() {
        return new Object[][] {
            {1, 1, 2},
            {2, 3, 5},
            {5, 5, 10}
        };
    }

    @Test(dataProvider = "additionData")
    public void testAddition(int a, int b, int expected) {
        assertEquals(calculator.add(a, b), expected);
    }

    @DataProvider(name = "userProvider")
    public Object[][] provideUsers() {
        return new Object[][] {
            {new User("John", 25)},
            {new User("Jane", 30)},
            {new User("Bob", 35)}
        };
    }

    @Test(dataProvider = "userProvider")
    public void testUserValidation(User user) {
        assertTrue(validator.isValid(user));
    }
}
```

## Exception Testing Patterns

### JUnit 5 Exception Testing

```java
import static org.junit.jupiter.api.Assertions.*;

@Test
void testException() {
    // Assert that exception is thrown
    assertThrows(IllegalArgumentException.class, () -> {
        calculator.divide(10, 0);
    });

    // Capture exception and verify message
    Exception exception = assertThrows(IllegalArgumentException.class, () -> {
        calculator.divide(10, 0);
    });
    assertEquals("Division by zero", exception.getMessage());

    // Assert that no exception is thrown
    assertDoesNotThrow(() -> {
        calculator.divide(10, 2);
    });
}
```

### TestNG Exception Testing

```java
@Test(expectedExceptions = IllegalArgumentException.class)
public void testDivisionByZero() {
    calculator.divide(10, 0);
}

@Test(expectedExceptions = IllegalArgumentException.class,
      expectedExceptionsMessageRegExp = ".*zero.*")
public void testDivisionByZeroWithMessage() {
    calculator.divide(10, 0);
}
```

## Setup and Teardown Patterns

### Resource Management

```java
@Test
public void testWithResources() {
    // Try-with-resources for automatic cleanup
    try (Database db = new Database();
         Connection conn = db.getConnection()) {

        // Test code
        ResultSet rs = conn.query("SELECT * FROM users");
        assertTrue(rs.hasNext());

    } // Resources automatically closed
}
```

### Test Fixtures

```java
public class DatabaseTest {
    private Database database;
    private Connection connection;

    @BeforeEach
    void setupDatabase() {
        database = new InMemoryDatabase();
        connection = database.connect();

        // Populate test data
        connection.execute("CREATE TABLE users (id INT, name VARCHAR(50))");
        connection.execute("INSERT INTO users VALUES (1, 'John')");
        connection.execute("INSERT INTO users VALUES (2, 'Jane')");
    }

    @AfterEach
    void cleanupDatabase() {
        if (connection != null) {
            connection.close();
        }
        if (database != null) {
            database.shutdown();
        }
    }

    @Test
    void testUserQuery() {
        List<User> users = connection.query("SELECT * FROM users");
        assertEquals(2, users.size());
    }
}
```

### Temporary Files

```java
import org.junit.jupiter.api.io.TempDir;
import java.nio.file.Path;

public class FileServiceTest {
    @TempDir
    Path tempDir;

    @Test
    void testFileCreation() {
        Path file = tempDir.resolve("test.txt");
        fileService.createFile(file, "content");

        assertTrue(Files.exists(file));
        assertEquals("content", Files.readString(file));
    }
    // tempDir automatically cleaned up after test
}
```

## Test Organization Patterns

### Nested Tests

```java
import org.junit.jupiter.api.Nested;

public class CalculatorTest {
    private Calculator calculator = new Calculator();

    @Nested
    class AdditionTests {
        @Test
        void testPositiveNumbers() {
            assertEquals(5, calculator.add(2, 3));
        }

        @Test
        void testNegativeNumbers() {
            assertEquals(-5, calculator.add(-2, -3));
        }
    }

    @Nested
    class DivisionTests {
        @Test
        void testValidDivision() {
            assertEquals(2.0, calculator.divide(10, 5));
        }

        @Test
        void testDivisionByZero() {
            assertThrows(ArithmeticException.class,
                () -> calculator.divide(10, 0));
        }
    }
}
```

### Display Names

```java
import org.junit.jupiter.api.DisplayName;

@DisplayName("Calculator Tests")
public class CalculatorTest {
    @Test
    @DisplayName("Adding two positive numbers should return their sum")
    void testAddition() {
        assertEquals(5, calculator.add(2, 3));
    }

    @Test
    @DisplayName("Division by zero should throw IllegalArgumentException")
    void testDivisionByZero() {
        assertThrows(IllegalArgumentException.class,
            () -> calculator.divide(10, 0));
    }
}
```

## Timeout Patterns

```java
import org.junit.jupiter.api.Timeout;
import java.util.concurrent.TimeUnit;

@Test
@Timeout(value = 100, unit = TimeUnit.MILLISECONDS)
void testPerformance() {
    // Test must complete within 100ms
    service.performOperation();
}

@Test
void testWithAssertTimeout() {
    assertTimeout(Duration.ofSeconds(2), () -> {
        // Code that should complete within 2 seconds
        service.longRunningOperation();
    });
}
```
