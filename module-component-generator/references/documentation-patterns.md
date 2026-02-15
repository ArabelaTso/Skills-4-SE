# Documentation Generation Patterns

## Python Documentation

### Module-Level Documentation

```python
"""
User Service Module
===================

This module provides user management functionality including creation,
retrieval, update, and deletion of user records.

Classes
-------
User
    Domain model representing a user
UserRepository
    Data access layer for user persistence
UserService
    Business logic layer for user operations

Exceptions
----------
UserServiceError
    Base exception for user service errors
UserAlreadyExistsException
    Raised when attempting to create duplicate user
UserNotFoundException
    Raised when user is not found

Examples
--------
Basic usage:

>>> repository = UserRepository()
>>> service = UserService(repository)
>>> user = service.create_user("john@example.com", "John Doe")
>>> print(user.name)
John Doe

See Also
--------
user_service.models : User domain models
user_service.repository : Data access layer
"""
```

### Class Documentation

```python
class UserService:
    """
    Service layer for user operations.

    This class provides high-level business logic for managing users,
    including validation, error handling, and coordination with the
    repository layer.

    Parameters
    ----------
    repository : UserRepository
        Repository instance for data persistence

    Attributes
    ----------
    repository : UserRepository
        The repository used for data access

    Examples
    --------
    Create and manage users:

    >>> repo = UserRepository()
    >>> service = UserService(repo)
    >>> user = service.create_user("jane@example.com", "Jane Smith")
    >>> updated = service.update_user(user.id, name="Jane Doe")

    Notes
    -----
    All methods validate inputs and raise appropriate exceptions
    for error conditions. The service ensures business rules are
    enforced before delegating to the repository.
    """
```

### Method Documentation

```python
def create_user(self, email: str, name: str) -> User:
    """
    Create a new user.

    Parameters
    ----------
    email : str
        User's email address (must be unique)
    name : str
        User's full name

    Returns
    -------
    User
        The created user instance with generated ID and timestamp

    Raises
    ------
    UserAlreadyExistsException
        If a user with the given email already exists
    ValueError
        If email format is invalid

    Examples
    --------
    >>> service = UserService(UserRepository())
    >>> user = service.create_user("john@example.com", "John Doe")
    >>> print(user.id)
    '550e8400-e29b-41d4-a716-446655440000'

    Notes
    -----
    The user ID is automatically generated using UUID4.
    The created_at timestamp is set to the current time.
    """
```

## Java Documentation

### Package Documentation (package-info.java)

```java
/**
 * User Service Module
 * <p>
 * This package provides user management functionality including creation,
 * retrieval, update, and deletion of user records.
 *
 * <h2>Main Components</h2>
 * <ul>
 *   <li>{@link com.example.user.model.User} - Domain model representing a user</li>
 *   <li>{@link com.example.user.repository.UserRepository} - Data access layer</li>
 *   <li>{@link com.example.user.service.UserService} - Business logic layer</li>
 * </ul>
 *
 * <h2>Exception Hierarchy</h2>
 * <ul>
 *   <li>{@link com.example.user.exception.UserServiceException} - Base exception</li>
 *   <li>{@link com.example.user.exception.UserAlreadyExistsException} - Duplicate user</li>
 *   <li>{@link com.example.user.exception.UserNotFoundException} - User not found</li>
 * </ul>
 *
 * <h2>Usage Example</h2>
 * <pre>{@code
 * UserRepository repository = new UserRepository();
 * UserService service = new UserService(repository);
 * User user = service.createUser("john@example.com", "John Doe");
 * System.out.println(user.getName());
 * }</pre>
 *
 * @since 1.0
 * @version 1.0
 */
package com.example.user;
```

### Class Documentation

```java
/**
 * Service layer for user operations.
 * <p>
 * This class provides high-level business logic for managing users,
 * including validation, error handling, and coordination with the
 * repository layer.
 *
 * <h2>Thread Safety</h2>
 * This class is thread-safe when used with a thread-safe repository
 * implementation.
 *
 * <h2>Usage Example</h2>
 * <pre>{@code
 * UserRepository repo = new UserRepository();
 * UserService service = new UserService(repo);
 * User user = service.createUser("jane@example.com", "Jane Smith");
 * User updated = service.updateUser(user.getId(), "Jane Doe");
 * }</pre>
 *
 * @author Development Team
 * @version 1.0
 * @since 1.0
 * @see UserRepository
 * @see User
 */
public class UserService {
```

### Method Documentation

```java
/**
 * Create a new user.
 * <p>
 * This method validates the email format, checks for existing users
 * with the same email, and creates a new user with a generated ID
 * and current timestamp.
 *
 * @param email User's email address (must be unique and valid format)
 * @param name User's full name (cannot be null or empty)
 * @return The created user instance with generated ID and timestamp
 * @throws NullPointerException if email or name is null
 * @throws UserAlreadyExistsException if a user with the email already exists
 * @throws IllegalArgumentException if email format is invalid
 *
 * @see #getUser(String)
 * @see #updateUser(String, String)
 *
 * @since 1.0
 */
public User createUser(String email, String name) {
```

## Documentation Structure Templates

### README Template

```markdown
# [Module Name]

Brief description of what this module does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```[language]
[installation instructions]
```

## Quick Start

```[language]
[basic usage example]
```

## API Reference

### [Class/Module Name]

Description of the class/module.

#### Methods

##### `method_name(param1, param2)`

Description of what the method does.

**Parameters:**
- `param1` (type): Description
- `param2` (type): Description

**Returns:**
- type: Description

**Raises:**
- ExceptionType: When this happens

**Example:**
```[language]
[usage example]
```

## Architecture

[Diagram or description of module architecture]

## Design Decisions

- Decision 1: Rationale
- Decision 2: Rationale

## Testing

```[language]
[how to run tests]
```

## Contributing

[Contribution guidelines]

## License

[License information]
```

### API Documentation Template

```markdown
# [Module] API Documentation

## Overview

[Brief description of the module's purpose and capabilities]

## Core Concepts

### [Concept 1]
[Explanation]

### [Concept 2]
[Explanation]

## Classes

### [ClassName]

[Class description]

**Constructor:**
```[language]
[constructor signature]
```

**Methods:**

#### `methodName(params)`

[Method description]

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| param1 | type | description |
| param2 | type | description |

**Returns:**
| Type | Description |
|------|-------------|
| type | description |

**Exceptions:**
| Exception | Condition |
|-----------|-----------|
| ExceptionType | When this happens |

**Example:**
```[language]
[usage example]
```

## Usage Patterns

### [Pattern Name]

[Description and example]

## Error Handling

[How errors are handled in this module]

## Best Practices

- Practice 1
- Practice 2
- Practice 3

## Examples

### [Example Scenario]

[Complete working example]
```

## Documentation Best Practices

### Python
- Use NumPy or Google docstring format consistently
- Include type hints in signatures
- Provide examples in docstrings
- Document exceptions that can be raised
- Use Sphinx for generating HTML documentation

### Java
- Use standard JavaDoc tags (@param, @return, @throws)
- Include @since and @version tags
- Use {@link} for cross-references
- Provide code examples in {@code} blocks
- Use Maven or Gradle JavaDoc plugin

### General
- Keep documentation close to code
- Update docs when code changes
- Include architecture diagrams for complex modules
- Document design decisions and trade-offs
- Provide both reference and tutorial documentation
