# CWE Vulnerability Patterns

## Table of Contents
1. Memory Safety Vulnerabilities
2. Injection Vulnerabilities
3. Authentication and Authorization
4. Cryptographic Issues
5. Deserialization Vulnerabilities
6. Input Validation Issues

## 1. Memory Safety Vulnerabilities

### CWE-119: Buffer Overflow
**Description**: Writing data beyond buffer boundaries
**Languages**: C, C++
**Patterns**:
```c
// Vulnerable: No bounds checking
char buffer[10];
strcpy(buffer, user_input);  // VULNERABLE

// Vulnerable: Off-by-one
for(int i = 0; i <= 10; i++) {  // VULNERABLE: should be i < 10
    buffer[i] = data[i];
}
```
**Remediation**:
- Use safe functions: `strncpy`, `snprintf`
- Check bounds before writing
- Use modern C++ containers (std::string, std::vector)

### CWE-125: Out-of-bounds Read
**Description**: Reading data outside allocated memory
**Patterns**:
```c
// Vulnerable: No bounds checking
int arr[10];
int value = arr[user_index];  // VULNERABLE if user_index >= 10
```
**Remediation**:
- Validate array indices before access
- Use safe accessors with bounds checking

### CWE-416: Use After Free
**Description**: Accessing memory after it's been freed
**Patterns**:
```c
// Vulnerable
free(ptr);
ptr->field = value;  // VULNERABLE: use after free
```
**Remediation**:
- Set pointers to NULL after freeing
- Use smart pointers (C++)
- Avoid manual memory management when possible

### CWE-415: Double Free
**Description**: Freeing memory twice
**Patterns**:
```c
// Vulnerable
free(ptr);
// ... code ...
free(ptr);  // VULNERABLE: double free
```
**Remediation**:
- Set pointer to NULL after first free
- Use RAII patterns (C++)

## 2. Injection Vulnerabilities

### CWE-89: SQL Injection
**Description**: Unsanitized user input in SQL queries
**Patterns**:
```python
# Vulnerable: String concatenation
query = "SELECT * FROM users WHERE username = '" + username + "'"
cursor.execute(query)  # VULNERABLE

# Vulnerable: String formatting
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)  # VULNERABLE
```
**Remediation**:
```python
# Safe: Parameterized queries
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))

# Safe: ORM
user = User.objects.get(username=username)
```

### CWE-78: OS Command Injection
**Description**: Unsanitized user input in system commands
**Patterns**:
```python
# Vulnerable: Shell=True with user input
os.system("ls " + user_path)  # VULNERABLE
subprocess.call("ping " + user_host, shell=True)  # VULNERABLE
```
**Remediation**:
```python
# Safe: Use list arguments, no shell
subprocess.call(["ping", user_host])

# Safe: Validate and sanitize input
if re.match(r'^[a-zA-Z0-9_-]+$', user_host):
    subprocess.call(["ping", user_host])
```

### CWE-79: Cross-Site Scripting (XSS)
**Description**: Unsanitized user input in HTML output
**Patterns**:
```javascript
// Vulnerable: Direct HTML insertion
element.innerHTML = user_input;  // VULNERABLE

// Vulnerable: Unescaped template
response.write("<div>" + user_name + "</div>");  // VULNERABLE
```
**Remediation**:
```javascript
// Safe: Use textContent
element.textContent = user_input;

// Safe: Use escaping library
element.innerHTML = DOMPurify.sanitize(user_input);
```

### CWE-91: XML Injection
**Description**: Unsanitized user input in XML
**Patterns**:
```python
# Vulnerable: String concatenation
xml = f"<user><name>{user_name}</name></user>"  # VULNERABLE
```
**Remediation**:
```python
# Safe: Use XML library
import xml.etree.ElementTree as ET
user = ET.Element('user')
name = ET.SubElement(user, 'name')
name.text = user_name
```

## 3. Authentication and Authorization

### CWE-287: Improper Authentication
**Description**: Weak or missing authentication checks
**Patterns**:
```python
# Vulnerable: No authentication
@app.route('/admin')
def admin_panel():
    return render_template('admin.html')  # VULNERABLE

# Vulnerable: Client-side only check
if request.cookies.get('is_admin') == 'true':  # VULNERABLE
    show_admin_panel()
```
**Remediation**:
```python
# Safe: Server-side authentication
@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    return render_template('admin.html')
```

### CWE-798: Hard-coded Credentials
**Description**: Credentials embedded in source code
**Patterns**:
```python
# Vulnerable: Hard-coded password
PASSWORD = "admin123"  # VULNERABLE
API_KEY = "sk-1234567890abcdef"  # VULNERABLE

# Vulnerable: Hard-coded in connection string
conn = psycopg2.connect("host=localhost user=admin password=secret")  # VULNERABLE
```
**Remediation**:
```python
# Safe: Use environment variables
PASSWORD = os.environ.get('DB_PASSWORD')
API_KEY = os.environ.get('API_KEY')

# Safe: Use secrets management
from secrets_manager import get_secret
password = get_secret('db_password')
```

### CWE-862: Missing Authorization
**Description**: No check if user is authorized for action
**Patterns**:
```python
# Vulnerable: No authorization check
@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    User.delete(user_id)  # VULNERABLE: anyone can delete any user
```
**Remediation**:
```python
# Safe: Check authorization
@app.route('/delete_user/<user_id>')
@login_required
def delete_user(user_id):
    if current_user.id != user_id and not current_user.is_admin:
        abort(403)
    User.delete(user_id)
```

