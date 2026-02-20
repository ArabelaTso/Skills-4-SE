---
name: incremental-java-programmer
description: Incrementally implement new features in Java repositories from natural language descriptions. Use when adding functionality to existing Java codebases (Maven or Gradle projects). Takes a feature description as input and outputs modified repository with implementation code, corresponding JUnit tests, and verification that all tests pass. Supports method additions, new class creation, and method modifications with proper Java conventions.
---

# Incremental Java Programmer

## Overview

Implement new features in Java repositories by analyzing the codebase, generating implementation code, creating comprehensive tests, and ensuring all tests pass before completion.

## Workflow

### 1. Analyze Repository Structure

Understand the Java project structure and build system:

**Identify build system**:
- Maven: Look for `pom.xml` in root directory
- Gradle: Look for `build.gradle` or `build.gradle.kts`

**Examine project structure**:
```
src/
├── main/
│   └── java/
│       └── com/example/project/
│           ├── model/
│           ├── service/
│           ├── controller/
│           └── util/
└── test/
    └── java/
        └── com/example/project/
            ├── model/
            ├── service/
            └── controller/
```

**Extract key information**:
- Package structure and naming conventions
- Existing class hierarchy and relationships
- Dependencies from `pom.xml` or `build.gradle`
- Testing framework (JUnit 4, JUnit 5, TestNG)
- Code style and patterns used in the project

### 2. Parse Feature Description

Break down the natural language feature description into actionable components:

**Identify feature type**:
- **New functionality**: Adding entirely new capabilities
- **Enhancement**: Extending existing functionality
- **Modification**: Changing existing behavior

**Extract requirements**:
- What classes/methods need to be created or modified
- Input parameters and return types
- Business logic and validation rules
- Error handling requirements
- Integration points with existing code

**Example feature description**:
```
"Add a method to calculate the total price of items in a shopping cart,
including tax. The tax rate should be configurable. If the cart is empty,
return 0. The method should throw an exception if the tax rate is negative."
```

**Parsed components**:
- Target class: `ShoppingCart`
- New method: `calculateTotalWithTax(double taxRate)`
- Return type: `double`
- Validation: Check for negative tax rate, handle empty cart
- Exception: `IllegalArgumentException` for negative tax rate

### 3. Locate Target Files

Find where the implementation should be added:

**For new classes**:
- Determine appropriate package based on functionality
- Follow existing package structure conventions
- Place in `src/main/java/[package-path]/`

**For existing classes**:
- Use Grep to find the target class
- Read the class to understand current structure
- Identify where new methods should be added

**For modifications**:
- Locate the specific method to modify
- Understand current implementation
- Plan minimal changes to achieve feature

### 4. Implement Feature Code

Write Java code following project conventions:

**Code structure**:
```java
/**
 * [Javadoc description of what the method does]
 *
 * @param paramName description of parameter
 * @return description of return value
 * @throws ExceptionType description of when exception is thrown
 */
public ReturnType methodName(ParamType paramName) {
    // Input validation
    if (invalidCondition) {
        throw new IllegalArgumentException("Error message");
    }

    // Business logic
    ReturnType result = performCalculation();

    // Return result
    return result;
}
```

**Best practices**:
- Follow existing code style (indentation, naming, formatting)
- Add comprehensive Javadoc comments
- Include input validation
- Handle edge cases
- Use appropriate access modifiers
- Follow SOLID principles
- Avoid code duplication

**For new classes**:
```java
package com.example.project.service;

import java.util.List;

/**
 * Service class for managing shopping cart operations.
 */
public class ShoppingCartService {

    private final TaxCalculator taxCalculator;

    public ShoppingCartService(TaxCalculator taxCalculator) {
        this.taxCalculator = taxCalculator;
    }

    // Methods here
}
```

### 5. Generate Unit Tests

Create comprehensive JUnit tests for the new functionality:

**Test class structure**:
```java
package com.example.project.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

class ShoppingCartServiceTest {

    private ShoppingCartService service;

    @BeforeEach
    void setUp() {
        service = new ShoppingCartService(new TaxCalculator());
    }

    @Test
    @DisplayName("Should calculate total with tax correctly")
    void testCalculateTotalWithTax() {
        // Arrange
        double subtotal = 100.0;
        double taxRate = 0.08;

        // Act
        double result = service.calculateTotalWithTax(subtotal, taxRate);

        // Assert
        assertEquals(108.0, result, 0.01);
    }

    @Test
    @DisplayName("Should throw exception for negative tax rate")
    void testNegativeTaxRate() {
        assertThrows(IllegalArgumentException.class, () -> {
            service.calculateTotalWithTax(100.0, -0.05);
        });
    }

    @Test
    @DisplayName("Should return zero for empty cart")
    void testEmptyCart() {
        double result = service.calculateTotalWithTax(0.0, 0.08);
        assertEquals(0.0, result, 0.01);
    }
}
```

