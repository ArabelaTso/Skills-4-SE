# Use Cases

## 1. Bug Debugging

### Scenario

You have a bug that occurs deep in your program's execution, and traditional debugging is difficult because:
- The bug is intermittent
- The program state is complex
- The bug occurs after many operations
- You need to understand the full execution context

### Workflow

1. **Instrument the program** with automatic mode to capture comprehensive state:

```bash
python scripts/instrument_python.py buggy_program.py --mode auto
```

2. **Run the instrumented program** to reproduce the bug:

```bash
python buggy_program_instrumented.py
```

3. **Analyze snapshots** to identify the failure point:

```bash
# List all snapshots
python scripts/analyze_snapshots.py snapshots.json --list

# Show timeline to understand execution flow
python scripts/analyze_snapshots.py snapshots.json --timeline

# Examine snapshot before failure
python scripts/analyze_snapshots.py snapshots.json --show 42
```

4. **Track variable changes** to understand how state evolved:

```bash
# Track a specific variable across execution
python scripts/analyze_snapshots.py snapshots.json --track-var "user_id"
```

5. **Compare snapshots** to identify when state became incorrect:

```bash
# Compare good state vs bad state
python scripts/analyze_snapshots.py snapshots.json --compare 40 42
```

### Example

```python
# Original buggy code
def process_data(items):
    total = 0
    for item in items:
        if item > 0:
            total += item
    return total / len(items)  # Bug: division by zero if no positive items
```

After instrumentation and analysis:
- Snapshot 15 shows `items = [-1, -2, -3]`
- Snapshot 16 shows `total = 0` before division
- Snapshot 17 captures the exception
- Root cause: no positive items, division by zero

## 2. Test Case Reproduction

### Scenario

You need to reproduce a failing test case or bug report, but:
- The exact inputs are unknown
- The environment setup is unclear
- The execution sequence is complex
- External dependencies are involved

### Workflow

1. **Instrument the failing execution** with manual snapshots at key points:

```python
def process_request(request):
    __SNAPSHOT__("process_request:entry")

    user = authenticate(request)
    __SNAPSHOT__("after_auth")

    data = fetch_data(user.id)
    __SNAPSHOT__("after_fetch")

    result = transform(data)
    __SNAPSHOT__("before_return")

    return result
```

2. **Run and capture the failing execution**:

```bash
python scripts/instrument_python.py server.py --mode manual
python server_instrumented.py
```

3. **Extract input dependencies** from snapshots:

```bash
# Show the entry snapshot to see inputs
python scripts/analyze_snapshots.py snapshots.json --show 1

# Track how inputs flow through the program
python scripts/analyze_snapshots.py snapshots.json --track-var "request"
```

4. **Reconstruct the minimal test case** using captured state:

```python
# Extracted from snapshots
def test_bug_reproduction():
    # From snapshot 1: entry state
    request = {"user_id": 123, "action": "delete"}

    # From snapshot 2: authentication result
    user = User(id=123, role="guest")

    # From snapshot 3: fetched data
    data = {"items": [], "status": "empty"}

    # This should reproduce the bug
    result = transform(data)
    assert result is not None  # Fails!
```

### Benefits

- Exact reproduction of the failure
- No need to guess inputs or state
- Can create minimal test cases
- Understand the full execution context

## 3. Formal Verification Input

### Scenario

You want to verify program properties using formal methods, but need:
- Concrete execution traces as test cases
- State invariants to verify
- Pre/post conditions for functions
- Execution paths to explore

### Workflow

1. **Instrument with function boundaries** to capture contracts:

```bash
python scripts/instrument_c.py program.c --mode auto
```

2. **Run test suite** to collect execution traces:

```bash
./program_instrumented
# Generates snapshots.json with all executions
```

3. **Extract invariants** from snapshots:

