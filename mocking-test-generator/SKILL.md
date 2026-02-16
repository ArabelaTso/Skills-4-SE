---
name: mocking-test-generator
description: Generate unit tests with proper mocking for Python (unittest.mock/pytest) or Java (Mockito/JUnit) code. Use when users request test generation, unit tests with mocks, or testing code that has external dependencies like database calls, API requests, file I/O, or network operations. Automatically identifies dependencies to mock and creates executable, maintainable test code.
---

# Mocking Test Generator

Generate unit tests with proper mocking of external dependencies for Python and Java code.

## Workflow

1. **Analyze the code** - Identify external dependencies, side effects, and testable units
2. **Select framework** - Determine Python (unittest.mock/pytest) or Java (Mockito/JUnit)
3. **Generate mocks** - Create mock objects for external dependencies
4. **Write tests** - Generate executable test code with assertions
5. **Add documentation** - Include clear comments explaining mocks and test logic

## Step 1: Analyze the Code

Read the target code to identify:

- **External dependencies**: API clients, database connections, third-party libraries
- **I/O operations**: File reads/writes, network requests, system calls
- **Side effects**: Email sending, logging, state modifications
- **Testable units**: Functions, methods, or classes to test in isolation

Ask clarifying questions if:
- Multiple functions/classes exist (which to test?)
- Testing scope is unclear (unit vs integration?)
- Mock behavior needs specification (return values, exceptions?)

## Step 2: Select Framework

**Python**: Use `unittest.mock` with `pytest` or `unittest`
- Prefer `@patch` decorator for external calls
- Use `Mock()` objects for complex dependencies
- Apply `pytest.fixture` for reusable mocks

**Java**: Use Mockito with JUnit 5
- Use `@Mock` annotation for dependencies
- Apply `@ExtendWith(MockitoExtension.class)` to test class
- Use `when().thenReturn()` for stubbing

## Step 3: Generate Mocks

Identify what to mock:

**Always mock**:
- External API calls (HTTP requests, REST clients)
- Database connections and queries
- File system operations
- Network I/O
- Time/date functions
- Random number generators
- Environment variables

**Never mock** (unless explicitly requested):
- Internal business logic
- Pure functions
- Data structures
- Simple utilities

For common patterns, reference:
- **Python**: See [references/python_patterns.md](references/python_patterns.md)
- **Java**: See [references/java_patterns.md](references/java_patterns.md)

## Step 4: Write Tests

Generate test code that:

1. **Imports** - Include necessary testing and mocking libraries
2. **Setup** - Initialize mocks and test fixtures
3. **Execution** - Call the function/method under test
4. **Assertions** - Verify expected behavior and outputs
5. **Verification** - Confirm mocks were called correctly

**Test structure**:

```python
# Python example
from unittest.mock import patch, Mock
import pytest

@patch('module.external_dependency')
def test_function_name(mock_dependency):
    # Arrange: Setup mock behavior
    mock_dependency.return_value = expected_value

    # Act: Execute function under test
    result = function_under_test(input_data)

    # Assert: Verify results
    assert result == expected_output
    mock_dependency.assert_called_once_with(expected_args)
```

```java
// Java example
@ExtendWith(MockitoExtension.class)
class ServiceTest {
    @Mock
    private ExternalDependency dependency;

    @Test
    void testMethodName() {
        // Arrange: Setup mock behavior
        when(dependency.method()).thenReturn(expectedValue);

        // Act: Execute method under test
        Service service = new Service(dependency);
        String result = service.methodUnderTest();

        // Assert: Verify results
        assertEquals(expectedOutput, result);
        verify(dependency).method();
    }
}
```

**Include**:
- Multiple test cases for different scenarios (happy path, edge cases, errors)
- Descriptive test names that explain what is being tested
- Setup/teardown if needed for test isolation

## Step 5: Add Documentation

Include comments that explain:
- What external dependency is being mocked and why
- What behavior the mock simulates
- What the test verifies

Keep comments concise and focused on non-obvious aspects.

## Output Format

Provide:
1. **Complete test file** - Fully executable with all imports
2. **Test class/module** - Properly structured for the framework
3. **Multiple test methods** - Cover main scenarios
4. **Clear naming** - Descriptive test and variable names

**Do not**:
- Modify the original code under test
- Mock internal logic unless explicitly requested
- Generate incomplete or pseudo-code tests

## Example Usage

**User request**: "Generate unit tests for this Python function that calls an external API"

**Response**:
1. Read the function code
2. Identify the API call to mock
3. Generate pytest test file with `@patch` decorator
4. Include tests for success case, error handling, and edge cases
5. Add comments explaining the mock setup

## Framework-Specific Notes

**Python (pytest)**:
- Use `@pytest.fixture` for reusable mock setups
- Apply `@patch` as decorator or context manager
- Use `mock_open` for file operations
- Apply `@patch.dict` for environment variables

**Python (unittest)**:
- Use `unittest.TestCase` base class
- Apply `@patch` decorator or `patch()` context manager
- Use `setUp()` and `tearDown()` methods
- Call `self.assert*` methods

**Java (Mockito + JUnit 5)**:
- Use `@ExtendWith(MockitoExtension.class)` on test class
- Apply `@Mock` for dependencies
- Use `@BeforeEach` for setup, `@AfterEach` for teardown
- Apply `ArgumentCaptor` to verify complex arguments
- Use `MockedStatic` for static method mocking (Mockito 3.4+)

## Common Patterns

Reference files contain detailed examples for:

**Python** ([references/python_patterns.md](references/python_patterns.md)):
- External API calls
- Database operations
- File system operations
- Environment variables
- Time-dependent code
- Exception handling

**Java** ([references/java_patterns.md](references/java_patterns.md)):
- External API calls
- Database operations
- File system operations
- Void methods
- Exception handling
- Argument captors
- Static method mocking
- Constructor mocking
