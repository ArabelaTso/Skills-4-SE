# Security Remediation Examples

This document provides complete before/after examples of security vulnerability remediations with detailed explanations and trade-off analysis.

## Example 1: SQL Injection Remediation

### Vulnerable Code (Python)
```python
def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = '" + email + "'"
    cursor.execute(query)
    return cursor.fetchone()
```

**Vulnerability:** CWE-89 (SQL Injection)
**Risk:** Attacker can inject SQL commands via email parameter
**Attack Example:** `' OR '1'='1` would return all users

### Remediated Code (Parameterized Query)
```python
def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = ?"
    cursor.execute(query, (email,))
    return cursor.fetchone()
```

**Changes:**
- Replaced string concatenation with parameterized query
- User input passed as tuple parameter
- Database driver handles escaping automatically

**Trade-offs:**
- ✅ Complete protection against SQL injection
- ✅ No performance impact
- ✅ Minimal code changes
- ⚠️ Requires understanding of parameterized queries

### Alternative: ORM Approach
```python
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
```

**Trade-offs:**
- ✅ Even simpler code
- ✅ Built-in injection protection
- ⚠️ Requires ORM framework (SQLAlchemy, Django ORM)
- ⚠️ May have performance overhead for complex queries

---

## Example 2: Command Injection Remediation

### Vulnerable Code (Python)
```python
import os

def resize_image(filename, width, height):
    cmd = f"convert {filename} -resize {width}x{height} output.jpg"
    os.system(cmd)
```

**Vulnerability:** CWE-78 (OS Command Injection)
**Risk:** Attacker can execute arbitrary commands
**Attack Example:** `image.jpg; rm -rf /` would delete files

### Remediated Code (Subprocess with List)
```python
import subprocess

def resize_image(filename, width, height):
    # Validate inputs
    if not filename.endswith(('.jpg', '.png', '.gif')):
        raise ValueError("Invalid file type")
    if not (0 < width <= 5000 and 0 < height <= 5000):
        raise ValueError("Invalid dimensions")

    # Use subprocess with argument list
    subprocess.run([
        'convert',
        filename,
        '-resize',
        f'{width}x{height}',
        'output.jpg'
    ], check=True, capture_output=True)
```

**Changes:**
- Replaced `os.system()` with `subprocess.run()`
- Arguments passed as list (not concatenated string)
- Added input validation
- Added error handling with `check=True`

**Trade-offs:**
- ✅ Prevents command injection
- ✅ Better error handling
- ✅ More explicit and readable
- ⚠️ More verbose code
- ⚠️ Requires input validation logic

### Alternative: Use Library Instead
```python
from PIL import Image

def resize_image(filename, width, height):
    # Validate inputs
    if not (0 < width <= 5000 and 0 < height <= 5000):
        raise ValueError("Invalid dimensions")

    # Use library instead of shell command
    img = Image.open(filename)
    img = img.resize((width, height))
    img.save('output.jpg')
```

**Trade-offs:**
- ✅ No shell execution at all
- ✅ More portable (no external dependency)
- ✅ Better performance
- ⚠️ Requires PIL/Pillow library
- ⚠️ May have different features than ImageMagick

---

## Example 3: Buffer Overflow Remediation

### Vulnerable Code (C)
```c
void process_username(char *input) {
    char username[32];
    strcpy(username, input);  // Unsafe!
    printf("Username: %s\n", username);
}
```

**Vulnerability:** CWE-120 (Buffer Copy without Checking Size)
**Risk:** Stack buffer overflow, potential code execution
**Attack Example:** Input > 32 bytes overwrites stack

### Remediated Code (Bounds Checking)
```c
void process_username(const char *input) {
    char username[32];

    // Check input length
    if (strlen(input) >= sizeof(username)) {
        fprintf(stderr, "Username too long\n");
        return;
    }

    // Use safe copy function
    strncpy(username, input, sizeof(username) - 1);
    username[sizeof(username) - 1] = '\0';  // Ensure null termination

    printf("Username: %s\n", username);
}
```

