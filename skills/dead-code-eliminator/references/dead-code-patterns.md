# Dead Code Patterns Reference

This document catalogs common patterns of dead code and how to identify them.

## Unused Functions and Methods

### Pattern 1: Orphaned Helper Functions

**Description:** Utility functions that were written but never actually used.

**Indicators:**
- Function defined but no calls anywhere in codebase
- Often in utility modules or helper files
- May have been written "just in case" but never needed

**Example:**
```python
# utils.py
def format_date(date):
    """Format date to ISO string."""
    return date.isoformat()  # Never called anywhere

def parse_date(date_str):
    """Parse ISO date string."""  # This one IS used
    return datetime.fromisoformat(date_str)
```

**Detection:** AST analysis showing function definition but no call sites.

### Pattern 2: Refactoring Leftovers

**Description:** Old functions that were replaced but not removed.

**Indicators:**
- Function name suggests old implementation (e.g., `process_data_old`, `legacy_handler`)
- Similar function with newer name exists
- Comments like "deprecated" or "use X instead"

**Example:**
```python
def calculate_total_v1(items):
    # Old implementation - DO NOT USE
    return sum(item.price for item in items)

def calculate_total(items, tax_rate=0.1):
    # New implementation with tax
    return sum(item.price for item in items) * (1 + tax_rate)
```

### Pattern 3: Test Helpers Never Used

**Description:** Test utility functions that aren't called by any tests.

**Indicators:**
- Defined in test files or conftest.py
- Not used by any test functions
- May be fixtures that were never referenced

**Example:**
```python
# test_utils.py
def create_sample_user():  # Never used
    return User(name="Test", email="test@example.com")

def create_sample_order():  # This one IS used in tests
    return Order(user_id=1, total=100)
```

## Unused Imports

### Pattern 4: Removed Usage

**Description:** Import was needed but code using it was removed.

**Example:**
```python
import os
import sys
from datetime import datetime  # Used
from pathlib import Path  # Not used anymore

def get_timestamp():
    return datetime.now()

# Previously had code using Path but it was removed
```

### Pattern 5: Overly Broad Imports

**Description:** Importing entire module when only one function is needed, or vice versa.

**Example:**
```python
import json
import re  # Never used
from typing import List, Dict, Optional, Tuple  # Only List is used

def parse_data(data: List[str]):
    return json.loads(data[0])
```

### Pattern 6: Duplicate Imports

**Description:** Same module imported multiple times or in different forms.

**Example:**
```python
import os
from os import path  # Redundant - can use os.path
from os.path import join  # Actually used

def get_file_path(dir, filename):
    return join(dir, filename)
```

## Unreachable Code

### Pattern 7: Code After Return

**Description:** Code that appears after a return statement in the same block.

**Example:**
```python
def process(data):
    if not data:
        return None
        print("Data is empty")  # Unreachable

    return data.upper()
```

### Pattern 8: Impossible Conditions

**Description:** Conditions that can never be true due to previous logic.

**Example:**
```python
def validate_age(age):
    if age < 0:
        return False

    if age >= 0 and age < 18:
        return "minor"

    if age < 0:  # Impossible - already checked above
        return "invalid"

    return "adult"
```

### Pattern 9: Always-False Conditions

**Description:** Conditions that are always False due to constants or previous checks.

**Example:**
```python
def check_value(x):
    if x > 10:
        return "high"
    elif x > 5:
        return "medium"
    elif x > 10:  # Impossible - already handled above
        return "very high"
    else:
        return "low"
```

### Pattern 10: Code After Break/Continue/Raise

**Description:** Statements after control flow statements in loops.

**Example:**
```python
def find_item(items, target):
    for item in items:
        if item.id == target:
            return item
            print(f"Found: {item}")  # Unreachable

    return None
```

## Redundant Code

### Pattern 11: Redundant Conditions

**Description:** Conditions that are always true or already checked.

**Example:**
```python
def process_user(user):
    if user is not None:
        if user:  # Redundant - already checked not None
            return user.name
    return "Unknown"
```

**Better:**
```python
def process_user(user):
    if user:
        return user.name
    return "Unknown"
```

