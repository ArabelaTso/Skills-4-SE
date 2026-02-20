---
name: failure-oriented-instrumentation
description: Selectively instruments code to capture runtime data for debugging failures and bugs. Use when investigating crashes, exceptions, unexpected behavior, test failures, or performance issues. Analyzes stack traces and error messages to identify suspicious code regions, then adds targeted logging, tracing, and assertions to capture variable values, execution paths, timing, and conditional branches. Supports Python, JavaScript/TypeScript, Java, and C/C++.
---

# Failure-Oriented Instrumentation

Strategically instrument code to capture high-signal runtime data for debugging failures, focusing only on suspicious regions rather than comprehensive instrumentation.

## Workflow

### 1. Analyze the Failure

Gather and analyze failure information:
- Error message and exception type
- Stack trace showing call chain
- Failure location (file, line, function)
- Reproduction steps or test case
- Expected vs actual behavior

Identify suspicious code regions:
- Functions in the stack trace
- Code paths leading to the failure
- Variables involved in the error
- Conditional branches that may affect the outcome

### 2. Determine Instrumentation Strategy

Based on the failure type, choose instrumentation targets:

**For crashes/exceptions:**
- Function entry/exit in stack trace
- Variable values before the crash
- Conditional branches leading to error path
- Exception handling blocks

**For incorrect results:**
- Variable values at key computation points
- Conditional branch decisions
- Loop iterations and state changes
- Function return values

**For performance issues:**
- Timing information for slow operations
- Loop iteration counts
- Resource allocation/deallocation
- Function call frequency

**For intermittent failures:**
- State variables that may cause non-determinism
- Thread/concurrency information
- External dependencies (I/O, network, time)
- Retry logic and error recovery paths

### 3. Select Instrumentation Patterns

Choose appropriate patterns based on language and context. See language-specific references:

- **Python**: [references/python.md](references/python.md)
- **JavaScript/TypeScript**: [references/javascript.md](references/javascript.md)
- **Java**: [references/java.md](references/java.md)
- **C/C++**: [references/c-cpp.md](references/c-cpp.md)

Common patterns:
- Function entry/exit logging
- Variable value tracking
- Conditional branch tracking
- Loop iteration monitoring
- Timing measurements
- Assertions for invariants

### 4. Insert Instrumentation

Apply instrumentation to identified code regions:

**Minimal approach** (start here):
- Instrument only the immediate failure location
- Add 2-3 key variable logs
- Track the critical conditional branch

**Expanded approach** (if minimal is insufficient):
- Instrument entire call chain from stack trace
- Add comprehensive variable tracking
- Monitor all branches and loops in suspicious functions

**Principles:**
- Start minimal, expand as needed
- Focus on high-signal data (variables that affect control flow)
- Avoid instrumenting stable, well-tested code
- Minimize performance overhead

### 5. Run and Collect Data

Execute the instrumented code:
- Run the failing test case or reproduction steps
- Capture all instrumentation output (logs, traces)
- Ensure instrumentation doesn't change behavior (except performance)

### 6. Analyze Results

Review captured data to identify root cause:
- Compare variable values against expectations
- Identify which branch was taken and why
- Look for unexpected state transitions
- Check timing for performance issues
- Correlate multiple data points

## Quick Start Examples

### Example 1: NullPointerException in Java

**Failure:**
```
NullPointerException at UserService.java:45
  at UserService.processUser(UserService.java:45)
  at UserController.handleRequest(UserController.java:23)
```

**Instrumentation:**
```java
public void processUser(String userId) {
    logger.debug("ENTER processUser: userId={}", userId);

    User user = userRepository.findById(userId);
    logger.debug("Retrieved user: {}", user);  // Check if null

    if (user == null) {
        logger.warn("User not found for userId={}", userId);
        return;
    }

    String email = user.getEmail();  // Line 45 - was failing here
    logger.debug("User email: {}", email);

    sendNotification(email);
}
```

### Example 2: Incorrect Calculation in Python

**Failure:**
```
AssertionError: Expected 100, got 95
  at test_calculate_total (test_billing.py:12)
  at calculate_total (billing.py:34)
```

**Instrumentation:**
```python
def calculate_total(items, discount_rate):
    logger.debug(f"ENTER calculate_total: items={items}, discount_rate={discount_rate}")

    subtotal = sum(item.price for item in items)
    logger.debug(f"Subtotal: {subtotal}")

    if discount_rate > 0:
        logger.debug(f"Applying discount: rate={discount_rate}")
        discount = subtotal * discount_rate
        logger.debug(f"Discount amount: {discount}")
    else:
        logger.debug("No discount applied")
        discount = 0

    total = subtotal - discount
    logger.debug(f"Final total: {total}")

    return total
```

### Example 3: Intermittent Test Failure in JavaScript

**Failure:**
```
Test "should process async data" fails randomly
Expected: data processed
Actual: timeout
```

**Instrumentation:**
```javascript
async function processAsyncData(dataId) {
    console.log(`ENTER processAsyncData: dataId=${dataId}, time=${Date.now()}`);

    const data = await fetchData(dataId);
    console.log(`Fetched data: ${JSON.stringify(data)}, time=${Date.now()}`);

    if (!data) {
        console.warn(`No data returned for dataId=${dataId}`);
        return null;
    }

    const processed = await processData(data);
    console.log(`Processed data: ${JSON.stringify(processed)}, time=${Date.now()}`);

    return processed;
}
```

## Instrumentation Guidelines

### What to Instrument

**High priority:**
- Functions in the stack trace
- Variables mentioned in error messages
- Conditional branches near the failure
- Loop conditions and iteration variables
- Function parameters and return values

**Medium priority:**
- State variables that affect control flow
- Resource allocations (memory, files, connections)
- External dependencies (API calls, database queries)
- Error handling and recovery logic

**Low priority:**
- Stable utility functions
- Simple getters/setters
- Well-tested library code
- Performance-critical hot paths (unless investigating performance)

### What NOT to Instrument

- Code unrelated to the failure
- Third-party libraries (unless suspected)
- Trivial operations (assignments, simple math)
- Code that would generate excessive output
- Security-sensitive operations (passwords, tokens)

### Instrumentation Best Practices

1. **Use appropriate log levels**: DEBUG for detailed tracing, INFO for key events, ERROR for exceptions
2. **Include context**: Variable names, values, types, and relevant state
3. **Mark entry/exit**: Clear boundaries for function execution
4. **Timestamp when relevant**: For timing and ordering issues
5. **Avoid side effects**: Instrumentation should not change program behavior
6. **Clean up after**: Remove temporary instrumentation once bug is fixed
7. **Consider permanence**: Some instrumentation may be valuable long-term for observability

## Language-Specific References

Load these references for detailed instrumentation patterns:

- **Python**: [references/python.md](references/python.md) - logging, tracing, decorators, context managers
- **JavaScript/TypeScript**: [references/javascript.md](references/javascript.md) - console, debug module, proxies, async patterns
- **Java**: [references/java.md](references/java.md) - SLF4J, AspectJ, wrappers, assertions
- **C/C++**: [references/c-cpp.md](references/c-cpp.md) - printf, macros, RAII, GDB scripting

## Tips

- **Start small**: Instrument one function, run, analyze, then expand if needed
- **Be specific**: Log exact variable values, not just "processing data"
- **Use structured logging**: Include variable names and context, not just values
- **Test instrumentation**: Verify logs appear and contain expected information
- **Iterate quickly**: Add instrumentation, run, analyze, repeat
- **Consider performance**: For production code, use conditional compilation or feature flags
- **Document findings**: Comment why instrumentation was added and what it revealed
