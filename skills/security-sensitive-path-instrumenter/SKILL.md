---
name: security-sensitive-path-instrumenter
description: Instruments authentication, authorization, and input-handling code paths to monitor security-relevant events and states at runtime. Use this skill when developers need to add security monitoring and logging to their code, including tracking authentication attempts (login/logout), authorization decisions (access control checks), input validation failures, session management events, and other security-critical operations. Supports Python, JavaScript/TypeScript, and Java with structured logging patterns. Triggers when users ask to add security instrumentation, monitor security events, log authentication/authorization, track security-sensitive operations, or add security observability to their codebase.
---

# Security-Sensitive Path Instrumenter

Add structured logging instrumentation to security-critical code paths for runtime monitoring of authentication, authorization, input validation, session management, and other security-relevant events.

## Workflow

1. **Identify security-sensitive code paths** - Locate authentication, authorization, input validation, or session management code that needs instrumentation

2. **Determine event types** - Classify the security events to monitor (see [security_events.md](references/security_events.md) for taxonomy)

3. **Review best practices** - Check [best_practices.md](references/best_practices.md) for what to log and what to avoid (never log passwords, secrets, or sensitive PII)

4. **Select language patterns** - Use [language_patterns.md](references/language_patterns.md) for language-specific instrumentation code (Python, JavaScript/TypeScript, Java)

5. **Add instrumentation** - Insert structured logging calls at key decision points:
   - Before and after authentication attempts
   - At authorization check points
   - When validation fails
   - During session lifecycle events

6. **Include context** - Log relevant data points:
   - User identifier
   - Timestamp (automatically added)
   - IP address
   - Resource accessed
   - Success/failure status
   - Failure reasons

7. **Verify instrumentation** - Ensure:
   - No sensitive data (passwords, tokens, secrets) is logged
   - Structured format (JSON) is used for machine parsing
   - Appropriate log levels are set
   - Performance impact is minimal

## Quick Reference

### Event Categories

- **Authentication**: Login attempts, logout, password changes, MFA, token validation
- **Authorization**: Access control decisions, permission checks, RBAC evaluations
- **Input Validation**: Validation failures, injection detection, format violations
- **Session Management**: Session creation/expiration, IP changes, hijacking detection
- **Sensitive Data Access**: PII access, financial data, encryption key usage
- **Configuration Changes**: Permission changes, role assignments, security policy updates

### Common Patterns

**Authentication (Python/Flask)**:
```python
log_security_event(
    event_type='authentication_attempt',
    username=username,
    ip_address=request.remote_addr
)
```

**Authorization (JavaScript/Express)**:
```typescript
logSecurityEvent('authorization_check', {
  user_id: user.id,
  resource: resourceId,
  permission: requiredPermission,
  decision: hasPermission ? 'granted' : 'denied'
});
```

**Validation (Java/Spring)**:
```java
Map<String, Object> data = new HashMap<>();
data.put("user_id", user.getId());
data.put("errors", validationErrors);
SecurityLogger.logSecurityEvent("validation_failure", data);
```

## Helper Script

Use `scripts/generate_instrumentation.py` to generate code snippets:

```bash
# Generate Python authentication instrumentation
python scripts/generate_instrumentation.py python authentication

# Generate JavaScript authorization instrumentation
python scripts/generate_instrumentation.py javascript authorization

# Generate Java validation instrumentation
python scripts/generate_instrumentation.py java validation
```

## Important Reminders

**Never log**:
- Passwords (plaintext or hashed)
- API keys or secrets
- Full session tokens
- Credit card numbers
- Social Security numbers
- Encryption keys

**Always log**:
- Event type and timestamp
- User identifier (when available)
- Success/failure status
- IP address (consider GDPR)
- Resource accessed
- Action performed

**Use structured logging** (JSON format) for machine parsing and analysis.
