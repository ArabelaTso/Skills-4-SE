# Security Remediation Strategies

This document provides comprehensive remediation strategies for common security vulnerabilities, organized by vulnerability category.

## Buffer Overflow Vulnerabilities

### CWE-120: Buffer Copy without Checking Size of Input
**Unsafe Patterns:**
- `strcpy()`, `strcat()`, `sprintf()`, `gets()`
- Fixed-size buffers with unchecked input

**Remediation Strategies:**

1. **Use Safe String Functions**
   - Replace `strcpy()` with `strncpy()` or `strlcpy()`
   - Replace `strcat()` with `strncat()` or `strlcat()`
   - Replace `sprintf()` with `snprintf()`
   - Never use `gets()` - use `fgets()` instead

2. **Bounds Checking**
   - Always validate input length before copying
   - Use `sizeof()` to determine buffer capacity
   - Leave room for null terminator

3. **Modern Language Features**
   - Use `std::string` in C++ instead of char arrays
   - Use safe string libraries (SafeStr, Bstrlib)

**Trade-offs:**
- Performance: Minimal overhead for bounds checking
- Compatibility: May require refactoring existing code
- Complexity: Slightly more verbose code

### CWE-121: Stack-based Buffer Overflow
**Remediation Strategies:**

1. **Stack Canaries**
   - Enable compiler protections (`-fstack-protector-all`)
   - Use Address Space Layout Randomization (ASLR)

2. **Input Validation**
   - Validate all external input sizes
   - Use length-prefixed strings
   - Implement maximum size limits

3. **Safe Alternatives**
   - Use dynamic allocation with size tracking
   - Implement custom safe buffer types

## Injection Vulnerabilities

### CWE-89: SQL Injection
**Unsafe Patterns:**
- String concatenation for SQL queries
- Unescaped user input in queries
- Dynamic query construction

**Remediation Strategies:**

1. **Parameterized Queries (Preferred)**
   - Use prepared statements with bound parameters
   - Separates SQL logic from data
   - Prevents injection by design

2. **ORM Frameworks**
   - Use Object-Relational Mapping tools
   - Abstracts SQL generation
   - Built-in injection protection

3. **Input Validation**
   - Whitelist allowed characters
   - Validate data types and formats
   - Reject suspicious patterns

4. **Stored Procedures**
   - Encapsulate SQL logic
   - Parameterized by default
   - Centralized security control

**Trade-offs:**
- Parameterized queries: Best security, minimal performance impact
- ORMs: Easier development, potential performance overhead
- Stored procedures: Centralized logic, less flexible

### CWE-78: OS Command Injection
**Unsafe Patterns:**
- `system()`, `exec()`, `popen()` with user input
- Shell metacharacters in commands
- Unvalidated command arguments

**Remediation Strategies:**

1. **Avoid Shell Execution**
   - Use language-specific APIs instead of shell commands
   - Direct system calls (e.g., `os.remove()` vs `rm`)
   - Library functions for file operations

2. **Parameterized Execution**
   - Use `subprocess` with argument lists (Python)
   - Use `execve()` family instead of `system()`
   - Pass arguments as array, not concatenated string

3. **Input Sanitization**
   - Whitelist allowed characters
   - Escape shell metacharacters
   - Validate against expected patterns

4. **Sandboxing**
   - Run commands in restricted environment
   - Use containers or VMs
   - Apply principle of least privilege

**Trade-offs:**
- API alternatives: Best security, may require code restructuring
- Sanitization: Defense in depth, but error-prone
- Sandboxing: Strong isolation, operational complexity

### CWE-79: Cross-Site Scripting (XSS)
**Remediation Strategies:**

1. **Output Encoding**
   - HTML entity encoding for HTML context
   - JavaScript encoding for JS context
   - URL encoding for URL parameters
   - CSS encoding for style attributes

2. **Content Security Policy (CSP)**
   - Restrict script sources
   - Disable inline scripts
   - Use nonces or hashes for trusted scripts

