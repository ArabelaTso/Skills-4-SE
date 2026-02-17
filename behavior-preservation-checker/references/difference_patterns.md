# Behavioral Difference Patterns

## Overview

This document catalogs common patterns of behavioral differences found when comparing original and migrated repositories, along with diagnostic approaches and remediation strategies.

## Logic Errors

### Pattern: Off-by-One Error

**Symptoms**:
- Array index out of bounds
- Loop iterations differ by one
- Boundary conditions fail

**Example**:
```python
# Original
for i in range(len(items)):
    process(items[i])

# Migrated (incorrect)
for i in range(len(items) - 1):  # Missing last item!
    process(items[i])
```

**Detection**:
- Test with edge cases (empty, single item, full)
- Compare loop iteration counts
- Check boundary value tests

**Remediation**:
1. Review loop conditions
2. Add boundary tests
3. Use inclusive/exclusive range correctly

### Pattern: Operator Inversion

**Symptoms**:
- Opposite boolean results
- Inverted comparisons
- Wrong conditional branches

**Example**:
```python
# Original
if x > threshold:
    return "high"

# Migrated (incorrect)
if x < threshold:  # Inverted!
    return "high"
```

**Detection**:
- Compare boolean return values
- Test boundary conditions
- Check conditional logic

**Remediation**:
1. Review all comparison operators
2. Add tests for both branches
3. Use truth tables to verify logic

### Pattern: Missing Null Check

**Symptoms**:
- NullPointerException / AttributeError
- Crashes on edge cases
- Tests pass in original, fail in migrated

**Example**:
```python
# Original
if user is not None:
    return user.name

# Migrated (incorrect)
return user.name  # Missing null check!
```

**Detection**:
- Test with null/None inputs
- Check error handling
- Review defensive programming

**Remediation**:
1. Add null checks
2. Use optional types
3. Add tests for null cases

## Missing Functionality

### Pattern: Unimplemented Method

**Symptoms**:
- NotImplementedError
- AttributeError
- Method not found

**Example**:
```python
# Original
class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

# Migrated (incomplete)
class Calculator:
    def add(self, a, b):
        return a + b
    # multiply() missing!
```

**Detection**:
- Compare class interfaces
- Check method signatures
- Run comprehensive test suite

**Remediation**:
1. List all missing methods
2. Implement missing functionality
3. Add interface tests

### Pattern: Incomplete Migration

**Symptoms**:
- Some features work, others don't
- Partial functionality
- TODO comments in code

**Example**:
```python
# Migrated
def process_data(data):
    # TODO: Implement validation
    return transform(data)
```

**Detection**:
- Search for TODO/FIXME comments
- Compare feature lists
- Run full test suite

**Remediation**:
1. Complete all TODOs
2. Implement missing features
3. Remove placeholder code

## API Contract Violations

### Pattern: Changed Response Structure

**Symptoms**:
- JSON structure differs
- Missing fields
- Different data types

**Example**:
```json
// Original
{
  "user": {
    "id": 123,
    "name": "Alice"
  }
}

// Migrated (incorrect)
{
  "userId": 123,
  "userName": "Alice"
}
```

**Detection**:
- Compare JSON schemas
- Validate against OpenAPI spec
- Test API clients

**Remediation**:
1. Document API contract
2. Match original structure
3. Add schema validation tests

### Pattern: Changed Status Codes

**Symptoms**:
- Different HTTP status codes
- Error handling breaks
- Client expectations violated

**Example**:
```python
# Original
return Response(data, status=200)

# Migrated (incorrect)
return Response(data, status=201)  # Changed from 200 to 201
```

**Detection**:
- Compare status codes
- Test error scenarios
- Check API documentation

**Remediation**:
1. Match original status codes
2. Document intentional changes
3. Add status code tests

## Performance Regressions

### Pattern: Algorithmic Complexity Change

**Symptoms**:
- Significantly slower execution
- Timeout on large inputs
- Memory exhaustion

**Example**:
```python
# Original: O(n)
def find_item(items, target):
    return target in items  # Uses hash lookup

# Migrated: O(n²) - incorrect!
def find_item(items, target):
    for item in items:
        if item == target:
            return True
    return False
```

**Detection**:
- Benchmark with varying input sizes
- Profile execution time
- Analyze algorithm complexity

**Remediation**:
1. Identify bottleneck
2. Restore efficient algorithm
3. Add performance tests

### Pattern: Missing Optimization

**Symptoms**:
- Slower than original
- Repeated computations
- No caching

**Example**:
```python
# Original (optimized)
@lru_cache(maxsize=128)
def expensive_computation(x):
    return complex_calculation(x)

# Migrated (missing cache)
def expensive_computation(x):
    return complex_calculation(x)
```

**Detection**:
- Compare execution times
- Profile function calls
- Check for repeated work

**Remediation**:
1. Add caching
2. Optimize hot paths
3. Benchmark improvements

## State Management Issues

### Pattern: Shared Mutable State

**Symptoms**:
- Tests fail when run together
- Order-dependent failures
- Intermittent bugs

**Example**:
```python
# Migrated (incorrect - shared state)
cache = {}  # Global mutable state

def process(key, value):
    cache[key] = value  # Modifies shared state
    return cache
```

**Detection**:
- Run tests in random order
- Check for global variables
- Test isolation

