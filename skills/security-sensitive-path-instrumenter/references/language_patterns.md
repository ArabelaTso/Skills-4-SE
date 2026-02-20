# Language-Specific Instrumentation Patterns

This document provides instrumentation patterns for Python, JavaScript/TypeScript, and Java.

## Python

### Logging Setup

```python
import logging
import json
from datetime import datetime

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

def log_security_event(event_type, user_id=None, success=None, **kwargs):
    """Log a security event with structured data"""
    event = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'user_id': user_id,
        'success': success,
        **kwargs
    }
    logger.info(json.dumps(event))
```

### Authentication Instrumentation

```python
# Flask example
from flask import request

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    ip_address = request.remote_addr

    # Instrument authentication attempt
    log_security_event(
        event_type='authentication_attempt',
        username=username,
        ip_address=ip_address,
        user_agent=request.headers.get('User-Agent')
    )

    user = authenticate(username, password)

    if user:
        log_security_event(
            event_type='authentication_success',
            user_id=user.id,
            username=username,
            ip_address=ip_address
        )
        return {'token': generate_token(user)}
    else:
        log_security_event(
            event_type='authentication_failure',
            username=username,
            ip_address=ip_address,
            failure_reason='invalid_credentials'
        )
        return {'error': 'Invalid credentials'}, 401
```

### Authorization Instrumentation

```python
def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            resource = kwargs.get('resource_id')

            # Instrument authorization check
            has_permission = user.has_permission(permission)

            log_security_event(
                event_type='authorization_check',
                user_id=user.id,
                resource=resource,
                permission=permission,
                decision='granted' if has_permission else 'denied'
            )

            if not has_permission:
                log_security_event(
                    event_type='authorization_violation',
                    user_id=user.id,
                    resource=resource,
                    permission=permission
                )
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

### Input Validation Instrumentation

```python
from marshmallow import Schema, fields, ValidationError

def validate_with_logging(schema, data, context=None):
    """Validate data and log validation failures"""
    try:
        result = schema.load(data)
        return result, None
    except ValidationError as e:
        log_security_event(
            event_type='validation_failure',
            user_id=context.get('user_id') if context else None,
            errors=e.messages,
            field_count=len(e.messages)
        )
        return None, e.messages
```

## JavaScript/TypeScript

### Logging Setup

```typescript
// logger.ts
interface SecurityEvent {
  timestamp: string;
  event_type: string;
  user_id?: string;
  success?: boolean;
  [key: string]: any;
}

export function logSecurityEvent(
  eventType: string,
  data: Omit<SecurityEvent, 'timestamp' | 'event_type'>
): void {
  const event: SecurityEvent = {
    timestamp: new Date().toISOString(),
    event_type: eventType,
    ...data
  };
  console.log(JSON.stringify(event));
}
```

### Authentication Instrumentation (Express)

```typescript
// auth.controller.ts
import { Request, Response } from 'express';
import { logSecurityEvent } from './logger';

export async function login(req: Request, res: Response) {
  const { username, password } = req.body;
  const ipAddress = req.ip;
  const userAgent = req.get('user-agent');

  // Instrument authentication attempt
  logSecurityEvent('authentication_attempt', {
    username,
    ip_address: ipAddress,
    user_agent: userAgent
  });

  try {
    const user = await authenticateUser(username, password);

    if (user) {
      logSecurityEvent('authentication_success', {
        user_id: user.id,
        username,
        ip_address: ipAddress
      });

      const token = generateToken(user);
      return res.json({ token });
    } else {
      logSecurityEvent('authentication_failure', {
        username,
        ip_address: ipAddress,
        failure_reason: 'invalid_credentials'
      });

      return res.status(401).json({ error: 'Invalid credentials' });
    }
  } catch (error) {
    logSecurityEvent('authentication_error', {
      username,
      ip_address: ipAddress,
      error: error.message
    });

    return res.status(500).json({ error: 'Authentication failed' });
  }
}
```

### Authorization Instrumentation (Middleware)

```typescript
// auth.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { logSecurityEvent } from './logger';

