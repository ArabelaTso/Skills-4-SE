---
name: python-test-updater
description: "Updates Python test code to work with new versions of the code being tested. Use when Claude needs to: (1) Update tests after code changes, (2) Fix broken tests due to signature changes, (3) Update assertions to match new behavior, (4) Add test cases for new functionality, (5) Analyze code differences and their test impact, (6) Run tests and fix failures based on error messages. Takes old code, new code, and old tests as input, outputs updated tests that pass."
---

# Python Test Updater

Update Python tests to work correctly with new code versions.

## Workflow

### 1. Understand the Inputs

**Gather required inputs:**
- Old version of Python code (file or content)
- New version of Python code (file or content)
- Old test module or test functions (file or content)

**Verify inputs:**
- Code files are valid Python
- Test files use pytest or unittest
- Files are readable

### 2. Analyze Code Changes

**Automated analysis:**
```bash
python scripts/analyze_code_diff.py <old_file> <new_file>
```

**Manual analysis:**
- Read both old and new code versions
- Identify what changed
- Understand the nature of changes

**Identify change types:**

**Function signature changes:**
- Added parameters
- Removed parameters
- Renamed parameters
- Changed parameter types
- Changed default values

**Return value changes:**
- Changed return type
- Changed return structure
- Added return fields
- Removed return fields

**Behavior changes:**
- Modified logic
- Changed validation rules
- Updated error handling
- Altered workflows

**Class changes:**
- Added/removed methods
- Modified constructor
- Changed inheritance
- Updated attributes

**Async changes:**
- Sync to async conversion
- Async to sync conversion

See [test-update-patterns.md](references/test-update-patterns.md) for detailed patterns.

### 3. Analyze Test Structure

**Read the old tests:**
- Identify test functions
- Understand test setup (fixtures, mocks)
- Note test assertions
- Check test organization

**Identify test components:**
- Test functions/methods
- Fixtures
- Parametrized tests
- Mocked dependencies
- Assertions

**Map tests to code:**
- Which tests cover which functions/classes
- What behavior each test verifies
- What assertions check what conditions

### 4. Determine Required Updates

**For each code change, identify test impact:**

**Signature changes → Update function calls**
```python
# Old code: function(arg1, arg2)
# New code: function(arg1, arg2, arg3=default)

# Old test
result = function(value1, value2)

# Updated test
result = function(value1, value2)  # Works with default
# OR
result = function(value1, value2, value3)  # Explicit value
```

**Return value changes → Update assertions**
```python
# Old code: return value
# New code: return {"result": value, "status": "ok"}

# Old test
assert result == expected_value

# Updated test
assert result["result"] == expected_value
assert result["status"] == "ok"
```

**Behavior changes → Update expected values**
```python
# Old code: validates length >= 6
# New code: validates length >= 8 and has digit

# Old test
assert validate("abc123") == True

# Updated test
assert validate("abc12345") == True  # Updated
assert validate("abc123") == False   # Now fails
```

**New functionality → Add new tests**
```python
# New code: added get_display_name() method

# Add new test
def test_get_display_name():
    obj = MyClass("value")
    assert obj.get_display_name() == "Value: value"
```

### 5. Update Test Code

**Apply updates systematically:**

**Step 1: Update imports if needed**
```python
# If new exceptions or classes added
from module import NewException, NewClass
```

**Step 2: Update function/method calls**
- Add new required parameters
- Remove obsolete parameters
- Rename parameters if changed
- Update keyword arguments

**Step 3: Update assertions**
- Change expected values if behavior changed
- Update assertion structure if return type changed
- Add new assertions for new fields
- Remove assertions for removed fields

**Step 4: Update exception handling**
```python
# Old
with pytest.raises(OldException):
    function()

# New
with pytest.raises(NewException):
    function()
```

**Step 5: Update async/await if needed**
```python
# Old
def test_function():
    result = function()

# New (if function became async)
@pytest.mark.asyncio
async def test_function():
    result = await function()
```

**Step 6: Add new test cases**
- Test new functionality
- Test new parameters
- Test new behavior
- Test edge cases

### 6. Run Tests

**Execute the updated tests:**
```bash
# Run all tests
pytest test_file.py

# Run specific test
pytest test_file.py::test_function

# Run with verbose output
pytest -v test_file.py
```

**Check results:**
- All tests should pass
- No import errors
- No syntax errors
- No assertion failures

### 7. Fix Remaining Failures

**If tests still fail:**

**Analyze error messages:**
- Read the error carefully
- Identify what's failing
- Understand why it's failing

**Common failure types:**

**1. AssertionError**
```
AssertionError: assert 10 == 15
```
→ Expected value changed, update assertion

**2. TypeError**
```
TypeError: function() missing 1 required positional argument: 'new_param'
```
→ Add missing parameter to function call

**3. AttributeError**
```
AttributeError: 'dict' object has no attribute 'field'
```
→ Return type changed, update how result is accessed

**4. ImportError**
```
ImportError: cannot import name 'OldClass'
```
→ Class renamed or removed, update import

