---
name: static-vulnerability-detector
description: "Statically analyze code to detect security vulnerabilities including buffer overflows, injection risks (SQL, command, XSS), insecure deserialization, improper authentication, hard-coded credentials, and unsafe cryptography. Use when: (1) Performing security code review, (2) Analyzing code for OWASP Top 10 vulnerabilities, (3) Identifying CWE-classified weaknesses, (4) Generating security audit reports, (5) Reviewing code before deployment, or (6) Assessing third-party code security. Findings categorized by CWE ID and severity (Critical/High/Medium/Low)."
---

# Static Vulnerability Detector

Analyze code for security vulnerabilities with CWE classification and severity assessment.

## Analysis Workflow

### 1. Code Scanning

Systematically examine code for vulnerability patterns:

**Memory Safety** (C/C++):
- Buffer overflows (CWE-119)
- Out-of-bounds access (CWE-125)
- Use-after-free (CWE-416)
- Double free (CWE-415)
- Null pointer dereference (CWE-476)

**Injection Vulnerabilities**:
- SQL injection (CWE-89)
- Command injection (CWE-78)
- Cross-site scripting (CWE-79)
- XML injection (CWE-91)
- LDAP injection (CWE-90)

**Authentication & Authorization**:
- Missing authentication (CWE-306)
- Improper authentication (CWE-287)
- Missing authorization (CWE-862)
- Hard-coded credentials (CWE-798)

**Cryptographic Issues**:
- Weak algorithms (CWE-327)
- Inadequate encryption (CWE-326)
- Weak random values (CWE-330)
- Missing encryption (CWE-311)

**Deserialization**:
- Untrusted deserialization (CWE-502)
- Mass assignment (CWE-915)

**Input Validation**:
- Improper validation (CWE-20)
- Path traversal (CWE-22)
- SSRF (CWE-918)

### 2. Pattern Matching

For each vulnerability category, identify:

**Dangerous Functions**:
- C/C++: `strcpy`, `sprintf`, `gets`, `scanf`
- Python: `pickle.loads`, `eval`, `exec`
- SQL: String concatenation in queries
- Shell: `os.system`, `subprocess` with `shell=True`

**Unsafe Patterns**:
- Unvalidated user input
- Missing bounds checking
- Weak cryptographic algorithms
- Hard-coded secrets
- Missing authentication decorators

**Context Analysis**:
- Data flow from user input to sink
- Sanitization and validation presence
- Authentication/authorization checks
- Error handling adequacy

### 3. Severity Assessment

Assign severity based on:

**CRITICAL**:
- Remote code execution possible
- Authentication bypass
- SQL injection with admin access
- Arbitrary file read/write

**HIGH**:
- Privilege escalation
- Sensitive data exposure
- Hard-coded credentials
- Weak cryptography for sensitive data

**MEDIUM**:
- Information disclosure
- Denial of service
- Missing input validation
- Insecure configuration

**LOW**:
- Minor information leaks
- Verbose error messages
- Missing security headers

### 4. Confidence Level

Assess confidence in finding:

**HIGH**: Clear vulnerability pattern, no mitigating factors
**MEDIUM**: Vulnerability likely but context unclear
**LOW**: Potential issue requiring manual verification

### 5. Generate Report

Structure findings as:

```markdown
## Vulnerability: [Title]

**ID**: VULN-[number]
**CWE**: CWE-[ID]
**Severity**: [CRITICAL/HIGH/MEDIUM/LOW]
**Confidence**: [HIGH/MEDIUM/LOW]
**Location**: [File:Line]

### Description
[What the vulnerability is]

### Code Snippet
```[language]
[vulnerable code]
```

### Impact
- [Potential consequences]

### Remediation
```[language]
[fixed code]
```

### References
- [CWE link]
- [OWASP reference]
```

## Vulnerability Categories

### Memory Safety (C/C++)

**Buffer Overflow (CWE-119)**:
```c
// VULNERABLE
char buf[10];
strcpy(buf, user_input);  // No bounds check
```

**Use-After-Free (CWE-416)**:
```c
// VULNERABLE
free(ptr);
ptr->field = value;  // Use after free
```

