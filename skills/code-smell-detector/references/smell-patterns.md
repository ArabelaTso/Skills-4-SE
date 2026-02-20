# Code Smell Patterns Reference

Comprehensive catalog of code quality and design smells in Python.

## Code Quality Smells

### Pattern 1: Duplicate Code

**Description:** Same or very similar code appears in multiple places.

**Impact:** Changes must be made in multiple locations, increasing maintenance burden and bug risk.

**Detection:**
- Identical or nearly identical code blocks
- Copy-pasted functions with minor variations
- Similar logic in multiple methods

**Example:**
```python
# ❌ Duplicate code
class UserService:
    def create_user(self, data):
        if not data.get('email'):
            raise ValueError("Email required")
        if not data.get('name'):
            raise ValueError("Name required")
        # Create user...

    def update_user(self, data):
        if not data.get('email'):
            raise ValueError("Email required")
        if not data.get('name'):
            raise ValueError("Name required")
        # Update user...

# ✅ Extract common validation
class UserService:
    def _validate_user_data(self, data):
        if not data.get('email'):
            raise ValueError("Email required")
        if not data.get('name'):
            raise ValueError("Name required")

    def create_user(self, data):
        self._validate_user_data(data)
        # Create user...

    def update_user(self, data):
        self._validate_user_data(data)
        # Update user...
```

**Refactoring:** Extract Method, Pull Up Method, Form Template Method

### Pattern 2: Magic Numbers

**Description:** Numeric literals with unclear meaning appearing directly in code.

**Impact:** Hard to understand intent, difficult to change, easy to make mistakes.

**Example:**
```python
# ❌ Magic numbers
def calculate_discount(price):
    if price > 1000:
        return price * 0.15
    elif price > 500:
        return price * 0.10
    else:
        return price * 0.05

# ✅ Named constants
BULK_ORDER_THRESHOLD = 1000
LARGE_ORDER_THRESHOLD = 500
BULK_DISCOUNT_RATE = 0.15
LARGE_DISCOUNT_RATE = 0.10
STANDARD_DISCOUNT_RATE = 0.05

def calculate_discount(price):
    if price > BULK_ORDER_THRESHOLD:
        return price * BULK_DISCOUNT_RATE
    elif price > LARGE_ORDER_THRESHOLD:
        return price * LARGE_DISCOUNT_RATE
    else:
        return price * STANDARD_DISCOUNT_RATE
```

**Refactoring:** Replace Magic Number with Symbolic Constant

### Pattern 3: Hardcoded Values

**Description:** Configuration values, paths, or strings embedded directly in code.

**Impact:** Difficult to change for different environments, violates DRY principle.

**Example:**
```python
# ❌ Hardcoded values
def save_file(data):
    with open('/var/app/data/output.txt', 'w') as f:
        f.write(data)

def send_email(user):
    send_to('admin@example.com', f'User {user.name} registered')

# ✅ Configuration-based
import os

class Config:
    OUTPUT_PATH = os.getenv('OUTPUT_PATH', '/var/app/data/output.txt')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')

def save_file(data):
    with open(Config.OUTPUT_PATH, 'w') as f:
        f.write(data)

def send_email(user):
    send_to(Config.ADMIN_EMAIL, f'User {user.name} registered')
```

**Refactoring:** Introduce Parameter Object, Use Configuration

### Pattern 4: Commented-Out Code

**Description:** Code that has been commented out but not removed.

**Impact:** Clutters codebase, creates confusion about what's actually used.

**Example:**
```python
# ❌ Commented code
def process_order(order):
    # Old implementation
    # validate_order(order)
    # calculate_total(order)
    # charge_payment(order)

    # New implementation
    process_payment_v2(order)
    send_confirmation(order)

# ✅ Clean code
def process_order(order):
    process_payment(order)
    send_confirmation(order)
```

**Refactoring:** Delete the code (version control preserves history)

### Pattern 5: Long Identifier Names

**Description:** Excessively long variable or function names.

