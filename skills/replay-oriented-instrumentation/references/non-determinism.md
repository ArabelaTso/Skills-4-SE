# Sources of Non-Determinism

Understanding and recording non-deterministic events is essential for deterministic replay.

## Categories of Non-Determinism

### 1. Input/Output Operations

**File I/O:**
- File read operations (content, size, existence)
- File write operations (success/failure)
- File system state (directory listings, permissions)

**Network I/O:**
- Socket reads (data received, timing)
- Socket writes (bytes sent, errors)
- DNS lookups
- Connection establishment/teardown

**Standard I/O:**
- stdin reads
- Environment variables
- Command-line arguments

**Recording strategy:**
- Capture all input data and return values
- Record timing of I/O operations
- Log error conditions and exceptions

### 2. Time and Timing

**Sources:**
- System clock (time(), gettimeofday())
- High-resolution timers (clock_gettime())
- Sleep operations
- Timeouts

**Recording strategy:**
- Record all time-related system call results
- Capture sleep durations
- Log timeout occurrences

### 3. Randomness

**Sources:**
- Random number generators (rand(), random())
- Cryptographic random sources (/dev/urandom)
- Hash functions with random seeds
- UUID generation

**Recording strategy:**
- Record all random values generated
- Capture RNG seeds
- Log random function call results

### 4. Concurrency and Threading

**Sources:**
- Thread scheduling decisions
- Lock acquisition order
- Race conditions
- Thread creation/termination timing
- Signal delivery timing

**Recording strategy:**
- Record thread interleaving order
- Capture synchronization events (lock/unlock)
- Log thread creation/join events
- Record signal delivery order

### 5. Memory and Addresses

**Sources:**
- Memory allocation addresses (malloc, new)
- Stack addresses
- Address space layout randomization (ASLR)
- Garbage collection timing

**Recording strategy:**
- Record allocation addresses (if address-dependent)
- Capture GC events and timing
- Log memory layout information

### 6. External System State

**Sources:**
- Process IDs
- User IDs
- Hostname
- System load
- Available memory/disk space

**Recording strategy:**
- Record all system state queries
- Capture environment information
- Log resource availability

## Recording Strategies by Granularity

### Function-Level Recording

Record inputs and outputs of functions:
```
CALL function_name(arg1=value1, arg2=value2)
RETURN function_name -> result_value
```

**Pros:** Low overhead, easy to implement
**Cons:** May miss intra-function non-determinism

### Event-Based Recording

Record specific non-deterministic events:
```
EVENT read(fd=3) -> "data content"
EVENT time() -> 1234567890
EVENT random() -> 0.42
```

**Pros:** Captures only essential non-determinism
**Cons:** Requires identifying all sources

### Instruction-Level Recording

Record every instruction execution:
```
PC=0x1000 R1=5 R2=10
PC=0x1004 R1=15 R2=10
```

**Pros:** Complete determinism
**Cons:** Very high overhead, large logs

## Minimizing Recording Overhead

### Selective Recording

Only record non-deterministic operations:
- Skip deterministic computations
- Focus on I/O and system calls
- Record thread scheduling points only

### Efficient Log Format

Use binary formats instead of text:
- Smaller log files
- Faster writing
- Structured data

### Buffering

Buffer log entries before writing:
- Reduce I/O overhead
- Batch writes
- Async logging

### Sampling

For performance-critical code:
- Record every Nth event
- Probabilistic recording
- Adaptive sampling based on overhead
