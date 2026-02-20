# Security Logging Best Practices

## What to Log

**Always log:**
- Event type and timestamp
- User identifier (when available)
- Success/failure status
- Source IP address
- Resource accessed
- Action performed

**Context to include:**
- Request ID for correlation
- Session ID (hashed)
- User agent
- Relevant business context

## What NOT to Log

**Never log:**
- Passwords (plaintext or hashed)
- Credit card numbers
- Social Security numbers
- API keys or secrets
- Session tokens (full value)
- Encryption keys
- Personal health information (PHI)

**Sanitize before logging:**
- Email addresses (consider hashing or masking)
- Phone numbers
- Full names (in some contexts)
- IP addresses (consider GDPR implications)

## Log Levels

**CRITICAL/ERROR:**
- Authentication failures after multiple attempts
- Authorization violations
- Detected attack patterns
- System security failures

**WARNING:**
- Single authentication failure
- Suspicious patterns
- Deprecated security features used
- Configuration issues

**INFO:**
- Successful authentication
- Authorization decisions
- Session lifecycle events
- Configuration changes

**DEBUG:**
- Detailed validation steps
- Internal security checks
- Performance metrics

## Structured Logging

Use structured logging (JSON) for machine parsing:

```json
{
  "timestamp": "2026-02-17T10:30:45Z",
  "event_type": "authentication_attempt",
  "user_id": "user123",
  "username": "john.doe",
  "ip_address": "192.168.1.100",
  "success": false,
  "failure_reason": "invalid_password",
  "attempt_count": 2,
  "request_id": "req-abc-123"
}
```

## Performance Considerations

- Use asynchronous logging to avoid blocking
- Implement log sampling for high-volume events
- Set appropriate log retention policies
- Consider log aggregation costs

## Compliance

**GDPR:**
- Minimize personal data in logs
- Implement log retention limits
- Support data deletion requests
- Document legitimate interest

**PCI DSS:**
- Never log full credit card numbers
- Mask PANs if logging required
- Secure log storage and transmission
- Implement access controls

**HIPAA:**
- Avoid logging PHI when possible
- Encrypt logs containing health data
- Implement audit trails
- Control access to logs

## Correlation and Context

- Use request IDs to trace requests across services
- Include session IDs for user journey tracking
- Add correlation IDs for distributed tracing
- Link related security events

## Alerting

Configure alerts for:
- Multiple failed authentication attempts
- Authorization violations
- Unusual access patterns
- Detected injection attempts
- Configuration changes
- Privilege escalations