**Impact:** Reduces readability, makes code harder to scan.

**Example:**
```python
# ❌ Too long
def calculate_total_price_including_tax_and_shipping_for_customer_order(order):
    pass

# ✅ Appropriately named
def calculate_order_total(order):
    """Calculate total including tax and shipping."""
    pass
```

**Refactoring:** Rename, use docstrings for detailed explanations

### Pattern 6: Inconsistent Naming

**Description:** Similar concepts use different naming conventions.

**Impact:** Confusing, harder to learn codebase.

**Example:**
```python
# ❌ Inconsistent
def getUserData(user_id):
    pass

def fetch_product_info(product_id):
    pass

def RetrieveOrderDetails(order_id):
    pass

# ✅ Consistent
def get_user(user_id):
    pass

def get_product(product_id):
    pass

def get_order(order_id):
    pass
```

**Refactoring:** Standardize naming conventions

## Design Smells

### Pattern 7: God Class

**Description:** Class that knows too much or does too much.

**Impact:** Hard to understand, test, and maintain. Violates Single Responsibility Principle.

**Indicators:**
- More than 20 methods
- Touches many different concerns
- Large number of fields
- Many dependencies

**Example:**
```python
# ❌ God class
class UserManager:
    def create_user(self, data): pass
    def update_user(self, user_id, data): pass
    def delete_user(self, user_id): pass
    def authenticate_user(self, username, password): pass
    def send_welcome_email(self, user): pass
    def send_password_reset_email(self, user): pass
    def generate_password_reset_token(self, user): pass
    def validate_password_strength(self, password): pass
    def hash_password(self, password): pass
    def log_user_activity(self, user, action): pass
    def export_user_data(self, user): pass
    def import_user_data(self, data): pass
    def calculate_user_statistics(self, user): pass
    def get_user_recommendations(self, user): pass
    # ... 20+ more methods

# ✅ Split by responsibility
class UserRepository:
    def create(self, data): pass
    def update(self, user_id, data): pass
    def delete(self, user_id): pass
    def find_by_id(self, user_id): pass

class UserAuthenticationService:
    def authenticate(self, username, password): pass
    def hash_password(self, password): pass
    def validate_password_strength(self, password): pass
    def generate_reset_token(self, user): pass

class UserNotificationService:
    def send_welcome_email(self, user): pass
    def send_password_reset_email(self, user): pass

class UserAnalyticsService:
    def log_activity(self, user, action): pass
    def calculate_statistics(self, user): pass
    def get_recommendations(self, user): pass
```

**Refactoring:** Extract Class, Extract Service

### Pattern 8: Feature Envy

**Description:** Method uses more features from another class than its own.

**Impact:** Poor cohesion, method is in the wrong place.

**Example:**
```python
# ❌ Feature envy
class Order:
    def __init__(self, items, customer):
        self.items = items
        self.customer = customer

    def calculate_total(self):
        # Uses customer features heavily
        discount_rate = self.customer.get_discount_rate()
        is_premium = self.customer.is_premium_member()
        shipping_address = self.customer.get_shipping_address()

        total = sum(item.price for item in self.items)

        if is_premium:
            total *= (1 - discount_rate)

        if shipping_address.country != 'US':
            total += 50  # International shipping

        return total

# ✅ Move method to appropriate class
class Customer:
    def calculate_order_total(self, items):
        total = sum(item.price for item in items)

        if self.is_premium_member():
            total *= (1 - self.get_discount_rate())

        if self.shipping_address.country != 'US':
            total += 50

        return total

class Order:
    def __init__(self, items, customer):
        self.items = items
        self.customer = customer

    def calculate_total(self):
        return self.customer.calculate_order_total(self.items)
```

**Refactoring:** Move Method, Extract Method

### Pattern 9: Inappropriate Intimacy

**Description:** Classes that access each other's internal details too much.

**Impact:** Tight coupling, changes ripple across classes.

