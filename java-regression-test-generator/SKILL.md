---
name: java-regression-test-generator
description: "Automatically generate regression tests for Java codebases by analyzing changes between old and new code versions. Use when users need to: (1) Generate tests after refactoring or code changes, (2) Ensure previously tested behavior still works in new versions, (3) Cover modified or newly added code paths, (4) Migrate existing tests to work with updated APIs or signatures, (5) Maintain test coverage during code evolution. Supports JUnit and TestNG frameworks with unit tests, parameterized tests, and exception testing patterns."
---

# Java Regression Test Generator

Automatically generate regression tests for Java code based on version changes.

## Overview

This skill analyzes changes between old and new versions of Java code and generates regression tests that ensure previously tested behavior still works while covering new or modified functionality. It preserves correctness guarantees from existing tests and suggests updates when old tests become invalid.

## How to Use

Provide:
1. **Old version**: The previous version of Java code
2. **New version**: The updated version of Java code
3. **Existing tests**: Test classes or methods for the old version
4. **Framework** (optional): JUnit 5 (default) or TestNG

The skill will:
- Analyze changes between versions
- Identify modified, added, or removed functionality
- Generate regression tests for the new code
- Suggest updates for invalid existing tests
- Produce executable test code ready for integration

## Test Generation Workflow

### Step 1: Analyze Code Changes

Compare old and new versions to identify changes:

**Method-level changes**:
- Signature changes (parameters, return type)
- Logic modifications (algorithm, error handling)
- New methods added
- Methods removed

**Class-level changes**:
- Field additions or removals
- Constructor changes
- Inheritance modifications
- Access modifier changes

**Dependency changes**:
- New dependencies injected
- Dependency injection patterns added
- External API changes

### Step 2: Classify Change Types

Categorize each change to determine test generation strategy:

**Type 1: Signature Changes**
- Parameter added/removed/reordered
- Return type changed
- Exception declarations modified

**Type 2: Behavioral Changes**
- Algorithm optimized (same behavior)
- Error handling added
- Validation logic added

**Type 3: Structural Changes**
- New methods/classes added
- Methods/classes removed
- Refactoring (extract method, rename)

**Type 4: Dependency Changes**
- Constructor injection added
- Dependencies replaced
- Mock requirements changed

### Step 3: Determine Test Strategy

For each change type, decide on test generation approach:

| Change Type | Strategy |
|-------------|----------|
| Parameter added | Migrate existing tests + generate new parameter tests |
| Return type changed | Update assertions + add new type-specific tests |
| New method | Generate full test coverage (normal, edge, error cases) |
| Logic optimized | Preserve existing tests + add performance/edge tests |
| Error handling added | Preserve existing tests + add exception tests |
| Method removed | Mark tests as obsolete, suggest removal |
| Dependency injection | Update test setup with mocks |

See [change_patterns.md](references/change_patterns.md) for detailed strategies.

### Step 4: Generate Regression Tests

Create test code following these principles:

**Preserve existing behavior**:
- Keep all tests that verify unchanged functionality
- Migrate tests when signatures change but behavior is preserved
- Maintain test names and structure when possible

**Cover new functionality**:
- Generate tests for new methods
- Add tests for new parameters or return types
- Test new error conditions

**Ensure quality**:
- Use appropriate assertions
- Include setup/teardown code
- Add mocks for dependencies
- Follow framework conventions (JUnit 5 or TestNG)

### Step 5: Handle Invalid Tests

When existing tests become invalid, suggest updates:

**Scenario 1: Signature changed**
```java
// Old test (invalid)
@Test
public void testCalculateDiscount() {
    assertEquals(10, calculator.calculateDiscount(100));
}

// Suggested update
@Test
public void testCalculateDiscount_WithDefaultPercent() {
    // Updated to use new signature with default value
    assertEquals(10, calculator.calculateDiscount(100, 10));
}
```

**Scenario 2: Return type changed**
```java
// Old test (invalid)
@Test
public void testGetUser() {
    User user = service.getUser("123");
    assertEquals("John", user.getName());
}

// Suggested update
@Test
public void testGetUser() {
    Optional<User> userOpt = service.getUser("123");
    assertTrue(userOpt.isPresent());
    assertEquals("John", userOpt.get().getName());
}
```

**Scenario 3: Method removed**
```java
// Old test (obsolete)
// @Test
// public void testDeprecatedMethod() {
//     service.deprecatedMethod();
// }
// OBSOLETE: deprecatedMethod() removed in new version
// Consider: Check if functionality moved to another method
```

## Example: Parameter Added

**Old Code**:
```java
public class DiscountCalculator {
    public int calculateDiscount(int price) {
        return price * 10 / 100;  // Fixed 10% discount
    }
}
```

