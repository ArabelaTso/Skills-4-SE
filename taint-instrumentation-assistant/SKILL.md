---
name: taint-instrumentation-assistant
description: "Instruments code to track the flow of untrusted or sensitive data at runtime, enabling detection of injection vulnerabilities, data leaks, and privilege violations. Use when users need to: (1) Track untrusted input propagation through code, (2) Detect SQL injection, XSS, or command injection vulnerabilities, (3) Identify sensitive data leaks, (4) Monitor privilege escalation paths, (5) Perform dynamic taint analysis for security testing. Supports Python, Java, JavaScript, and C/C++ with configurable taint sources and sinks."
---

# Taint Instrumentation Assistant

Instrument code to track untrusted and sensitive data flow for security vulnerability detection.

## Workflow

Follow these steps to add taint tracking instrumentation:

### 1. Identify Taint Sources and Sinks

Define what data to track and where violations occur:

**Taint sources** (untrusted/sensitive data origins):
- User input (HTTP parameters, form data, command-line args)
- File reads (configuration files, user uploads)
- Database queries (user-provided data)
- Network input (API responses, socket data)
- Environment variables

**Taint sinks** (dangerous operations):
- SQL queries (SQL injection risk)
- System commands (command injection risk)
- HTML output (XSS risk)
- File operations (path traversal risk)
- Eval/exec statements (code injection risk)
- Network output (data leak risk)

### 2. Instrument Taint Sources

Mark data from untrusted sources as tainted:

```python
# Mark user input as tainted
def mark_tainted(value, source):
    """Mark a value as tainted from a specific source"""
    if hasattr(value, '__taint__'):
        value.__taint__ = source
    return value

# Example: HTTP parameter
user_input = request.GET['username']
user_input = mark_tainted(user_input, source="HTTP_PARAM")
```

### 3. Propagate Taint Through Operations

Track taint as data flows through the program:

```python
# Taint propagation for string operations
def tainted_concat(str1, str2):
    result = str1 + str2
    # If either input is tainted, result is tainted
    if hasattr(str1, '__taint__') or hasattr(str2, '__taint__'):
        result.__taint__ = getattr(str1, '__taint__', None) or getattr(str2, '__taint__', None)
    return result
```

### 4. Check Taint at Sinks

Detect when tainted data reaches dangerous operations:

```python
# Check for tainted data at SQL sink
def execute_query(query):
    if hasattr(query, '__taint__'):
        print(f"TAINT VIOLATION: Tainted data from {query.__taint__} used in SQL query")
        print(f"Query: {query}")
        # Optionally: raise exception or log for analysis
    # Execute query...
```

### 5. Generate Instrumented Code

Produce code with complete taint tracking:

- Instrumented source code with taint tracking
- Taint policy configuration (sources and sinks)
- Violation report format
- Usage instructions

## Language-Specific Patterns

### Python

```python
# Taint tracking infrastructure
class TaintedStr(str):
    """String wrapper that carries taint information"""
    def __new__(cls, value, taint_source=None):
        instance = super().__new__(cls, value)
        instance.taint_source = taint_source
        return instance

    def __add__(self, other):
        result = TaintedStr(super().__add__(other))
        result.taint_source = self.taint_source or getattr(other, 'taint_source', None)
        return result

# Mark taint source
def get_user_input():
    user_data = input("Enter username: ")
    return TaintedStr(user_data, taint_source="USER_INPUT")

# Check taint sink
def execute_sql(query):
    if isinstance(query, TaintedStr) and query.taint_source:
        print(f"[TAINT VIOLATION] SQL Injection risk!")
        print(f"  Source: {query.taint_source}")
        print(f"  Query: {query}")
        raise SecurityError("Tainted data in SQL query")
    # Execute query...

# Example usage
username = get_user_input()
query = TaintedStr("SELECT * FROM users WHERE name = '") + username + TaintedStr("'")
execute_sql(query)  # Triggers violation
```