### Injection Attacks

**SQL Injection (CWE-89)**:
```python
# VULNERABLE
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
```

**Command Injection (CWE-78)**:
```python
# VULNERABLE
os.system("ping " + user_host)
```

**XSS (CWE-79)**:
```javascript
// VULNERABLE
element.innerHTML = user_input;
```

### Authentication Issues

**Missing Authentication (CWE-306)**:
```python
# VULNERABLE
@app.route('/admin')
def admin_panel():
    return render_template('admin.html')  # No auth check
```

**Hard-coded Credentials (CWE-798)**:
```python
# VULNERABLE
PASSWORD = "admin123"
API_KEY = "sk-1234567890"
```

### Cryptographic Weaknesses

**Weak Algorithm (CWE-327)**:
```python
# VULNERABLE
hash = hashlib.md5(password.encode()).hexdigest()
```

**Weak Random (CWE-330)**:
```python
# VULNERABLE
token = random.randint(1000, 9999)  # For security token
```

### Deserialization

**Untrusted Data (CWE-502)**:
```python
# VULNERABLE
obj = pickle.loads(user_data)  # RCE possible
```

### Input Validation

**Path Traversal (CWE-22)**:
```python
# VULNERABLE
with open(f'/uploads/{filename}', 'r') as f:  # ../../../etc/passwd
    content = f.read()
```

**SSRF (CWE-918)**:
```python
# VULNERABLE
response = requests.get(user_url)  # Can access internal services
```

## Detection Heuristics

### Data Flow Analysis

Track tainted data from source to sink:

**Sources** (user input):
- HTTP parameters, headers, body
- Command-line arguments
- File contents
- Environment variables
- Database queries

**Sinks** (dangerous operations):
- SQL query execution
- System command execution
- File operations
- HTML output
- Deserialization

**Sanitization** (check for):
- Input validation
- Escaping/encoding
- Parameterized queries
- Whitelist filtering

### Pattern Recognition

**Dangerous function calls**:
- Without input validation
- With user-controlled arguments
- In security-sensitive contexts

**Missing security controls**:
- No authentication decorator
- No authorization check
- No CSRF protection
- No rate limiting

**Weak configurations**:
- Debug mode enabled
- Verbose errors
- Insecure defaults

## CWE Reference

For detailed vulnerability patterns and remediation, see [cwe_patterns.md](references/cwe_patterns.md).

Key CWE categories:
- Memory safety (CWE-119, 125, 416, 415)
- Injection (CWE-89, 78, 79, 91)
- Authentication (CWE-287, 306, 798, 862)
- Cryptography (CWE-327, 326, 330, 311)
- Deserialization (CWE-502, 915)
- Input validation (CWE-20, 22, 918)

## Report Format

### Summary Section

```markdown
# Security Vulnerability Report

**Scan Date**: [Date]
**Code Base**: [Project]
**Total Findings**: [Count]

## Severity Breakdown
- Critical: [Count]
- High: [Count]
- Medium: [Count]
- Low: [Count]
```

### Detailed Findings

For each vulnerability:
- Unique ID
- CWE classification
- Severity and confidence
- Location (file, line, function)
- Description
- Code snippet
- Impact assessment
- Remediation guidance
- References

### Recommendations

Prioritized action items:
1. Fix critical vulnerabilities immediately
2. Address high-severity issues
3. Plan remediation for medium/low issues
4. Implement security best practices

## Examples

For complete vulnerability detection examples including:
- SQL injection analysis
- Buffer overflow detection
- Hard-coded credentials
- Insecure deserialization
- Missing authentication
- Weak cryptography

See [examples.md](references/examples.md).

## Analysis Tips

- **Context matters**: Consider surrounding code and mitigations
- **False positives**: Mark uncertain findings as low confidence
- **Data flow**: Trace user input to dangerous sinks
- **Defense in depth**: Note multiple security layers
- **Language-specific**: Apply appropriate patterns per language
- **Framework awareness**: Consider framework protections
- **Configuration**: Check for insecure settings
- **Dependencies**: Note vulnerable library versions
- **Completeness**: Scan all code paths
- **Prioritize**: Focus on critical and high severity first