**New Code**:
```java
public class DiscountCalculator {
    public int calculateDiscount(int price, int discountPercent) {
        return price * discountPercent / 100;  // Configurable discount
    }
}
```

**Existing Test**:
```java
@Test
public void testCalculateDiscount() {
    DiscountCalculator calc = new DiscountCalculator();
    assertEquals(10, calc.calculateDiscount(100));
}

@Test
public void testCalculateDiscount_LargeAmount() {
    DiscountCalculator calc = new DiscountCalculator();
    assertEquals(100, calc.calculateDiscount(1000));
}
```

**Generated Regression Tests**:
```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DiscountCalculatorTest {
    private DiscountCalculator calculator = new DiscountCalculator();

    // Migrated tests - preserve original behavior with default 10%
    @Test
    public void testCalculateDiscount_WithDefaultPercent() {
        // Migrated from testCalculateDiscount
        // Uses 10% to match old behavior
        assertEquals(10, calculator.calculateDiscount(100, 10));
    }

    @Test
    public void testCalculateDiscount_LargeAmount_WithDefaultPercent() {
        // Migrated from testCalculateDiscount_LargeAmount
        assertEquals(100, calculator.calculateDiscount(1000, 10));
    }

    // New tests for added parameter
    @Test
    public void testCalculateDiscount_WithCustomPercent() {
        assertEquals(25, calculator.calculateDiscount(100, 25));
        assertEquals(50, calculator.calculateDiscount(200, 25));
    }

    @Test
    public void testCalculateDiscount_WithZeroPercent() {
        assertEquals(0, calculator.calculateDiscount(100, 0));
    }

    @Test
    public void testCalculateDiscount_WithHundredPercent() {
        assertEquals(100, calculator.calculateDiscount(100, 100));
    }

    @Test
    public void testCalculateDiscount_WithNegativePercent() {
        // Edge case: negative discount
        assertEquals(-10, calculator.calculateDiscount(100, -10));
    }
}
```

**Analysis**:
- **Change type**: Parameter added (discountPercent)
- **Strategy**: Migrate existing tests + generate new parameter tests
- **Preserved**: Original test logic with default 10% discount
- **Added**: Tests for various discount percentages (0%, 25%, 100%, negative)

## Example: New Method Added

**Old Code**:
```java
public class UserService {
    private UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = repository;
    }

    public User getUser(String id) {
        return repository.findById(id);
    }
}
```

**New Code**:
```java
public class UserService {
    private UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = repository;
    }

    public User getUser(String id) {
        return repository.findById(id);
    }

    // New method added
    public List<User> getUsersByRole(String role) {
        return repository.findAll().stream()
            .filter(u -> u.getRole().equals(role))
            .collect(Collectors.toList());
    }
}
```

**Existing Tests**:
```java
@Test
public void testGetUser() {
    UserRepository mockRepo = mock(UserRepository.class);
    when(mockRepo.findById("123")).thenReturn(new User("123", "John", "admin"));

    UserService service = new UserService(mockRepo);
    User user = service.getUser("123");

    assertEquals("John", user.getName());
}
```

**Generated Regression Tests**:
```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class UserServiceTest {
    private UserRepository mockRepository;
    private UserService service;

    @BeforeEach
    public void setup() {
        mockRepository = mock(UserRepository.class);
        service = new UserService(mockRepository);
    }

    // Existing test preserved
    @Test
    public void testGetUser() {
        when(mockRepository.findById("123"))
            .thenReturn(new User("123", "John", "admin"));

        User user = service.getUser("123");

        assertEquals("John", user.getName());
        verify(mockRepository).findById("123");
    }

    // New tests for getUsersByRole method
    @Test
    public void testGetUsersByRole_WithMatchingUsers() {
        List<User> allUsers = Arrays.asList(
            new User("1", "John", "admin"),
            new User("2", "Jane", "user"),
            new User("3", "Bob", "admin")
        );
        when(mockRepository.findAll()).thenReturn(allUsers);

        List<User> admins = service.getUsersByRole("admin");

        assertEquals(2, admins.size());
        assertTrue(admins.stream().allMatch(u -> u.getRole().equals("admin")));
        verify(mockRepository).findAll();
    }

    @Test
    public void testGetUsersByRole_NoMatches() {
        List<User> allUsers = Arrays.asList(
            new User("1", "John", "user"),
            new User("2", "Jane", "user")
        );
        when(mockRepository.findAll()).thenReturn(allUsers);

        List<User> admins = service.getUsersByRole("admin");

        assertTrue(admins.isEmpty());
    }

    @Test
    public void testGetUsersByRole_EmptyRepository() {
        when(mockRepository.findAll()).thenReturn(Collections.emptyList());

        List<User> users = service.getUsersByRole("admin");

        assertTrue(users.isEmpty());
    }

    @Test
    public void testGetUsersByRole_NullRole() {
        List<User> allUsers = Arrays.asList(
            new User("1", "John", "admin")
        );
        when(mockRepository.findAll()).thenReturn(allUsers);

        assertThrows(NullPointerException.class, () -> {
            service.getUsersByRole(null);
        });
    }
}
```

