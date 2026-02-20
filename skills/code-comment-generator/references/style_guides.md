# Comment Style Guides

Language-specific comment conventions and best practices for Python and Java.

## Table of Contents

1. [Python Style Guide](#python-style-guide)
2. [Java Style Guide](#java-style-guide)
3. [General Best Practices](#general-best-practices)

---

## Python Style Guide

### Documentation Strings (Docstrings)

Python uses docstrings for documenting modules, classes, and functions. Follow **PEP 257** conventions.

#### Module Docstrings

```python
"""
User authentication and authorization module.

This module provides functions for user login, logout, password management,
and permission checking. Uses JWT tokens for stateless authentication.

Example:
    from auth import authenticate, check_permission

    user = authenticate(username, password)
    if check_permission(user, 'admin'):
        perform_admin_action()
"""
```

#### Function Docstrings - Google Style

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief one-line summary of what function does.

    Optional longer description that provides more detail about the
    function's behavior, algorithms used, or important considerations.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        Description of return value

    Raises:
        ValueError: When param2 is negative
        TypeError: When param1 is not a string

    Example:
        >>> function_name("test", 42)
        True

    Note:
        Any important notes or caveats about usage
    """
```

#### Function Docstrings - NumPy Style

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief one-line summary of what function does.

    Optional longer description that provides more detail.

    Parameters
    ----------
    param1 : str
        Description of first parameter
    param2 : int
        Description of second parameter

    Returns
    -------
    bool
        Description of return value

    Raises
    ------
    ValueError
        When param2 is negative

    Examples
    --------
    >>> function_name("test", 42)
    True

    Notes
    -----
    Any important notes or caveats
    """
```

#### Class Docstrings

```python
class ClassName:
    """
    Brief one-line summary of class purpose.

    Longer description of what the class does, its responsibility,
    and how it should be used. Mention any design patterns or
    important implementation details.

    Attributes:
        attribute1: Description of attribute1
        attribute2: Description of attribute2

    Example:
        >>> obj = ClassName(param)
        >>> obj.method()
        'result'

    Note:
        Any important usage notes or warnings
    """

    def __init__(self, param):
        """
        Initialize ClassName instance.

        Args:
            param: Description of initialization parameter
        """
```

### Inline Comments

#### Comment Style

```python
# Single-line comments use hash and space
# Multiple single-line comments for longer explanations
# Continue on new lines as needed

# Leave blank line before comment block for readability
def function():
    pass
```

#### When to Use Inline Comments

```python
# GOOD: Explain WHY, not WHAT
# Use binary search because list is pre-sorted and may contain millions of items
result = binary_search(items, target)

# BAD: Obvious comment
# Call binary search function
result = binary_search(items, target)

# GOOD: Explain business logic
# Free shipping for orders over $50 (marketing promotion until Q4 2024)
if order_total > 50:
    shipping_cost = 0

# GOOD: Explain workaround
# HACK: Add delay to work around rate limiting bug in API v1.2
# Remove when upgrading to v2.0 (scheduled for March 2024)
time.sleep(0.1)
```

### Type Hints

Type hints reduce the need for comments by making code self-documenting:

```python
# Without type hints - needs comment
def process_users(users, active):
    """Process users. active filters for active users only."""
    pass

# With type hints - self-documenting
def process_users(users: List[User], active: bool) -> List[User]:
    """Process user list, optionally filtering by active status."""
    pass
```

### TODOs and Annotations

```python
# TODO: Add email validation
# Format: TODO: Brief description of what needs to be done

# FIXME: This breaks when input is None
# Format: FIXME: Description of the bug

# XXX: Questionable code that works but needs review
# Format: XXX: Description of the concern

# HACK: Workaround for library bug #123
# Format: HACK: Description and reason for workaround

# NOTE: Important information about implementation
# Format: NOTE: The information

# OPTIMIZE: This could be faster with caching
# Format: OPTIMIZE: Suggestion for optimization
```

### PEP 8 Comment Guidelines

- Limit line length to 72 characters for comments
- Use complete sentences with proper capitalization
- Use two spaces after sentence-ending period (optional but recommended)
- Block comments generally consist of paragraphs built from complete sentences
- Each sentence in block comments should end with a period

---

## Java Style Guide

### Javadoc Comments

Java uses Javadoc comments for API documentation. Start with `/**` and include structured tags.

#### Class Javadoc

```java
/**
 * Brief one-line summary of class purpose.
 *
 * <p>Longer description of class behavior, responsibilities, and usage.
 * Use paragraph tags to separate paragraphs. Can include HTML formatting.
 *
 * <p>Additional paragraphs as needed to fully describe the class,
 * including design patterns, thread safety, or important implementation
 * details.
 *
 * <h3>Usage Example:</h3>
 * <pre>{@code
 * ClassName obj = new ClassName(param);
 * obj.method();
 * }</pre>
 *
 * @author Author Name
 * @version 1.0
 * @since 1.0
 * @see RelatedClass
 */
public class ClassName {
}
```

#### Method Javadoc

```java
/**
 * Brief one-line summary of what method does.
 *
 * <p>Optional longer description providing more detail about behavior,
 * algorithms, or important considerations.
 *
 * @param param1 description of first parameter
 * @param param2 description of second parameter
 * @return description of return value
 * @throws IllegalArgumentException if param1 is null
 * @throws IOException if file cannot be read
 * @see #relatedMethod(String)
 * @since 1.5
 */
public String methodName(String param1, int param2)
        throws IllegalArgumentException, IOException {
    return "";
}
```

#### Field Javadoc

```java
/**
 * Brief description of field purpose.
 *
 * <p>Longer explanation if needed, including valid values,
 * constraints, or important usage notes.
 */
private String fieldName;

/** Brief description for simple fields (one-liner acceptable). */
private static final int MAX_SIZE = 100;
```

### Javadoc Tags

Common Javadoc tags and their usage:

```java
/**
 * @param paramName Description of parameter
 * @return Description of return value
 * @throws ExceptionType When and why this exception is thrown
 * @see ClassName For related information
 * @see #methodName(Type) For related method
 * @see <a href="URL">External reference</a>
 * @since version Version when this was added
 * @deprecated Explanation and alternative to use
 * @author Author name (usually for classes)
 * @version Version number (usually for classes)
 */
```

### Inline Comments

```java
// Single-line comments use double slash and space
// Multiple lines continue on new lines

/*
 * Multi-line comments use this format
 * with asterisks on each line for readability
 */

/* Single-line multi-line comment also valid */
```

### When to Comment

```java
// GOOD: Explain WHY
// Use HashMap for O(1) lookup performance - critical for this hot path
Map<String, User> userCache = new HashMap<>();

// BAD: State the obvious
// Create a new HashMap
Map<String, User> userCache = new HashMap<>();

// GOOD: Explain business logic
// Orders over $50 qualify for free shipping (marketing policy Q4 2024)
if (orderTotal > 50.00) {
    shippingCost = 0.0;
}

// GOOD: Document workarounds
// HACK: Sleep to avoid connection pool bug in driver v1.5
// Remove when upgrading to v2.0 (scheduled March 2024)
Thread.sleep(100);
```

### TODOs and Annotations

```java
// TODO: Add input validation
// Format: TODO: Description of what needs doing

// FIXME: NullPointerException when user is null
// Format: FIXME: Description of bug

// HACK: Workaround for library bug #456
// Format: HACK: Description and reason

// NOTE: This must be called before init()
// Format: NOTE: Important information

// @deprecated Use {@link #newMethod()} instead. Scheduled for removal in v3.0.
@Deprecated
public void oldMethod() {
}
```

### Javadoc Best Practices

**1. Use HTML formatting:**

```java
/**
 * Process items in the following order:
 * <ol>
 *   <li>Validate input
 *   <li>Transform data
 *   <li>Save to database
 * </ol>
 *
 * <p>Supported formats:
 * <ul>
 *   <li>JSON
 *   <li>XML
 *   <li>CSV
 * </ul>
 */
```

**2. Link to related code:**

```java
/**
 * Processes user input.
 *
 * @see UserValidator#validate(String)
 * @see #processInternal(User)
 * @see <a href="https://docs.example.com/api">API Documentation</a>
 */
```

**3. Include code examples:**

```java
/**
 * Calculates discount based on quantity.
 *
 * <p>Example usage:
 * <pre>{@code
 * double price = 100.0;
 * int quantity = 10;
 * double discount = calculator.calculateDiscount(price, quantity);
 * // Returns 90.0 (10% discount for bulk order)
 * }</pre>
 */
```

**4. Document thread safety:**

```java
/**
 * Thread-safe cache implementation.
 *
 * <p>All methods are synchronized and safe for concurrent access
 * from multiple threads. However, iterating over entries requires
 * external synchronization.
 *
 * @see java.util.concurrent.ConcurrentHashMap for lock-free alternative
 */
```

---

## General Best Practices

### 1. Write Comments for the Reader

Comments should help future maintainers understand the code:

```python
# POOR: Cryptic abbreviation
# Calc ttl amt w/ disc
total = calculate_total(items, discount)

# GOOD: Clear explanation
# Calculate total price including 15% volume discount for bulk orders
total = calculate_total(items, discount=0.15)
```

### 2. Keep Comments Updated

Outdated comments are worse than no comments:

```python
# BAD: Comment doesn't match code
# Return user age in years
return user.birth_date  # Actually returns birth_date, not age!

# GOOD: Accurate comment
# Return user's birth date for age calculation
return user.birth_date
```

### 3. Use Consistent Terminology

Match the language of your domain:

```python
# If your domain uses "customer", don't say "user" in comments
# INCONSISTENT:
def get_customer(customer_id):
    """Retrieve user by ID."""  # Says "user"

# CONSISTENT:
def get_customer(customer_id):
    """Retrieve customer by ID."""  # Says "customer"
```

### 4. Don't Comment Bad Code - Rewrite It

```java
// BAD: Commenting messy code
// This is messy but necessary because of edge cases
if ((x > 0 && y < 10 && (z == 5 || z == 7) && !flag) ||
    (x < 0 && special)) {
    doSomething();
}

// GOOD: Refactor instead
private boolean shouldDoSomething(int x, int y, int z,
                                 boolean flag, boolean special) {
    boolean normalCase = x > 0 && y < 10 &&
                        (z == 5 || z == 7) && !flag;
    boolean specialCase = x < 0 && special;
    return normalCase || specialCase;
}

if (shouldDoSomething(x, y, z, flag, special)) {
    doSomething();
}
```

### 5. Avoid Noise Comments

```python
# BAD: Adds no value
i = 0  # Set i to zero
i += 1  # Increment i
return True  # Return true

# GOOD: Only comment non-obvious code
# Reset cursor to beginning of file
file.seek(0)
```

### 6. Use Comments to Mark Sections

For large files, section comments help navigation:

```python
# ============================================================================
# Database Operations
# ============================================================================

def save_user(user):
    pass

def delete_user(user_id):
    pass


# ============================================================================
# Email Operations
# ============================================================================

def send_email(to, subject, body):
    pass
```

```java
// ========================================================================
// Constructors
// ========================================================================

public ClassName() {
}


// ========================================================================
// Public Methods
// ========================================================================

public void method() {
}
```

### 7. Document Complex Regular Expressions

```python
# Email validation regex (RFC 5322 simplified):
# ^[a-zA-Z0-9._%+-]+  - Local part (before @)
# @                   - Literal @ symbol
# [a-zA-Z0-9.-]+      - Domain name
# \.                  - Literal dot
# [a-zA-Z]{2,}$       - Top-level domain (min 2 chars)
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
```

### 8. Explain Magic Numbers

```python
# BAD: Unexplained constant
if temperature > 273.15:
    status = "above_freezing"

# GOOD: Explained constant
WATER_FREEZING_POINT_KELVIN = 273.15
if temperature > WATER_FREEZING_POINT_KELVIN:
    status = "above_freezing"
```

### 9. Document Assumptions

```python
def calculate_tax(amount):
    """
    Calculate sales tax on amount.

    Assumes:
    - Amount is in USD
    - Tax rate is for California (7.25%)
    - No special tax exemptions apply

    Args:
        amount: Purchase amount in dollars

    Returns:
        Tax amount in dollars
    """
    CA_TAX_RATE = 0.0725
    return amount * CA_TAX_RATE
```

### 10. Use Diagrams When Helpful

For complex flows, consider ASCII art:

```python
"""
Authentication Flow:
┌──────┐     ┌──────┐     ┌────────┐
│Client│────▶│Server│────▶│Database│
└──────┘     └──────┘     └────────┘
   │            │              │
   │  username  │              │
   │  password  │              │
   │───────────▶│              │
   │            │   verify     │
   │            │─────────────▶│
   │            │              │
   │            │◀─────────────│
   │   token    │              │
   │◀───────────│              │
"""
```

### 11. When in Doubt, Err on the Side of Clarity

If you're unsure whether to add a comment, consider:
- Will this be obvious to someone seeing this code for the first time?
- Will I understand this in 6 months?
- Does this follow a common pattern that needs no explanation?

When in doubt, add the comment. It's easier to remove unnecessary comments during review than to debug unclear code later.
