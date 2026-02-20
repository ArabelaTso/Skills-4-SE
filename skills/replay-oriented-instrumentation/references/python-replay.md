# Python Replay Techniques

## Recording Non-Determinism in Python

### System Call Interception

Use `unittest.mock` or custom wrappers:

```python
import time
import random
from functools import wraps

# Recording infrastructure
replay_log = []

def record_call(func_name, args, result):
    replay_log.append({
        'type': 'call',
        'function': func_name,
        'args': args,
        'result': result
    })

# Wrap non-deterministic functions
original_time = time.time
original_random = random.random

def instrumented_time():
    result = original_time()
    record_call('time.time', (), result)
    return result

def instrumented_random():
    result = original_random()
    record_call('random.random', (), result)
    return result

# Replace functions
time.time = instrumented_time
random.random = instrumented_random
```

### File I/O Recording

```python
class RecordingFile:
    def __init__(self, file_obj, filename):
        self.file = file_obj
        self.filename = filename

    def read(self, size=-1):
        data = self.file.read(size)
        record_call('file.read', (self.filename, size), data)
        return data

    def write(self, data):
        result = self.file.write(data)
        record_call('file.write', (self.filename, data), result)
        return result

# Wrap open()
original_open = open

def instrumented_open(filename, mode='r', *args, **kwargs):
    file_obj = original_open(filename, mode, *args, **kwargs)
    return RecordingFile(file_obj, filename)

__builtins__.open = instrumented_open
```

### Thread Scheduling Recording

```python
import threading

class RecordingThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread_id = id(self)

    def run(self):
        record_call('thread.start', (self.thread_id,), None)
        super().run()
        record_call('thread.end', (self.thread_id,), None)

# Replace Thread class
threading.Thread = RecordingThread
```

## Replay from Logs

```python
class ReplayLog:
    def __init__(self, log_data):
        self.log = log_data
        self.index = 0

    def get_next_result(self, func_name, args):
        if self.index >= len(self.log):
            raise Exception("Replay log exhausted")

        entry = self.log[self.index]
        if entry['function'] != func_name:
            raise Exception(f"Replay mismatch: expected {func_name}, got {entry['function']}")

        self.index += 1
        return entry['result']

# Replay mode
replay_log_obj = ReplayLog(recorded_log)

def replay_time():
    return replay_log_obj.get_next_result('time.time', ())

def replay_random():
    return replay_log_obj.get_next_result('random.random', ())

time.time = replay_time
random.random = replay_random
```

## Using Python Debugger with Replay

```python
import pdb

# Record mode
def record_and_debug():
    # Run with recording
    result = run_program()

    # Save log
    with open('replay.log', 'w') as f:
        json.dump(replay_log, f)

    return result

# Replay mode with debugger
def replay_with_debugger():
    # Load log
    with open('replay.log', 'r') as f:
        global replay_log_obj
        replay_log_obj = ReplayLog(json.load(f))

    # Set up replay hooks
    setup_replay_hooks()

    # Run with debugger
    pdb.set_trace()
    result = run_program()

    return result
```

## Decorator-Based Instrumentation

```python
def record_replay(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if RECORDING_MODE:
            result = func(*args, **kwargs)
            record_call(func.__name__, args, result)
            return result
        elif REPLAY_MODE:
            return replay_log_obj.get_next_result(func.__name__, args)
        else:
            return func(*args, **kwargs)
    return wrapper

@record_replay
def get_current_time():
    return time.time()

@record_replay
def get_random_value():
    return random.random()
```

## Async/Await Recording

```python
import asyncio

async def record_async_call(coro, name):
    result = await coro
    record_call(name, (), result)
    return result

# Instrument async functions
original_sleep = asyncio.sleep

async def instrumented_sleep(seconds):
    record_call('asyncio.sleep', (seconds,), None)
    await original_sleep(seconds)

asyncio.sleep = instrumented_sleep
```

## Complete Example

```python
import json
import time
import random

class ReplayRecorder:
    def __init__(self, mode='record'):
        self.mode = mode
        self.log = []
        self.replay_index = 0

    def record(self, func_name, result):
        if self.mode == 'record':
            self.log.append({'func': func_name, 'result': result})

    def replay(self, func_name):
        if self.mode == 'replay':
            entry = self.log[self.replay_index]
            assert entry['func'] == func_name
            self.replay_index += 1
            return entry['result']

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.log, f)

    def load(self, filename):
        with open(filename, 'r') as f:
            self.log = json.load(f)

# Global recorder
recorder = ReplayRecorder(mode='record')

# Instrumented functions
def get_time():
    if recorder.mode == 'record':
        result = time.time()
        recorder.record('time', result)
        return result
    else:
        return recorder.replay('time')

def get_random():
    if recorder.mode == 'record':
        result = random.random()
        recorder.record('random', result)
        return result
    else:
        return recorder.replay('random')

# Usage
def main():
    t = get_time()
    r = get_random()
    print(f"Time: {t}, Random: {r}")

# Record
recorder = ReplayRecorder(mode='record')
main()
recorder.save('replay.log')

# Replay
recorder = ReplayRecorder(mode='replay')
recorder.load('replay.log')
main()  # Will produce identical output
```