### Pattern 12: Unnecessary Else After Return

**Description:** Else block that's unnecessary because previous block always returns.

**Example:**
```python
def get_status(value):
    if value > 0:
        return "positive"
    else:  # Unnecessary else
        return "non-positive"
```

**Better:**
```python
def get_status(value):
    if value > 0:
        return "positive"
    return "non-positive"
```

### Pattern 13: Redundant Boolean Operations

**Description:** Unnecessary boolean comparisons or conversions.

**Example:**
```python
def is_valid(data):
    if data is not None:
        return True
    else:
        return False

# Better:
def is_valid(data):
    return data is not None
```

### Pattern 14: Duplicate Logic

**Description:** Same logic repeated in multiple places.

**Example:**
```python
def process_a(data):
    if not data:
        return []
    result = []
    for item in data:
        if item.active:
            result.append(item.name)
    return result

def process_b(data):
    if not data:
        return []
    result = []
    for item in data:
        if item.active:  # Duplicate logic
            result.append(item.name)
    return result
```

## Unused Variables

### Pattern 15: Assigned But Never Read

**Description:** Variables assigned but never used afterwards.

**Example:**
```python
def calculate(a, b):
    total = a + b  # Never used
    result = a * b
    return result
```

### Pattern 16: Loop Variables Never Used

**Description:** Loop iteration variables that aren't used in the loop body.

**Example:**
```python
# Bad
for i in range(10):
    print("Hello")  # i is never used

# Better - use underscore to indicate intentionally unused
for _ in range(10):
    print("Hello")
```

### Pattern 17: Function Parameters Never Used

**Description:** Parameters declared but not used in function body.

**Example:**
```python
def greet(name, title):  # title is never used
    return f"Hello, {name}!"
```

## Detection Strategies

### Static Analysis

**AST-based detection:**
- Parse Python code into Abstract Syntax Tree
- Track all definitions (functions, imports, variables)
- Track all usages (calls, references)
- Report definitions without usages

**Tools:**
- `vulture` - Find unused code in Python
- `autoflake` - Remove unused imports and variables
- `pylint` - Detects various forms of dead code
- Custom AST analysis scripts

### Dynamic Analysis

**Coverage-based detection:**
- Run test suite with coverage enabled
- Identify lines never executed
- May indicate dead code (or missing tests)

**Tools:**
- `coverage.py` - Measure code coverage
- `pytest-cov` - Coverage plugin for pytest

### Manual Review

**Code review indicators:**
- Functions with no callers
- Imports highlighted as unused by IDE
- Comments like "TODO: remove this"
- Version control history showing code not modified in years
- Duplicate or very similar functions

## Special Cases and Exceptions

### When "Dead" Code Isn't Really Dead

**1. Public API Functions**
- May be unused internally but called by external users
- Keep if part of documented public API

**2. Plugin/Hook Functions**
- Called dynamically via strings or introspection
- Examples: Django signal handlers, pytest fixtures

**3. Decorators and Metaclasses**
- May be used but hard to detect statically
- Check for `@` usage or metaclass assignments

**4. Template/Example Code**
- Intentionally unused examples in documentation
- Should be in docs directory, not main codebase

**5. Future/Planned Features**
- Code written in advance for planned features
- Should have clear comments and tickets

**6. CLI Entry Points**
- Functions called from command line or config
- Check setup.py entry_points

**7. Dynamically Called Functions**
```python
# May appear unused but called via getattr
handlers = {
    'create': create_handler,
    'update': update_handler,
    'delete': delete_handler,
}

action = request.get('action')
handler = handlers.get(action)
handler(data)  # Dynamic dispatch
```

## Prioritization

Not all dead code is equally important to remove:

**High Priority:**
- Unused imports (easy to remove, reduce namespace pollution)
- Unreachable code (clearly bugs or confusion)
- Duplicate logic (maintenance burden)

**Medium Priority:**
- Unused utility functions (clutter but low risk)
- Redundant conditions (minor performance impact)
- Unused variables (code smell but harmless)

**Low Priority:**
- Private helper functions never called (may be OK)
- Code in deprecated modules (being phased out anyway)
- Example/template code in proper location