**Analysis**:
- **Change type**: New method added (getUsersByRole)
- **Strategy**: Preserve existing tests + generate full coverage for new method
- **Preserved**: testGetUser remains unchanged
- **Added**: 4 tests covering normal case, no matches, empty repository, null input

## Example: Return Type Changed

**Old Code**:
```java
public class UserService {
    public User getUserById(String id) {
        return database.findUser(id);  // Returns null if not found
    }
}
```

**New Code**:
```java
public class UserService {
    public Optional<User> getUserById(String id) {
        return Optional.ofNullable(database.findUser(id));
    }
}
```

**Existing Tests**:
```java
@Test
public void testGetUserById_ExistingUser() {
    User user = service.getUserById("123");
    assertNotNull(user);
    assertEquals("John", user.getName());
}

@Test
public void testGetUserById_NonExistentUser() {
    User user = service.getUserById("999");
    assertNull(user);
}
```

**Generated Regression Tests**:
```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Optional;

public class UserServiceTest {
    private UserService service = new UserService();

    // Updated tests for Optional return type
    @Test
    public void testGetUserById_ExistingUser() {
        // Migrated: Updated to handle Optional
        Optional<User> userOpt = service.getUserById("123");

        assertTrue(userOpt.isPresent(), "User should be present");
        assertEquals("John", userOpt.get().getName());
    }

    @Test
    public void testGetUserById_NonExistentUser() {
        // Migrated: Updated to check for empty Optional
        Optional<User> userOpt = service.getUserById("999");

        assertFalse(userOpt.isPresent(), "User should not be present");
    }

    // New tests for Optional-specific behavior
    @Test
    public void testGetUserById_OptionalChaining() {
        Optional<User> userOpt = service.getUserById("123");

        String name = userOpt
            .map(User::getName)
            .orElse("Unknown");

        assertEquals("John", name);
    }

    @Test
    public void testGetUserById_OrElseThrow() {
        Optional<User> userOpt = service.getUserById("999");

        assertThrows(NoSuchElementException.class, () -> {
            userOpt.orElseThrow();
        });
    }
}
```

**Analysis**:
- **Change type**: Return type changed (User → Optional<User>)
- **Strategy**: Update existing tests + add Optional-specific tests
- **Updated**: Both existing tests adapted to handle Optional
- **Added**: Tests for Optional chaining and orElseThrow behavior

## Output Format

Generated tests follow this structure:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * Regression tests for [ClassName]
 * Generated from version comparison
 */
public class [ClassName]Test {
    // Test fixtures
    private [ClassName] instance;
    private [Dependency] mockDependency;

    @BeforeEach
    public void setup() {
        // Initialize test fixtures
        mockDependency = mock([Dependency].class);
        instance = new [ClassName](mockDependency);
    }

    @AfterEach
    public void teardown() {
        // Cleanup if needed
    }

    // Preserved tests (migrated if needed)
    @Test
    public void test[MethodName]_[Scenario]() {
        // Arrange
        // Act
        // Assert
    }

    // New tests for added/modified functionality
    @Test
    public void test[NewMethod]_[Scenario]() {
        // Arrange
        // Act
        // Assert
    }
}
```

## References

Detailed patterns and examples:

- **[change_patterns.md](references/change_patterns.md)**: Comprehensive catalog of code change types and corresponding test generation strategies
- **[test_patterns.md](references/test_patterns.md)**: JUnit and TestNG patterns for unit tests, mocking, parameterized tests, and exception testing

Load these references when:
- Need detailed examples for specific change types
- Want to see complete test patterns for JUnit/TestNG
- Working with complex scenarios (inheritance changes, dependency injection)

## Tips

1. **Analyze changes carefully**: Understand what changed and why before generating tests
2. **Preserve test intent**: Keep the purpose of existing tests even when updating syntax
3. **Cover edge cases**: Generate tests for boundary conditions and error scenarios
4. **Use appropriate mocks**: Mock external dependencies to isolate unit behavior
5. **Follow naming conventions**: Use descriptive test names that explain what is being tested
6. **Maintain readability**: Generate clean, well-structured test code
7. **Verify compilation**: Ensure generated tests compile with the new code
8. **Check for redundancy**: Avoid generating tests that duplicate existing coverage