**Example:**
```python
# ❌ Inappropriate intimacy
class BankAccount:
    def __init__(self):
        self.balance = 0
        self._transaction_log = []

class AccountManager:
    def transfer_funds(self, from_account, to_account, amount):
        # Directly accessing internals
        if from_account.balance >= amount:
            from_account.balance -= amount
            to_account.balance += amount
            from_account._transaction_log.append(f"Transferred {amount}")
            to_account._transaction_log.append(f"Received {amount}")

# ✅ Use proper encapsulation
class BankAccount:
    def __init__(self):
        self._balance = 0
        self._transaction_log = []

    def withdraw(self, amount):
        if self._balance >= amount:
            self._balance -= amount
            self._log_transaction(f"Withdrew {amount}")
            return True
        return False

    def deposit(self, amount):
        self._balance += amount
        self._log_transaction(f"Deposited {amount}")

    def _log_transaction(self, message):
        self._transaction_log.append(message)

class AccountManager:
    def transfer_funds(self, from_account, to_account, amount):
        if from_account.withdraw(amount):
            to_account.deposit(amount)
            return True
        return False
```

**Refactoring:** Move Method, Hide Delegate, Encapsulate Field

### Pattern 10: Data Clumps

**Description:** Same group of variables appears together in multiple places.

**Impact:** Suggests missing abstraction, code duplication.

**Example:**
```python
# ❌ Data clumps
def create_user(name, email, phone, address_street, address_city, address_zip):
    pass

def update_user(user_id, name, email, phone, address_street, address_city, address_zip):
    pass

def send_mail(name, email, phone, address_street, address_city, address_zip):
    pass

# ✅ Introduce parameter object
from dataclasses import dataclass

@dataclass
class Address:
    street: str
    city: str
    zip_code: str

@dataclass
class ContactInfo:
    name: str
    email: str
    phone: str
    address: Address

def create_user(contact_info: ContactInfo):
    pass

def update_user(user_id: int, contact_info: ContactInfo):
    pass

def send_mail(contact_info: ContactInfo):
    pass
```

**Refactoring:** Extract Class, Introduce Parameter Object

### Pattern 11: Primitive Obsession

**Description:** Using primitive types instead of small objects for simple tasks.

**Impact:** Missing domain concepts, validation logic scattered.

**Example:**
```python
# ❌ Primitive obsession
def process_order(order_id: str, customer_email: str, total_cents: int):
    # Validation scattered
    if '@' not in customer_email:
        raise ValueError("Invalid email")
    if total_cents < 0:
        raise ValueError("Invalid amount")
    # Process...

# ✅ Use value objects
from dataclasses import dataclass

@dataclass
class Email:
    address: str

    def __post_init__(self):
        if '@' not in self.address:
            raise ValueError("Invalid email")

@dataclass
class Money:
    cents: int

    def __post_init__(self):
        if self.cents < 0:
            raise ValueError("Amount cannot be negative")

    @property
    def dollars(self):
        return self.cents / 100

@dataclass
class OrderId:
    value: str

def process_order(order_id: OrderId, email: Email, total: Money):
    # Validation is built into the types
    # Process...
```

**Refactoring:** Replace Data Value with Object, Introduce Value Object

### Pattern 12: Long Parameter List

**Description:** Functions with too many parameters.

**Impact:** Hard to understand, remember, and use correctly.

**Example:**
```python
# ❌ Long parameter list
def create_invoice(
    customer_id,
    customer_name,
    customer_email,
    items,
    subtotal,
    tax_rate,
    tax_amount,
    discount_code,
    discount_amount,
    shipping_cost,
    total,
    payment_method,
    billing_address,
    shipping_address
):
    pass

# ✅ Use parameter objects
from dataclasses import dataclass
from typing import List

@dataclass
class Customer:
    id: str
    name: str
    email: str

@dataclass
class InvoiceDetails:
    items: List[object]
    subtotal: float
    tax_rate: float
    tax_amount: float
    discount_code: str
    discount_amount: float
    shipping_cost: float
    total: float

@dataclass
class PaymentInfo:
    method: str
    billing_address: str
    shipping_address: str

def create_invoice(customer: Customer, details: InvoiceDetails, payment: PaymentInfo):
    pass
```

