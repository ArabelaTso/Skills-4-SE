---
name: replay-oriented-instrumentation
description: Instruments programs to record execution information for deterministic replay debugging. Use when debugging hard-to-reproduce bugs (race conditions, timing issues, intermittent failures, heisenbugs), reproducing production failures, or analyzing complex execution sequences. Records non-deterministic events (I/O, threading, randomness, time) to enable exact replay of program executions. Supports Python, JavaScript, Java, and C/C++ with both custom instrumentation and existing replay tools.
---

# Replay-Oriented Instrumentation

Instrument programs to capture execution information that enables deterministic replay, making it possible to reproduce and debug failures that are difficult to reproduce normally.

## Core Concept

Deterministic replay works by:
1. **Recording**: Capture all non-deterministic inputs during execution
2. **Replaying**: Re-execute the program using recorded inputs to reproduce exact behavior
3. **Debugging**: Use replay to analyze failures with time-travel debugging

## Workflow

### 1. Identify Non-Determinism Sources

Analyze the program to find sources of non-determinism. See [references/non-determinism.md](references/non-determinism.md) for comprehensive coverage.

Common sources:
- **I/O operations**: File reads, network requests, user input
- **Time**: System clock, timestamps, timeouts
- **Randomness**: Random number generation, hash functions
- **Threading**: Thread scheduling, race conditions, lock ordering
- **System state**: Process IDs, memory addresses, environment variables

### 2. Choose Recording Granularity

Select appropriate recording level based on needs:

**Function-level** (recommended starting point):
- Record function calls and return values
- Low overhead
- Good for most debugging scenarios
- Example: Record all I/O function calls

**Event-based** (balanced approach):
- Record specific non-deterministic events
- Moderate overhead
- Captures essential non-determinism
- Example: Record syscalls, thread events, random values

**Instruction-level** (comprehensive):
- Record every instruction execution
- High overhead, large logs
- Complete determinism
- Use only when necessary

### 3. Implement Recording Infrastructure

Choose between custom instrumentation or existing tools:

**Custom instrumentation** (flexible):
- Wrap non-deterministic functions
- Log inputs and outputs
- Control what gets recorded
- See language-specific guides below

**Existing tools** (easier):
- Use established replay frameworks
- Less implementation effort
- May have limitations
- See [references/replay-tools.md](references/replay-tools.md)

### 4. Record Execution

Run the program in recording mode:
- Execute the failing scenario
- Capture all non-deterministic events
- Save recording log
- Verify recording completed successfully

### 5. Replay Execution

Reproduce the execution from the log:
- Load recorded events
- Replace non-deterministic operations with logged values
- Verify replay matches original execution
- Use debugger during replay for analysis

### 6. Debug with Replay

Leverage replay for debugging:
- Set breakpoints without affecting timing
- Use time-travel debugging (reverse execution)
- Inspect state at any point in execution
- Reproduce failure consistently

## Quick Start by Language

### Python

For custom instrumentation, see [references/python-replay.md](references/python-replay.md).

**Basic example:**
```python
import json
import time
import random

class ReplayRecorder:
    def __init__(self, mode='record'):
        self.mode = mode
        self.log = []
        self.index = 0

    def record_call(self, func_name, result):
        if self.mode == 'record':
            self.log.append({'func': func_name, 'result': result})
        else:
            entry = self.log[self.index]
            self.index += 1
            return entry['result']

recorder = ReplayRecorder(mode='record')

def get_time():
    if recorder.mode == 'record':
        result = time.time()
        recorder.record_call('time', result)
        return result
    else:
        return recorder.record_call('time', None)

# Record mode
result = get_time()
with open('replay.log', 'w') as f:
    json.dump(recorder.log, f)

# Replay mode
recorder = ReplayRecorder(mode='replay')
with open('replay.log', 'r') as f:
    recorder.log = json.load(f)
result = get_time()  # Returns same value
```

**Using RR (system-level):**
```bash
rr record python script.py
rr replay
```

### JavaScript/Node.js

**Recording HTTP requests with Nock:**
```javascript
const nock = require('nock');

// Record mode
nock.recorder.rec();
// ... make requests ...
const fixtures = nock.recorder.play();

// Replay mode
nock('http://api.example.com')
  .get('/data')
  .reply(200, { data: 'recorded response' });
```

### Java