3. **Input Validation**
   - Whitelist allowed HTML tags (if needed)
   - Sanitize user input
   - Reject dangerous patterns

4. **Framework Protection**
   - Use auto-escaping templates
   - React/Vue/Angular built-in XSS protection
   - Avoid `dangerouslySetInnerHTML` or `v-html`

**Trade-offs:**
- Output encoding: Essential, minimal overhead
- CSP: Strong protection, may break legacy code
- Framework protection: Easiest, requires framework adoption

## Insecure Deserialization

### CWE-502: Deserialization of Untrusted Data
**Unsafe Patterns:**
- Deserializing user-controlled data
- Using `pickle`, `marshal`, `eval()` on untrusted input
- Accepting serialized objects from network

**Remediation Strategies:**

1. **Avoid Deserialization**
   - Use data-only formats (JSON, XML)
   - Avoid object serialization for untrusted data
   - Use simple data structures

2. **Integrity Checks**
   - Sign serialized data with HMAC
   - Verify signatures before deserialization
   - Use authenticated encryption

3. **Type Validation**
   - Whitelist allowed classes
   - Implement custom deserializers
   - Validate object types before use

4. **Sandboxing**
   - Deserialize in isolated environment
   - Restrict class loading
   - Use security managers

**Trade-offs:**
- JSON/XML: Safest, limited to data structures
- Integrity checks: Good protection, key management overhead
- Sandboxing: Strong isolation, performance impact

## Authentication & Authorization

### CWE-287: Improper Authentication
**Remediation Strategies:**

1. **Multi-Factor Authentication**
   - Implement 2FA/MFA
   - Use TOTP or hardware tokens
   - SMS as fallback only

2. **Strong Password Policies**
   - Minimum length requirements
   - Complexity requirements
   - Password strength meters
   - Breach detection (HaveIBeenPwned)

3. **Secure Session Management**
   - Generate cryptographically random session IDs
   - Implement session timeout
   - Regenerate session ID after login
   - Secure cookie flags (HttpOnly, Secure, SameSite)

4. **Account Lockout**
   - Rate limiting on login attempts
   - Progressive delays
   - CAPTCHA after failures
   - Account lockout with recovery

**Trade-offs:**
- MFA: Best security, user friction
- Password policies: Improved security, user annoyance
- Rate limiting: Prevents brute force, potential DoS

### CWE-862: Missing Authorization
**Remediation Strategies:**

1. **Centralized Authorization**
   - Implement authorization middleware
   - Check permissions on every request
   - Use role-based access control (RBAC)

2. **Principle of Least Privilege**
   - Grant minimum necessary permissions
   - Default deny policy
   - Explicit permission checks

3. **Resource-Level Checks**
   - Verify user owns resource
   - Check permissions before operations
   - Validate indirect object references

4. **Authorization Frameworks**
   - Use established libraries (Casbin, Spring Security)
   - Policy-based access control
   - Attribute-based access control (ABAC)

**Trade-offs:**
- Centralized authorization: Consistent enforcement, single point of failure
- Fine-grained checks: Better security, more code
- Frameworks: Robust features, learning curve

## Cryptographic Issues

### CWE-327: Use of Broken Cryptography
**Unsafe Patterns:**
- MD5, SHA1 for security purposes
- DES, 3DES, RC4 encryption
- ECB mode for block ciphers
- Custom crypto implementations

**Remediation Strategies:**

1. **Modern Algorithms**
   - Use SHA-256 or SHA-3 for hashing
   - Use AES-256 for symmetric encryption
   - Use RSA-2048+ or ECC for asymmetric crypto
   - Use Argon2, bcrypt, or scrypt for passwords

2. **Proper Modes**
   - Use GCM or CCM for authenticated encryption
   - Use CBC with HMAC if GCM unavailable
   - Never use ECB mode
   - Use random IVs for each encryption

3. **Established Libraries**
   - Use libsodium, OpenSSL, or platform crypto APIs
   - Avoid implementing crypto primitives
   - Keep libraries updated

