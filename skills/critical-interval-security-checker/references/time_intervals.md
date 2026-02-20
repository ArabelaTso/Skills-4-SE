# Security-Critical Time Intervals

This document defines common security-critical time intervals and their recommended values.

## Authentication & Session Management

### Session Timeouts

**Idle Session Timeout**:
- **Purpose**: Automatically log out inactive users
- **Recommended**: 15-30 minutes for general applications
- **High Security**: 5-10 minutes for sensitive applications
- **Risk**: Too long = unauthorized access if user leaves workstation

**Absolute Session Timeout**:
- **Purpose**: Force re-authentication after maximum session duration
- **Recommended**: 8-12 hours for general applications
- **High Security**: 1-2 hours for sensitive applications
- **Risk**: Too long = prolonged access with stolen session tokens

**Remember Me Token Expiration**:
- **Purpose**: Persistent login across browser sessions
- **Recommended**: 7-30 days
- **Risk**: Too long = extended vulnerability window for stolen tokens

### Authentication Tokens

**JWT Access Token Expiration**:
- **Purpose**: Short-lived tokens for API access
- **Recommended**: 5-15 minutes
- **Risk**: Too long = extended window for token theft/replay

**JWT Refresh Token Expiration**:
- **Purpose**: Long-lived tokens to obtain new access tokens
- **Recommended**: 7-30 days
- **Risk**: Too long = persistent access if compromised

**API Key Rotation Period**:
- **Purpose**: Regular rotation of API keys
- **Recommended**: 90 days
- **Risk**: Too long = increased exposure if key is leaked

**OAuth Authorization Code Expiration**:
- **Purpose**: Time-limited authorization codes
- **Recommended**: 10 minutes (OAuth 2.0 spec)
- **Risk**: Too long = authorization code interception attacks

### Password Reset & Recovery

**Password Reset Token Expiration**:
- **Purpose**: Time-limited password reset links
- **Recommended**: 15-60 minutes
- **Risk**: Too long = token interception and account takeover

**Email Verification Token Expiration**:
- **Purpose**: Time-limited email verification links
- **Recommended**: 24 hours
- **Risk**: Too long = email account compromise window

**Account Unlock Token Expiration**:
- **Purpose**: Time-limited account unlock links
- **Recommended**: 30-60 minutes
- **Risk**: Too long = unauthorized account access

**Magic Link Expiration**:
- **Purpose**: Passwordless authentication links
- **Recommended**: 5-15 minutes
- **Risk**: Too long = link interception and unauthorized access

## Rate Limiting & Throttling

### Login Attempts

**Failed Login Lockout Duration**:
- **Purpose**: Temporary account lock after failed attempts
- **Recommended**: 15-30 minutes
- **Risk**: Too short = brute force attacks; too long = DoS

**Failed Login Window**:
- **Purpose**: Time window for counting failed attempts
- **Recommended**: 5-15 minutes
- **Risk**: Too long = slow brute force attacks succeed

**Failed Login Threshold**:
- **Recommended**: 3-5 attempts per window
- **Risk**: Too high = brute force vulnerability

### API Rate Limiting

**Rate Limit Window**:
- **Purpose**: Time window for counting API requests
- **Recommended**: 1 minute, 1 hour, or 24 hours
- **Risk**: Too long = resource exhaustion

**Rate Limit Reset**:
- **Purpose**: When rate limit counters reset
- **Recommended**: Sliding window or fixed window
- **Risk**: Fixed window = burst attacks at window boundaries

**Retry-After Header**:
- **Purpose**: Tell clients when to retry after rate limit
- **Recommended**: Match rate limit window
- **Risk**: Too short = continued hammering

### CAPTCHA & Challenge-Response

**CAPTCHA Expiration**:
- **Purpose**: Time-limited CAPTCHA challenges
- **Recommended**: 2-5 minutes
- **Risk**: Too long = CAPTCHA solving services

**Challenge Token Expiration**:
- **Purpose**: Time-limited security challenges
- **Recommended**: 5-10 minutes
- **Risk**: Too long = challenge bypass

## Multi-Factor Authentication

### MFA Code Expiration

**TOTP Code Validity**:
- **Purpose**: Time-based one-time password validity
- **Standard**: 30 seconds (TOTP spec)
- **Risk**: Too long = code reuse attacks

**SMS/Email OTP Expiration**:
- **Purpose**: One-time password sent via SMS/email
- **Recommended**: 5-10 minutes
- **Risk**: Too long = code interception window

**Push Notification Timeout**:
- **Purpose**: Time to respond to push MFA notification
- **Recommended**: 1-2 minutes
- **Risk**: Too long = unauthorized approval

**Backup Code Usage Window**:
- **Purpose**: Time window for using backup codes
- **Recommended**: Single use, no expiration (but rotate periodically)
- **Risk**: Unlimited validity = long-term compromise

## Cryptographic Operations

### Certificate & Key Expiration

