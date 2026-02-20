# Design Smells Catalog

## Table of Contents
- [Coupling Smells](#coupling-smells)
- [Cohesion Smells](#cohesion-smells)
- [Complexity Smells](#complexity-smells)
- [Size Smells](#size-smells)
- [Encapsulation Smells](#encapsulation-smells)

## Coupling Smells

### High Coupling (Tight Coupling)

**Definition**: Class or module depends on too many other classes/modules.

**Detection**:
- Too many import statements (>20)
- Too many dependencies in constructor
- Changes in one class frequently require changes in others

**Example**:
```python
# ❌ High coupling
class UserService:
    def __init__(self):
        self.db = Database()
        self.cache = Cache()
        self.logger = Logger()
        self.validator = Validator()
        self.email_service = EmailService()
        self.sms_service = SMSService()
        self.analytics = Analytics()
        # ... many more dependencies
```

**Refactoring**:
```python
# ✅ Lower coupling with dependency injection
class UserService:
    def __init__(self, db, logger, notifier):
        self.db = db
        self.logger = logger
        self.notifier = notifier  # Abstraction for email/SMS
```

**Severity**: Major
**Metrics**: Count of dependencies, fan-out

### Feature Envy

**Definition**: Method accesses data/methods of another class more than its own.

**Detection**:
- Method makes many calls to other object's methods
- Method uses other object's data extensively
- Ratio of external access > internal access

**Example**:
```python
# ❌ Feature Envy
class OrderPrinter:
    def print_total(self, order):
        total = order.get_subtotal()
        total += order.get_tax()
        total -= order.get_discount()
        return f"Total: ${total}"
```

**Refactoring**:
```python
# ✅ Move method to Order class
class Order:
    def get_total(self):
        return self.get_subtotal() + self.get_tax() - self.get_discount()

class OrderPrinter:
    def print_total(self, order):
        return f"Total: ${order.get_total()}"
```

**Severity**: Minor
**Metrics**: External method calls / internal method calls

### Inappropriate Intimacy

**Definition**: Classes access each other's private data or implementation details.

**Detection**:
- Accessing private fields of other classes
- Friend classes in C++
- Excessive use of getters/setters

**Example**:
```python
# ❌ Inappropriate Intimacy
class Account:
    def transfer(self, other_account, amount):
        other_account._balance += amount  # Accessing private field
        self._balance -= amount
```

**Refactoring**:
```python
# ✅ Proper encapsulation
class Account:
    def deposit(self, amount):
        self._balance += amount

    def withdraw(self, amount):
        self._balance -= amount

    def transfer(self, other_account, amount):
        self.withdraw(amount)
        other_account.deposit(amount)
```

**Severity**: Major
**Metrics**: Private field access count

## Cohesion Smells

### Low Cohesion (Lack of Cohesion)

**Definition**: Class members are not related; class does too many unrelated things.

**Detection**:
- LCOM (Lack of Cohesion of Methods) > 0.7
- Methods don't share instance variables
- Class has multiple responsibilities

**Example**:
```python
# ❌ Low Cohesion
class UserManager:
    def create_user(self, name, email):
        pass

    def send_email(self, to, subject, body):
        pass

    def log_activity(self, message):
        pass

    def calculate_discount(self, price, percent):
        pass
```

**Refactoring**:
```python
# ✅ High Cohesion - Split into focused classes
class UserRepository:
    def create_user(self, name, email):
        pass

class EmailService:
    def send_email(self, to, subject, body):
        pass

class Logger:
    def log_activity(self, message):
        pass

class PricingCalculator:
    def calculate_discount(self, price, percent):
        pass
```

**Severity**: Major
**Metrics**: LCOM, method-attribute correlation

### God Class (Large Class)

**Definition**: Class that knows too much or does too much.

**Detection**:
- Too many methods (>20)
- Too many attributes (>15)
- Too many lines of code (>500)
- Low cohesion

**Example**:
```python
# ❌ God Class
class Application:
    def __init__(self):
        # 20+ attributes
        pass

    # 30+ methods handling:
    # - User management
    # - Order processing
    # - Payment handling
    # - Reporting
    # - Email notifications
    # - File operations
    # - Database access
    # ...
```

**Refactoring**:
```python
# ✅ Split into focused classes
class UserManager:
    pass

class OrderProcessor:
    pass

class PaymentHandler:
    pass

class ReportGenerator:
    pass
```

**Severity**: Critical
**Metrics**: Method count, attribute count, LOC

## Complexity Smells

### High Cyclomatic Complexity

**Definition**: Too many decision points in a method.

**Detection**:
- Cyclomatic complexity > 10
- Too many if/else, switch, loops
- Deep nesting levels

**Example**:
```python
# ❌ High Complexity (complexity = 12)
def process_order(order):
    if order.is_valid():
        if order.has_items():
            if order.customer.is_verified():
                if order.total > 1000:
                    if order.customer.credit_score > 700:
                        # Apply discount
                    else:
                        # Require approval
                else:
                    # Process normally
            else:
                # Verify customer
        else:
            # Add items
    else:
        # Handle invalid
```

**Refactoring**:
```python
# ✅ Lower Complexity - Extract methods
def process_order(order):
    validate_order(order)
    verify_customer(order.customer)
    apply_pricing_rules(order)
    process_payment(order)
```

**Severity**: Major
**Metrics**: Cyclomatic complexity

### Long Method

**Definition**: Method that is too long and does too much.

**Detection**:
- Method > 50 lines
- Method has multiple responsibilities
- Many local variables

**Example**:
```python
# ❌ Long Method (100+ lines)
def process_user_registration(data):
    # Validate input (20 lines)
    # Check for duplicates (15 lines)
    # Create user record (10 lines)
    # Send confirmation email (20 lines)
    # Update statistics (10 lines)
    # Log activity (15 lines)
    # Notify admins (10 lines)
    pass
```

**Refactoring**:
```python
# ✅ Extract smaller methods
def process_user_registration(data):
    validate_input(data)
    check_duplicates(data['email'])
    user = create_user(data)
    send_confirmation_email(user)
    update_statistics()
    log_registration(user)
    notify_admins(user)
```

**Severity**: Major
**Metrics**: Lines of code, statement count

## Size Smells

### Long Parameter List

**Definition**: Method has too many parameters.

**Detection**:
- More than 5 parameters
- Difficult to understand method signature
- Parameters are related

**Example**:
```python
# ❌ Long Parameter List
def create_user(name, email, phone, address, city, state, zip, country, age, gender):
    pass
```

**Refactoring**:
```python
# ✅ Use parameter object
class UserInfo:
    def __init__(self, name, email, contact, address, demographics):
        self.name = name
        self.email = email
        self.contact = contact
        self.address = address
        self.demographics = demographics

def create_user(user_info: UserInfo):
    pass
```

**Severity**: Minor
**Metrics**: Parameter count

### Large Module

**Definition**: Module/package with too many classes or functions.

**Detection**:
- More than 20 classes in module
- More than 1000 LOC in module
- Module has multiple responsibilities

**Refactoring**:
- Split into sub-modules by responsibility
- Use package structure
- Apply separation of concerns

**Severity**: Major
**Metrics**: Class count, LOC

## Encapsulation Smells

### Data Class

**Definition**: Class that only contains data with getters/setters, no behavior.

**Detection**:
- Only public fields or getters/setters
- No business logic
- Just a data container

**Example**:
```python
# ❌ Data Class
class Customer:
    def __init__(self):
        self.name = None
        self.email = None
        self.phone = None

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
    # More getters/setters...
```

**Refactoring**:
```python
# ✅ Add behavior or use dataclass
from dataclasses import dataclass

@dataclass
class Customer:
    name: str
    email: str
    phone: str

    def send_notification(self, message):
        # Add business logic
        pass
```

**Severity**: Minor
**Metrics**: Method-to-field ratio

### Exposed Internal State

**Definition**: Class exposes its internal implementation details.

**Detection**:
- Public mutable fields
- Returning references to internal collections
- Getters for implementation details

**Example**:
```python
# ❌ Exposed Internal State
class ShoppingCart:
    def __init__(self):
        self.items = []  # Public list

    def get_items(self):
        return self.items  # Returns mutable reference
```

**Refactoring**:
```python
# ✅ Encapsulate internal state
class ShoppingCart:
    def __init__(self):
        self._items = []  # Private

    def add_item(self, item):
        self._items.append(item)

    def get_items(self):
        return list(self._items)  # Return copy
```

**Severity**: Minor
**Metrics**: Public field count

## Detection Thresholds

| Smell | Metric | Threshold |
|-------|--------|-----------|
| God Class | Methods | > 20 |
| God Class | Attributes | > 15 |
| God Class | LOC | > 500 |
| High Coupling | Imports | > 20 |
| High Coupling | Dependencies | > 10 |
| Low Cohesion | LCOM | > 0.7 |
| Long Method | LOC | > 50 |
| High Complexity | Cyclomatic | > 10 |
| Long Parameter List | Parameters | > 5 |
| Large Module | Classes | > 20 |

## Metrics Explained

**LCOM (Lack of Cohesion of Methods)**:
- Measures how methods share instance variables
- Range: 0.0 (high cohesion) to 1.0 (low cohesion)
- Formula: (P - Q) / M where P = pairs that don't share attributes, Q = pairs that do, M = total pairs

**Cyclomatic Complexity**:
- Number of linearly independent paths
- Each if, while, for, except adds 1
- Each boolean operator (and, or) adds 1

**Fan-out**:
- Number of classes/modules this class depends on
- High fan-out = high coupling

**Fan-in**:
- Number of classes/modules that depend on this class
- High fan-in with low coupling = good reusability