4. **Key Management**
   - Generate keys with CSPRNG
   - Store keys securely (HSM, key vault)
   - Rotate keys regularly
   - Use key derivation functions

**Trade-offs:**
- Modern algorithms: Better security, may break compatibility
- Authenticated encryption: Prevents tampering, slightly larger output
- Library updates: Security patches, potential breaking changes

### CWE-330: Insufficient Randomness
**Remediation Strategies:**

1. **Cryptographically Secure RNG**
   - Use `/dev/urandom` (Linux)
   - Use `CryptGenRandom` (Windows)
   - Use `secrets` module (Python)
   - Use `crypto.randomBytes()` (Node.js)

2. **Avoid Weak RNGs**
   - Never use `rand()`, `srand()` for security
   - Don't use `Math.random()` for tokens
   - Avoid predictable seeds

3. **Sufficient Entropy**
   - Use at least 128 bits for session tokens
   - Use 256 bits for cryptographic keys
   - Don't truncate random values

**Trade-offs:**
- CSPRNG: Essential for security, slightly slower
- Entropy requirements: Better security, larger tokens

## Memory Safety

### CWE-416: Use After Free
**Remediation Strategies:**

1. **Nullify Pointers**
   - Set pointers to NULL after free
   - Check for NULL before dereferencing
   - Use defensive programming

2. **Smart Pointers**
   - Use `std::unique_ptr`, `std::shared_ptr` (C++)
   - Automatic memory management
   - RAII pattern

3. **Memory-Safe Languages**
   - Use Rust for memory safety guarantees
   - Use garbage-collected languages
   - Consider language migration

4. **Static Analysis**
   - Use AddressSanitizer (ASan)
   - Use Valgrind for memory debugging
   - Enable compiler warnings

**Trade-offs:**
- Smart pointers: Prevents many issues, slight overhead
- Language migration: Best long-term solution, high cost
- Static analysis: Catches bugs early, CI/CD integration needed

### CWE-476: NULL Pointer Dereference
**Remediation Strategies:**

1. **Null Checks**
   - Check return values before use
   - Validate pointers before dereferencing
   - Use assertions in debug builds

2. **Error Handling**
   - Return error codes or exceptions
   - Use Option/Maybe types
   - Fail fast on invalid state

3. **Defensive Programming**
   - Initialize pointers to NULL
   - Use const correctness
   - Validate function parameters

**Trade-offs:**
- Null checks: Prevents crashes, verbose code
- Option types: Type-safe, requires language support
- Defensive programming: Robust code, more boilerplate

## Configuration & Deployment

### CWE-798: Hard-coded Credentials
**Remediation Strategies:**

1. **Environment Variables**
   - Store secrets in environment
   - Use `.env` files (not in version control)
   - Access via `os.getenv()` or similar

2. **Secret Management**
   - Use HashiCorp Vault
   - Use AWS Secrets Manager
   - Use Azure Key Vault
   - Use Kubernetes Secrets

3. **Configuration Files**
   - External config files (not in repo)
   - Encrypted configuration
   - File permissions (600)

4. **Credential Rotation**
   - Regular password changes
   - Automated rotation
   - Revoke old credentials

**Trade-offs:**
- Environment variables: Simple, limited features
- Secret management: Enterprise-grade, operational complexity
- Rotation: Better security, coordination overhead

### CWE-732: Incorrect Permission Assignment
**Remediation Strategies:**

1. **Principle of Least Privilege**
   - Minimum necessary permissions
   - Restrict file permissions (644 for files, 755 for dirs)
   - Use umask appropriately

2. **Access Control Lists**
   - Fine-grained permissions
   - Group-based access
   - Regular audits

3. **Secure Defaults**
   - Restrictive default permissions
   - Explicit permission grants
   - Deny by default

**Trade-offs:**
- Restrictive permissions: Better security, may break functionality
- ACLs: Fine-grained control, complexity
- Regular audits: Catches drift, requires automation