**Changes:**
- Added length check before copying
- Replaced `strcpy()` with `strncpy()`
- Ensured null termination
- Made input parameter const

**Trade-offs:**
- ✅ Prevents buffer overflow
- ✅ Minimal performance impact
- ⚠️ More verbose
- ⚠️ Requires careful size calculations

### Alternative: Dynamic Allocation
```c
void process_username(const char *input) {
    size_t len = strlen(input);

    // Allocate exact size needed
    char *username = malloc(len + 1);
    if (username == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return;
    }

    strcpy(username, input);  // Safe now - exact size
    printf("Username: %s\n", username);

    free(username);
}
```

**Trade-offs:**
- ✅ No arbitrary size limit
- ✅ Handles any input length
- ⚠️ Requires memory management
- ⚠️ Potential memory leaks if not freed
- ⚠️ Heap allocation overhead

### Alternative: C++ String
```cpp
void process_username(const std::string& input) {
    std::string username = input;
    std::cout << "Username: " << username << std::endl;
}
```

**Trade-offs:**
- ✅ Automatic memory management
- ✅ No buffer overflow possible
- ✅ Simplest code
- ⚠️ Requires C++ (not C)
- ⚠️ Slight performance overhead

---

## Example 4: XSS Remediation

### Vulnerable Code (JavaScript/Node.js)
```javascript
app.get('/profile', (req, res) => {
    const username = req.query.name;
    res.send(`<h1>Welcome ${username}!</h1>`);
});
```

**Vulnerability:** CWE-79 (Cross-Site Scripting)
**Risk:** Attacker can inject malicious scripts
**Attack Example:** `?name=<script>alert(document.cookie)</script>`

### Remediated Code (Output Encoding)
```javascript
const escapeHtml = require('escape-html');

app.get('/profile', (req, res) => {
    const username = escapeHtml(req.query.name);
    res.send(`<h1>Welcome ${username}!</h1>`);
});
```

**Changes:**
- Added HTML entity encoding
- User input escaped before output
- Special characters converted to entities

**Trade-offs:**
- ✅ Prevents XSS attacks
- ✅ Minimal code changes
- ✅ No performance impact
- ⚠️ Requires escaping library

### Alternative: Template Engine
```javascript
app.set('view engine', 'ejs');

app.get('/profile', (req, res) => {
    res.render('profile', { username: req.query.name });
});
```

**Template (profile.ejs):**
```html
<h1>Welcome <%= username %>!</h1>
```

**Trade-offs:**
- ✅ Auto-escaping by default
- ✅ Separation of concerns
- ✅ More maintainable
- ⚠️ Requires template engine setup
- ⚠️ Learning curve for template syntax

### Alternative: Content Security Policy
```javascript
const helmet = require('helmet');

app.use(helmet.contentSecurityPolicy({
    directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
    }
}));

app.get('/profile', (req, res) => {
    const username = escapeHtml(req.query.name);
    res.send(`<h1>Welcome ${username}!</h1>`);
});
```

**Trade-offs:**
- ✅ Defense in depth
- ✅ Blocks inline scripts even if XSS exists
- ✅ Protects entire application
- ⚠️ May break existing functionality
- ⚠️ Requires careful configuration

---

## Example 5: Insecure Deserialization Remediation

### Vulnerable Code (Python)
```python
import pickle

def load_user_data(data):
    user = pickle.loads(data)  # Unsafe!
    return user
```

**Vulnerability:** CWE-502 (Deserialization of Untrusted Data)
**Risk:** Arbitrary code execution via malicious pickle data
**Attack Example:** Crafted pickle can execute system commands

### Remediated Code (Use JSON)
```python
import json

def load_user_data(data):
    try:
        user = json.loads(data)
        # Validate expected structure
        if not isinstance(user, dict):
            raise ValueError("Invalid user data format")
        if 'username' not in user or 'email' not in user:
            raise ValueError("Missing required fields")
        return user
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON data")
```

