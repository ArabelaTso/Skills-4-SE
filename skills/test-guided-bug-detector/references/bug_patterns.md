# Common Bug Patterns

Catalog of common bug patterns that cause test failures and how to detect them.

## Logic Errors

### Wrong Operator

**Pattern:** Using incorrect operator.

**Examples:**
```python
# BUG: == instead of =
if x == 5:  # Assignment intended

# BUG: // instead of /
result = 10 // 3  # Integer division, expected float

# BUG: & instead of and
if x > 0 & y > 0:  # Bitwise AND, expected logical

# BUG: | instead of or
if x < 0 | y < 0:  # Bitwise OR, expected logical
```

**Detection:**
- Compare expected vs actual values
- Check if different operator would give expected result
- Look for type mismatches (int vs float)

### Wrong Condition

**Pattern:** Incorrect conditional logic.

**Examples:**
```python
# BUG: < instead of <=
if i < len(arr):  # Should be <= for inclusive range

# BUG: Inverted condition
if not is_valid:  # Should be if is_valid

# BUG: Wrong comparison
if x > 10:  # Should be x >= 10
```

**Detection:**
- Trace execution with boundary values
- Check if inverting condition fixes test
- Look for off-by-one patterns

### Missing Case

**Pattern:** Conditional doesn't handle all cases.

**Examples:**
```python
# BUG: Missing else case
if x > 0:
    return 1
elif x < 0:
    return -1
# Missing: what if x == 0?

# BUG: Incomplete pattern match
def process(value):
    if isinstance(value, int):
        return value * 2
    elif isinstance(value, str):
        return value.upper()
    # Missing: list, dict, None, etc.
```

**Detection:**
- Check if test input falls outside handled cases
- Look for missing else/default branches
- Verify all enum/type cases covered

## State Management Bugs

### Uninitialized Variable

**Pattern:** Variable used before initialization.

**Examples:**
```python
# BUG: result not initialized
def compute(x):
    if x > 0:
        result = x * 2
    return result  # Error if x <= 0

# BUG: Conditional initialization
def process(items):
    for item in items:
        if item > 10:
            max_item = item
    return max_item  # Error if no item > 10
```

**Detection:**
- Trace all code paths
- Check if variable defined in all branches
- Look for conditional initialization

### Stale State

**Pattern:** Using outdated state.

**Examples:**
```python
# BUG: Cached value not updated
class Cache:
    def __init__(self):
        self.value = None

    def get(self):
        if self.value is None:
            self.value = expensive_compute()
        return self.value  # Never updates!

# BUG: Loop variable persists
for i in range(10):
    process(i)
return i  # Uses last value from loop
```

**Detection:**
- Check if state updates when it should
- Look for caching without invalidation
- Verify loop variables don't leak

### Shared Mutable State

**Pattern:** Unintended sharing of mutable objects.

**Examples:**
```python
# BUG: Mutable default argument
def append_to(item, lst=[]):
    lst.append(item)
    return lst  # Same list reused!

# BUG: Shared class variable
class Counter:
    count = 0  # Shared across all instances!

    def increment(self):
        Counter.count += 1
```

**Detection:**
- Check for mutable defaults
- Look for class variables vs instance variables
- Verify object identity vs equality

## Boundary Condition Bugs

### Off-by-One Error

**Pattern:** Loop or index off by one.

**Examples:**
```python
# BUG: Should be range(len(arr))
for i in range(len(arr) - 1):
    process(arr[i])  # Misses last element

# BUG: Should be i < len(arr)
i = 0
while i <= len(arr):  # Goes one past end
    process(arr[i])
    i += 1

# BUG: Slice off by one
arr[0:n-1]  # Should be arr[0:n]
```

**Detection:**
- Test with boundary values (0, 1, n-1, n)
- Check loop conditions (< vs <=)
- Verify slice indices

### Empty Collection

**Pattern:** Not handling empty input.

**Examples:**
```python
# BUG: Assumes non-empty
def get_first(lst):
    return lst[0]  # Error if empty

# BUG: Division by zero
def average(numbers):
    return sum(numbers) / len(numbers)  # Error if empty
```

**Detection:**
- Test with empty inputs
- Check for length/size checks
- Look for assumptions about non-empty

### Null/None Handling

**Pattern:** Not checking for null/None.