**Refactoring:** Introduce Parameter Object, Preserve Whole Object

### Pattern 13: Shotgun Surgery

**Description:** Single change requires modifications across many classes.

**Impact:** Easy to miss changes, high risk of bugs.

**Example:**
```python
# ❌ Shotgun surgery - adding a new payment method requires changes everywhere
class OrderProcessor:
    def process(self, order):
        if order.payment_method == 'credit_card':
            # handle credit card
        elif order.payment_method == 'paypal':
            # handle paypal
        # Need to add cash here

class InvoiceGenerator:
    def generate(self, order):
        if order.payment_method == 'credit_card':
            # credit card invoice
        elif order.payment_method == 'paypal':
            # paypal invoice
        # Need to add cash here

class Receipt:
    def create(self, order):
        if order.payment_method == 'credit_card':
            # credit card receipt
        elif order.payment_method == 'paypal':
            # paypal receipt
        # Need to add cash here

# ✅ Use polymorphism
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount): pass

    @abstractmethod
    def generate_invoice(self): pass

    @abstractmethod
    def create_receipt(self): pass

class CreditCardPayment(PaymentMethod):
    def process(self, amount): pass
    def generate_invoice(self): pass
    def create_receipt(self): pass

class PayPalPayment(PaymentMethod):
    def process(self, amount): pass
    def generate_invoice(self): pass
    def create_receipt(self): pass

class CashPayment(PaymentMethod):  # Just add one new class
    def process(self, amount): pass
    def generate_invoice(self): pass
    def create_receipt(self): pass

class OrderProcessor:
    def process(self, order):
        order.payment_method.process(order.total)
```

**Refactoring:** Move Method, Inline Class, Replace Conditional with Polymorphism

### Pattern 14: Lazy Class

**Description:** Class that doesn't do enough to justify its existence.

**Impact:** Unnecessary complexity, maintenance overhead.

**Example:**
```python
# ❌ Lazy class
class UserNameFormatter:
    def format(self, name):
        return name.strip().title()

class User:
    def __init__(self, name):
        formatter = UserNameFormatter()
        self.name = formatter.format(name)

# ✅ Inline the class
class User:
    def __init__(self, name):
        self.name = name.strip().title()
```

**Refactoring:** Inline Class, Collapse Hierarchy

## Detection Strategies

### Metrics-Based Detection

**Function/Method Complexity:**
- Lines of code > 50
- Cyclomatic complexity > 10
- Nesting depth > 4
- Parameters > 5

**Class Complexity:**
- Methods > 15 (large class)
- Methods > 20 (god class)
- Fields > 10
- Dependencies > 7

**Code Duplication:**
- Identical code blocks > 5 lines
- Similar code with minor variations
- Token-based similarity > 80%

### Pattern-Based Detection

**Look for:**
- Multiple methods accessing same external data (Feature Envy)
- Same parameter groups (Data Clumps)
- Primitive types for domain concepts (Primitive Obsession)
- Direct field access between classes (Inappropriate Intimacy)
- Long if-else chains on type (Switch Statements smell)

### Tool-Based Detection

**Python tools:**
- `radon` - Cyclomatic complexity, maintainability index
- `pylint` - General code quality
- `flake8` - Style and quality
- `mccabe` - Complexity checker
- `vulture` - Dead code
- `bandit` - Security issues

## Prioritization

**High Priority (Fix Soon):**
- God classes
- Shotgun surgery
- Feature envy
- Long parameter lists

**Medium Priority (Plan Refactoring):**
- Large classes
- Duplicate code
- Data clumps
- Primitive obsession

**Low Priority (Nice to Have):**
- Magic numbers
- Lazy classes
- Long method names
- Inconsistent naming