### CWE-306: Missing Authentication for Critical Function
**Description**: Critical operations without authentication
**Patterns**:
```python
# Vulnerable: No authentication on sensitive endpoint
@app.route('/api/transfer_funds', methods=['POST'])
def transfer_funds():
    # VULNERABLE: no authentication check
    amount = request.json['amount']
    to_account = request.json['to_account']
    transfer(amount, to_account)
```

## 4. Cryptographic Issues

### CWE-327: Use of Broken Cryptography
**Description**: Using weak or broken cryptographic algorithms
**Patterns**:
```python
# Vulnerable: MD5 for passwords
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()  # VULNERABLE

# Vulnerable: DES encryption
from Crypto.Cipher import DES
cipher = DES.new(key)  # VULNERABLE: DES is broken
```
**Remediation**:
```python
# Safe: Use bcrypt for passwords
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Safe: Use AES for encryption
from Crypto.Cipher import AES
cipher = AES.new(key, AES.MODE_GCM)
```

### CWE-326: Inadequate Encryption Strength
**Description**: Using insufficient key sizes
**Patterns**:
```python
# Vulnerable: Short key
key = os.urandom(8)  # VULNERABLE: 64-bit key too short
cipher = AES.new(key, AES.MODE_ECB)
```
**Remediation**:
```python
# Safe: Adequate key size
key = os.urandom(32)  # 256-bit key
cipher = AES.new(key, AES.MODE_GCM)
```

### CWE-330: Use of Insufficiently Random Values
**Description**: Using predictable random values for security
**Patterns**:
```python
# Vulnerable: Predictable random
import random
token = random.randint(1000, 9999)  # VULNERABLE for security tokens
```
**Remediation**:
```python
# Safe: Cryptographically secure random
import secrets
token = secrets.token_urlsafe(32)
```

### CWE-311: Missing Encryption of Sensitive Data
**Description**: Storing or transmitting sensitive data unencrypted
**Patterns**:
```python
# Vulnerable: Plaintext password storage
user.password = password  # VULNERABLE

# Vulnerable: Unencrypted transmission
requests.get(f"http://api.example.com/user?ssn={ssn}")  # VULNERABLE
```
**Remediation**:
```python
# Safe: Hash passwords
user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Safe: Use HTTPS
requests.get(f"https://api.example.com/user?ssn={ssn}")
```

## 5. Deserialization Vulnerabilities

### CWE-502: Deserialization of Untrusted Data
**Description**: Deserializing data from untrusted sources
**Patterns**:
```python
# Vulnerable: Pickle untrusted data
import pickle
data = pickle.loads(user_input)  # VULNERABLE: arbitrary code execution

# Vulnerable: YAML unsafe load
import yaml
config = yaml.load(user_input)  # VULNERABLE
```
**Remediation**:
```python
# Safe: Use safe formats
import json
data = json.loads(user_input)

# Safe: Use safe YAML loader
config = yaml.safe_load(user_input)
```

### CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes
**Description**: Mass assignment vulnerabilities
**Patterns**:
```python
# Vulnerable: Mass assignment
user = User()
for key, value in request.json.items():
    setattr(user, key, value)  # VULNERABLE: can set is_admin=True
```
**Remediation**:
```python
# Safe: Whitelist allowed fields
ALLOWED_FIELDS = ['name', 'email', 'bio']
user = User()
for key, value in request.json.items():
    if key in ALLOWED_FIELDS:
        setattr(user, key, value)
```

## 6. Input Validation Issues

### CWE-20: Improper Input Validation
**Description**: Insufficient validation of user input
**Patterns**:
```python
# Vulnerable: No validation
age = int(request.form['age'])  # VULNERABLE: can crash or overflow

# Vulnerable: Insufficient validation
if len(username) > 0:  # VULNERABLE: doesn't check for special chars
    create_user(username)
```
**Remediation**:
```python
# Safe: Comprehensive validation
age = int(request.form['age'])
if not (0 <= age <= 150):
    raise ValueError("Invalid age")

# Safe: Regex validation
if re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
    create_user(username)
```

### CWE-22: Path Traversal
**Description**: Accessing files outside intended directory
**Patterns**:
```python
# Vulnerable: Unsanitized file path
filename = request.args.get('file')
with open(f'/uploads/{filename}', 'r') as f:  # VULNERABLE: ../../../etc/passwd
    content = f.read()
```
**Remediation**:
```python
# Safe: Validate and sanitize path
import os
filename = os.path.basename(request.args.get('file'))
safe_path = os.path.join('/uploads', filename)
if not safe_path.startswith('/uploads/'):
    raise ValueError("Invalid path")
with open(safe_path, 'r') as f:
    content = f.read()
```

### CWE-918: Server-Side Request Forgery (SSRF)
**Description**: Server makes requests to attacker-controlled URLs
**Patterns**:
```python
# Vulnerable: Unvalidated URL
url = request.args.get('url')
response = requests.get(url)  # VULNERABLE: can access internal services
```
**Remediation**:
```python
# Safe: Whitelist allowed domains
ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']
parsed = urlparse(url)
if parsed.netloc not in ALLOWED_DOMAINS:
    raise ValueError("Domain not allowed")
response = requests.get(url)
```
