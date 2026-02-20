# Architecture Patterns in Legacy Systems

Common architectural patterns found in legacy codebases and how to identify them.

## Table of Contents

1. [MVC (Model-View-Controller)](#mvc-model-view-controller)
2. [Layered Architecture](#layered-architecture)
3. [Microservices](#microservices)
4. [Monolithic Architecture](#monolithic-architecture)
5. [Plugin/Module-Based](#pluginmodule-based-architecture)
6. [Event-Driven Architecture](#event-driven-architecture)

---

## MVC (Model-View-Controller)

### Description
Separates application into three interconnected components: Model (data), View (presentation), Controller (logic).

### How to Identify

**Directory Structure:**
```
project/
├── models/        # Data structures and business entities
├── views/         # Templates, UI components
├── controllers/   # Request handlers, business logic
└── routes/        # URL routing
```

**Framework Indicators:**
- **Django (Python):** `models.py`, `views.py`, `urls.py`
- **Rails (Ruby):** `app/models/`, `app/views/`, `app/controllers/`
- **Spring MVC (Java):** `@Controller`, `@Service`, `@Entity` annotations
- **Express (JavaScript):** Routing files, template engines

**Code Patterns:**

```python
# Django example
# models.py
class User(models.Model):
    name = models.CharField(max_length=100)

# views.py
def user_detail(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'user_detail.html', {'user': user})

# urls.py
urlpatterns = [
    path('user/<int:user_id>/', user_detail),
]
```

### Characteristics
- Clear separation of concerns
- Models are independent of views
- Controllers mediate between models and views
- Routes map URLs to controllers

---

## Layered Architecture

### Description
Organizes code into horizontal layers, each with specific responsibility.

### Common Layers

**4-Tier Architecture:**
```
┌─────────────────────────────────┐
│   Presentation Layer            │  (UI, API endpoints)
├─────────────────────────────────┤
│   Business Logic Layer          │  (Services, domain logic)
├─────────────────────────────────┤
│   Data Access Layer             │  (Repositories, DAO)
├─────────────────────────────────┤
│   Database Layer                │  (Persistence)
└─────────────────────────────────┘
```

### How to Identify

**Directory Structure:**
```
project/
├── presentation/   # or api/, controllers/, routes/
├── services/       # or business/, domain/
├── repositories/   # or dao/, data/
└── models/         # or entities/
```

**Java/Spring Example:**
```java
// Presentation Layer
@RestController
public class UserController {
    @Autowired
    private UserService userService;
}

// Business Logic Layer
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
}

// Data Access Layer
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
}
```

**Python Example:**
```
project/
├── api/
│   └── routes.py           # Presentation
├── services/
│   └── user_service.py     # Business Logic
├── repositories/
│   └── user_repository.py  # Data Access
└── models/
    └── user.py             # Entities
```

### Characteristics
- Each layer only interacts with adjacent layers
- Top-down dependency flow
- Horizontal separation of concerns
- Clear interfaces between layers

---

## Microservices

### Description
Application composed of small, independent services communicating via APIs.

### How to Identify

**Repository Structure:**
```
monorepo/
├── user-service/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── payment-service/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── order-service/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

**Or Multiple Repositories:**
```
company/
├── user-service/
├── payment-service/
├── order-service/
└── notification-service/
```

**Indicators:**
- Multiple `Dockerfile`s
- `docker-compose.yml` or Kubernetes manifests
- API gateway or service mesh
- Each service has own database
- Inter-service communication (REST, gRPC, message queues)

**Code Patterns:**

```javascript
// Service A calls Service B via HTTP
const response = await fetch('http://payment-service:8080/process', {
    method: 'POST',
    body: JSON.stringify(paymentData)
});
```

```python
# Message queue communication
import pika
channel.basic_publish(
    exchange='',
    routing_key='order.created',
    body=json.dumps(order_data)
)
```

### Characteristics
- Independent deployment
- Technology diversity (different languages per service)
- Decentralized data management
- Service discovery mechanisms
- API contracts between services

---

## Monolithic Architecture

### Description
Single unified codebase with all functionality in one application.

### How to Identify

**Directory Structure:**
```
monolith/
├── src/
│   ├── auth/
│   ├── users/
│   ├── products/
│   ├── orders/
│   ├── payments/
│   ├── notifications/
│   └── reports/
├── config/
└── main.py  # or app.py, server.js
```

**Indicators:**
- Single entry point (one `main()` function)
- All modules in same codebase
- Shared database
- Deployed as single unit
- No inter-process communication

**Code Patterns:**

```python
# All imports are local
from auth import authenticate
from users import get_user
from orders import create_order
from payments import process_payment

def checkout(user_id, cart):
    user = get_user(user_id)
    order = create_order(user, cart)
    payment = process_payment(order)
    return order
```

### Characteristics
- Simple deployment (single artifact)
- Tight coupling between modules
- Shared dependencies
- Difficult to scale individual components
- Often grows very large over time

---

## Plugin/Module-Based Architecture

### Description
Core application with extensible plugin system.

### How to Identify

**Directory Structure:**
```
application/
├── core/           # Core functionality
├── plugins/        # or extensions/, modules/
│   ├── plugin_a/
│   ├── plugin_b/
│   └── plugin_c/
└── plugin_loader.py  # Plugin discovery/loading
```

**Indicators:**
- Plugin registration mechanism
- Plugin discovery (directory scanning, manifest files)
- Hook/event system
- Plugin configuration files

**Code Patterns:**

```python
# Plugin interface
class Plugin:
    def initialize(self):
        pass

    def process(self, data):
        pass

# Core loads plugins
import importlib
import os

plugins = []
for filename in os.listdir('plugins'):
    if filename.endswith('.py'):
        module = importlib.import_module(f'plugins.{filename[:-3]}')
        plugins.append(module.Plugin())
```

```javascript
// WordPress-style hooks
function register_plugin(name, callback) {
    hooks[name] = callback;
}

function apply_filters(name, value) {
    if (hooks[name]) {
        return hooks[name](value);
    }
    return value;
}
```

### Characteristics
- Core remains stable
- Features added via plugins
- Loose coupling
- Plugin isolation
- Often has plugin marketplace/ecosystem

---

## Event-Driven Architecture

### Description
Components communicate through events rather than direct calls.

### How to Identify

**Indicators:**
- Event bus or message broker (RabbitMQ, Kafka, Redis)
- Event publishers and subscribers
- Event handlers/listeners
- Async processing

**Code Patterns:**

```python
# Event publisher
from event_bus import publish

def create_order(order_data):
    order = Order.create(order_data)
    publish('order.created', order)
    return order

# Event subscriber
from event_bus import subscribe

@subscribe('order.created')
def send_confirmation_email(order):
    email.send(order.user.email, 'Order Confirmation')

@subscribe('order.created')
def update_inventory(order):
    for item in order.items:
        inventory.decrease(item.product_id, item.quantity)
```

```java
// Spring Event-Driven
@Component
public class OrderEventPublisher {
    @Autowired
    private ApplicationEventPublisher publisher;

    public void createOrder(Order order) {
        publisher.publishEvent(new OrderCreatedEvent(order));
    }
}

@Component
public class EmailListener {
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Send email
    }
}
```

### Characteristics
- Loose coupling between components
- Asynchronous processing
- Event log/history
- Eventual consistency
- Scalable and resilient

---

## Pattern Detection Checklist

Use this checklist to identify the architecture:

### 1. Check Project Structure
```bash
# List top-level directories
ls -la

# Look for common patterns
find . -type d -maxdepth 2 | head -20
```

### 2. Check for Framework Indicators
```bash
# Python
ls | grep -E "manage.py|setup.py|pyproject.toml"
cat requirements.txt | grep -E "django|flask|fastapi"

# Java
ls | grep -E "pom.xml|build.gradle"
cat pom.xml | grep -E "spring|jakarta"

# JavaScript
cat package.json | grep -E "express|react|vue|angular"
```

### 3. Check Entry Points
```bash
# Find main entry points
grep -r "if __name__ == '__main__'" --include="*.py"
grep -r "public static void main" --include="*.java"
cat package.json | grep "main"
```

### 4. Check Dependencies
```bash
# Look for service communication
grep -r "requests.get\|requests.post" --include="*.py"
grep -r "HttpClient\|RestTemplate" --include="*.java"

# Look for message queues
grep -r "rabbitmq\|kafka\|redis" .

# Look for database per service (microservices indicator)
find . -name "database.yml" -o -name "db.properties"
```

### 5. Check Deployment Configuration
```bash
# Microservices indicators
ls -la | grep -E "Dockerfile|docker-compose|kubernetes"

# Monolith indicators
ls -la | grep -E "Procfile|uwsgi|gunicorn"
```

---

## Mixed/Hybrid Patterns

Many legacy systems use multiple patterns:

**Common Combinations:**

1. **Monolith with Layers**
   - Single deployable unit
   - Organized into presentation/business/data layers
   - Most common in enterprise apps

2. **Modular Monolith**
   - Single deployment
   - Strongly separated modules with clear boundaries
   - Potential microservices candidates

3. **Microservices with Shared Database** (Anti-pattern)
   - Multiple services
   - BUT sharing same database
   - Indicates migration in progress

4. **MVC + Event-Driven**
   - MVC for HTTP requests
   - Events for background processing
   - Common in modern web apps

---

## Architecture Assessment

After identifying the pattern, assess its health:

### Good Signs
- ✓ Clear separation of concerns
- ✓ Consistent naming and structure
- ✓ Well-defined interfaces
- ✓ Appropriate for application size

### Warning Signs
- ⚠ Mixed patterns without clear reason
- ⚠ Tight coupling across layers
- ⚠ Circular dependencies
- ⚠ Inconsistent implementation of pattern

### Red Flags
- ❌ No discernible pattern
- ❌ "Big ball of mud" (everything depends on everything)
- ❌ Business logic scattered everywhere
- ❌ Data access mixed with presentation

---

## Documentation Template

After identifying the pattern, document it:

```markdown
## Architecture Pattern

**Primary Pattern:** [Pattern Name]

**Rationale:** [Why this pattern was chosen]

**Implementation:**
- [Layer/Component 1]: [Purpose and location]
- [Layer/Component 2]: [Purpose and location]
- [Layer/Component 3]: [Purpose and location]

**Data Flow:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Strengths:**
- [Advantage 1]
- [Advantage 2]

**Weaknesses:**
- [Issue 1]
- [Issue 2]

**Improvement Opportunities:**
- [Suggestion 1]
- [Suggestion 2]
```