**Examples:**
```python
# BUG: No None check
def process(value):
    return value.upper()  # Error if value is None

# BUG: Returning None unexpectedly
def find(lst, target):
    for item in lst:
        if item == target:
            return item
    # Returns None implicitly if not found
```

**Detection:**
- Check for None checks before use
- Verify return value in all paths
- Look for implicit None returns

## Type Errors

### Implicit Type Conversion

**Pattern:** Unexpected type conversion.

**Examples:**
```python
# BUG: String concatenation instead of addition
result = "10" + "20"  # "1020" not 30

# BUG: Integer division in Python 2
result = 5 / 2  # 2 in Python 2, 2.5 in Python 3

# BUG: Truthy/falsy confusion
if len(lst):  # 0 is falsy, but valid length
```

**Detection:**
- Check types of operands
- Look for mixed types in operations
- Verify type conversions are explicit

### Type Mismatch

**Pattern:** Wrong type passed or returned.

**Examples:**
```python
# BUG: Returns wrong type
def get_count() -> int:
    return "5"  # Should return int

# BUG: Expects different type
def process(items: List[int]):
    for item in items:
        result = item.upper()  # Expects strings!
```

**Detection:**
- Check type annotations
- Verify actual types match expected
- Look for type-specific operations on wrong types

## Return Value Bugs

### Missing Return

**Pattern:** Function doesn't return in all paths.

**Examples:**
```python
# BUG: No return in else branch
def compute(x):
    if x > 0:
        return x * 2
    # Missing return for x <= 0

# BUG: No return after loop
def find(lst, target):
    for item in lst:
        if item == target:
            return item
    # Missing return None or -1
```

**Detection:**
- Trace all code paths
- Check if return in all branches
- Verify expected return type

### Wrong Return Value

**Pattern:** Returns incorrect value.

**Examples:**
```python
# BUG: Returns input instead of result
def double(x):
    result = x * 2
    return x  # Should return result

# BUG: Returns intermediate value
def process(items):
    for item in items:
        result = transform(item)
    return result  # Only last result!
```

**Detection:**
- Compare returned value to expected
- Check if wrong variable returned
- Verify return statement location

## Side Effect Bugs

### Unintended Mutation

**Pattern:** Modifying input unexpectedly.

**Examples:**
```python
# BUG: Modifies input list
def remove_negatives(numbers):
    for i, num in enumerate(numbers):
        if num < 0:
            numbers.pop(i)  # Modifies input!
    return numbers

# BUG: Modifies shared object
def update_config(config):
    config['updated'] = True  # Modifies original!
    return config
```

**Detection:**
- Check if input modified
- Look for in-place operations
- Verify copy vs reference

### Missing Side Effect

**Pattern:** Expected side effect doesn't occur.

**Examples:**
```python
# BUG: Doesn't update state
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        count = self.count + 1  # Local variable!
        # Should be: self.count += 1

# BUG: Doesn't save to database
def update_user(user_id, name):
    user = get_user(user_id)
    user.name = name
    # Missing: save_user(user)
```

**Detection:**
- Check if expected state changes
- Look for local vs instance variables
- Verify persistence operations

## Concurrency Bugs

### Race Condition

**Pattern:** Outcome depends on timing.

**Examples:**
```python
# BUG: Non-atomic check-then-act
if not file_exists(path):
    create_file(path)  # Another thread might create it first

# BUG: Shared counter without lock
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1  # Not atomic!
```

**Detection:**
- Look for shared mutable state
- Check for synchronization
- Test with concurrent execution

### Deadlock

**Pattern:** Circular wait for resources.

**Examples:**
```python
# BUG: Lock ordering inconsistency
def transfer(from_account, to_account, amount):
    with from_account.lock:
        with to_account.lock:  # Deadlock if reversed elsewhere
            from_account.balance -= amount
            to_account.balance += amount
```

**Detection:**
- Check lock acquisition order
- Look for nested locks
- Verify lock release

## Detection Strategy

1. **Read error message** - Often points to bug type
2. **Compare expected vs actual** - Reveals discrepancy
3. **Trace execution** - Find where divergence occurs
4. **Match pattern** - Identify which bug pattern fits
5. **Verify hypothesis** - Check if pattern explains failure
6. **Propose fix** - Address root cause
