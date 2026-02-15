# Refactoring Strategies

## Coupling Reduction

### Strategy: Dependency Injection

**Problem**: Class creates its own dependencies (tight coupling)

**Solution**: Inject dependencies through constructor or setters

```python
# Before
class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()  # Hardcoded dependency
        self.logger = FileLogger()

# After
class OrderService:
    def __init__(self, db, logger):
        self.db = db  # Injected - can use any database
        self.logger = logger  # Injected - can use any logger
```

### Strategy: Interface/Abstract Base Class

**Problem**: Direct dependency on concrete implementations

**Solution**: Depend on abstractions (interfaces)

```python
# Before
class PaymentProcessor:
    def process(self, amount):
        stripe_api = StripeAPI()  # Tight coupling to Stripe
        stripe_api.charge(amount)

# After
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount):
        pass

class StripeGateway(PaymentGateway):
    def charge(self, amount):
        # Stripe implementation
        pass

class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def process(self, amount):
        self.gateway.charge(amount)
```

### Strategy: Facade Pattern

**Problem**: Client knows too much about subsystem complexity

**Solution**: Provide simplified interface

```python
# Before - Client deals with complexity
class Client:
    def process_order(self):
        inventory = InventorySystem()
        payment = PaymentSystem()
        shipping = ShippingSystem()
        notification = NotificationSystem()

        inventory.check_availability()
        payment.process()
        shipping.schedule()
        notification.send()

# After - Facade simplifies
class OrderFacade:
    def __init__(self):
        self.inventory = InventorySystem()
        self.payment = PaymentSystem()
        self.shipping = ShippingSystem()
        self.notification = NotificationSystem()

    def process_order(self):
        self.inventory.check_availability()
        self.payment.process()
        self.shipping.schedule()
        self.notification.send()

class Client:
    def process_order(self):
        facade = OrderFacade()
        facade.process_order()
```

## Cohesion Improvement

### Strategy: Extract Class

**Problem**: Class does too many things (low cohesion)

**Solution**: Split into focused classes

```python
# Before - Low cohesion
class User:
    def __init__(self):
        self.name = ""
        self.email = ""
        # Database fields
        self.db_connection = None
        # Email fields
        self.smtp_server = None

    def save_to_database(self):
        pass

    def send_email(self, subject, body):
        pass

# After - High cohesion
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def save(self, user):
        pass

class EmailService:
    def __init__(self, smtp_server):
        self.smtp = smtp_server

    def send(self, to, subject, body):
        pass
```

### Strategy: Move Method

**Problem**: Method belongs in different class (Feature Envy)

**Solution**: Move method to appropriate class

```python
# Before
class Account:
    def __init__(self):
        self.balance = 0

class AccountReporter:
    def get_formatted_balance(self, account):
        return f"${account.balance:.2f}"

# After - Move formatting to Account
class Account:
    def __init__(self):
        self.balance = 0

    def get_formatted_balance(self):
        return f"${self.balance:.2f}"

class AccountReporter:
    def generate_report(self, account):
        return f"Balance: {account.get_formatted_balance()}"
```

## Complexity Reduction

### Strategy: Extract Method

**Problem**: Long, complex method

**Solution**: Break into smaller, focused methods

```python
# Before - Complex method
def process_order(order):
    # Validation (20 lines)
    if not order.items:
        raise ValueError("No items")
    for item in order.items:
        if item.quantity <= 0:
            raise ValueError("Invalid quantity")
    # ... more validation

    # Price calculation (15 lines)
    subtotal = sum(item.price * item.quantity for item in order.items)
    tax = subtotal * 0.1
    # ... more calculation

    # Save to database (10 lines)
    connection = get_db_connection()
    cursor = connection.cursor()
    # ... database operations

# After - Extracted methods
def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    save_order(order, total)

def validate_order(order):
    if not order.items:
        raise ValueError("No items")
    validate_items(order.items)

def validate_items(items):
    for item in items:
        if item.quantity <= 0:
            raise ValueError("Invalid quantity")

def calculate_total(order):
    subtotal = calculate_subtotal(order.items)
    tax = calculate_tax(subtotal)
    return subtotal + tax

def save_order(order, total):
    repository = OrderRepository()
    repository.save(order, total)
```

### Strategy: Replace Conditional with Polymorphism

**Problem**: Complex conditional logic based on type

**Solution**: Use polymorphism

```python
# Before - Complex conditionals
def calculate_price(customer_type, base_price):
    if customer_type == "regular":
        return base_price
    elif customer_type == "premium":
        return base_price * 0.9
    elif customer_type == "vip":
        return base_price * 0.8
    else:
        return base_price

# After - Polymorphism
class Customer:
    def calculate_price(self, base_price):
        return base_price

class PremiumCustomer(Customer):
    def calculate_price(self, base_price):
        return base_price * 0.9

class VIPCustomer(Customer):
    def calculate_price(self, base_price):
        return base_price * 0.8
```