**Remediation**:
1. Remove global state
2. Use dependency injection
3. Add proper setup/teardown

### Pattern: Missing State Reset

**Symptoms**:
- Second run behaves differently
- Accumulated state
- Memory leaks

**Example**:
```python
# Migrated (incorrect)
class Processor:
    def __init__(self):
        self.results = []

    def process(self, data):
        self.results.append(data)  # Never cleared!
        return self.results
```

**Detection**:
- Run operations multiple times
- Check memory usage
- Test state isolation

**Remediation**:
1. Reset state between operations
2. Use immutable data structures
3. Add cleanup methods

## Data Type Mismatches

### Pattern: Type Coercion Difference

**Symptoms**:
- Unexpected type conversions
- Precision loss
- String/number confusion

**Example**:
```python
# Original
def calculate(x, y):
    return x / y  # Returns float

# Migrated (incorrect)
def calculate(x, y):
    return x // y  # Returns int - different!
```

**Detection**:
- Check return types
- Test with various inputs
- Use type checking tools

**Remediation**:
1. Match original types
2. Add type annotations
3. Test type conversions

### Pattern: Encoding Issues

**Symptoms**:
- Character corruption
- Unicode errors
- Different string representations

**Example**:
```python
# Original
text = "Hello"  # UTF-8

# Migrated (incorrect)
text = b"Hello"  # Bytes instead of string
```

**Detection**:
- Test with non-ASCII characters
- Check encoding declarations
- Validate string operations

**Remediation**:
1. Use consistent encoding
2. Handle Unicode properly
3. Add encoding tests

## Error Handling Differences

### Pattern: Swallowed Exceptions

**Symptoms**:
- Silent failures
- Missing error messages
- Different error behavior

**Example**:
```python
# Original
def process(data):
    if not validate(data):
        raise ValueError("Invalid data")
    return transform(data)

# Migrated (incorrect)
def process(data):
    try:
        if not validate(data):
            raise ValueError("Invalid data")
        return transform(data)
    except:
        pass  # Swallows all exceptions!
```

**Detection**:
- Test error scenarios
- Check exception types
- Verify error messages

**Remediation**:
1. Preserve error handling
2. Don't catch all exceptions
3. Add error tests

### Pattern: Changed Exception Types

**Symptoms**:
- Different exception types
- Broken error handling
- Client code breaks

**Example**:
```python
# Original
raise ValueError("Invalid input")

# Migrated (incorrect)
raise Exception("Invalid input")  # Too generic!
```

**Detection**:
- Compare exception types
- Test error handling
- Check exception hierarchy

**Remediation**:
1. Use same exception types
2. Preserve exception hierarchy
3. Test exception handling

## Dependency Differences

### Pattern: Library Version Mismatch

**Symptoms**:
- Different behavior
- API changes
- Deprecated features

**Example**:
```python
# Original (pandas 1.0)
df.append(row)  # Works

# Migrated (pandas 2.0)
df.append(row)  # Deprecated!
```

**Detection**:
- Compare dependency versions
- Check deprecation warnings
- Test with same versions

**Remediation**:
1. Match library versions
2. Update deprecated APIs
3. Pin dependencies

### Pattern: Missing Dependency

**Symptoms**:
- Import errors
- Module not found
- Feature unavailable

**Example**:
```python
# Original
import numpy as np

# Migrated (missing dependency)
# numpy not installed!
```

**Detection**:
- Check requirements files
- Test imports
- Verify dependencies

**Remediation**:
1. Install missing dependencies
2. Update requirements.txt
3. Add dependency tests

## Timing and Concurrency Issues

### Pattern: Race Condition

**Symptoms**:
- Intermittent failures
- Non-deterministic behavior
- Concurrency bugs

**Example**:
```python
# Migrated (incorrect - race condition)
def increment():
    global counter
    temp = counter
    # Another thread might modify counter here!
    counter = temp + 1
```

**Detection**:
- Run tests with threading
- Use race detection tools
- Test under load

**Remediation**:
1. Add proper locking
2. Use thread-safe structures
3. Test concurrency

### Pattern: Timeout Difference

**Symptoms**:
- Operations timeout
- Different timing behavior
- Flaky tests

**Example**:
```python
# Original
response = requests.get(url, timeout=30)

# Migrated (incorrect)
response = requests.get(url)  # No timeout!
```

**Detection**:
- Test with slow operations
- Check timeout settings
- Monitor execution time

**Remediation**:
1. Set appropriate timeouts
2. Handle timeout errors
3. Add timeout tests

## Diagnostic Workflow

For any behavioral difference:

1. **Isolate**: Identify the minimal test case that reproduces the difference
2. **Compare**: Examine the relevant code in both versions side-by-side
3. **Trace**: Use execution tracing to see where behavior diverges
4. **Test**: Create a specific test for the difference
5. **Fix**: Implement the correction
6. **Verify**: Confirm the fix resolves the difference
7. **Prevent**: Add tests to prevent regression

## Summary

Common patterns by frequency:
1. Logic errors (40%)
2. Missing functionality (25%)
3. API contract violations (15%)
4. Performance regressions (10%)
5. State management issues (10%)

Most critical patterns:
1. Logic errors affecting core functionality
2. API contract violations breaking clients
3. Missing functionality causing failures
4. Performance regressions causing timeouts
5. Data corruption from state issues