```bash
# Analyze all function entry states
python scripts/analyze_snapshots.py snapshots.json --filter-type function_entry

# Analyze all function exit states
python scripts/analyze_snapshots.py snapshots.json --filter-type function_exit
```

4. **Generate verification conditions**:

```python
# Script to extract pre/post conditions
def extract_conditions(snapshots):
    for snapshot in snapshots:
        if snapshot['type'] == 'function_entry':
            # Extract preconditions
            preconditions = analyze_entry_state(snapshot)
        elif snapshot['type'] == 'function_exit':
            # Extract postconditions
            postconditions = analyze_exit_state(snapshot)
```

5. **Use with verification tools**:

- Feed snapshots to symbolic execution tools
- Generate test cases for model checkers
- Validate invariants against captured states
- Create counterexamples from failing executions

### Example: Verifying Array Bounds

```c
void process_array(int* arr, int size) {
    __SNAPSHOT__("entry");

    for (int i = 0; i < size; i++) {
        arr[i] = arr[i] * 2;
    }

    __SNAPSHOT__("exit");
}
```

From snapshots:
- Entry: `arr` pointer, `size = 10`
- Exit: All elements doubled, no buffer overflow
- Invariant: `0 <= i < size` throughout loop
- Verification: Prove no out-of-bounds access

## 4. Performance Analysis

### Scenario

Understand performance characteristics by analyzing state evolution:
- Identify memory growth patterns
- Track resource allocation/deallocation
- Understand algorithmic complexity
- Find performance bottlenecks

### Workflow

1. **Instrument performance-critical sections**:

```python
def process_large_dataset(data):
    __SNAPSHOT__("start")

    results = []
    for item in data:
        result = expensive_operation(item)
        results.append(result)

        if len(results) % 1000 == 0:
            __SNAPSHOT__(f"progress_{len(results)}")

    __SNAPSHOT__("end")
    return results
```

2. **Analyze memory growth**:

```bash
# Track results list size over time
python scripts/analyze_snapshots.py snapshots.json --track-var "results"
```

3. **Identify bottlenecks** from state changes:

```bash
# Compare state at different progress points
python scripts/analyze_snapshots.py snapshots.json --compare 1 10
python scripts/analyze_snapshots.py snapshots.json --compare 10 20
```

## 5. Debugging Concurrent Programs

### Scenario

Debug race conditions and concurrency issues:
- Understand thread interleaving
- Identify shared state access patterns
- Reproduce non-deterministic bugs
- Verify synchronization correctness

### Workflow

1. **Instrument with thread information**:

```python
import threading

def worker(shared_data):
    thread_id = threading.get_ident()
    __SNAPSHOT__(f"worker_{thread_id}:entry")

    # Critical section
    with lock:
        __SNAPSHOT__(f"worker_{thread_id}:critical_section")
        shared_data.append(value)

    __SNAPSHOT__(f"worker_{thread_id}:exit")
```

2. **Analyze thread interleaving**:

```bash
# Show timeline with thread information
python scripts/analyze_snapshots.py snapshots.json --timeline
```

3. **Identify race conditions** from snapshot ordering:

- Compare snapshots from different threads
- Identify conflicting accesses to shared state
- Understand synchronization points

## Best Practices for Each Use Case

### Debugging
- Use automatic mode for comprehensive coverage
- Focus on snapshots near the failure point
- Track key variables through execution
- Compare good vs bad executions

### Reproduction
- Use manual snapshots at key decision points
- Capture all inputs and external dependencies
- Document the execution environment
- Create minimal reproducible examples

### Verification
- Capture function entry/exit states
- Extract invariants from multiple executions
- Validate properties against snapshots
- Generate test cases from traces

### Performance
- Use periodic snapshots to track growth
- Focus on resource-intensive operations
- Compare state at different scales
- Identify memory leaks and inefficiencies

### Concurrency
- Include thread/process identifiers
- Capture synchronization points
- Analyze interleaving patterns
- Reproduce non-deterministic failures
