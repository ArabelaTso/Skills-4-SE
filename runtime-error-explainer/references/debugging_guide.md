# Debugging Guide

Systematic debugging strategies, tools, and techniques for complex runtime and compilation errors.

## Table of Contents

1. [Systematic Debugging Process](#systematic-debugging-process)
2. [Python Debugging Tools](#python-debugging-tools)
3. [Java Debugging Tools](#java-debugging-tools)
4. [Common Debugging Techniques](#common-debugging-techniques)
5. [Advanced Strategies](#advanced-strategies)

---

## Systematic Debugging Process

Follow this methodical approach when errors are not immediately obvious:

### 1. Reproduce the Error

**Goal:** Ensure error happens consistently

```
Steps:
1. Document exact steps to trigger error
2. Note any variations (works sometimes, fails sometimes)
3. Identify minimum inputs required to trigger error
4. Test if error occurs in different environments
```

**Questions to ask:**
- Does the error happen every time?
- Does it only happen with specific input?
- Did it work before? What changed?
- Can you reproduce it in a simpler test case?

### 2. Isolate the Problem

**Goal:** Narrow down to the smallest failing code segment

```
Binary search approach:
1. Comment out half the code
2. Does error still occur?
   - YES: Problem is in remaining half
   - NO: Problem is in commented half
3. Repeat until you find the exact line(s)
```

**Techniques:**
- Create minimal reproduction (remove everything unrelated)
- Test individual functions in isolation
- Use print statements to identify last successful operation

### 3. Understand the Error

**Goal:** Comprehend what the error message tells you

```
Read the error message carefully:
1. Error type (AttributeError, NullPointerException, etc.)
2. Line number where error occurred
3. Stack trace (call chain leading to error)
4. Expected vs actual values (if provided)
```

**Don't skip the stack trace!** It shows:
- Where error originated
- How execution got there
- Whether error is in your code or library code

### 4. Form Hypothesis

**Goal:** Develop theory about root cause

```
Based on error and context, hypothesize:
1. What might have caused this?
2. Why would this value be null/wrong?
3. What assumptions might be violated?
4. What recent changes could relate?
```

### 5. Test Hypothesis

**Goal:** Verify or disprove your theory

```
Add logging/debugging:
1. Print variable values before error
2. Add assertions to check assumptions
3. Use debugger to inspect state
4. Test edge cases
```

### 6. Fix and Verify

**Goal:** Apply fix and confirm it solves the problem

```
After fixing:
1. Run the code that previously failed
2. Test edge cases
3. Run related tests
4. Verify no new issues introduced
```

---

## Python Debugging Tools

### Built-in pdb Debugger

**Basic Usage:**

```python
import pdb

def calculate(x, y):
    result = x + y
    pdb.set_trace()  # Debugger stops here
    return result

calculate(5, 10)
```

**Common pdb Commands:**

```
n (next)       - Execute next line
s (step)       - Step into function
c (continue)   - Continue execution
l (list)       - Show source code around current line
p var          - Print variable value
pp var         - Pretty-print variable
w (where)      - Show stack trace
q (quit)       - Quit debugger
h (help)       - Show help
```

**Post-mortem Debugging:**

```python
import pdb

try:
    # Code that might fail
    result = risky_operation()
except Exception:
    pdb.post_mortem()  # Start debugger at exception point
```

### breakpoint() (Python 3.7+)

Simpler than import pdb:

```python
def process_data(items):
    total = 0
    for item in items:
        breakpoint()  # Debugger starts here
        total += item['value']
    return total
```

### Logging

**Strategic Logging:**

```python
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def process_user(user_id):
    logging.debug(f"Processing user {user_id}")
    user = get_user(user_id)
    logging.debug(f"Retrieved user: {user}")

    if user is None:
        logging.error(f"User {user_id} not found")
        return None

    logging.info(f"Processing user {user.name}")
    return user
```

### Python Traceback Module

**Get detailed traceback info:**

```python
import traceback
import sys

try:
    risky_operation()
except Exception as e:
    # Print full traceback
    traceback.print_exc()

    # Get traceback as string
    tb_str = ''.join(traceback.format_exception(*sys.exc_info()))
    print(tb_str)

    # Get traceback details
    tb_lines = traceback.format_tb(sys.exc_info()[2])
    for line in tb_lines:
        print(line)
```

### iPython/Jupyter Debugging

```python
# In Jupyter/iPython, automatically start debugger on exception
%pdb on

# Run code - debugger starts if exception occurs
def buggy_function():
    x = None
    return x.upper()  # AttributeError - debugger starts

buggy_function()
```

---

## Java Debugging Tools

### Using jdb (Command-Line Debugger)

**Start debugging:**

```bash
# Compile with debug info
javac -g MyClass.java

# Run with jdb
jdb MyClass

# Common jdb commands:
stop at MyClass:15     # Set breakpoint at line 15
stop in MyClass.myMethod  # Set breakpoint at method
run                    # Start execution
step                   # Step into next line
next                   # Execute next line (don't step into)
cont                   # Continue execution
print variable         # Print variable value
locals                 # List all local variables
where                  # Show stack trace
quit                   # Exit debugger
```

### IDE Debugging (IntelliJ/Eclipse)

**IntelliJ IDEA:**
1. Click left margin to set breakpoint
2. Click "Debug" button (or Shift+F9)
3. When breakpoint hits:
   - F8: Step over
   - F7: Step into
   - Shift+F8: Step out
   - F9: Resume
4. Hover over variables to see values
5. Use "Evaluate Expression" (Alt+F8) to test code

**Eclipse:**
1. Double-click left margin to set breakpoint
2. Right-click → Debug As → Java Application
3. When breakpoint hits:
   - F6: Step over
   - F5: Step into
   - F7: Step out
   - F8: Resume
4. Variables view shows current values
5. Use "Display" to evaluate expressions

### Logging with java.util.logging

```java
import java.util.logging.*;

public class MyClass {
    private static final Logger logger = Logger.getLogger(MyClass.class.getName());

    public void processUser(int userId) {
        logger.info("Processing user " + userId);

        User user = getUser(userId);
        logger.fine("Retrieved user: " + user);

        if (user == null) {
            logger.severe("User " + userId + " not found!");
            return;
        }

        logger.info("Processing user " + user.getName());
    }
}
```

### Logging with SLF4J/Logback (Recommended)

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MyClass {
    private static final Logger log = LoggerFactory.getLogger(MyClass.class);

    public void processOrder(int orderId) {
        log.debug("Processing order {}", orderId);

        Order order = getOrder(orderId);
        log.trace("Order details: {}", order);

        if (order == null) {
            log.error("Order {} not found!", orderId);
            return;
        }

        log.info("Order {} processed successfully", orderId);
    }
}
```

### Stack Trace Analysis

```java
try {
    riskyOperation();
} catch (Exception e) {
    // Print stack trace to stderr
    e.printStackTrace();

    // Get stack trace as string
    StringWriter sw = new StringWriter();
    PrintWriter pw = new PrintWriter(sw);
    e.printStackTrace(pw);
    String stackTrace = sw.toString();
    System.out.println(stackTrace);

    // Analyze stack trace elements
    for (StackTraceElement element : e.getStackTrace()) {
        System.out.println("Class: " + element.getClassName());
        System.out.println("Method: " + element.getMethodName());
        System.out.println("Line: " + element.getLineNumber());
    }
}
```

---

## Common Debugging Techniques

### 1. Print Debugging (Quickest but not always best)

**Python:**
```python
def calculate_total(items):
    total = 0
    print(f"DEBUG: Processing {len(items)} items")  # Debug print

    for item in items:
        print(f"DEBUG: Item = {item}, Current total = {total}")  # Debug print
        total += item['price']

    print(f"DEBUG: Final total = {total}")  # Debug print
    return total
```

**Java:**
```java
public int calculateTotal(List<Item> items) {
    int total = 0;
    System.out.println("DEBUG: Processing " + items.size() + " items");

    for (Item item : items) {
        System.out.println("DEBUG: Item = " + item + ", Current total = " + total);
        total += item.getPrice();
    }

    System.out.println("DEBUG: Final total = " + total);
    return total;
}
```

**Pros:**
- Quick and easy
- Works anywhere

**Cons:**
- Clutters code
- Easy to forget to remove
- Can affect performance

**Best practice:** Use logging instead of print

### 2. Assertion Debugging

**Python:**
```python
def divide(a, b):
    assert b != 0, "Divisor must not be zero"
    assert isinstance(a, (int, float)), "a must be numeric"
    assert isinstance(b, (int, float)), "b must be numeric"

    return a / b
```

**Java:**
```java
public double divide(double a, double b) {
    assert b != 0 : "Divisor must not be zero";
    return a / b;
}

// Run with: java -ea MyClass (enable assertions)
```

**When to use:**
- Verify assumptions during development
- Check preconditions/postconditions
- Validate internal invariants

### 3. Binary Search Debugging

When code suddenly stops working:

```
1. Identify last known good state (e.g., git commit)
2. Identify first known bad state (current code)
3. Test midpoint:
   git checkout <midpoint-commit>
   Test if bug exists
4. If bug exists: Search between last-good and midpoint
   If bug doesn't exist: Search between midpoint and current
5. Repeat until you find the exact commit that introduced bug
```

**Git bisect automates this:**
```bash
git bisect start
git bisect bad              # Current commit is bad
git bisect good <commit>    # This commit was good
# Git checks out midpoint
# Test and mark as good or bad:
git bisect good  # or git bisect bad
# Repeat until git identifies the problematic commit
git bisect reset  # Return to original state
```

### 4. Rubber Duck Debugging

Explain the code line-by-line to an inanimate object (rubber duck).

**Process:**
1. Start from beginning of function
2. Explain what each line does
3. Explain what you expect to happen
4. Explain what actually happens

**Why it works:**
- Forces you to slow down
- Makes you question assumptions
- Often reveals logic errors

---

## Advanced Strategies

### Debugging Concurrent Code

**Python threading issues:**

```python
import threading
import logging

# Enable thread name in logging
logging.basicConfig(
    format='%(threadName)s - %(message)s',
    level=logging.DEBUG
)

def worker(name, counter):
    logging.debug(f"Worker {name} starting, counter={counter}")
    # ... do work ...
    logging.debug(f"Worker {name} finished")

# Create threads
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(f"Thread-{i}", i), name=f"Worker-{i}")
    threads.append(t)
    t.start()
```

**Java threading issues:**

```java
// Use thread dumps to diagnose deadlocks
// Send SIGQUIT to running Java process:
kill -3 <pid>

// Or use jstack
jstack <pid>

// Look for "BLOCKED" threads in output
```

### Memory Leak Debugging

**Python:**

```python
import tracemalloc

# Start tracing
tracemalloc.start()

# Run code that might leak memory
large_list = []
for i in range(1000000):
    large_list.append([i] * 100)

# Take snapshot
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("Top 10 memory allocations:")
for stat in top_stats[:10]:
    print(stat)
```

**Java:**

```bash
# Run with verbose GC
java -verbose:gc -XX:+PrintGCDetails MyClass

# Take heap dump
jmap -dump:format=b,file=heap.bin <pid>

# Analyze with tools like VisualVM or Eclipse MAT
```

### Performance Debugging

**Python profiling:**

```python
import cProfile
import pstats

# Profile function
cProfile.run('my_function()', 'profile_stats')

# Analyze results
p = pstats.Stats('profile_stats')
p.sort_stats('cumulative')
p.print_stats(10)  # Top 10 slowest functions
```

**Java profiling:**

```bash
# Use Java Flight Recorder
java -XX:+UnlockCommercialFeatures -XX:+FlightRecorder \
     -XX:StartFlightRecording=duration=60s,filename=recording.jfr \
     MyClass

# Or use VisualVM, YourKit, or JProfiler
```

### Debugging Third-Party Libraries

**When error is in library code:**

1. **Check library version** - Is it up to date?
   ```bash
   pip show requests  # Python
   mvn dependency:tree  # Java
   ```

2. **Read library source** - Understand what it's trying to do
   ```python
   import inspect
   print(inspect.getsourcefile(problematic_function))
   ```

3. **Check issue tracker** - Has someone else reported this?
   - GitHub issues
   - Stack Overflow

4. **Try different version** - Downgrade/upgrade to see if bug exists
   ```bash
   pip install requests==2.25.0  # Specific version
   ```

5. **Minimal reproduction** - Create smallest example that triggers bug

### Remote Debugging

**Python remote debugging with pdb:**

```python
import pdb
import sys

# Allow remote connection
pdb.Pdb(stdin=sys.stdin, stdout=sys.stdout).set_trace()
```

**Java remote debugging:**

```bash
# Start Java with debug agent
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 MyClass

# Connect from IDE (IntelliJ/Eclipse) to localhost:5005
```

---

## Debugging Checklist

Before asking for help, have you:

- [ ] Read the full error message and stack trace?
- [ ] Identified the exact line where error occurs?
- [ ] Reproduced the error consistently?
- [ ] Created a minimal reproduction?
- [ ] Checked recent changes (git diff)?
- [ ] Verified assumptions with print statements or debugger?
- [ ] Searched online for the error message?
- [ ] Checked library documentation?
- [ ] Tried simplifying the code?
- [ ] Tested with different inputs?
- [ ] Verified environment (dependencies, versions)?
- [ ] Consulted rubber duck?

---

## When to Ask for Help

Ask for help when:

1. **After reasonable debugging effort** - You've tried the above strategies
2. **With context** - Provide error message, code, what you've tried
3. **With minimal reproduction** - Smallest code that demonstrates problem
4. **On appropriate platform** - Stack Overflow, GitHub issues, forums

**Good help request includes:**
- Full error message and stack trace
- Minimal code that reproduces error
- What you expected vs what happened
- What you've already tried
- Environment details (language version, OS, dependencies)
