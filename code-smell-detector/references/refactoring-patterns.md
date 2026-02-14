# Refactoring Patterns

Common refactoring techniques for addressing code smells.

## Extract Method

**When to use:** Long methods, duplicate code

**Before:**
```python
def print_invoice(order):
    print("=" * 40)
    print(f"Order #{order.id}")
    print("=" * 40)

    total = 0
    for item in order.items:
        price = item.quantity * item.unit_price
        total += price
        print(f"{item.name}: ${price}")

    tax = total * 0.08
    print(f"Tax: ${tax}")
    print(f"Total: ${total + tax}")
```

**After:**
```python
def print_invoice(order):
    print_header(order)
    print_items(order.items)
    print_total(order)

def print_header(order):
    print("=" * 40)
    print(f"Order #{order.id}")
    print("=" * 40)

def print_items(items):
    for item in items:
        price = item.quantity * item.unit_price
        print(f"{item.name}: ${price}")

def calculate_subtotal(items):
    return sum(item.quantity * item.unit_price for item in items)

def print_total(order):
    subtotal = calculate_subtotal(order.items)
    tax = subtotal * 0.08
    print(f"Tax: ${tax}")
    print(f"Total: ${subtotal + tax}")
```

## Extract Class

**When to use:** God class, large class, data clumps

**Before:**
```python
class Person:
    def __init__(self, name, street, city, zip_code, country):
        self.name = name
        self.street = street
        self.city = city
        self.zip_code = zip_code
        self.country = country

    def get_full_address(self):
        return f"{self.street}, {self.city}, {self.zip_code}, {self.country}"
```

**After:**
```python
class Address:
    def __init__(self, street, city, zip_code, country):
        self.street = street
        self.city = city
        self.zip_code = zip_code
        self.country = country

    def get_full_address(self):
        return f"{self.street}, {self.city}, {self.zip_code}, {self.country}"

class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address
```

## Replace Magic Number with Symbolic Constant

**When to use:** Magic numbers

**Before:**
```python
def calculate_energy(mass):
    return mass * 299792458 ** 2
```

**After:**
```python
SPEED_OF_LIGHT = 299792458  # m/s

def calculate_energy(mass):
    return mass * SPEED_OF_LIGHT ** 2
```

## Introduce Parameter Object

**When to use:** Long parameter lists, data clumps

**Before:**
```python
def create_rectangle(x, y, width, height, color, border_width, border_color):
    pass
```

**After:**
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Size:
    width: int
    height: int

@dataclass
class Style:
    color: str
    border_width: int
    border_color: str

def create_rectangle(position: Point, size: Size, style: Style):
    pass
```

## Replace Conditional with Polymorphism

**When to use:** Long if-else chains, shotgun surgery

**Before:**
```python
class Bird:
    def __init__(self, bird_type):
        self.type = bird_type

    def get_speed(self):
        if self.type == "european":
            return 35
        elif self.type == "african":
            return 40
        elif self.type == "norwegian_blue":
            return 24
```

**After:**
```python
from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def get_speed(self):
        pass

class EuropeanBird(Bird):
    def get_speed(self):
        return 35

class AfricanBird(Bird):
    def get_speed(self):
        return 40

class NorwegianBlueBird(Bird):
    def get_speed(self):
        return 24
```

## Move Method

**When to use:** Feature envy, inappropriate intimacy

**Before:**
```python
class Account:
    def __init__(self, balance, overdraft_limit):
        self.balance = balance
        self.overdraft_limit = overdraft_limit

class AccountType:
    def __init__(self, premium):
        self.premium = premium

    def overdraft_charge(self, account):
        if self.premium:
            return account.overdraft_limit * 0.05
        else:
            return account.overdraft_limit * 0.10
```

**After:**
```python
class Account:
    def __init__(self, balance, overdraft_limit, account_type):
        self.balance = balance
        self.overdraft_limit = overdraft_limit
        self.account_type = account_type

    def overdraft_charge(self):
        if self.account_type.premium:
            return self.overdraft_limit * 0.05
        else:
            return self.overdraft_limit * 0.10

class AccountType:
    def __init__(self, premium):
        self.premium = premium
```

## Encapsulate Field

**When to use:** Inappropriate intimacy, direct field access

**Before:**
```python
class Person:
    def __init__(self, name):
        self.name = name

# Direct field access
person = Person("John")
person.name = "Jane"  # No validation
```

**After:**
```python
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

# Controlled access
person = Person("John")
person.name = "Jane"  # Goes through validation
```

## Inline Class

**When to use:** Lazy class

**Before:**
```python
class PhoneNumber:
    def __init__(self, area_code, number):
        self.area_code = area_code
        self.number = number

    def get_full_number(self):
        return f"({self.area_code}) {self.number}"

class Person:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def get_phone_number(self):
        return self.phone.get_full_number()
```

**After:**
```python
class Person:
    def __init__(self, name, area_code, number):
        self.name = name
        self.area_code = area_code
        self.number = number

    def get_phone_number(self):
        return f"({self.area_code}) {self.number}"
```