**Changes:**
- Replaced `pickle` with `json`
- Added data validation
- Added error handling
- Validates data structure

**Trade-offs:**
- ✅ Safe for untrusted data
- ✅ Human-readable format
- ✅ Cross-language compatibility
- ⚠️ Only supports basic data types (no custom objects)
- ⚠️ Requires restructuring if using complex objects

### Alternative: Signed Pickle
```python
import pickle
import hmac
import hashlib

SECRET_KEY = b'your-secret-key-here'

def serialize_user(user):
    data = pickle.dumps(user)
    signature = hmac.new(SECRET_KEY, data, hashlib.sha256).digest()
    return signature + data

def load_user_data(signed_data):
    # Extract signature and data
    signature = signed_data[:32]
    data = signed_data[32:]

    # Verify signature
    expected_sig = hmac.new(SECRET_KEY, data, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected_sig):
        raise ValueError("Invalid signature - data may be tampered")

    # Safe to deserialize now
    user = pickle.loads(data)
    return user
```

**Trade-offs:**
- ✅ Allows complex objects
- ✅ Detects tampering
- ⚠️ Still vulnerable if attacker gets secret key
- ⚠️ More complex implementation
- ⚠️ Key management required

---

## Example 6: Weak Cryptography Remediation

### Vulnerable Code (Python)
```python
import hashlib

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def verify_password(password, hash):
    return hash_password(password) == hash
```

**Vulnerability:** CWE-327 (Use of Broken Cryptography)
**Risk:** MD5 is cryptographically broken, vulnerable to rainbow tables
**Attack Example:** Pre-computed hash tables can crack passwords

### Remediated Code (bcrypt)
```python
import bcrypt

def hash_password(password):
    # Generate salt and hash password
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(password, hash):
    return bcrypt.checkpw(password.encode(), hash)
```

**Changes:**
- Replaced MD5 with bcrypt
- Automatic salt generation
- Configurable work factor (rounds=12)
- Slow by design (prevents brute force)

**Trade-offs:**
- ✅ Resistant to rainbow tables (salted)
- ✅ Resistant to brute force (slow)
- ✅ Industry standard
- ⚠️ Slower than MD5 (intentional)
- ⚠️ Requires bcrypt library

### Alternative: Argon2
```python
from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password):
    return ph.hash(password)

def verify_password(password, hash):
    try:
        ph.verify(hash, password)
        return True
    except:
        return False
```

**Trade-offs:**
- ✅ Winner of Password Hashing Competition
- ✅ Resistant to GPU/ASIC attacks
- ✅ Memory-hard algorithm
- ⚠️ Newer (less widely deployed)
- ⚠️ Requires argon2 library

---

## Example 7: Authentication Bypass Remediation

### Vulnerable Code (Node.js/Express)
```javascript
app.post('/login', (req, res) => {
    const { username, password } = req.body;

    db.query('SELECT * FROM users WHERE username = ?', [username], (err, users) => {
        if (users.length > 0 && users[0].password === password) {
            req.session.userId = users[0].id;
            res.json({ success: true });
        } else {
            res.json({ success: false });
        }
    });
});
```

**Vulnerabilities:**
- CWE-287 (Improper Authentication)
- Plain text password comparison
- No rate limiting
- Timing attack vulnerability

### Remediated Code (Secure Authentication)
```javascript
const bcrypt = require('bcrypt');
const rateLimit = require('express-rate-limit');

// Rate limiting
const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // 5 attempts
    message: 'Too many login attempts, please try again later'
});

app.post('/login', loginLimiter, async (req, res) => {
    const { username, password } = req.body;

    // Input validation
    if (!username || !password) {
        return res.status(400).json({ error: 'Missing credentials' });
    }

    try {
        // Get user from database
        const users = await db.query(
            'SELECT id, password_hash FROM users WHERE username = ?',
            [username]
        );

        // Constant-time comparison to prevent timing attacks
        let isValid = false;
        if (users.length > 0) {
            isValid = await bcrypt.compare(password, users[0].password_hash);
        } else {
            // Perform dummy comparison to prevent timing attack
            await bcrypt.compare(password, '$2b$12$dummyhashtopreventtiming');
        }

        if (isValid) {
            // Regenerate session ID to prevent session fixation
            req.session.regenerate((err) => {
                if (err) {
                    return res.status(500).json({ error: 'Session error' });
                }

                req.session.userId = users[0].id;
                res.json({ success: true });
            });
        } else {
            res.status(401).json({ error: 'Invalid credentials' });
        }
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});
```

