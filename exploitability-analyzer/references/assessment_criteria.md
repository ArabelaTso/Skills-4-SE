# Exploitability Assessment Criteria

Framework for assessing whether vulnerabilities are realistically exploitable.

## Table of Contents
- [Exploitability Factors](#exploitability-factors)
- [SQL Injection](#sql-injection)
- [Command Injection](#command-injection)
- [Cross-Site Scripting (XSS)](#cross-site-scripting-xss)
- [Path Traversal](#path-traversal)
- [LDAP Injection](#ldap-injection)

## Exploitability Factors

### Factor 1: Reachability

**Question**: Can an attacker reach the vulnerable code path?

**High**: Public endpoint, no authentication required
**Medium**: Authenticated endpoint, common user role
**Low**: Admin-only, internal function, rare code path
**None**: Dead code, unreachable path

### Factor 2: Controllability

**Question**: Can an attacker control the vulnerable input?

**High**: Direct user input (query params, POST data, headers)
**Medium**: Indirect control (database values, config files)
**Low**: Derived values, heavily processed input
**None**: Hardcoded values, system-generated data

### Factor 3: Sanitization

**Question**: Is the input sanitized before reaching the sink?

**None**: No sanitization, direct pass-through
**Weak**: Blacklist filtering, incomplete escaping
**Partial**: Some sanitization but bypassable
**Strong**: Whitelist validation, proper escaping, parameterization

### Factor 4: Impact

**Question**: What damage can an attacker cause?

**Critical**: RCE, full system compromise, data exfiltration
**High**: Data breach, privilege escalation, DoS
**Medium**: Limited data access, information disclosure
**Low**: Minor information leak, cosmetic issues

## SQL Injection

### Exploitability Checklist

1. **Input Source**
   - [ ] User-controlled (query params, POST, cookies)
   - [ ] Database-sourced (second-order injection)
   - [ ] Configuration file
   - [ ] Hardcoded

2. **Query Construction**
   - [ ] String concatenation
   - [ ] String formatting (f-strings, %)
   - [ ] Parameterized query
   - [ ] ORM with raw SQL

3. **Sanitization**
   - [ ] No sanitization
   - [ ] Blacklist filtering (', --, etc.)
   - [ ] Escaping function (mysql_real_escape_string)
   - [ ] Parameterized/prepared statements

4. **Database Context**
   - [ ] SELECT (data exfiltration)
   - [ ] INSERT/UPDATE (data manipulation)
   - [ ] DELETE (data destruction)
   - [ ] Stored procedures (potential RCE)

5. **Database Permissions**
   - [ ] DBA/root privileges
   - [ ] Read/write on sensitive tables
   - [ ] Limited to specific tables
   - [ ] Read-only access

### Exploitability Matrix

| Input Control | Sanitization | DB Privileges | Exploitability | Impact |
|---------------|--------------|---------------|----------------|---------|
| User input | None | DBA | **Critical** | Full DB compromise, potential RCE |
| User input | None | Read/Write | **High** | Data breach, manipulation |
| User input | Weak blacklist | Read/Write | **High** | Likely bypassable |
| User input | Parameterized | Any | **None** | Not exploitable |
| DB-sourced | None | Read/Write | **Medium** | Second-order injection |
| Config file | None | Read/Write | **Low** | Requires config access |

### Example: High Exploitability

```python
# Vulnerable code
username = request.GET['username']
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

**Assessment**:
- **Reachability**: High (public endpoint)
- **Controllability**: High (direct user input)
- **Sanitization**: None (string formatting)
- **Impact**: High (data breach)
- **Exploitability**: **CRITICAL**

**Exploit**: `' OR '1'='1' --` bypasses authentication

### Example: Low Exploitability

```python
# Less vulnerable code
username = request.GET['username']
if not re.match(r'^[a-zA-Z0-9_]+$', username):
    return error("Invalid username")
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

**Assessment**:
- **Reachability**: High (public endpoint)
- **Controllability**: High (user input)
- **Sanitization**: Strong (whitelist + parameterized)
- **Impact**: None
- **Exploitability**: **NONE**

## Command Injection

### Exploitability Checklist

1. **Input Source**
   - [ ] User-controlled (form data, file names)
   - [ ] Environment variables
   - [ ] Configuration
   - [ ] Hardcoded

2. **Command Construction**
   - [ ] Shell invocation (os.system, subprocess with shell=True)
   - [ ] Direct execution (subprocess without shell)
   - [ ] Command builder with escaping

3. **Sanitization**
   - [ ] No sanitization
   - [ ] Blacklist (;, |, &, etc.)
   - [ ] Shell escaping (shlex.quote)
   - [ ] Whitelist validation

4. **Execution Context**
   - [ ] Root/admin privileges
   - [ ] Web server user
   - [ ] Restricted user
   - [ ] Sandboxed environment

### Exploitability Matrix

| Input Control | Shell Invocation | Sanitization | Privileges | Exploitability | Impact |
|---------------|------------------|--------------|------------|----------------|---------|
| User input | Yes (shell=True) | None | Root | **Critical** | Full system compromise |
| User input | Yes | None | Web user | **High** | Web server compromise |
| User input | Yes | Weak blacklist | Web user | **High** | Likely bypassable |
| User input | No (direct exec) | None | Web user | **Low** | Limited to command args |
| User input | Yes | Shell escaping | Web user | **None** | Not exploitable |

### Example: Critical Exploitability

```python
# Vulnerable code
filename = request.POST['filename']
os.system(f"cat {filename}")
```

**Assessment**:
- **Reachability**: High (public endpoint)
- **Controllability**: High (user input)
- **Sanitization**: None
- **Impact**: Critical (RCE)
- **Exploitability**: **CRITICAL**

**Exploit**: `; rm -rf /` executes arbitrary commands

### Example: Medium Exploitability

```python
# Partially vulnerable code
filename = request.POST['filename']
if ';' in filename or '|' in filename:
    return error("Invalid filename")
os.system(f"cat {filename}")
```

**Assessment**:
- **Reachability**: High
- **Controllability**: High
- **Sanitization**: Weak (incomplete blacklist)
- **Impact**: Critical
- **Exploitability**: **HIGH** (bypassable with `$(command)` or backticks)

## Cross-Site Scripting (XSS)

### Exploitability Checklist

1. **Input Source**
   - [ ] User-controlled (query params, POST)
   - [ ] Database-stored (stored XSS)
   - [ ] URL fragment (DOM-based)
   - [ ] Third-party API

2. **Output Context**
   - [ ] HTML body
   - [ ] HTML attribute
   - [ ] JavaScript context
   - [ ] CSS context
   - [ ] URL context

3. **Encoding**
   - [ ] No encoding
   - [ ] HTML entity encoding
   - [ ] JavaScript escaping
   - [ ] URL encoding
   - [ ] Context-appropriate encoding

4. **Mitigations**
   - [ ] No CSP
   - [ ] Weak CSP (unsafe-inline)
   - [ ] Strong CSP
   - [ ] HTTPOnly cookies
   - [ ] SameSite cookies

### Exploitability Matrix

| Input Control | Context | Encoding | CSP | Exploitability | Impact |
|---------------|---------|----------|-----|----------------|---------|
| User input | HTML body | None | None | **High** | Session hijacking, defacement |
| User input | HTML body | None | Strong CSP | **Medium** | Limited by CSP |
| User input | HTML attr | None | None | **High** | Event handler injection |
| User input | JS context | None | None | **Critical** | Direct code execution |
| User input | HTML body | HTML entities | None | **None** | Properly encoded |

### Example: High Exploitability

```python
# Vulnerable code
name = request.GET['name']
return f"<h1>Hello {name}</h1>"
```

**Assessment**:
- **Reachability**: High
- **Controllability**: High
- **Sanitization**: None
- **Impact**: High (session hijacking)
- **Exploitability**: **HIGH**

**Exploit**: `<script>alert(document.cookie)</script>`

### Example: Medium Exploitability

```python
# Partially protected code
name = request.GET['name']
response = f"<h1>Hello {html.escape(name)}</h1>"
# But no CSP header
return response
```

**Assessment**:
- **Reachability**: High
- **Controllability**: High
- **Sanitization**: Strong (HTML encoding)
- **Impact**: None (properly encoded)
- **Exploitability**: **NONE**

## Path Traversal

### Exploitability Checklist

1. **Input Source**
   - [ ] User-controlled (filename parameter)
   - [ ] URL path component
   - [ ] File upload name
   - [ ] Configuration

2. **Path Construction**
   - [ ] Direct concatenation
   - [ ] Path joining (os.path.join)
   - [ ] Normalized path
   - [ ] Whitelist validation

3. **Sanitization**
   - [ ] No sanitization
   - [ ] Blacklist (../, ..\)
   - [ ] Path normalization
   - [ ] Whitelist + chroot

4. **File System Access**
   - [ ] Arbitrary file read
   - [ ] Restricted to directory
   - [ ] Read-only access
   - [ ] No file access

### Exploitability Matrix

| Input Control | Sanitization | FS Access | Exploitability | Impact |
|---------------|--------------|-----------|----------------|---------|
| User input | None | Arbitrary | **High** | Sensitive file disclosure |
| User input | Blacklist | Arbitrary | **High** | Likely bypassable |
| User input | Normalization | Restricted | **Medium** | Limited disclosure |
| User input | Whitelist | Restricted | **Low** | Minimal risk |

### Example: High Exploitability

```python
# Vulnerable code
filename = request.GET['file']
with open(f"/var/www/uploads/{filename}") as f:
    return f.read()
```

**Assessment**:
- **Reachability**: High
- **Controllability**: High
- **Sanitization**: None
- **Impact**: High (file disclosure)
- **Exploitability**: **HIGH**

**Exploit**: `../../etc/passwd` reads sensitive files

## LDAP Injection

### Exploitability Checklist

1. **Input Source**
   - [ ] User-controlled (username, search)
   - [ ] Form data
   - [ ] Configuration

2. **Query Construction**
   - [ ] String concatenation
   - [ ] LDAP filter builder
   - [ ] Parameterized query

3. **Sanitization**
   - [ ] No sanitization
   - [ ] Partial escaping
   - [ ] Full LDAP escaping
   - [ ] Whitelist validation

4. **LDAP Permissions**
   - [ ] Admin bind
   - [ ] User bind
   - [ ] Anonymous bind
   - [ ] Read-only

### Example: High Exploitability

```python
# Vulnerable code
username = request.POST['username']
filter = f"(uid={username})"
results = ldap_conn.search_s(base_dn, ldap.SCOPE_SUBTREE, filter)
```

**Assessment**:
- **Reachability**: High
- **Controllability**: High
- **Sanitization**: None
- **Impact**: High (authentication bypass)
- **Exploitability**: **HIGH**

**Exploit**: `*)(uid=*))(|(uid=*` bypasses authentication

## General Assessment Framework

### Step 1: Identify Vulnerability Type

Classify the vulnerability (SQL injection, XSS, etc.)

### Step 2: Trace Data Flow

- **Source**: Where does the input come from?
- **Transformations**: What happens to the input?
- **Sink**: Where is the input used dangerously?

### Step 3: Evaluate Each Factor

- **Reachability**: Can attacker reach the code?
- **Controllability**: Can attacker control the input?
- **Sanitization**: Is input properly sanitized?
- **Impact**: What damage is possible?

### Step 4: Determine Exploitability

| Factors | Exploitability |
|---------|----------------|
| Reachable + Controllable + No Sanitization + High Impact | **CRITICAL** |
| Reachable + Controllable + Weak Sanitization + High Impact | **HIGH** |
| Reachable + Controllable + Partial Sanitization + Medium Impact | **MEDIUM** |
| Reachable + Limited Control + Strong Sanitization + Low Impact | **LOW** |
| Not Reachable OR Strong Sanitization | **NONE** |

### Step 5: Report Findings

Include:
- Vulnerability type and location
- Data flow (source → sink)
- Exploitability assessment
- Impact severity
- Proof-of-concept (if applicable)
- Remediation recommendations
