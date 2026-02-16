# Analysis Strategies by Vulnerability Type

## Memory Safety Analysis

### Buffer Overflow Analysis

**Step 1: Identify the vulnerable operation**
- Look for array/buffer writes
- String operations (strcpy, strcat, sprintf)
- Memory operations (memcpy, memmove)

**Step 2: Trace data flow**
- Where does the data come from?
- Is it user-controlled or external input?
- What transformations occur?

**Step 3: Find missing checks**
- Is buffer size validated?
- Is input length checked?
- Are loop bounds correct?

**Step 4: Determine root cause**
- What assumption was violated?
- What check should exist but doesn't?
- Why did the developer miss this?

**Example Analysis:**
```c
void handle_request(char *request) {
    char buffer[256];
    strcpy(buffer, request);  // Vulnerable line
    process(buffer);
}
```

**Root Cause:** Assumes request length < 256 bytes. Missing: `strlen(request) < sizeof(buffer)` check.

### Use-After-Free Analysis

**Step 1: Identify the free operation**
- Where is memory deallocated?
- What triggers the deallocation?

**Step 2: Find subsequent uses**
- Where is the pointer used after free?
- What operations access the freed memory?

**Step 3: Analyze lifetime management**
- Who owns the object?
- Is there reference counting?
- Are there multiple paths to free?

**Step 4: Determine root cause**
- Why wasn't the pointer invalidated?
- What ownership assumption was violated?
- Is there a race condition?

## Injection Analysis

### SQL Injection Analysis

**Step 1: Identify query construction**
- How is the SQL query built?
- String concatenation vs parameterized?

**Step 2: Trace input sources**
- Where does user input enter?
- Is it sanitized or validated?

**Step 3: Check escaping/encoding**
- Are special characters escaped?
- Is the escaping context-appropriate?

**Step 4: Determine root cause**
- Why is input treated as code?
- What trust boundary was violated?
- Why wasn't parameterization used?

**Example Analysis:**
```python
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
```

**Root Cause:** Treats user_id as trusted code. Missing: parameterized query or input validation.

### Command Injection Analysis

**Step 1: Identify command execution**
- system(), popen(), exec() calls
- Shell invocation points

**Step 2: Trace command construction**
- How is the command string built?
- What parts are user-controlled?

**Step 3: Check sanitization**
- Are shell metacharacters filtered?
- Is input properly quoted?

**Step 4: Determine root cause**
- Why is shell invocation necessary?
- What safer alternative exists?
- Why wasn't input validated?

## Authentication/Authorization Analysis

### Authentication Bypass Analysis

**Step 1: Map authentication flow**
- What are the authentication steps?
- What checks are performed?

**Step 2: Identify logic errors**
- Are there alternative paths?
- Can checks be skipped?
- Are there race conditions?

**Step 3: Check state management**
- How is authentication state stored?
- Can it be manipulated?

**Step 4: Determine root cause**
- What logic flaw exists?
- What assumption was violated?
- Why wasn't the check comprehensive?

**Example Analysis:**
```python
def login(username, password):
    user = get_user(username)
    if user and user.password == hash(password):
        return True
    if username == "admin":  # Logic error
        return True
    return False
```

**Root Cause:** Logic error allows admin bypass without password. Missing: proper authentication for all paths.

### Authorization Analysis

**Step 1: Identify protected resource**
- What resource is being accessed?
- What permissions are required?

**Step 2: Find authorization checks**
- Where are permissions verified?
- Are checks comprehensive?

**Step 3: Check for bypasses**
- Can checks be circumvented?
- Are there alternative access paths?

**Step 4: Determine root cause**
- Why is the check missing/incomplete?
- What assumption about access control failed?

## Concurrency Analysis

### Race Condition Analysis

**Step 1: Identify shared state**
- What data is accessed by multiple threads?
- What operations modify shared state?

**Step 2: Check synchronization**
- Are locks used?
- Is lock granularity correct?
- Are all accesses protected?

**Step 3: Find TOCTOU patterns**
- Check-then-use sequences
- Time gaps between operations

**Step 4: Determine root cause**
- Why is synchronization missing?
- What atomicity assumption was violated?
- Why wasn't the race considered?

**Example Analysis:**
```c
if (file_exists(path)) {      // Check
    fd = open(path, O_RDWR);  // Use
    // Race: file can change between check and use
}
```

**Root Cause:** TOCTOU vulnerability. Missing: atomic check-and-open operation.

## Logic Vulnerability Analysis

### Integer Overflow Analysis

**Step 1: Identify arithmetic operations**
- Multiplication, addition on size calculations
- Type conversions

**Step 2: Check for overflow detection**
- Are results validated?
- Are safe arithmetic functions used?

**Step 3: Trace consequences**
- How is the result used?
- What happens if overflow occurs?

**Step 4: Determine root cause**
- Why is overflow check missing?
- What assumption about value ranges failed?

**Example Analysis:**
```c
size_t total = width * height * 4;
buffer = malloc(total);
```

**Root Cause:** Assumes width * height * 4 doesn't overflow. Missing: overflow check before allocation.

## Information Disclosure Analysis

### Path Traversal Analysis

**Step 1: Identify file operations**
- File reads, writes, includes
- Path construction

**Step 2: Trace path components**
- What parts are user-controlled?
- Is path sanitized?

**Step 3: Check canonicalization**
- Are ".." sequences removed?
- Are symbolic links resolved?

**Step 4: Determine root cause**
- Why is path validation missing?
- What assumption about input failed?

## General Analysis Framework

### For Any Vulnerability

1. **Understand the vulnerability**
   - What is the security impact?
   - How is it exploited?

2. **Identify the vulnerable code**
   - What line/function is problematic?
   - What operation is unsafe?

3. **Trace the data flow**
   - Where does problematic data originate?
   - How does it reach the vulnerable point?

4. **Find the root cause**
   - What assumption was violated?
   - What check is missing?
   - What invariant was broken?
   - What interaction is unsafe?

5. **Determine the fix**
   - What validation should be added?
   - What design should change?
   - What safer alternative exists?

6. **Assess systemic issues**
   - Is this pattern repeated elsewhere?
   - What process failed to prevent this?
   - What tools could detect this?
