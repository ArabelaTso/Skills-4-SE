# Security Event Taxonomy

This document defines the categories of security-relevant events to monitor through instrumentation.

## Authentication Events

**Event Types:**
- Login attempts (success/failure)
- Logout events
- Password changes
- Password reset requests
- Multi-factor authentication (MFA) challenges
- Session creation/destruction
- Token generation/validation

**Key Data Points:**
- User identifier (username, email, user ID)
- Timestamp
- Source IP address
- User agent
- Authentication method (password, OAuth, SSO, etc.)
- Success/failure status
- Failure reason (invalid credentials, account locked, etc.)

## Authorization Events

**Event Types:**
- Access control decisions (allow/deny)
- Permission checks
- Role-based access control (RBAC) evaluations
- Resource access attempts
- Privilege escalation attempts
- API endpoint access

**Key Data Points:**
- User identifier
- Resource being accessed
- Action/operation attempted
- Authorization decision (granted/denied)
- Timestamp
- Required permissions
- User's current permissions/roles

## Input Validation Events

**Event Types:**
- Validation failures
- Sanitization operations
- Type coercion failures
- Format violations
- Boundary violations (length, range)
- Injection attempt detection (SQL, XSS, command injection)

**Key Data Points:**
- Input field/parameter name
- Validation rule violated
- Input value (sanitized/truncated if sensitive)
- Expected format/type
- Timestamp
- Source (form, API, query parameter)

## Session Management Events

**Event Types:**
- Session creation
- Session expiration
- Session invalidation
- Session fixation attempts
- Concurrent session detection
- Session hijacking detection

**Key Data Points:**
- Session ID (hashed or truncated)
- User identifier
- Session lifetime
- Timestamp
- IP address changes
- User agent changes

## Sensitive Data Access

**Event Types:**
- PII access
- Financial data access
- Health records access
- Encryption key usage
- Secrets/credentials access

**Key Data Points:**
- Data type accessed
- User identifier
- Timestamp
- Purpose/context
- Data volume

## Security Configuration Changes

**Event Types:**
- Permission changes
- Role assignments
- Security policy updates
- Firewall rule changes
- Encryption settings changes

**Key Data Points:**
- Configuration changed
- Old value
- New value
- User who made change
- Timestamp
- Justification/reason
