# Python Instrumentation Patterns

## Logging Instrumentation

### Function Entry/Exit
```python
import logging
logger = logging.getLogger(__name__)

def target_function(arg1, arg2):
    logger.debug(f"ENTER target_function: arg1={arg1}, arg2={arg2}")
    try:
        # original code
        result = process(arg1, arg2)
        logger.debug(f"EXIT target_function: result={result}")
        return result
    except Exception as e:
        logger.error(f"EXCEPTION in target_function: {e}", exc_info=True)
        raise
```

### Variable Tracking
```python
# Track variable changes
x = compute_value()
logger.debug(f"Variable x after compute: {x}, type={type(x)}")

# Track state changes
self.state = new_state
logger.debug(f"State transition: {old_state} -> {self.state}")
```

### Conditional Branch Tracking
```python
if condition:
    logger.debug(f"Branch: condition=True, value={condition}")
    # true branch
else:
    logger.debug(f"Branch: condition=False, value={condition}")
    # false branch
```

### Loop Iteration Tracking
```python
for i, item in enumerate(items):
    logger.debug(f"Loop iteration {i}: item={item}")
    # loop body
```

## Tracing with sys.settrace

```python
import sys

def trace_calls(frame, event, arg):
    if event == 'call':
        code = frame.f_code
        print(f"Call: {code.co_filename}:{frame.f_lineno} {code.co_name}")
        print(f"  Locals: {frame.f_locals}")
    elif event == 'return':
        print(f"Return: {arg}")
    return trace_calls

sys.settrace(trace_calls)
# code to trace
sys.settrace(None)
```

## Assertions for Invariants

```python
def process_data(data):
    assert data is not None, "Data should not be None"
    assert len(data) > 0, f"Data should not be empty, got {len(data)}"

    result = transform(data)

    assert result is not None, "Result should not be None"
    assert isinstance(result, list), f"Result should be list, got {type(result)}"
    return result
```

## Timing Information

```python
import time

start = time.time()
result = expensive_operation()
elapsed = time.time() - start
logger.debug(f"Operation took {elapsed:.3f}s")
```

## Context Managers for Scoped Instrumentation

```python
from contextlib import contextmanager

@contextmanager
def instrument_section(name):
    logger.debug(f"ENTER section: {name}")
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        logger.debug(f"EXIT section: {name} ({elapsed:.3f}s)")

with instrument_section("data_processing"):
    # code to instrument
    process_data()
```

## Decorator-Based Instrumentation

```python
from functools import wraps

def instrument(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"CALL {func.__name__}: args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"RETURN {func.__name__}: {result}")
            return result
        except Exception as e:
            logger.error(f"EXCEPTION {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper

@instrument
def my_function(x, y):
    return x + y
```