### Java

```java
// Taint tracking class
class TaintedString {
    private String value;
    private String taintSource;

    public TaintedString(String value, String taintSource) {
        this.value = value;
        this.taintSource = taintSource;
    }

    public String getValue() { return value; }
    public String getTaintSource() { return taintSource; }
    public boolean isTainted() { return taintSource != null; }

    public TaintedString concat(TaintedString other) {
        String newValue = this.value + other.value;
        String newSource = this.taintSource != null ? this.taintSource : other.taintSource;
        return new TaintedString(newValue, newSource);
    }
}

// Mark taint source
TaintedString getUserInput() {
    Scanner scanner = new Scanner(System.in);
    String input = scanner.nextLine();
    return new TaintedString(input, "USER_INPUT");
}

// Check taint sink
void executeSQL(TaintedString query) {
    if (query.isTainted()) {
        System.err.println("[TAINT VIOLATION] SQL Injection risk!");
        System.err.println("  Source: " + query.getTaintSource());
        System.err.println("  Query: " + query.getValue());
        throw new SecurityException("Tainted data in SQL query");
    }
    // Execute query...
}
```

### JavaScript

```javascript
// Taint tracking wrapper
class TaintedString {
    constructor(value, taintSource = null) {
        this.value = value;
        this.taintSource = taintSource;
    }

    concat(other) {
        const newValue = this.value + (other.value || other);
        const newSource = this.taintSource || other.taintSource;
        return new TaintedString(newValue, newSource);
    }

    toString() {
        return this.value;
    }
}

// Mark taint source
function getUserInput() {
    const input = prompt("Enter username:");
    return new TaintedString(input, "USER_INPUT");
}

// Check taint sink
function executeSQL(query) {
    if (query instanceof TaintedString && query.taintSource) {
        console.error("[TAINT VIOLATION] SQL Injection risk!");
        console.error(`  Source: ${query.taintSource}`);
        console.error(`  Query: ${query.value}`);
        throw new Error("Tainted data in SQL query");
    }
    // Execute query...
}
```

## Common Vulnerability Patterns

### SQL Injection Detection

```python
# Original vulnerable code
def login(username, password):
    query = f"SELECT * FROM users WHERE name='{username}' AND pass='{password}'"
    return db.execute(query)

# Instrumented code
def login(username, password):
    # Mark inputs as tainted
    username = TaintedStr(username, "HTTP_PARAM:username")
    password = TaintedStr(password, "HTTP_PARAM:password")

    # Build query (taint propagates)
    query = TaintedStr(f"SELECT * FROM users WHERE name='") + username + TaintedStr("' AND pass='") + password + TaintedStr("'")

    # Check at sink
    if isinstance(query, TaintedStr) and query.taint_source:
        print(f"[TAINT VIOLATION] SQL Injection detected!")
        print(f"  Tainted input: {query.taint_source}")
        print(f"  Query: {query}")

    return db.execute(str(query))
```

### XSS Detection

```python
# Original vulnerable code
def render_greeting(name):
    return f"<h1>Hello, {name}!</h1>"

# Instrumented code
def render_greeting(name):
    # Mark input as tainted
    name = TaintedStr(name, "HTTP_PARAM:name")

    # Build HTML (taint propagates)
    html = TaintedStr("<h1>Hello, ") + name + TaintedStr("!</h1>")

    # Check at sink (HTML output)
    if isinstance(html, TaintedStr) and html.taint_source:
        print(f"[TAINT VIOLATION] XSS risk detected!")
        print(f"  Tainted input: {html.taint_source}")
        print(f"  HTML: {html}")

    return str(html)
```

### Command Injection Detection

