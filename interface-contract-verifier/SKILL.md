---
name: interface-contract-verifier
description: Verify that interface and class contracts (preconditions, postconditions, invariants) are preserved across program versions. Use when validating refactorings, checking API compatibility, verifying design-by-contract implementations, or ensuring behavioral contracts remain intact after code changes. Automatically detects contract violations, identifies affected methods and classes, and provides actionable guidance for resolving violations while maintaining program correctness.
---

# Interface Contract Verifier

## Overview

Verify that formal or structured contracts (preconditions, postconditions, invariants) defined in interfaces and classes are preserved when updating to a new program version.

## Core Workflow

### 1. Extract Contracts

Extract contracts from both versions:

```bash
python scripts/contract_extractor.py --program old_version --output old_contracts.json
python scripts/contract_extractor.py --program new_version --output new_contracts.json
```

### 2. Verify Contracts

Compare and verify contract preservation:

```bash
python scripts/contract_verifier.py --old old_contracts.json --new new_contracts.json --output report.json
```

### 3. Review Violations

Examine violations: weakened preconditions, strengthened postconditions, broken invariants.

## Contract Types

### Preconditions
Requirements before method execution:
```python
def withdraw(amount):
    """Precondition: amount > 0 and amount <= balance"""
```

### Postconditions
Guarantees after method execution:
```python
def deposit(amount):
    """Postcondition: balance == old(balance) + amount"""
```

### Invariants
Properties always true for a class:
```python
class BankAccount:
    """Invariant: balance >= 0"""
```

## Verification Rules

**Liskov Substitution Principle**:
- Preconditions can be weakened (accept more)
- Postconditions can be strengthened (guarantee more)
- Invariants must be maintained

## Violation Types

### Strengthened Precondition (Error)
New version rejects previously valid inputs.

### Weakened Postcondition (Error)
New version guarantees less.

### Broken Invariant (Critical)
Class invariant no longer holds.

## Resolution Guidance

### Fix Strengthened Precondition
Relax precondition or update callers.

### Fix Weakened Postcondition
Strengthen implementation to meet original guarantee.

### Fix Broken Invariant
Add checks to maintain invariant in all methods.

## Resources

- **[references/design_by_contract.md](references/design_by_contract.md)**: Design by Contract principles
- **scripts/contract_extractor.py**: Extract contracts from code
- **scripts/contract_verifier.py**: Verify contract preservation
