# Python Mocking Patterns

## Common Mock Patterns

### External API Calls

```python
from unittest.mock import Mock, patch
import pytest

@patch('module.requests.get')
def test_api_call(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'data': 'value'}

    result = function_under_test()

    assert result == expected_value
    mock_get.assert_called_once_with('https://api.example.com/endpoint')
```

### Database Operations

```python
@patch('module.database.connect')
def test_database_query(mock_connect):
    mock_cursor = Mock()
    mock_cursor.fetchall.return_value = [('row1',), ('row2',)]
    mock_connect.return_value.cursor.return_value = mock_cursor

    result = function_under_test()

    assert len(result) == 2
    mock_cursor.execute.assert_called_once()
```

### File System Operations

```python
from unittest.mock import mock_open

@patch('builtins.open', mock_open(read_data='file content'))
def test_file_read():
    result = function_under_test()

    assert 'file content' in result
```

### Environment Variables

```python
@patch.dict('os.environ', {'API_KEY': 'test_key'})
def test_with_env_var():
    result = function_under_test()

    assert result.api_key == 'test_key'
```

### Time-Dependent Code

```python
from datetime import datetime

@patch('module.datetime')
def test_time_dependent(mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)

    result = function_under_test()

    assert result.timestamp == '2024-01-01 12:00:00'
```

### Class Method Mocking

```python
@patch.object(ClassName, 'method_name')
def test_class_method(mock_method):
    mock_method.return_value = 'mocked_value'

    obj = ClassName()
    result = obj.method_name()

    assert result == 'mocked_value'
```

### Side Effects and Exceptions

```python
@patch('module.external_service')
def test_exception_handling(mock_service):
    mock_service.side_effect = ConnectionError('Network error')

    with pytest.raises(ConnectionError):
        function_under_test()
```

### Multiple Return Values

```python
@patch('module.api_call')
def test_multiple_calls(mock_api):
    mock_api.side_effect = [
        {'status': 'pending'},
        {'status': 'complete'}
    ]

    result = function_under_test()

    assert result == 'complete'
    assert mock_api.call_count == 2
```

## Pytest Fixtures for Mocks

```python
@pytest.fixture
def mock_database():
    with patch('module.database.connect') as mock_conn:
        mock_cursor = Mock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        yield mock_cursor

def test_with_fixture(mock_database):
    mock_database.fetchall.return_value = [('data',)]
    result = function_under_test()
    assert result is not None
```

## Context Managers

```python
@patch('module.ExternalResource')
def test_context_manager(mock_resource):
    mock_instance = Mock()
    mock_resource.return_value.__enter__.return_value = mock_instance

    with ExternalResource() as resource:
        result = resource.do_something()

    mock_instance.do_something.assert_called_once()
```