**TLS Certificate Validity**:
- **Purpose**: Maximum certificate lifetime
- **Recommended**: 90 days (Let's Encrypt), 1 year (commercial)
- **Risk**: Too long = prolonged exposure if private key compromised

**Signing Key Rotation**:
- **Purpose**: Regular rotation of signing keys
- **Recommended**: 90-180 days
- **Risk**: Too long = extended impact of key compromise

**Encryption Key Rotation**:
- **Purpose**: Regular rotation of encryption keys
- **Recommended**: 90-365 days depending on sensitivity
- **Risk**: Too long = more data encrypted with compromised key

### Nonce & Challenge Expiration

**Nonce Validity Period**:
- **Purpose**: Prevent replay attacks
- **Recommended**: 5-15 minutes
- **Risk**: Too long = replay attack window

**CSRF Token Expiration**:
- **Purpose**: Prevent cross-site request forgery
- **Recommended**: Session lifetime or 1-2 hours
- **Risk**: Too long = CSRF token theft window

## Payment & Financial Operations

### Payment Authorization

**Payment Authorization Hold**:
- **Purpose**: Time to capture authorized payment
- **Recommended**: 7 days (card networks)
- **Risk**: Too long = funds held unnecessarily

**Payment Confirmation Window**:
- **Purpose**: Time to confirm payment intent
- **Recommended**: 15-30 minutes
- **Risk**: Too long = price changes, inventory issues

**Refund Processing Window**:
- **Purpose**: Time limit for processing refunds
- **Recommended**: 30-90 days
- **Risk**: Too short = customer service issues

## Data Retention & Deletion

### Temporary Data Retention

**Audit Log Retention**:
- **Purpose**: Keep security logs for investigation
- **Recommended**: 90-365 days (compliance dependent)
- **Risk**: Too short = insufficient forensic data

**Deleted Data Grace Period**:
- **Purpose**: Soft delete before permanent deletion
- **Recommended**: 30 days
- **Risk**: Too long = data breach exposure

**Cache Expiration (Sensitive Data)**:
- **Purpose**: Automatic cache invalidation
- **Recommended**: 5-15 minutes
- **Risk**: Too long = stale sensitive data exposure

## Vulnerability Windows

### Security Update Deadlines

**Critical Patch Application**:
- **Purpose**: Time to apply critical security patches
- **Recommended**: 24-48 hours
- **Risk**: Too long = known vulnerability exploitation

**Dependency Update Window**:
- **Purpose**: Time to update vulnerable dependencies
- **Recommended**: 7-14 days
- **Risk**: Too long = supply chain attacks

### Incident Response

**Breach Notification Deadline**:
- **Purpose**: Legal requirement to notify users of breach
- **Recommended**: 72 hours (GDPR)
- **Risk**: Too long = legal penalties, user harm

**Credential Rotation After Breach**:
- **Purpose**: Rotate all credentials after security incident
- **Recommended**: Immediate (within hours)
- **Risk**: Delay = continued unauthorized access

## Common Timing Vulnerabilities

### Too Long Intervals

**Symptoms**:
- Tokens valid for days/weeks
- Sessions never expire
- No rate limiting
- Permanent API keys

**Risks**:
- Extended attack windows
- Token theft impact
- Brute force attacks
- Resource exhaustion

### Too Short Intervals

**Symptoms**:
- Tokens expire during normal use
- Aggressive rate limiting
- Frequent re-authentication

**Risks**:
- Poor user experience
- Workarounds that reduce security
- Support burden

### Missing Expiration

**Symptoms**:
- No expiration checks
- Tokens valid indefinitely
- No cleanup of old data

**Risks**:
- Unlimited attack window
- Data accumulation
- Compliance violations

### Inconsistent Enforcement

**Symptoms**:
- Expiration set but not checked
- Different timeouts across services
- Race conditions in expiration checks

**Risks**:
- False sense of security
- Exploitable timing windows
- Confused deputy attacks

## Best Practices

### Setting Intervals

1. **Balance security and usability**: Too short = poor UX, too long = security risk
2. **Consider threat model**: High-value targets need shorter intervals
3. **Follow industry standards**: OAuth, TOTP, etc. have recommended values
4. **Comply with regulations**: GDPR, PCI-DSS, HIPAA have requirements
5. **Document decisions**: Explain why specific intervals were chosen

### Implementing Intervals

1. **Use UTC timestamps**: Avoid timezone issues
2. **Check expiration server-side**: Never trust client-side checks
3. **Use constant-time comparisons**: Prevent timing attacks
4. **Log expiration events**: Track when tokens/sessions expire
5. **Handle edge cases**: Clock skew, leap seconds, DST

### Testing Intervals

1. **Test expiration enforcement**: Verify expired tokens are rejected
2. **Test boundary conditions**: Test at exact expiration time
3. **Test clock manipulation**: Ensure system time changes don't break security
4. **Test race conditions**: Concurrent expiration checks
5. **Load test rate limits**: Verify limits hold under load
