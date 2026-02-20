# Design by Contract in Python

## Overview

Design by Contract (DbC) is a software development approach where software components specify formal contracts consisting of preconditions, postconditions, and invariants.

## Contract Types

### Preconditions (Requires)

Conditions that must be true before a function executes:

```python
def sqrt(x: float) -> float:
    """
    Calculate square root.

    Requires:
        - x >= 0

    Ensures:
        - result * result ≈ x
    """
    assert x >= 0, "Input must be non-negative"
    return x ** 0.5
```

### Postconditions (Ensures)

Conditions guaranteed to be true after function execution:

```python
def deposit(account: Account, amount: float) -> None:
    """
    Deposit money into account.

    Requires:
        - amount > 0

    Ensures:
        - account.balance == old(account.balance) + amount
    """
    old_balance = account.balance
    account.balance += amount
    assert account.balance == old_balance + amount
```

### Invariants

Conditions that must always hold true for a class:

```python
class BankAccount:
    """
    Bank account with balance.

    Invariant:
        - self.balance >= 0  # Never negative
    """

    def __init__(self, initial_balance: float):
        assert initial_balance >= 0
        self.balance = initial_balance
        self._check_invariant()

    def _check_invariant(self):
        assert self.balance >= 0, "Balance cannot be negative"

    def withdraw(self, amount: float):
        """
        Requires: amount > 0 and amount <= self.balance
        Ensures: self.balance == old(self.balance) - amount
        """
        assert amount > 0
        assert amount <= self.balance

        self.balance -= amount
        self._check_invariant()
```

## Implementation Patterns

### Decorator-Based Contracts

```python
from functools import wraps
from typing import Callable, Any

def requires(condition: Callable[[Any], bool], message: str = "Precondition failed"):
    """Precondition decorator."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not condition(*args, **kwargs):
                raise AssertionError(f"{message} in {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def ensures(condition: Callable[[Any, Any], bool], message: str = "Postcondition failed"):
    """Postcondition decorator."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not condition(result, *args, **kwargs):
                raise AssertionError(f"{message} in {func.__name__}")
            return result
        return wrapper
    return decorator

# Usage
@requires(lambda x: x >= 0, "Input must be non-negative")
@ensures(lambda result, x: result * result >= x - 0.01 and result * result <= x + 0.01)
def sqrt(x: float) -> float:
    return x ** 0.5
```

### Docstring-Based Contracts

```python
def divide(a: float, b: float) -> float:
    """
    Divide two numbers.

    Precondition:
        - b != 0

    Postcondition:
        - result * b ≈ a

    Args:
        a: Numerator
        b: Denominator (must not be zero)

    Returns:
        Result of a / b

    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Division by zero")

    result = a / b

    # Verify postcondition (in debug mode)
    if __debug__:
        assert abs(result * b - a) < 1e-10

    return result
```

## Type Annotations as Contracts

### Function Signatures

```python
from typing import List, Optional, Union

def process_items(items: List[int], threshold: int = 0) -> List[int]:
    """
    Filter items above threshold.

    Requires:
        - All items are integers
        - threshold is an integer

    Ensures:
        - All returned items > threshold
        - Returned list length <= input list length
    """
    result = [item for item in items if item > threshold]

    # Postcondition check
    assert all(item > threshold for item in result)
    assert len(result) <= len(items)

    return result
```

### Optional and Union Types

```python
def find_user(user_id: int) -> Optional[User]:
    """
    Find user by ID.

    Requires:
        - user_id > 0

    Ensures:
        - result is None or result.id == user_id
    """
    assert user_id > 0
    user = database.get_user(user_id)

    assert user is None or user.id == user_id
    return user
```

## Common Contract Patterns

### Range Validation

```python
def set_age(person: Person, age: int) -> None:
    """
    Requires: 0 <= age <= 150
    Ensures: person.age == age
    """
    assert 0 <= age <= 150, "Age must be between 0 and 150"
    person.age = age
```

### Collection Constraints

```python
def process_batch(items: List[Item]) -> None:
    """
    Requires:
        - len(items) > 0
        - len(items) <= 1000
    """
    assert len(items) > 0, "Batch cannot be empty"
    assert len(items) <= 1000, "Batch too large"
    # Process items
```

### State Validation

```python
class Order:
    """
    Invariant:
        - self.status in ['pending', 'processing', 'shipped', 'delivered']
        - self.items is not empty when status != 'pending'
    """

    def ship(self):
        """
        Requires: self.status == 'processing'
        Ensures: self.status == 'shipped'
        """
        assert self.status == 'processing'
        self.status = 'shipped'
        self._check_invariant()
```

## Tools and Libraries

### icontract

```python
from icontract import require, ensure, invariant

@require(lambda x: x > 0)
@ensure(lambda result: result > 0)
def increment(x: int) -> int:
    return x + 1

@invariant(lambda self: self.balance >= 0)
class Account:
    def __init__(self, balance: float):
        self.balance = balance
```

### deal

```python
import deal

@deal.pre(lambda x: x > 0)
@deal.post(lambda result: result > 0)
def increment(x: int) -> int:
    return x + 1
```

## Best Practices

### 1. Write Contracts First

Define contracts before implementation:

```python
def sort_list(items: List[int]) -> List[int]:
    """
    Sort list in ascending order.

    Requires:
        - items is a list

    Ensures:
        - len(result) == len(items)
        - result is sorted (result[i] <= result[i+1])
        - result contains same elements as items
    """
    # Implementation
```

### 2. Keep Contracts Simple

```python
# ✅ Good - Simple, clear
def withdraw(amount: float):
    """Requires: amount > 0 and amount <= balance"""
    assert amount > 0 and amount <= self.balance

# ❌ Bad - Too complex
def withdraw(amount: float):
    """Requires: complex formula involving multiple conditions..."""
```

### 3. Use Assertions for Internal Contracts

```python
def _internal_helper(x: int) -> int:
    """Internal function with strict contracts."""
    assert x >= 0, "Internal contract: x must be non-negative"
    # Implementation
```

### 4. Raise Exceptions for Public Contracts

```python
def public_api(x: int) -> int:
    """Public API with validated input."""
    if x < 0:
        raise ValueError("x must be non-negative")
    # Implementation
```

### 5. Document Side Effects

```python
def update_database(user: User) -> None:
    """
    Update user in database.

    Requires:
        - user.id is set

    Ensures:
        - Database contains updated user

    Side effects:
        - Modifies database
        - May raise DatabaseError
    """
```

## Verification Checklist

- [ ] All public functions have documented preconditions
- [ ] All public functions have documented postconditions
- [ ] Classes with state have documented invariants
- [ ] Contracts are verified with assertions (debug mode)
- [ ] Type annotations match contract specifications
- [ ] Edge cases are covered by contracts
- [ ] Contracts don't have side effects
- [ ] Contracts are simple and understandable