**Test coverage requirements**:
- Happy path (normal operation)
- Edge cases (empty inputs, boundary values)
- Error cases (invalid inputs, exceptions)
- Integration with existing code

**Test naming conventions**:
- Use descriptive test method names
- Follow project's existing test naming pattern
- Use `@DisplayName` for readable test descriptions

### 6. Update Existing Tests

Modify existing tests if the feature changes existing behavior:

**Identify affected tests**:
- Search for tests that call modified methods
- Find tests that assert on changed behavior
- Locate integration tests that may be affected

**Update test assertions**:
```java
// Before
assertEquals(100.0, cart.getTotal());

// After (if feature adds tax calculation)
assertEquals(108.0, cart.getTotalWithTax(0.08));
```

**Add new test cases**:
- Test interactions between new and existing features
- Verify backward compatibility if applicable
- Test integration points

### 7. Run and Verify Tests

Execute the test suite to ensure all tests pass:

**For Maven projects**:
```bash
# Run all tests
mvn test

# Run specific test class
mvn test -Dtest=ShoppingCartServiceTest

# Run with verbose output
mvn test -X
```

**For Gradle projects**:
```bash
# Run all tests
./gradlew test

# Run specific test class
./gradlew test --tests ShoppingCartServiceTest

# Run with detailed output
./gradlew test --info
```

**Verify test results**:
- All tests must pass (green)
- No compilation errors
- No test failures or errors
- Check test coverage if available

**If tests fail**:
1. Read the failure message and stack trace
2. Identify the root cause
3. Fix the implementation or test code
4. Re-run tests
5. Repeat until all tests pass

### 8. Validate Implementation

Perform final checks before completion:

**Code quality checks**:
- No compiler warnings
- Follows project code style
- Proper exception handling
- Appropriate logging (if project uses logging)
- No hardcoded values (use constants or configuration)

**Integration checks**:
- New code integrates cleanly with existing code
- No breaking changes to existing APIs
- Dependencies are properly declared
- Imports are organized

**Documentation checks**:
- All public methods have Javadoc
- Complex logic has inline comments
- README updated if needed (for major features)

## Implementation Patterns

### Pattern 1: Adding a New Method

**Feature**: "Add a method to validate email addresses"

**Implementation**:
```java
/**
 * Validates if the given string is a valid email address.
 *
 * @param email the email address to validate
 * @return true if valid, false otherwise
 * @throws IllegalArgumentException if email is null
 */
public boolean isValidEmail(String email) {
    if (email == null) {
        throw new IllegalArgumentException("Email cannot be null");
    }

    String emailRegex = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$";
    return email.matches(emailRegex);
}
```

**Test**:
```java
@Test
void testValidEmail() {
    assertTrue(validator.isValidEmail("user@example.com"));
}

@Test
void testInvalidEmail() {
    assertFalse(validator.isValidEmail("invalid-email"));
}

@Test
void testNullEmail() {
    assertThrows(IllegalArgumentException.class, () -> {
        validator.isValidEmail(null);
    });
}
```

### Pattern 2: Creating a New Class

**Feature**: "Create a UserService class to manage user operations"

**Implementation**:
```java
package com.example.project.service;

import com.example.project.model.User;
import com.example.project.repository.UserRepository;
import java.util.Optional;

/**
 * Service class for managing user-related operations.
 */
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /**
     * Finds a user by their ID.
     *
     * @param userId the user ID
     * @return Optional containing the user if found
     */
    public Optional<User> findById(Long userId) {
        if (userId == null || userId <= 0) {
            throw new IllegalArgumentException("Invalid user ID");
        }
        return userRepository.findById(userId);
    }
}
```

### Pattern 3: Modifying Existing Method

**Feature**: "Update the calculateDiscount method to support percentage-based discounts"

**Before**:
```java
public double calculateDiscount(double price) {
    return price * 0.1; // Fixed 10% discount
}
```

**After**:
```java
public double calculateDiscount(double price, double discountRate) {
    if (price < 0) {
        throw new IllegalArgumentException("Price cannot be negative");
    }
    if (discountRate < 0 || discountRate > 1) {
        throw new IllegalArgumentException("Discount rate must be between 0 and 1");
    }
    return price * discountRate;
}
```

## Tips

- Always read existing code before making changes
- Follow the project's existing patterns and conventions
- Write tests before or alongside implementation (TDD approach)
- Keep changes minimal and focused on the feature
- Use meaningful variable and method names
- Handle all edge cases and error conditions
- Run tests frequently during development
- Check for compilation errors after each change
- Use IDE refactoring tools when available
- Commit changes incrementally with clear messages
