---
name: vulnerability-pattern-matcher
description: Detects security vulnerabilities by matching code against known vulnerability patterns, insecure coding idioms, and CVE-style patterns. Explains why patterns are risky and under what conditions they are exploitable. Use when analyzing code for security issues, reviewing for common vulnerabilities, or assessing exploitability of suspicious code patterns.
---

# Vulnerability Pattern Matcher

## Overview

This skill detects security vulnerabilities by matching code against a comprehensive database of known vulnerability patterns, insecure coding idioms, and historical CVE-style patterns. It identifies risky code, explains why each pattern is dangerous, assesses exploitability conditions, and provides severity ratings with confidence levels.

## Detection Workflow

Follow these steps to detect and assess vulnerabilities:

### 1. Analyze Code Structure

**Identify key security-relevant elements:**
- User input sources (request parameters, form data, file uploads)
- Data sinks (database queries, file operations, command execution)
- Authentication and authorization mechanisms
- Cryptographic operations
- Network communications
- File and resource handling

**Map data flow:**
- Trace user input through the application
- Identify where untrusted data reaches sensitive operations
- Note any validation or sanitization applied

### 2. Match Vulnerability Patterns

**Scan for known patterns:**
- Injection vulnerabilities (SQL, NoSQL, LDAP, XSS, command injection)
- Authentication issues (hardcoded credentials, weak session management)
- Cryptographic failures (weak algorithms, insecure random numbers)
- Access control problems (IDOR, missing authorization)
- Deserialization vulnerabilities
- Path traversal and file inclusion
- SSRF and XXE
- Buffer overflows and memory safety
- Race conditions

**For each match:**
- Identify the specific pattern
- Note the exact code location
- Determine the vulnerability category

### 3. Assess Exploitability

**For each detected vulnerability, evaluate:**

**Attack Complexity:**
- Low: Simple exploit, no special conditions required
- Medium: Requires specific conditions, timing, or configuration
- High: Complex exploit chain, rare conditions, or significant obstacles

**Privileges Required:**
- None: Unauthenticated attacker can exploit
- Low: Basic user account needed
- High: Administrative or privileged access required

**User Interaction:**
- None: Fully automated exploit
- Required: Victim must take action (click link, open file, etc.)

**Exploitation Conditions:**
- What must be true for successful exploitation?
- Are there mitigating controls present?
- What is the attack surface?

### 4. Determine Severity

**Critical:**
- Remote code execution
- Authentication bypass
- Complete system compromise
- Mass data breach

**High:**
- Privilege escalation
- Sensitive data exposure
- SQL injection with data access
- SSRF to internal services

**Medium:**
- XSS with session theft
- IDOR to user data
- Information disclosure
- Weak cryptography

**Low:**
- Minor information leakage
- Low-impact XSS
- Configuration issues
- Verbose error messages

### 5. Generate Report

**For each vulnerability, provide:**
- Pattern name and category
- Code location (file:line)
- Why the pattern is risky
- Exploitation conditions
- Severity level
- Detection confidence (High/Medium/Low)
- Recommended fix

## Detection Examples

### Example 1: SQL Injection

**Code (Python):**
```python
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()
```

**Detection:**
- Pattern: SQL Injection (String Concatenation)
- Location: Line 2
- Category: Injection Vulnerability

**Why Risky:**
User input is directly concatenated into SQL query without parameterization. Attacker can inject SQL code to bypass authentication, extract data, or modify the database.

**Exploitation Conditions:**
- User controls `username` parameter
- No input validation or sanitization
- Database errors may be exposed to attacker

**Severity:** High
**Confidence:** High (95%)

**Recommended Fix:**
```python
def get_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchone()
```

### Example 2: Hardcoded Credentials

**Code (JavaScript):**
```javascript
const config = {
    apiKey: "sk-1234567890abcdef",
    dbPassword: "admin123",
    jwtSecret: "my-secret-key"
};
```

**Detection:**
- Pattern: Hardcoded Credentials
- Location: Lines 2-4
- Category: Authentication & Session Management

**Why Risky:**
Credentials are embedded in source code and likely committed to version control. Anyone with repository access can authenticate as the application. Credentials are difficult to rotate if compromised.

**Exploitation Conditions:**
- Code repository is public or leaked
- Credentials are still valid
- No additional authentication factors

**Severity:** Critical
**Confidence:** High (100%)

**Recommended Fix:**
```javascript
const config = {
    apiKey: process.env.API_KEY,
    dbPassword: process.env.DB_PASSWORD,
    jwtSecret: process.env.JWT_SECRET
};
```

### Example 3: XSS via innerHTML

**Code (JavaScript):**
```javascript
function displayWelcome(username) {
    document.getElementById('welcome').innerHTML = "Hello " + username;
}
```

**Detection:**
- Pattern: DOM-based XSS
- Location: Line 2
- Category: Cross-Site Scripting

**Why Risky:**
User-controlled data is directly inserted into DOM via innerHTML without encoding. Attacker can inject JavaScript to steal cookies, session tokens, or perform actions as the victim.