**Using AspectJ for recording:**
```java
@Aspect
public class ReplayAspect {
    private List<Event> events = new ArrayList<>();

    @Around("execution(* java.io..*(..))")
    public Object recordIO(ProceedingJoinPoint pjp) throws Throwable {
        Object result = pjp.proceed();
        events.add(new Event(pjp.getSignature(), pjp.getArgs(), result));
        return result;
    }
}
```

### C/C++

**Using RR (recommended):**
```bash
# Record
rr record ./program arg1 arg2

# Replay with GDB
rr replay -d gdb

# In GDB, use reverse execution
(gdb) reverse-continue
(gdb) reverse-step
```

**Custom instrumentation with macros:**
```c
#define RECORD_CALL(func, ...) \
    ({ \
        auto result = func(__VA_ARGS__); \
        log_event(#func, result); \
        result; \
    })

// Usage
int fd = RECORD_CALL(open, "file.txt", O_RDONLY);
```

## Common Scenarios

### Scenario 1: Race Condition Debugging

**Problem**: Test fails intermittently due to race condition

**Solution**:
1. Record thread scheduling events
2. Capture lock acquisition order
3. Replay with same thread interleaving
4. Use debugger to inspect race condition

**Implementation**:
```python
import threading

class ThreadRecorder:
    def __init__(self):
        self.events = []

    def record_lock(self, lock_id, acquired):
        self.events.append({
            'type': 'lock',
            'lock_id': lock_id,
            'acquired': acquired,
            'thread': threading.current_thread().ident
        })

recorder = ThreadRecorder()

class RecordingLock:
    def __init__(self, lock_id):
        self.lock = threading.Lock()
        self.lock_id = lock_id

    def acquire(self):
        result = self.lock.acquire()
        recorder.record_lock(self.lock_id, True)
        return result

    def release(self):
        recorder.record_lock(self.lock_id, False)
        self.lock.release()
```

### Scenario 2: Network Request Failure

**Problem**: API call fails in production, can't reproduce locally

**Solution**:
1. Record network requests and responses
2. Replay with recorded responses
3. Debug with exact production data

**Implementation** (JavaScript):
```javascript
const nock = require('nock');
const fs = require('fs');

// Record mode (run in production)
nock.recorder.rec({ output_objects: true });
// ... application runs ...
const recordings = nock.recorder.play();
fs.writeFileSync('recordings.json', JSON.stringify(recordings));

// Replay mode (run locally)
const recordings = JSON.parse(fs.readFileSync('recordings.json'));
nock.define(recordings);
// ... application runs with recorded responses ...
```

### Scenario 3: Time-Dependent Bug

**Problem**: Bug only occurs at specific times or after certain duration

**Solution**:
1. Record all time-related calls
2. Replay with recorded timestamps
3. Debug without waiting for real time

**Implementation**:
```python
import time

class TimeRecorder:
    def __init__(self, mode='record'):
        self.mode = mode
        self.times = []
        self.index = 0

    def time(self):
        if self.mode == 'record':
            t = time.time()
            self.times.append(t)
            return t
        else:
            t = self.times[self.index]
            self.index += 1
            return t

recorder = TimeRecorder(mode='record')
time.time = recorder.time
```

## Recording Strategies

### Minimize Overhead

- Record only non-deterministic operations
- Use binary log formats
- Buffer log writes
- Compress logs
- Sample when appropriate

### Ensure Completeness

- Identify all non-determinism sources
- Test replay matches recording
- Verify edge cases
- Handle errors during recording

### Optimize Log Size

- Use efficient encoding
- Deduplicate repeated values
- Compress similar events
- Prune unnecessary data

## Replay Verification

Always verify replay matches recording:

```python
def verify_replay(original_output, replay_output):
    if original_output != replay_output:
        print("REPLAY MISMATCH!")
        print(f"Original: {original_output}")
        print(f"Replay: {replay_output}")
        return False
    return True
```

## References

- **[non-determinism.md](references/non-determinism.md)**: Comprehensive guide to sources of non-determinism and recording strategies
- **[python-replay.md](references/python-replay.md)**: Python-specific replay techniques and examples
- **[replay-tools.md](references/replay-tools.md)**: Existing replay tools and frameworks (RR, PANDA, Jalangi, etc.)

## Tips

- **Start simple**: Begin with function-level recording
- **Test replay early**: Verify replay works before extensive recording
- **Use existing tools**: Leverage RR, Nock, etc. when possible
- **Record minimally**: Only capture what's needed for replay
- **Version logs**: Include version info for compatibility
- **Document sources**: Know what non-determinism exists in your code
- **Automate verification**: Check replay matches recording automatically
