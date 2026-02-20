# Replay Tools and Frameworks

## Record-Replay Tools by Language

### Python

**RR (Record and Replay)**
- System-level record-replay for Linux
- Records all non-deterministic inputs at syscall level
- Supports Python programs
- Usage: `rr record python script.py` then `rr replay`

**Python-specific approaches:**
- Mock-based recording (unittest.mock)
- Custom instrumentation with decorators
- Monkey-patching standard library

### JavaScript/Node.js

**Nock** (HTTP recording)
```javascript
const nock = require('nock');

// Record mode
nock.recorder.rec();
// ... make HTTP requests ...
const recorded = nock.recorder.play();

// Replay mode
nock('http://api.example.com')
  .get('/users')
  .reply(200, { users: [...] });
```

**Replay** (general-purpose)
- Records function calls and returns
- Supports async operations
- Deterministic replay

### Java

**JaRec (Java Recorder)**
- Bytecode instrumentation
- Records method calls and returns
- Handles threading and synchronization

**Java Flight Recorder (JFR)**
- Built into JVM
- Records events for profiling
- Can be used for replay debugging

**AspectJ-based recording:**
```java
@Aspect
public class RecordingAspect {
    @Around("execution(* java.io..*(..))")
    public Object recordIO(ProceedingJoinPoint pjp) throws Throwable {
        Object result = pjp.proceed();
        recordEvent(pjp.getSignature(), pjp.getArgs(), result);
        return result;
    }
}
```

### C/C++

**RR (Record and Replay)**
- Industry-standard for C/C++
- Records at syscall level
- Supports multithreading
- Usage:
  ```bash
  rr record ./program
  rr replay
  # Can attach gdb: rr replay -d gdb
  ```

**Valgrind with custom tools**
- Can instrument memory accesses
- Record execution traces
- Custom plugins for recording

**Pin (Intel)**
- Dynamic binary instrumentation
- Can record instruction-level traces
- Supports custom analysis tools

**QIRA (QEMU Interactive Runtime Analyser)**
- Records full execution traces
- Web-based replay interface
- Supports multiple architectures

## System-Level Replay Tools

### RR (Mozilla Record and Replay)

**Features:**
- Records all non-deterministic inputs
- Deterministic replay
- Time-travel debugging
- GDB integration

**Usage:**
```bash
# Record
rr record ./program arg1 arg2

# Replay
rr replay

# Replay with GDB
rr replay -d gdb

# In GDB, use reverse execution:
# reverse-continue, reverse-step, reverse-next
```

**What it records:**
- System calls and results
- Signal delivery
- Thread scheduling
- Memory maps

### PANDA (Platform for Architecture-Neutral Dynamic Analysis)

**Features:**
- Whole-system record-replay
- Based on QEMU
- Records entire VM execution
- Supports plugins for analysis

**Usage:**
```bash
# Record
panda-system-x86_64 -replay record -monitor stdio disk.qcow2

# Replay
panda-system-x86_64 -replay replay -monitor stdio disk.qcow2
```

### Simics

**Features:**
- Commercial full-system simulator
- Deterministic execution
- Reverse debugging
- Checkpoint and restore

## Application-Level Replay Frameworks

### Jalangi (JavaScript)

**Features:**
- Dynamic analysis framework
- Records JavaScript execution
- Supports Node.js and browsers

**Usage:**
```javascript
// Instrument code
node src/js/commands/jalangi.js --inlineIID --inlineSource --analysis src/js/sample_analyses/ChainedAnalyses.js test.js

// Record execution
node src/js/commands/record.js test.js

// Replay
node src/js/commands/replay.js test.js
```

### Chronicler (Web applications)

**Features:**
- Records browser interactions
- Captures network requests
- Replays user sessions

### Selenium/Puppeteer with recording

**Features:**
- Records browser automation
- Captures DOM state
- Replays interactions

## Debugging with Replay

### Time-Travel Debugging

**GDB with RR:**
```bash
rr replay -d gdb

# In GDB:
(gdb) continue          # Forward execution
(gdb) reverse-continue  # Backward execution
(gdb) reverse-step      # Step backward
(gdb) reverse-next      # Next backward
```

**WinDbg Time Travel Debugging (Windows):**
```
# Record
ttd.exe -out trace.run program.exe

# Replay
windbg -z trace.run

# Time travel commands:
!tt 0           # Go to start
!tt 100         # Go to position 100
g-              # Go backward
```

### Checkpoint-Based Replay

**DMTCP (Distributed MultiThreaded CheckPointing):**
```bash
# Start with checkpointing
dmtcp_launch ./program

# Checkpoint manually
dmtcp_command -c

# Restart from checkpoint
dmtcp_restart ckpt_*.dmtcp
```

## Custom Replay Infrastructure

### Log Format Design

**JSON format:**
```json
{
  "events": [
    {"type": "call", "func": "read", "args": [3, 1024], "result": "data", "timestamp": 1234567890},
    {"type": "call", "func": "time", "args": [], "result": 1234567890, "timestamp": 1234567891}
  ]
}
```

**Binary format (more efficient):**
```
[Event Type (1 byte)][Timestamp (8 bytes)][Data Length (4 bytes)][Data (variable)]
```

### Replay Engine Components

1. **Event Logger**: Records non-deterministic events
2. **Event Player**: Replays events from log
3. **Instrumentation Layer**: Intercepts non-deterministic operations
4. **Verification Layer**: Ensures replay matches recording

### Example Replay Engine Structure

```python
class ReplayEngine:
    def __init__(self, mode='record'):
        self.mode = mode
        self.events = []
        self.replay_index = 0

    def record_event(self, event_type, data):
        if self.mode == 'record':
            self.events.append({
                'type': event_type,
                'data': data,
                'timestamp': time.time()
            })

    def replay_event(self, event_type):
        if self.mode == 'replay':
            event = self.events[self.replay_index]
            assert event['type'] == event_type
            self.replay_index += 1
            return event['data']

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.events, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.events = pickle.load(f)
```

## Best Practices

1. **Record at appropriate granularity**: Balance overhead vs. completeness
2. **Minimize log size**: Use binary formats, compression
3. **Verify replay**: Check that replay matches recording
4. **Handle errors gracefully**: Log errors during recording
5. **Version logs**: Include version info for compatibility
6. **Test replay regularly**: Ensure logs remain valid
7. **Document non-determinism sources**: Know what needs recording