### Strategy: Introduce Parameter Object

**Problem**: Long parameter list

**Solution**: Group related parameters

```python
# Before - Long parameter list
def create_address(street, city, state, zip_code, country):
    pass

def create_user(name, email, phone,
                street, city, state, zip_code, country,
                birth_date, gender):
    pass

# After - Parameter object
class Address:
    def __init__(self, street, city, state, zip_code, country):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

class UserInfo:
    def __init__(self, name, email, phone, address, birth_date, gender):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.birth_date = birth_date
        self.gender = gender

def create_user(user_info: UserInfo):
    pass
```

## Size Reduction

### Strategy: Split Large Class

**Problem**: God class doing too much

**Solution**: Apply Single Responsibility Principle

```python
# Before - God class
class UserManager:
    def create_user(self):
        pass
    def update_user(self):
        pass
    def delete_user(self):
        pass
    def send_email(self):
        pass
    def log_activity(self):
        pass
    def generate_report(self):
        pass
    def export_to_csv(self):
        pass
    # ... 20 more methods

# After - Split by responsibility
class UserRepository:
    def create(self, user):
        pass
    def update(self, user):
        pass
    def delete(self, user_id):
        pass

class NotificationService:
    def send_email(self, user, message):
        pass

class ActivityLogger:
    def log(self, activity):
        pass

class ReportGenerator:
    def generate_user_report(self):
        pass

class DataExporter:
    def export_to_csv(self, data):
        pass
```

## Encapsulation Improvement

### Strategy: Encapsulate Field

**Problem**: Public fields expose internal state

**Solution**: Make fields private, provide methods

```python
# Before - Public fields
class Account:
    def __init__(self):
        self.balance = 0  # Public

# After - Encapsulated
class Account:
    def __init__(self):
        self._balance = 0  # Private

    def get_balance(self):
        return self._balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
```

### Strategy: Replace Data Value with Object

**Problem**: Primitive obsession, using primitives for domain concepts

**Solution**: Create domain objects

```python
# Before - Primitives
class Order:
    def __init__(self):
        self.customer_name = ""
        self.customer_email = ""
        self.customer_phone = ""

# After - Domain object
class Customer:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def send_notification(self, message):
        # Business logic
        pass

class Order:
    def __init__(self, customer: Customer):
        self.customer = customer
```

## Refactoring Workflow

### 1. Detect Smells

Run static analysis:
```bash
python scripts/detect_smells.py src/
```

### 2. Prioritize Issues

Focus on:
- Critical issues first (God classes, high coupling)
- High-impact, low-effort refactorings
- Areas with frequent changes

### 3. Write Tests

Before refactoring:
```python
def test_user_creation():
    user = create_user("John", "john@example.com")
    assert user.name == "John"
    assert user.email == "john@example.com"
```

### 4. Refactor Incrementally

Make small changes:
- Extract one method at a time
- Run tests after each change
- Commit frequently

### 5. Verify Improvements

Run smell detection again:
```bash
python scripts/detect_smells.py src/
```

Compare metrics before/after.

## Anti-Patterns to Avoid

### Premature Optimization

Don't refactor before proving there's a problem:
```python
# ❌ Premature - Complicating simple code
class CalculatorFactory:
    @staticmethod
    def create():
        return Calculator()

# ✅ Simple is better for simple cases
class Calculator:
    def add(self, a, b):
        return a + b
```

### Over-Engineering

Don't add unnecessary abstraction layers:
```python
# ❌ Over-engineered for simple CRUD
class UserRepositoryInterface:
    pass

class UserRepositoryImplementation(UserRepositoryInterface):
    pass

class UserRepositoryFactory:
    @staticmethod
    def create():
        return UserRepositoryImplementation()

# ✅ Simple CRUD doesn't need abstraction
class UserRepository:
    def create(self, user):
        pass
    def read(self, user_id):
        pass
```

### Shotgun Surgery

Avoid changes that require touching many files:
- Sign of high coupling
- Indicates need for better abstraction
- Extract common code to single location

## Metrics for Success

Track improvements:
- **Coupling**: Reduce import count, fan-out
- **Cohesion**: Increase LCOM score
- **Complexity**: Reduce cyclomatic complexity
- **Size**: Reduce method/class LOC
- **Test Coverage**: Maintain or improve

Example metrics dashboard:
```
Before Refactoring:
- God classes: 5
- Methods > 50 LOC: 23
- Cyclomatic > 10: 15
- LCOM > 0.7: 8

After Refactoring:
- God classes: 0
- Methods > 50 LOC: 3
- Cyclomatic > 10: 2
- LCOM > 0.7: 1
```
