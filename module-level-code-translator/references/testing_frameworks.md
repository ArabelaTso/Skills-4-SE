# Testing Framework Mappings

Equivalent testing patterns across languages.

## Test Structure

### Python (pytest) → JavaScript (Jest)
```python
def test_addition():
    assert add(2, 3) == 5
```
→
```javascript
test('addition', () => {
    expect(add(2, 3)).toBe(5);
});
```

### Python (unittest) → Java (JUnit)
```python
class TestMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(add(2, 3), 5)
```
→
```java
class MathTest {
    @Test
    void testAddition() {
        assertEquals(5, add(2, 3));
    }
}
```

### Python (pytest) → Go (testing)
```python
def test_addition():
    assert add(2, 3) == 5
```
→
```go
func TestAddition(t *testing.T) {
    if result := add(2, 3); result != 5 {
        t.Errorf("Expected 5, got %d", result)
    }
}
```

## Assertions

### Python → JavaScript (Jest)
- `assert x == y` → `expect(x).toBe(y)`
- `assert x in list` → `expect(list).toContain(x)`
- `assert len(list) == n` → `expect(list).toHaveLength(n)`
- `with pytest.raises(Error):` → `expect(() => {}).toThrow(Error)`

### Python → Java (JUnit)
- `assert x == y` → `assertEquals(y, x)`
- `assert x in list` → `assertTrue(list.contains(x))`
- `with pytest.raises(Error):` → `assertThrows(Error.class, () -> {})`

### Python → Go
- `assert x == y` → `if x != y { t.Errorf("Expected %v, got %v", y, x) }`
- `assert x in list` → Custom contains check with `t.Errorf`

## Fixtures/Setup

### Python (pytest) → JavaScript (Jest)
```python
@pytest.fixture
def setup_data():
    return {"key": "value"}
```
→
```javascript
beforeEach(() => {
    setupData = {key: "value"};
});
```

### Python (unittest) → Java (JUnit)
```python
def setUp(self):
    self.data = create_data()
```
→
```java
@BeforeEach
void setUp() {
    data = createData();
}
```

### Python (pytest) → Go
```python
@pytest.fixture
def setup_data():
    return create_data()
```
→
```go
func setup() Data {
    return createData()
}
// Call setup() in each test
```

## Mocking

### Python (unittest.mock) → JavaScript (Jest)
```python
with patch('module.function') as mock:
    mock.return_value = 42
```
→
```javascript
jest.mock('module');
module.function.mockReturnValue(42);
```

### Python (unittest.mock) → Java (Mockito)
```python
with patch('module.function') as mock:
    mock.return_value = 42
```
→
```java
Function mock = mock(Function.class);
when(mock.call()).thenReturn(42);
```

### Python (unittest.mock) → Go
Go typically uses interfaces for mocking:
```go
type MockService struct{}
func (m *MockService) Method() int { return 42 }
```

## Parametrized Tests

### Python (pytest) → JavaScript (Jest)
```python
@pytest.mark.parametrize("input,expected", [(1,2), (2,4)])
def test_double(input, expected):
    assert double(input) == expected
```
→
```javascript
test.each([
    [1, 2],
    [2, 4]
])('double(%i) = %i', (input, expected) => {
    expect(double(input)).toBe(expected);
});
```

### Python (pytest) → Java (JUnit)
```python
@pytest.mark.parametrize("input,expected", [(1,2), (2,4)])
def test_double(input, expected):
    assert double(input) == expected
```
→
```java
@ParameterizedTest
@CsvSource({"1,2", "2,4"})
void testDouble(int input, int expected) {
    assertEquals(expected, double(input));
}
```
