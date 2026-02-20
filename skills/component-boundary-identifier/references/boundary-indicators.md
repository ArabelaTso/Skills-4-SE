# Boundary Indicators

## Python Boundary Indicators

### Package Structure
Boundaries are typically defined by package structure:

```
project/
├── domain/          # Domain/business logic boundary
│   ├── models.py
│   └── services.py
├── infrastructure/  # Infrastructure boundary
│   ├── database.py
│   └── cache.py
├── api/            # API/presentation boundary
│   └── routes.py
└── shared/         # Shared utilities (cross-cutting)
    └── utils.py
```

### Import Patterns

**Strong boundary indicators:**
- Top-level packages (e.g., `domain`, `infrastructure`, `api`)
- Separate namespace packages
- Explicit `__init__.py` with controlled exports

**Weak boundary indicators:**
- Submodules within same package
- Internal modules (prefixed with `_`)
- Utility modules

### Dependency Direction Rules

**Allowed:**
```python
# API layer depends on domain
from domain.services import UserService

# Infrastructure implements domain interfaces
from domain.repositories import UserRepository
```

**Violation:**
```python
# Domain depends on infrastructure (wrong direction)
from infrastructure.database import DatabaseConnection

# Domain depends on API (wrong direction)
from api.routes import get_user_endpoint
```

### Coupling Indicators

**High coupling (boundary violation):**
- Direct imports of implementation details
- Accessing private attributes across modules
- Circular dependencies
- Deep import chains

**Low coupling (good boundaries):**
- Interface/protocol-based dependencies
- Dependency injection
- Event-based communication
- Facade patterns

## Java Boundary Indicators

### Package Structure
Boundaries defined by package hierarchy:

```
com.example.project/
├── domain/              # Domain boundary
│   ├── model/
│   └── service/
├── infrastructure/      # Infrastructure boundary
│   ├── persistence/
│   └── messaging/
├── application/         # Application boundary
│   └── api/
└── shared/             # Shared utilities
    └── util/
```

### Access Modifiers

**Boundary enforcement:**
- `public`: Cross-boundary API
- `protected`: Within hierarchy
- Package-private (no modifier): Within package boundary
- `private`: Within class

### Dependency Direction Rules

**Allowed:**
```java
// Application depends on domain
import com.example.project.domain.service.UserService;

// Infrastructure implements domain interfaces
import com.example.project.domain.repository.UserRepository;
```

**Violation:**
```java
// Domain depends on infrastructure
import com.example.project.infrastructure.persistence.JpaUserRepository;

// Domain depends on application
import com.example.project.application.api.UserController;
```

### Coupling Indicators

**High coupling:**
- Direct class dependencies across boundaries
- Static method calls across boundaries
- Concrete class instantiation across boundaries
- Tight coupling to implementation details

**Low coupling:**
- Interface-based dependencies
- Dependency injection (Spring, Guice)
- Factory patterns
- Service locator pattern

## Architectural Patterns

### Layered Architecture

**Layers (top to bottom):**
1. Presentation/API layer
2. Application/Service layer
3. Domain/Business layer
4. Infrastructure/Data layer

**Rules:**
- Each layer depends only on layers below
- No skipping layers
- No upward dependencies

### Hexagonal Architecture (Ports & Adapters)

**Core boundaries:**
- **Domain core**: Business logic (center)
- **Ports**: Interfaces for external interaction
- **Adapters**: Implementations of ports (outside)

**Rules:**
- Domain has no dependencies on adapters
- Adapters depend on ports (interfaces)
- All external dependencies go through ports

### Clean Architecture

**Boundaries (inside to outside):**
1. Entities (domain models)
2. Use Cases (business rules)
3. Interface Adapters (controllers, presenters)
4. Frameworks & Drivers (external)

**Dependency Rule:**
- Dependencies point inward only
- Inner layers know nothing about outer layers
- Interfaces in inner layers, implementations in outer

## Boundary Violation Patterns

### Direct Implementation Dependency

**Python:**
```python
# VIOLATION: Domain depends on specific infrastructure
from infrastructure.postgres_repository import PostgresUserRepository

class UserService:
    def __init__(self):
        self.repo = PostgresUserRepository()  # Concrete dependency
```

**Should be:**
```python
# CORRECT: Domain depends on interface
from domain.repositories import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo  # Interface dependency
```

### Circular Dependencies

**Python:**
```python
# module_a.py
from module_b import ClassB

class ClassA:
    def use_b(self):
        return ClassB()

# module_b.py
from module_a import ClassA  # VIOLATION: Circular

class ClassB:
    def use_a(self):
        return ClassA()
```

### Layer Skipping

**Java:**
```java
// VIOLATION: API layer directly accesses data layer
package com.example.api;

import com.example.infrastructure.JpaUserRepository;

public class UserController {
    private JpaUserRepository repo = new JpaUserRepository();  // Skips service layer
}
```

### Upward Dependencies

**Python:**
```python
# domain/services.py
from api.serializers import UserSerializer  # VIOLATION: Domain depends on API

class UserService:
    def get_user_data(self, user_id):
        user = self.repo.get(user_id)
        return UserSerializer(user).data  # Domain shouldn't know about API
```

## Boundary Identification Heuristics

### Module Cohesion
- **High cohesion within boundary**: Related functionality grouped together
- **Low cohesion across boundary**: Different concerns separated

### Coupling Metrics
- **Afferent coupling (Ca)**: Number of classes outside boundary depending on classes inside
- **Efferent coupling (Ce)**: Number of classes inside boundary depending on classes outside
- **Instability (I)**: Ce / (Ca + Ce) - ranges from 0 (stable) to 1 (unstable)

### Change Patterns
- **Boundary indicator**: Changes in one area don't require changes in another
- **Violation indicator**: Changes ripple across supposed boundaries

### Naming Conventions
- **Boundary packages**: `domain`, `infrastructure`, `api`, `application`
- **Boundary prefixes**: `core_`, `infra_`, `web_`
- **Boundary suffixes**: `_service`, `_repository`, `_controller`

## Detection Strategies

### Import Analysis
1. Map all imports between modules
2. Identify dependency clusters
3. Find circular dependencies
4. Detect layer violations

### Namespace Analysis
1. Identify top-level packages/namespaces
2. Analyze cross-namespace dependencies
3. Check for proper abstraction layers
4. Verify dependency directions

### Interface Analysis
1. Identify abstract interfaces/protocols
2. Find concrete implementations
3. Check if boundaries use interfaces
4. Verify dependency inversion

### Access Pattern Analysis
1. Check access modifiers (Java)
2. Identify public APIs
3. Find private/internal usage
4. Detect inappropriate access
