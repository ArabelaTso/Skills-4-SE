#!/usr/bin/env python3
"""
Generate security instrumentation code snippets for different languages and event types.
"""

import sys
import argparse

TEMPLATES = {
    'python': {
        'authentication': '''# Instrument authentication attempt
log_security_event(
    event_type='authentication_attempt',
    username={username},
    ip_address={ip_address},
    user_agent={user_agent}
)

# After authentication logic
if user:
    log_security_event(
        event_type='authentication_success',
        user_id=user.id,
        username={username},
        ip_address={ip_address}
    )
else:
    log_security_event(
        event_type='authentication_failure',
        username={username},
        ip_address={ip_address},
        failure_reason='invalid_credentials'
    )''',
        'authorization': '''# Instrument authorization check
has_permission = user.has_permission({permission})

log_security_event(
    event_type='authorization_check',
    user_id=user.id,
    resource={resource},
    permission={permission},
    decision='granted' if has_permission else 'denied'
)

if not has_permission:
    log_security_event(
        event_type='authorization_violation',
        user_id=user.id,
        resource={resource},
        permission={permission}
    )''',
        'validation': '''# Instrument validation failure
try:
    result = schema.load(data)
except ValidationError as e:
    log_security_event(
        event_type='validation_failure',
        user_id=context.get('user_id'),
        errors=e.messages,
        field_count=len(e.messages)
    )'''
    },
    'javascript': {
        'authentication': '''// Instrument authentication attempt
logSecurityEvent('authentication_attempt', {{
  username: {username},
  ip_address: {ip_address},
  user_agent: {user_agent}
}});

// After authentication logic
if (user) {{
  logSecurityEvent('authentication_success', {{
    user_id: user.id,
    username: {username},
    ip_address: {ip_address}
  }});
}} else {{
  logSecurityEvent('authentication_failure', {{
    username: {username},
    ip_address: {ip_address},
    failure_reason: 'invalid_credentials'
  }});
}}''',
        'authorization': '''// Instrument authorization check
const hasPermission = await user.hasPermission({permission});

logSecurityEvent('authorization_check', {{
  user_id: user.id,
  resource: {resource},
  permission: {permission},
  decision: hasPermission ? 'granted' : 'denied'
}});

if (!hasPermission) {{
  logSecurityEvent('authorization_violation', {{
    user_id: user.id,
    resource: {resource},
    permission: {permission}
  }});
}}''',
        'validation': '''// Instrument validation failure
try {{
  await schema.validate(data);
}} catch (error) {{
  logSecurityEvent('validation_failure', {{
    user_id: req.user?.id,
    errors: error.errors,
    field_count: error.errors.length
  }});
}}'''
    },
    'java': {
        'authentication': '''// Instrument authentication attempt
Map<String, Object> attemptData = new HashMap<>();
attemptData.put("username", {username});
attemptData.put("ip_address", {ip_address});
attemptData.put("user_agent", {user_agent});
SecurityLogger.logSecurityEvent("authentication_attempt", attemptData);

// After authentication logic
if (user != null) {{
    Map<String, Object> successData = new HashMap<>();
    successData.put("user_id", user.getId());
    successData.put("username", user.getUsername());
    successData.put("ip_address", {ip_address});
    SecurityLogger.logSecurityEvent("authentication_success", successData);
}} else {{
    Map<String, Object> failureData = new HashMap<>();
    failureData.put("username", {username});
    failureData.put("ip_address", {ip_address});
    failureData.put("failure_reason", "invalid_credentials");
    SecurityLogger.logSecurityEvent("authentication_failure", failureData);
}}''',
        'authorization': '''// Instrument authorization check
boolean hasPermission = user.hasPermission({permission});

Map<String, Object> checkData = new HashMap<>();
checkData.put("user_id", user.getId());
checkData.put("resource", {resource});
checkData.put("permission", {permission});
checkData.put("decision", hasPermission ? "granted" : "denied");
SecurityLogger.logSecurityEvent("authorization_check", checkData);

if (!hasPermission) {{
    Map<String, Object> violationData = new HashMap<>();
    violationData.put("user_id", user.getId());
    violationData.put("resource", {resource});
    violationData.put("permission", {permission});
    SecurityLogger.logSecurityEvent("authorization_violation", violationData);
}}''',
        'validation': '''// Instrument validation failure (in exception handler)
Map<String, Object> validationData = new HashMap<>();
if (user != null) {{
    validationData.put("user_id", user.getId());
}}
validationData.put("errors", errors);
validationData.put("field_count", errors.size());
SecurityLogger.logSecurityEvent("validation_failure", validationData);'''
    }
}

def generate_instrumentation(language, event_type):
    """Generate instrumentation code for the specified language and event type."""
    if language not in TEMPLATES:
        print(f"Error: Unsupported language '{language}'", file=sys.stderr)
        print(f"Supported languages: {', '.join(TEMPLATES.keys())}", file=sys.stderr)
        return None

    if event_type not in TEMPLATES[language]:
        print(f"Error: Unsupported event type '{event_type}' for {language}", file=sys.stderr)
        print(f"Supported event types: {', '.join(TEMPLATES[language].keys())}", file=sys.stderr)
        return None

    return TEMPLATES[language][event_type]

def main():
    parser = argparse.ArgumentParser(
        description='Generate security instrumentation code snippets'
    )
    parser.add_argument(
        'language',
        choices=['python', 'javascript', 'java'],
        help='Programming language'
    )
    parser.add_argument(
        'event_type',
        choices=['authentication', 'authorization', 'validation'],
        help='Type of security event to instrument'
    )

    args = parser.parse_args()

    code = generate_instrumentation(args.language, args.event_type)
    if code:
        print(code)
        return 0
    return 1

if __name__ == '__main__':
    sys.exit(main())