export function requirePermission(permission: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.user;
    const resource = req.params.id;

    // Instrument authorization check
    const hasPermission = await user.hasPermission(permission);

    logSecurityEvent('authorization_check', {
      user_id: user.id,
      resource,
      permission,
      decision: hasPermission ? 'granted' : 'denied'
    });

    if (!hasPermission) {
      logSecurityEvent('authorization_violation', {
        user_id: user.id,
        resource,
        permission
      });

      return res.status(403).json({ error: 'Forbidden' });
    }

    next();
  };
}
```

### Input Validation Instrumentation

```typescript
// validation.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { AnySchema } from 'yup';
import { logSecurityEvent } from './logger';

export function validateRequest(schema: AnySchema) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      await schema.validate(req.body, { abortEarly: false });
      next();
    } catch (error) {
      logSecurityEvent('validation_failure', {
        user_id: req.user?.id,
        errors: error.errors,
        field_count: error.errors.length,
        path: req.path
      });

      return res.status(400).json({
        error: 'Validation failed',
        details: error.errors
      });
    }
  };
}
```

## Java

### Logging Setup

```java
// SecurityLogger.java
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

public class SecurityLogger {
    private static final Logger logger = LoggerFactory.getLogger(SecurityLogger.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static void logSecurityEvent(String eventType, Map<String, Object> data) {
        try {
            Map<String, Object> event = new HashMap<>(data);
            event.put("timestamp", Instant.now().toString());
            event.put("event_type", eventType);

            String json = objectMapper.writeValueAsString(event);
            logger.info(json);
        } catch (Exception e) {
            logger.error("Failed to log security event", e);
        }
    }
}
```

### Authentication Instrumentation (Spring)

```java
// AuthController.java
import org.springframework.web.bind.annotation.*;
import javax.servlet.http.HttpServletRequest;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @PostMapping("/login")
    public ResponseEntity<?> login(
            @RequestBody LoginRequest request,
            HttpServletRequest httpRequest) {

        String ipAddress = httpRequest.getRemoteAddr();
        String userAgent = httpRequest.getHeader("User-Agent");

        // Instrument authentication attempt
        Map<String, Object> attemptData = new HashMap<>();
        attemptData.put("username", request.getUsername());
        attemptData.put("ip_address", ipAddress);
        attemptData.put("user_agent", userAgent);
        SecurityLogger.logSecurityEvent("authentication_attempt", attemptData);

        try {
            User user = authService.authenticate(
                request.getUsername(),
                request.getPassword()
            );

            if (user != null) {
                Map<String, Object> successData = new HashMap<>();
                successData.put("user_id", user.getId());
                successData.put("username", user.getUsername());
                successData.put("ip_address", ipAddress);
                SecurityLogger.logSecurityEvent("authentication_success", successData);

                String token = tokenService.generateToken(user);
                return ResponseEntity.ok(new AuthResponse(token));
            } else {
                Map<String, Object> failureData = new HashMap<>();
                failureData.put("username", request.getUsername());
                failureData.put("ip_address", ipAddress);
                failureData.put("failure_reason", "invalid_credentials");
                SecurityLogger.logSecurityEvent("authentication_failure", failureData);

                return ResponseEntity.status(401)
                    .body(new ErrorResponse("Invalid credentials"));
            }
        } catch (Exception e) {
            Map<String, Object> errorData = new HashMap<>();
            errorData.put("username", request.getUsername());
            errorData.put("ip_address", ipAddress);
            errorData.put("error", e.getMessage());
            SecurityLogger.logSecurityEvent("authentication_error", errorData);

            return ResponseEntity.status(500)
                .body(new ErrorResponse("Authentication failed"));
        }
    }
}
```

### Authorization Instrumentation (Aspect)

```java
// AuthorizationAspect.java
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;
import org.springframework.stereotype.Component;
import java.util.HashMap;
import java.util.Map;