**Changes:**
- Added rate limiting (5 attempts per 15 minutes)
- Replaced plain text with bcrypt comparison
- Added constant-time comparison to prevent timing attacks
- Added session regeneration to prevent session fixation
- Added input validation
- Added proper error handling
- Used async/await for cleaner code

**Trade-offs:**
- ✅ Prevents brute force attacks
- ✅ Prevents timing attacks
- ✅ Prevents session fixation
- ✅ Secure password storage
- ⚠️ More complex code
- ⚠️ Requires additional libraries
- ⚠️ May frustrate legitimate users with rate limiting

---

## Example 8: Missing Authorization Remediation

### Vulnerable Code (REST API)
```javascript
app.delete('/api/posts/:id', (req, res) => {
    const postId = req.params.id;

    db.query('DELETE FROM posts WHERE id = ?', [postId], (err) => {
        if (err) {
            res.status(500).json({ error: 'Database error' });
        } else {
            res.json({ success: true });
        }
    });
});
```

**Vulnerability:** CWE-862 (Missing Authorization)
**Risk:** Any authenticated user can delete any post
**Attack Example:** User can delete posts they don't own

### Remediated Code (Authorization Check)
```javascript
app.delete('/api/posts/:id', requireAuth, async (req, res) => {
    const postId = req.params.id;
    const userId = req.session.userId;

    try {
        // First, check if post exists and get owner
        const posts = await db.query(
            'SELECT user_id FROM posts WHERE id = ?',
            [postId]
        );

        if (posts.length === 0) {
            return res.status(404).json({ error: 'Post not found' });
        }

        // Check if user owns the post
        if (posts[0].user_id !== userId) {
            return res.status(403).json({ error: 'Forbidden: You do not own this post' });
        }

        // User is authorized, proceed with deletion
        await db.query('DELETE FROM posts WHERE id = ?', [postId]);
        res.json({ success: true });

    } catch (error) {
        console.error('Delete error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});
```

**Changes:**
- Added authentication middleware (`requireAuth`)
- Added ownership verification
- Check post exists before deletion
- Return appropriate HTTP status codes (403 for forbidden, 404 for not found)
- Added error handling

**Trade-offs:**
- ✅ Prevents unauthorized access
- ✅ Clear error messages
- ✅ Proper HTTP semantics
- ⚠️ Additional database query
- ⚠️ More complex logic

### Alternative: Role-Based Access Control
```javascript
const checkPermission = (resource, action) => {
    return async (req, res, next) => {
        const userId = req.session.userId;
        const resourceId = req.params.id;

        try {
            // Check if user has permission
            const hasPermission = await authService.checkPermission(
                userId,
                resource,
                action,
                resourceId
            );

            if (!hasPermission) {
                return res.status(403).json({ error: 'Forbidden' });
            }

            next();
        } catch (error) {
            res.status(500).json({ error: 'Authorization error' });
        }
    };
};

app.delete('/api/posts/:id',
    requireAuth,
    checkPermission('post', 'delete'),
    async (req, res) => {
        const postId = req.params.id;

        try {
            await db.query('DELETE FROM posts WHERE id = ?', [postId]);
            res.json({ success: true });
        } catch (error) {
            res.status(500).json({ error: 'Database error' });
        }
    }
);
```

**Trade-offs:**
- ✅ Centralized authorization logic
- ✅ Reusable across endpoints
- ✅ Supports complex permission models
- ✅ Easier to audit
- ⚠️ Requires authorization framework
- ⚠️ More initial setup
- ⚠️ Learning curve

