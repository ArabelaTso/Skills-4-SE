# Design by Contract

## Overview

Design by Contract (DbC) is a software design approach that views software components as having formal, precise, and verifiable interface specifications.

## Core Concepts

### Contracts

A **contract** defines obligations and benefits between a software component and its clients:

- **Preconditions**: What the client must ensure before calling
- **Postconditions**: What the component guarantees after execution
- **Invariants**: Properties that always hold for the component

### Example

```python
class BankAccount:
    """
    Invariant: balance >= 0
    """
    def __init__(self):
        self.balance = 0

    def withdraw(self, amount):
        """
        Precondition: amount > 0 and amount <= self.balance
        Postcondition: self.balance == old(self.balance) - amount
        """
        assert amount > 0, "Amount must be positive"
        assert amount <= self.balance, "Insufficient funds"
        old_balance = self.balance
        self.balance -= amount
        assert self.balance == old_balance - amount
```

## Liskov Substitution Principle

Subtypes must preserve contracts:

**Rules**:
- Preconditions can be weakened (accept more)
- Postconditions can be strengthened (guarantee more)
- Invariants must be maintained

**Example**:
```python
class Account:
    def withdraw(self, amount):
        """Precondition: amount > 0"""
        pass

class SavingsAccount(Account):
    def withdraw(self, amount):
        """Precondition: amount >= 0"""  # Weaker - OK!
        pass
```

## Benefits

1. **Clear specifications**: Explicit expectations
2. **Early error detection**: Violations caught at boundaries
3. **Better testing**: Contracts guide test generation
4. **Documentation**: Self-documenting code
5. **Reliability**: Formal guarantees of correctness

## Best Practices

1. Document contracts explicitly in docstrings
2. Use assertions to check contracts at runtime
3. Verify contracts in tests
4. Follow LSP when creating subtypes
5. Keep contracts simple and verifiable

## References

- Meyer, B. (1992). "Applying Design by Contract"
- Liskov, B., & Wing, J. (1994). "A behavioral notion of subtyping"
