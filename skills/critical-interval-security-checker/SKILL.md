---
name: critical-interval-security-checker
description: Analyzes code to identify security-critical time intervals and timing vulnerabilities in authentication, authorization, and time-sensitive security operations. Use this skill when reviewing code for proper timeout enforcement, token expiration, session management, rate limiting, password reset validity, or any time-sensitive security mechanism. Detects missing expiration checks, excessive timeout values, lack of rate limiting, client-side only validation, hardcoded timeouts, and timing attack vulnerabilities. Triggers when users ask to check security timeouts, verify token expiration handling, audit session timeout implementation, review rate limiting, or analyze time-based security controls.
---

# Critical Interval Security Checker

Analyze code to identify security-critical time intervals and timing vulnerabilities that could compromise security.

## Workflow

### 1. Identify Security-Critical Operations

Look for code that handles:
- **Authentication**: Login, logout, token generation
- **Session management**: Session creation, validation, expiration
- **Password operations**: Reset tokens, change requests
- **Rate limiting**: Login attempts, API calls, password resets
- **Token operations**: JWT, OAuth tokens, API keys
- **MFA**: OTP codes, push notifications, backup codes

### 2. Check for Common Vulnerabilities

See [vulnerability_patterns.md](references/vulnerability_patterns.md) for detailed patterns.

**Critical checks**:
- Missing expiration validation
- Excessive timeout values
- No rate limiting on sensitive endpoints
- Client-side only expiration checks
- Race conditions in expiration logic
- Hardcoded timeout values
- Inconsistent timeout enforcement
- Timezone handling issues
- Timing attack vulnerabilities

### 3. Use Automated Checker

Run the automated checker script:

```bash
# Check single file
python scripts/check_intervals.py path/to/file.py

# Check entire directory
python scripts/check_intervals.py src/

# Specify language
python scripts/check_intervals.py src/ --language python
```

The script detects:
- 🔴 **Critical**: JWT decode without verification, timing attacks
- 🟠 **High**: Missing expiration checks, no rate limiting
- 🟡 **Medium**: Excessive timeouts, inconsistent enforcement
- 🔵 **Low**: Hardcoded timeouts, magic numbers

### 4. Manual Code Review

For each security-critical operation, verify:

**Expiration is set**:
```python
# Good: Expiration set
token_expiry = datetime.utcnow() + timedelta(hours=1)
```

**Expiration is checked**:
```python
# Good: Expiration validated
if datetime.utcnow() > token_expiry:
    raise TokenExpiredError()
```

**Timeout is reasonable**:
```python
# Good: 1-hour reset token
RESET_TOKEN_EXPIRY = timedelta(hours=1)

# Bad: 7-day reset token (too long!)
RESET_TOKEN_EXPIRY = timedelta(days=7)
```

**Rate limiting exists**:
```python
# Good: Rate limited
@limiter.limit("5 per 15 minutes")
def login():
    pass
```

**Server-side enforcement**:
```python
# Good: Server validates expiration
decoded = jwt.decode(token, SECRET_KEY)  # Checks exp

# Bad: Client-side only
decoded = jwt.decode(token, options={"verify_signature": False})
```

### 5. Verify Against Standards

Consult [time_intervals.md](references/time_intervals.md) for recommended values:

**Common intervals**:
- JWT access token: 5-15 minutes
- JWT refresh token: 7-30 days
- Session timeout: 15-30 minutes (idle), 8-12 hours (absolute)
- Password reset token: 15-60 minutes
- Login rate limit: 5 attempts per 15 minutes
- TOTP code: 30 seconds
- SMS/Email OTP: 5-10 minutes

**Check if intervals match use case**:
- High-security apps need shorter timeouts
- User-facing apps balance security and UX
- API tokens can be shorter-lived with refresh tokens

### 6. Document Findings

For each issue found, document:

```
Issue: Missing expiration check on password reset token
Location: auth/reset_password.py:45
Severity: High
Current: Token created with expiry but never validated
Recommendation: Add expiration check before using token
Code fix:
  if datetime.utcnow() > token.expires_at:
      raise TokenExpiredError("Reset token expired")
```

### 7. Propose Fixes

**Fix missing expiration checks**:
```python
# Before
def validate_token(token):
    decoded = jwt.decode(token, SECRET_KEY, options={"verify_signature": False})
    return decoded['user_id']

# After
def validate_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY)  # Verifies exp automatically
        return decoded['user_id']
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token expired")
```

**Fix excessive timeouts**:
```python
# Before
RESET_TOKEN_EXPIRY = timedelta(days=7)  # Too long!

# After
RESET_TOKEN_EXPIRY = timedelta(hours=1)  # Appropriate
```

**Add rate limiting**:
```python
# Before
@app.route('/login', methods=['POST'])
def login():
    pass

# After
@app.route('/login', methods=['POST'])
@limiter.limit("5 per 15 minutes")
def login():
    pass
```

**Fix hardcoded timeouts**:
```python
# Before
expiry = datetime.utcnow() + timedelta(seconds=3600)  # Magic number

# After
SESSION_TIMEOUT = timedelta(hours=1)  # Named constant
expiry = datetime.utcnow() + SESSION_TIMEOUT
```

## Quick Reference

### Critical Vulnerabilities

**Missing expiration check**:
- Token/session has expiry field but it's never validated
- High risk: Expired tokens still work

**No rate limiting**:
- Authentication endpoints without throttling
- High risk: Brute force attacks

**Client-side only validation**:
- Expiration checked in frontend but not backend
- Critical risk: Easily bypassed

**Excessive timeouts**:
- Reset tokens valid for days
- Sessions never expire
- Medium risk: Extended attack window

### Detection Patterns

**Python**:
```python
# Look for
jwt.decode(..., verify=False)  # Bad
timedelta(days=7)  # Check context
@limiter.limit  # Good
datetime.now() vs datetime.utcnow()  # Timezone issue
```

**JavaScript**:
```javascript
// Look for
jwt.decode(...)  // Check if expiration validated
Date.now() < exp  // Client-side check
rateLimit(...)  // Good
setTimeout(..., 86400000)  // Magic number
```

**Java**:
```java
// Look for
Jwts.parser()  // Check if expiration validated
Duration.ofDays(30)  // Check context
@RateLimit  // Good
```

## Helper Script

The `check_intervals.py` script automates detection:

```bash
# Check Python code
python scripts/check_intervals.py src/ --language python

# Check JavaScript code
python scripts/check_intervals.py src/ --language javascript

# Auto-detect language
python scripts/check_intervals.py src/
```

Output provides:
- Categorized issues by severity
- File and line number
- Issue description
- Fix recommendation

## Best Practices

**Always**:
- Set expiration times for all security tokens
- Validate expiration server-side
- Use reasonable timeout values
- Implement rate limiting on auth endpoints
- Use UTC for all timestamps
- Use named constants for timeouts
- Document timeout decisions

**Never**:
- Skip expiration validation
- Use client-side only checks
- Set excessive timeout values
- Use magic number timeouts
- Mix timezone-aware and naive datetimes
- Use non-constant-time comparisons for secrets