```python
# Original vulnerable code
def process_file(filename):
    os.system(f"cat {filename}")

# Instrumented code
def process_file(filename):
    # Mark input as tainted
    filename = TaintedStr(filename, "USER_INPUT:filename")

    # Build command (taint propagates)
    command = TaintedStr("cat ") + filename

    # Check at sink (system command)
    if isinstance(command, TaintedStr) and command.taint_source:
        print(f"[TAINT VIOLATION] Command Injection risk!")
        print(f"  Tainted input: {command.taint_source}")
        print(f"  Command: {command}")

    os.system(str(command))
```

## Taint Policy Configuration

```python
# taint_policy.py
TAINT_SOURCES = {
    "HTTP_PARAM": ["request.GET", "request.POST", "request.args"],
    "USER_INPUT": ["input()", "sys.stdin.read()"],
    "FILE_READ": ["open().read()", "Path.read_text()"],
    "ENV_VAR": ["os.getenv()", "os.environ"],
}

TAINT_SINKS = {
    "SQL_QUERY": ["db.execute()", "cursor.execute()"],
    "SYSTEM_CMD": ["os.system()", "subprocess.call()"],
    "HTML_OUTPUT": ["render_template()", "HttpResponse()"],
    "FILE_WRITE": ["open().write()", "Path.write_text()"],
    "EVAL": ["eval()", "exec()"],
}

TAINT_ENABLED = True
REPORT_FORMAT = "detailed"  # or "summary"
```

## Output Format

### Taint Violation Report

```markdown
## Taint Analysis Report

**File**: app.py
**Analysis Date**: 2024-02-17

### Violations Detected

#### Violation 1: SQL Injection Risk
- **Severity**: HIGH
- **Location**: app.py:45
- **Taint Source**: HTTP_PARAM:username
- **Taint Sink**: db.execute()
- **Data Flow**:
  1. User input from HTTP parameter 'username' (line 42)
  2. String concatenation in query building (line 44)
  3. Passed to db.execute() without sanitization (line 45)
- **Recommendation**: Use parameterized queries

#### Violation 2: XSS Risk
- **Severity**: MEDIUM
- **Location**: app.py:78
- **Taint Source**: HTTP_PARAM:comment
- **Taint Sink**: render_template()
- **Data Flow**:
  1. User input from HTTP parameter 'comment' (line 75)
  2. Embedded in HTML template (line 78)
- **Recommendation**: Use HTML escaping

### Summary
- Total violations: 2
- High severity: 1
- Medium severity: 1
- Low severity: 0
```

## Best Practices

1. **Comprehensive source marking**: Mark all untrusted input sources
2. **Complete propagation**: Track taint through all operations
3. **Strict sink checking**: Verify all dangerous operations
4. **Minimal false positives**: Use precise taint rules
5. **Performance consideration**: Optimize for production use
6. **Clear reporting**: Provide actionable violation reports

## Advanced Features

### Sanitization Tracking

```python
def sanitize_sql(value):
    """Remove taint after sanitization"""
    if isinstance(value, TaintedStr):
        # Sanitize and remove taint
        sanitized = value.replace("'", "''")
        return str(sanitized)  # Return regular string (untainted)
    return value

# Usage
username = TaintedStr(user_input, "HTTP_PARAM")
safe_username = sanitize_sql(username)  # No longer tainted
query = f"SELECT * FROM users WHERE name='{safe_username}'"  # Safe
```

### Multi-Level Taint

```python
class TaintLevel:
    UNTAINTED = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TaintedStr(str):
    def __init__(self, value, taint_level=TaintLevel.UNTAINTED):
        self.taint_level = taint_level

# Different sources have different taint levels
public_data = TaintedStr(data, TaintLevel.LOW)
user_input = TaintedStr(input, TaintLevel.HIGH)
```

## Constraints

- **Preserve semantics**: Taint tracking shouldn't change program behavior
- **Minimal overhead**: Keep performance impact low
- **Complete coverage**: Track all taint propagation paths
- **Accurate detection**: Minimize false positives and negatives
