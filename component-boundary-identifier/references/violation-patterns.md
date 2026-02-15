# Violation Detection Patterns

## Python Violations

### 1. Domain Depending on Infrastructure

**Pattern:**
```python
# domain/user_service.py
from infrastructure.database import PostgresConnection  # VIOLATION

class UserService:
    def __init__(self):
        self.db = PostgresConnection()
```

**Detection:**
- Domain package imports from infrastructure package
- Business logic depends on specific implementation

**Impact:** High - Breaks dependency inversion principle

**Fix:**
```python
# domain/user_service.py
from domain.repositories import UserRepository  # Interface

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
```

### 2. Circular Dependencies

**Pattern:**
```python
# services/order_service.py
from services.payment_service import PaymentService

# services/payment_service.py
from services.order_service import OrderService  # VIOLATION
```

**Detection:**
- Module A imports from Module B
- Module B imports from Module A
- Can be indirect (A → B → C → A)

**Impact:** High - Prevents proper module isolation

**Fix:**
- Extract shared interface
- Use dependency injection
- Introduce mediator/event bus

### 3. Accessing Private Implementation

**Pattern:**
```python
# api/routes.py
from infrastructure.database import _get_connection  # VIOLATION: private

def get_users():
    conn = _get_connection()  # Accessing private implementation
```

**Detection:**
- Importing names starting with `_`
- Accessing `_private` attributes from outside module

**Impact:** Medium - Breaks encapsulation

**Fix:**
```python
# api/routes.py
from domain.services import UserService

def get_users():
    service = UserService()
    return service.get_all_users()
```

### 4. Layer Skipping

**Pattern:**
```python
# api/routes.py
from infrastructure.repositories import UserRepository  # VIOLATION

def get_user(user_id):
    repo = UserRepository()
    return repo.find_by_id(user_id)  # API directly uses repository
```

**Detection:**
- Presentation layer imports from data layer
- Skips service/business layer

**Impact:** High - Violates layered architecture

**Fix:**
```python
# api/routes.py
from domain.services import UserService

def get_user(user_id):
    service = UserService()
    return service.get_user(user_id)
```

### 5. Concrete Type Dependencies

**Pattern:**
```python
# domain/services.py
from infrastructure.email import SMTPEmailSender  # VIOLATION: concrete type

class NotificationService:
    def __init__(self):
        self.sender = SMTPEmailSender()  # Depends on concrete implementation
```

**Detection:**
- Importing concrete classes instead of interfaces
- Direct instantiation of implementation classes

**Impact:** High - Prevents dependency injection and testing

**Fix:**
```python
# domain/services.py
from domain.interfaces import EmailSender  # Protocol/ABC

class NotificationService:
    def __init__(self, sender: EmailSender):
        self.sender = sender
```

## Java Violations

### 1. Domain Depending on Infrastructure

**Pattern:**
```java
// domain/service/UserService.java
package com.example.domain.service;

import com.example.infrastructure.JpaUserRepository;  // VIOLATION

public class UserService {
    private JpaUserRepository repository = new JpaUserRepository();
}
```

**Detection:**
- Domain package imports infrastructure package
- Concrete infrastructure class used in domain

**Impact:** High - Violates clean architecture

**Fix:**
```java
// domain/service/UserService.java
package com.example.domain.service;

import com.example.domain.repository.UserRepository;  // Interface

public class UserService {
    private final UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}
```

### 2. Package-Private Access Violation

**Pattern:**
```java
// com/example/api/UserController.java
package com.example.api;

import com.example.infrastructure.DatabaseHelper;  // Package-private class

public class UserController {
    void handleRequest() {
        DatabaseHelper.internalMethod();  // VIOLATION: accessing package-private
    }
}
```

**Detection:**
- Accessing classes without public modifier from different package
- Using package-private methods across packages

**Impact:** Medium - Breaks encapsulation

**Fix:**
- Make proper public API
- Use service layer
- Don't expose internal helpers

### 3. Static Coupling

**Pattern:**
```java
// domain/service/OrderService.java
package com.example.domain.service;

import com.example.infrastructure.EmailSender;

public class OrderService {
    public void processOrder(Order order) {
        EmailSender.sendEmail(order.getEmail());  // VIOLATION: static coupling
    }
}
```

**Detection:**
- Static method calls across boundaries
- Direct class references without injection

**Impact:** High - Prevents testing and flexibility

**Fix:**
```java
// domain/service/OrderService.java
package com.example.domain.service;

import com.example.domain.port.EmailService;

public class OrderService {
    private final EmailService emailService;

    public OrderService(EmailService emailService) {
        this.emailService = emailService;
    }

    public void processOrder(Order order) {
        emailService.send(order.getEmail());
    }
}
```

### 4. Upward Dependencies

**Pattern:**
```java
// domain/model/User.java
package com.example.domain.model;

import com.example.api.dto.UserDTO;  // VIOLATION: domain depends on API

public class User {
    public UserDTO toDTO() {  // Domain shouldn't know about API DTOs
        return new UserDTO(this);
    }
}
```

**Detection:**
- Inner layer imports outer layer
- Domain depends on presentation/API

**Impact:** High - Inverts dependency direction

**Fix:**
```java
// api/dto/UserDTO.java
package com.example.api.dto;

import com.example.domain.model.User;

public class UserDTO {
    public static UserDTO from(User user) {  // Mapping in outer layer
        return new UserDTO(user.getId(), user.getName());
    }
}
```

### 5. Framework Coupling in Domain

**Pattern:**
```java
// domain/model/User.java
package com.example.domain.model;

import javax.persistence.*;  // VIOLATION: JPA in domain

@Entity
@Table(name = "users")
public class User {
    @Id
    private Long id;
}
```

**Detection:**
- Framework annotations in domain models
- Framework-specific types in domain

**Impact:** High - Couples domain to infrastructure

**Fix:**
```java
// domain/model/User.java - Pure domain model
package com.example.domain.model;

public class User {
    private Long id;
    private String name;
    // Pure domain logic, no framework dependencies
}

// infrastructure/persistence/UserEntity.java - Persistence model
package com.example.infrastructure.persistence;

import javax.persistence.*;

@Entity
@Table(name = "users")
public class UserEntity {
    @Id
    private Long id;

    public User toDomain() {
        return new User(id, name);
    }
}
```

## Detection Checklist

### Import Analysis
- [ ] Map all imports between packages
- [ ] Identify cross-boundary imports
- [ ] Check dependency directions
- [ ] Find circular dependencies

### Layer Violations
- [ ] Presentation → Domain (allowed)
- [ ] Presentation → Infrastructure (violation if skips domain)
- [ ] Domain → Infrastructure (violation)
- [ ] Domain → Presentation (violation)
- [ ] Infrastructure → Domain (allowed for interfaces)

### Coupling Checks
- [ ] Concrete class dependencies across boundaries
- [ ] Static method calls across boundaries
- [ ] Direct instantiation across boundaries
- [ ] Framework dependencies in domain

### Encapsulation Checks
- [ ] Private/internal access from outside
- [ ] Package-private access violations
- [ ] Accessing implementation details
- [ ] Bypassing public APIs

## Severity Levels

### Critical
- Domain depends on infrastructure
- Circular dependencies
- Upward dependencies in layered architecture

### High
- Layer skipping
- Concrete type dependencies across boundaries
- Framework coupling in domain

### Medium
- Accessing private/internal members
- Static coupling across boundaries
- Missing interfaces at boundaries

### Low
- Suboptimal package structure
- Inconsistent naming conventions
- Missing documentation of boundaries