---

## Example 9: Hard-coded Credentials Remediation

### Vulnerable Code (Python)
```python
import psycopg2

def connect_to_database():
    conn = psycopg2.connect(
        host="db.example.com",
        database="myapp",
        user="admin",
        password="SuperSecret123!"  # Hard-coded!
    )
    return conn
```

**Vulnerability:** CWE-798 (Hard-coded Credentials)
**Risk:** Credentials exposed in source code, version control
**Attack Example:** Anyone with code access has database credentials

### Remediated Code (Environment Variables)
```python
import psycopg2
import os

def connect_to_database():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn
```

**Environment file (.env - not in version control):**
```
DB_HOST=db.example.com
DB_NAME=myapp
DB_USER=admin
DB_PASSWORD=SuperSecret123!
```

**Changes:**
- Moved credentials to environment variables
- Used `os.getenv()` to read configuration
- Added default for non-sensitive values
- Created separate .env file

**Trade-offs:**
- ✅ Credentials not in source code
- ✅ Different credentials per environment
- ✅ Easy to rotate credentials
- ⚠️ Requires environment setup
- ⚠️ Must secure .env file

### Alternative: Secret Management Service
```python
import psycopg2
import boto3
import json

def get_db_credentials():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId='myapp/database')
    return json.loads(response['SecretString'])

def connect_to_database():
    creds = get_db_credentials()
    conn = psycopg2.connect(
        host=creds['host'],
        database=creds['database'],
        user=creds['username'],
        password=creds['password']
    )
    return conn
```

**Trade-offs:**
- ✅ Centralized secret management
- ✅ Automatic rotation support
- ✅ Audit logging
- ✅ Fine-grained access control
- ⚠️ Requires cloud service (AWS Secrets Manager)
- ⚠️ Additional API calls
- ⚠️ Cost for secret storage

---

## Example 10: Path Traversal Remediation

### Vulnerable Code (Node.js)
```javascript
const fs = require('fs');
const path = require('path');

app.get('/download', (req, res) => {
    const filename = req.query.file;
    const filepath = path.join(__dirname, 'uploads', filename);

    fs.readFile(filepath, (err, data) => {
        if (err) {
            res.status(404).send('File not found');
        } else {
            res.send(data);
        }
    });
});
```

**Vulnerability:** CWE-22 (Path Traversal)
**Risk:** Attacker can access files outside uploads directory
**Attack Example:** `?file=../../etc/passwd`

### Remediated Code (Path Validation)
```javascript
const fs = require('fs');
const path = require('path');

app.get('/download', (req, res) => {
    const filename = req.query.file;

    // Validate filename
    if (!filename || filename.includes('..') || filename.includes('/') || filename.includes('\\')) {
        return res.status(400).send('Invalid filename');
    }

    // Whitelist allowed extensions
    const allowedExtensions = ['.pdf', '.jpg', '.png', '.txt'];
    const ext = path.extname(filename).toLowerCase();
    if (!allowedExtensions.includes(ext)) {
        return res.status(400).send('File type not allowed');
    }

    const uploadsDir = path.join(__dirname, 'uploads');
    const filepath = path.join(uploadsDir, filename);

    // Verify resolved path is within uploads directory
    const resolvedPath = path.resolve(filepath);
    if (!resolvedPath.startsWith(uploadsDir)) {
        return res.status(403).send('Access denied');
    }

    fs.readFile(resolvedPath, (err, data) => {
        if (err) {
            res.status(404).send('File not found');
        } else {
            res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
            res.send(data);
        }
    });
});
```

**Changes:**
- Added filename validation (reject `..`, `/`, `\`)
- Whitelisted allowed file extensions
- Verified resolved path is within uploads directory
- Added Content-Disposition header
- Added proper error handling

**Trade-offs:**
- ✅ Prevents path traversal
- ✅ Restricts file types
- ✅ Defense in depth (multiple checks)
- ⚠️ More complex validation logic
- ⚠️ May reject legitimate filenames with special characters
```