@Aspect
@Component
public class AuthorizationAspect {

    @Around("@annotation(requirePermission)")
    public Object logAuthorization(
            ProceedingJoinPoint joinPoint,
            RequirePermission requirePermission) throws Throwable {

        User user = SecurityContextHolder.getContext().getUser();
        String permission = requirePermission.value();
        String resource = extractResourceId(joinPoint);

        // Instrument authorization check
        boolean hasPermission = user.hasPermission(permission);

        Map<String, Object> checkData = new HashMap<>();
        checkData.put("user_id", user.getId());
        checkData.put("resource", resource);
        checkData.put("permission", permission);
        checkData.put("decision", hasPermission ? "granted" : "denied");
        SecurityLogger.logSecurityEvent("authorization_check", checkData);

        if (!hasPermission) {
            Map<String, Object> violationData = new HashMap<>();
            violationData.put("user_id", user.getId());
            violationData.put("resource", resource);
            violationData.put("permission", permission);
            SecurityLogger.logSecurityEvent("authorization_violation", violationData);

            throw new AccessDeniedException("Insufficient permissions");
        }

        return joinPoint.proceed();
    }
}
```

### Input Validation Instrumentation

```java
// ValidationExceptionHandler.java
import org.springframework.web.bind.annotation.*;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import java.util.*;
import java.util.stream.Collectors;

@ControllerAdvice
public class ValidationExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<?> handleValidationException(
            MethodArgumentNotValidException ex,
            HttpServletRequest request) {

        User user = SecurityContextHolder.getContext().getUser();

        List<String> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(FieldError::getDefaultMessage)
            .collect(Collectors.toList());

        // Instrument validation failure
        Map<String, Object> validationData = new HashMap<>();
        if (user != null) {
            validationData.put("user_id", user.getId());
        }
        validationData.put("errors", errors);
        validationData.put("field_count", errors.size());
        validationData.put("path", request.getRequestURI());
        SecurityLogger.logSecurityEvent("validation_failure", validationData);

        return ResponseEntity.badRequest()
            .body(new ValidationErrorResponse(errors));
    }
}
```

## Session Management Patterns

### Python (Flask-Session)

```python
from flask import session
from datetime import datetime

@app.before_request
def track_session():
    if 'user_id' in session:
        current_ip = request.remote_addr
        session_ip = session.get('ip_address')

        if session_ip and session_ip != current_ip:
            log_security_event(
                event_type='session_ip_change',
                user_id=session['user_id'],
                old_ip=session_ip,
                new_ip=current_ip,
                session_id=hashlib.sha256(
                    session.sid.encode()
                ).hexdigest()[:16]
            )
```

### JavaScript (Express-Session)

```typescript
app.use((req, res, next) => {
  if (req.session.userId) {
    const currentIp = req.ip;
    const sessionIp = req.session.ipAddress;

    if (sessionIp && sessionIp !== currentIp) {
      logSecurityEvent('session_ip_change', {
        user_id: req.session.userId,
        old_ip: sessionIp,
        new_ip: currentIp,
        session_id: hashSessionId(req.sessionID)
      });
    }
  }
  next();
});
```

### Java (Spring Session)

```java
@Component
public class SessionMonitoringInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(
            HttpServletRequest request,
            HttpServletResponse response,
            Object handler) {

        HttpSession session = request.getSession(false);
        if (session != null && session.getAttribute("userId") != null) {
            String currentIp = request.getRemoteAddr();
            String sessionIp = (String) session.getAttribute("ipAddress");

            if (sessionIp != null && !sessionIp.equals(currentIp)) {
                Map<String, Object> data = new HashMap<>();
                data.put("user_id", session.getAttribute("userId"));
                data.put("old_ip", sessionIp);
                data.put("new_ip", currentIp);
                data.put("session_id", hashSessionId(session.getId()));
                SecurityLogger.logSecurityEvent("session_ip_change", data);
            }
        }
        return true;
    }
}
```