**Fix each failure:**
1. Identify the root cause
2. Apply appropriate fix
3. Re-run tests
4. Verify fix works

### 8. Verify and Refine

**Final verification:**
- All tests pass
- Test coverage maintained
- Test intent preserved
- Code quality good

**Refine if needed:**
- Improve test names
- Add docstrings
- Use fixtures for common setup
- Parametrize similar tests

**Example refinement:**
```python
# Before
def test_function_case1():
    assert function(5) == 10

def test_function_case2():
    assert function(10) == 20

# After (parametrized)
@pytest.mark.parametrize("input,expected", [
    (5, 10),
    (10, 20),
])
def test_function(input, expected):
    assert function(input) == expected
```

## Common Update Patterns

### Pattern 1: Add Parameter with Default

**Code change:**
```python
# Old
def function(a, b):
    return a + b

# New
def function(a, b, c=0):
    return a + b + c
```

**Test update:**
```python
# Old test (still works)
def test_function():
    assert function(1, 2) == 3

# Add new test for new parameter
def test_function_with_c():
    assert function(1, 2, 3) == 6
```

### Pattern 2: Change Return Type

**Code change:**
```python
# Old
def get_data():
    return [1, 2, 3]

# New
def get_data():
    return {"data": [1, 2, 3], "count": 3}
```

**Test update:**
```python
# Old
def test_get_data():
    data = get_data()
    assert len(data) == 3

# New
def test_get_data():
    result = get_data()
    assert len(result["data"]) == 3
    assert result["count"] == 3
```

### Pattern 3: Change Validation Logic

**Code change:**
```python
# Old
def validate(value):
    return len(value) >= 6

# New
def validate(value):
    return len(value) >= 8 and any(c.isdigit() for c in value)
```

**Test update:**
```python
# Old
def test_validate():
    assert validate("abc123") == True
    assert validate("abc") == False

# New
def test_validate():
    assert validate("abc12345") == True  # Updated
    assert validate("abc123") == False   # Now fails validation
    assert validate("abcdefgh") == False # No digit
    assert validate("abc") == False
```

### Pattern 4: Sync to Async

**Code change:**
```python
# Old
def fetch():
    return data

# New
async def fetch():
    return await async_data()
```

**Test update:**
```python
# Old
def test_fetch():
    result = fetch()
    assert result is not None

# New
@pytest.mark.asyncio
async def test_fetch():
    result = await fetch()
    assert result is not None
```

## Best Practices

### Preserve Test Intent
- Keep testing the same functionality
- Don't change what's being verified
- Only update how it's tested

### Maintain Coverage
- Don't remove tests unless functionality removed
- Add tests for new functionality
- Keep edge case tests

### Update Systematically
- Fix one type of issue at a time
- Run tests after each change
- Verify fixes don't break other tests

### Improve While Updating
- Use fixtures for common setup
- Parametrize similar tests
- Improve test names and docs

### Verify Thoroughly
- Run full test suite
- Check for flaky tests
- Verify test independence

## Troubleshooting

### Issue: Tests pass but don't test new behavior

**Solution:**
- Add new test cases for new functionality
- Update existing tests to cover new parameters
- Verify test coverage

### Issue: Can't determine what changed

**Solution:**
- Use code diff analyzer script
- Compare function signatures manually
- Run old tests against new code to see failures
- Analyze error messages

### Issue: Too many test failures

**Solution:**
- Fix one test at a time
- Group similar failures
- Fix systematic issues first (imports, signatures)
- Then fix assertion issues

### Issue: Tests pass but behavior seems wrong

**Solution:**
- Verify test assertions are correct
- Check if test is actually testing new behavior
- Add more specific assertions
- Test edge cases

## Example Workflow

### Scenario: Function signature changed

**Old code:**
```python
def calculate_price(quantity, unit_price):
    return quantity * unit_price
```

**New code:**
```python
def calculate_price(quantity, unit_price, discount=0.0):
    subtotal = quantity * unit_price
    return subtotal * (1 - discount)
```

**Old test:**
```python
def test_calculate_price():
    price = calculate_price(5, 10.0)
    assert price == 50.0
```

**Analysis:**
- Added parameter: `discount` with default value 0.0
- Behavior unchanged when discount not provided
- New behavior when discount provided

**Updated test:**
```python
def test_calculate_price():
    # Test without discount (original behavior)
    price = calculate_price(5, 10.0)
    assert price == 50.0

def test_calculate_price_with_discount():
    # Test with discount (new behavior)
    price = calculate_price(5, 10.0, 0.1)
    assert price == 45.0  # 50 * 0.9
```

**Verification:**
```bash
pytest test_file.py -v
# Both tests should pass
```

## Output Format

Provide updated test code with:

1. **Summary of changes:**
   - What was updated
   - Why it was updated
   - New tests added

2. **Updated test code:**
   - Complete updated test file
   - All necessary imports
   - All test functions

3. **Verification notes:**
   - How to run tests
   - Expected results
   - Any caveats or notes