**Exploitation Conditions:**
- `username` contains user input
- No Content-Security-Policy
- Sensitive data in cookies or localStorage

**Severity:** Medium
**Confidence:** High (90%)

**Recommended Fix:**
```javascript
function displayWelcome(username) {
    document.getElementById('welcome').textContent = "Hello " + username;
}
```

### Example 4: Path Traversal

**Code (Node.js):**
```javascript
app.get('/download', (req, res) => {
    const filename = req.query.file;
    res.sendFile('/uploads/' + filename);
});
```

**Detection:**
- Pattern: Directory Traversal
- Location: Line 3
- Category: Path Traversal

**Why Risky:**
User controls file path without validation. Attacker can use `../` sequences to access files outside the intended directory, potentially reading sensitive configuration files, source code, or credentials.

**Exploitation Conditions:**
- User controls `file` parameter
- No path canonicalization or validation
- Sensitive files accessible on filesystem

**Severity:** High
**Confidence:** High (95%)

**Recommended Fix:**
```javascript
const path = require('path');
app.get('/download', (req, res) => {
    const filename = path.basename(req.query.file);
    const filepath = path.join('/uploads/', filename);
    if (!filepath.startsWith('/uploads/')) {
        return res.status(400).send('Invalid file');
    }
    res.sendFile(filepath);
});
```

### Example 5: Insecure Deserialization

**Code (Python):**
```python
import pickle

@app.route('/load', methods=['POST'])
def load_data():
    user_data = pickle.loads(request.data)
    return process(user_data)
```

**Detection:**
- Pattern: Unsafe Deserialization
- Location: Line 5
- Category: Insecure Deserialization

**Why Risky:**
Deserializing untrusted data with pickle can lead to arbitrary code execution. Attacker can craft malicious serialized objects that execute code during deserialization.

**Exploitation Conditions:**
- Application deserializes user input
- Python gadget chains available
- No integrity checks on serialized data

**Severity:** Critical
**Confidence:** High (100%)

**Recommended Fix:**
```python
import json

@app.route('/load', methods=['POST'])
def load_data():
    user_data = json.loads(request.data)
    return process(user_data)
```

### Example 6: SSRF via URL Parameter

**Code (Python):**
```python
@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    response = requests.get(url)
    return response.content
```

**Detection:**
- Pattern: Server-Side Request Forgery
- Location: Line 4
- Category: SSRF

**Why Risky:**
Application makes HTTP requests to user-controlled URLs. Attacker can access internal services, cloud metadata endpoints (169.254.169.254), or perform port scanning of internal network.

**Exploitation Conditions:**
- User controls URL parameter
- Internal network accessible from server
- Cloud metadata endpoint available
- No URL allowlist or validation

**Severity:** High
**Confidence:** High (95%)

**Recommended Fix:**
```python
from urllib.parse import urlparse

ALLOWED_HOSTS = ['api.example.com', 'cdn.example.com']

@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    parsed = urlparse(url)
    if parsed.hostname not in ALLOWED_HOSTS:
        return "Invalid URL", 400
    response = requests.get(url, timeout=5)
    return response.content
```

## Confidence Levels

**High Confidence (90-100%):**
- Exact pattern match with known vulnerability
- Clear exploit path identified
- No mitigating controls present
- Well-documented vulnerability type

**Medium Confidence (60-89%):**
- Pattern resembles known vulnerability
- Exploitation requires specific conditions
- Some mitigating controls may be present
- Context suggests vulnerability but not certain

**Low Confidence (30-59%):**
- Potential vulnerability identified
- Unclear or complex exploit path
- Multiple mitigating factors present
- Requires manual verification
- May be false positive

## Constraints

**MUST:**
- Identify specific vulnerability patterns in code
- Explain why each pattern is risky
- Assess exploitability conditions
- Provide severity and confidence ratings
- Reference specific code locations (file:line)
- Suggest concrete fixes

**MUST NOT:**
- Report theoretical vulnerabilities without code evidence
- Provide exploits or attack code
- Assume vulnerabilities without pattern match
- Report false positives without noting low confidence
- Ignore mitigating controls when assessing severity

## Report Format

```
Vulnerability: [Pattern Name]
Category: [Vulnerability Category]
Location: [file:line]
Severity: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low] ([percentage]%)

Description:
[Why this pattern is risky]

Exploitation Conditions:
- [Condition 1]
- [Condition 2]
- [Condition 3]

Vulnerable Code:
[Code snippet]

Recommended Fix:
[Safe code example]
```

## Resources

### references/vulnerability_patterns.md
Comprehensive catalog of security vulnerability patterns including:
- Injection vulnerabilities (SQL, NoSQL, LDAP, XSS, command injection)
- Authentication and session management issues
- Cryptographic failures
- Access control problems
- Deserialization vulnerabilities
- Path traversal and file inclusion
- SSRF and XXE
- Buffer overflows
- Race conditions
- CVE-style pattern examples
- Exploitability assessment framework





