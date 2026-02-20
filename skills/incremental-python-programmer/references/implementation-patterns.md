# Python Implementation Patterns

## Code Addition Patterns

### Adding New Functions

**Pattern: Simple function addition**
```python
# Location: Identify appropriate module based on functionality
# Placement: After related functions, before main block

def new_feature_function(param1: str, param2: int) -> dict:
    """
    Brief description of what the function does.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input is provided
    """
    # Implementation
    result = {}
    # ... logic here
    return result
```

**Pattern: Method addition to existing class**
```python
# Location: Inside existing class definition
# Placement: Group with related methods

class ExistingClass:
    # ... existing methods ...

    def new_method(self, param: str) -> bool:
        """Method description."""
        # Implementation
        return True
```

### Adding New Classes

**Pattern: New class in existing module**
```python
# Location: After imports, before or after related classes
# Follow existing class organization pattern

class NewFeatureClass:
    """
    Class description.

    Attributes:
        attr1: Description
        attr2: Description
    """

    def __init__(self, param1: str, param2: int):
        """Initialize the class."""
        self.attr1 = param1
        self.attr2 = param2

    def method1(self) -> str:
        """Method description."""
        return self.attr1
```

### Adding New Modules

**Pattern: New module structure**
```python
# File: new_module.py
"""
Module description.

This module provides functionality for [feature description].
"""

from typing import List, Dict, Optional
import existing_module

# Constants
DEFAULT_VALUE = "default"

# Classes
class NewClass:
    """Class description."""
    pass

# Functions
def helper_function() -> None:
    """Helper function description."""
    pass

# Main functionality
def main_feature_function() -> None:
    """Main feature description."""
    pass
```

## Code Modification Patterns

### Extending Existing Functions

**Pattern: Add parameter with default value**
```python
# Before
def existing_function(param1: str) -> str:
    return param1.upper()

# After
def existing_function(param1: str, new_param: bool = False) -> str:
    result = param1.upper()
    if new_param:
        result = result + "_MODIFIED"
    return result
```

**Pattern: Add functionality to existing logic**
```python
# Before
def process_data(data: list) -> list:
    return [x * 2 for x in data]

# After
def process_data(data: list, apply_filter: bool = False) -> list:
    result = [x * 2 for x in data]
    if apply_filter:
        result = [x for x in result if x > 10]
    return result
```

### Modifying Class Behavior

**Pattern: Add attribute and update methods**
```python
# Before
class DataProcessor:
    def __init__(self, data: list):
        self.data = data

    def process(self) -> list:
        return [x * 2 for x in self.data]

# After
class DataProcessor:
    def __init__(self, data: list, multiplier: int = 2):
        self.data = data
        self.multiplier = multiplier  # New attribute

    def process(self) -> list:
        return [x * self.multiplier for x in self.data]  # Modified logic
```

## Dependency Management

### Import Patterns

**Standard library imports**
```python
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Union
```

**Third-party imports**
```python
import numpy as np
import pandas as pd
import requests
```

**Local imports**
```python
from .module import function
from ..parent_module import Class
import project.module as mod
```

### Adding Dependencies

**Check if dependency exists:**
1. Look in requirements.txt or pyproject.toml
2. Check existing imports in similar modules
3. Add to requirements if new

**Import placement:**
1. Standard library imports first
2. Third-party imports second
3. Local imports last
4. Alphabetical within each group

## Code Placement Strategies

### Function Placement

**In modules:**
1. After imports and constants
2. Helper functions before main functions
3. Related functions grouped together
4. Public functions before private (_prefixed)

**In classes:**
1. `__init__` first
2. Public methods next
3. Private methods last
4. Group related methods together

### Class Placement

**In modules:**
1. After imports and constants
2. Base classes before derived classes
3. Related classes grouped together
4. Exception classes at the top

### Module Organization

**Standard structure:**
```
module.py
├── Docstring
├── Imports
├── Constants
├── Exception classes
├── Helper classes
├── Main classes
├── Helper functions
├── Main functions
└── if __name__ == "__main__": block
```

## Pattern Matching

### Identifying Similar Code

**Look for:**
1. Similar function signatures
2. Similar class structures
3. Similar import patterns
4. Similar error handling
5. Similar data processing logic

**Use existing patterns for:**
1. Naming conventions
2. Documentation style
3. Error handling approach
4. Return value patterns
5. Type hints usage

### Adapting Existing Patterns

**Steps:**
1. Find similar existing implementation
2. Copy structure and style
3. Adapt logic for new feature
4. Maintain consistency with codebase
5. Follow existing conventions

**Example:**
```python
# Existing pattern
def get_user_by_id(user_id: int) -> Optional[User]:
    """Get user by ID."""
    try:
        return database.query(User).filter_by(id=user_id).first()
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        return None

# New feature following pattern
def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email."""
    try:
        return database.query(User).filter_by(email=email).first()
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        return None
```

## Integration Patterns

### Integrating with Existing Code

**Pattern: Extend existing functionality**
```python
# Existing code
def process_request(request: dict) -> dict:
    # ... existing logic
    return response

# Integration point
def enhanced_process_request(request: dict, enable_new_feature: bool = False) -> dict:
    """Enhanced version with new feature."""
    if enable_new_feature:
        request = apply_new_feature(request)
    return process_request(request)

def apply_new_feature(request: dict) -> dict:
    """New feature logic."""
    # ... new feature implementation
    return request
```

**Pattern: Hook into existing workflow**
```python
# Existing workflow
class DataPipeline:
    def run(self):
        self.load_data()
        self.process_data()
        self.save_data()

# Add new step
class DataPipeline:
    def run(self):
        self.load_data()
        self.process_data()
        self.apply_new_transformation()  # New step
        self.save_data()

    def apply_new_transformation(self):
        """New transformation step."""
        # ... implementation
        pass
```

## Error Handling Patterns

### Standard Error Handling

```python
def feature_function(param: str) -> dict:
    """Function with error handling."""
    try:
        # Main logic
        result = perform_operation(param)
        return result
    except ValueError as e:
        logger.error(f"Invalid value: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {}
```

### Validation Patterns

```python
def feature_function(param: str) -> dict:
    """Function with input validation."""
    # Validate inputs
    if not param:
        raise ValueError("param cannot be empty")

    if not isinstance(param, str):
        raise TypeError("param must be a string")

    # Main logic
    result = {}
    return result
```
