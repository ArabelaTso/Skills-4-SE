# Python Testing Patterns

## pytest Framework

### Basic Test Structure

```python
import pytest

def test_function_name():
    # Arrange
    input_data = setup_test_data()

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected_value
```

### Common Assertions

```python
assert value == expected
assert value != unexpected
assert value is None
assert value is not None
assert value in collection
assert len(collection) == expected_length
```

### Exception Testing

```python
def test_raises_exception():
    with pytest.raises(ValueError, match="error message pattern"):
        function_that_should_raise()
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    (0, 0),
    (1, 1),
    (5, 120),
    (-1, None),
])
def test_factorial(input, expected):
    assert factorial(input) == expected
```

### Edge Cases to Test

- Empty inputs ([], "", None)
- Single element
- Boundary values (0, -1, max_int)
- Invalid inputs (wrong type, out of range)
- Large inputs (performance)

### Test Organization

```python
class TestClassName:
    def test_normal_case(self):
        pass

    def test_edge_case(self):
        pass

    def test_error_case(self):
        pass
```
