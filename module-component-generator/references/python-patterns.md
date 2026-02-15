# Python Implementation Patterns

## Interface Implementation

### Protocol-Based Implementation

**From Protocol:**
```python
from typing import Protocol

class DataRepository(Protocol):
    def get(self, id: str) -> dict:
        ...

    def save(self, data: dict) -> str:
        ...

    def delete(self, id: str) -> bool:
        ...
```

**Implementation:**
```python
class InMemoryDataRepository:
    """In-memory implementation of DataRepository."""

    def __init__(self):
        self._storage: dict[str, dict] = {}

    def get(self, id: str) -> dict:
        """Retrieve data by ID."""
        if id not in self._storage:
            raise KeyError(f"Data with id '{id}' not found")
        return self._storage[id].copy()

    def save(self, data: dict) -> str:
        """Save data and return generated ID."""
        import uuid
        data_id = data.get('id', str(uuid.uuid4()))
        self._storage[data_id] = data.copy()
        return data_id

    def delete(self, id: str) -> bool:
        """Delete data by ID, return True if deleted."""
        if id in self._storage:
            del self._storage[id]
            return True
        return False
```

### Abstract Base Class Implementation

**From ABC:**
```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> str:
        """Process payment and return transaction ID."""
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """Refund a transaction."""
        pass
```

**Implementation:**
```python
class StripePaymentProcessor(PaymentProcessor):
    """Stripe implementation of PaymentProcessor."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._transactions: dict[str, dict] = {}

    def process_payment(self, amount: float, currency: str) -> str:
        """Process payment through Stripe API."""
        import uuid

        # Validate inputs
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if currency not in ['USD', 'EUR', 'GBP']:
            raise ValueError(f"Unsupported currency: {currency}")

        # Simulate API call
        transaction_id = str(uuid.uuid4())
        self._transactions[transaction_id] = {
            'amount': amount,
            'currency': currency,
            'status': 'completed'
        }

        return transaction_id

    def refund(self, transaction_id: str) -> bool:
        """Refund a Stripe transaction."""
        if transaction_id not in self._transactions:
            return False

        transaction = self._transactions[transaction_id]
        if transaction['status'] != 'completed':
            return False

        transaction['status'] = 'refunded'
        return True
```

## Module Structure Patterns

### Service Layer Module

**Structure:**
```
user_service/
├── __init__.py
├── models.py       # Data models
├── repository.py   # Data access
├── service.py      # Business logic
└── exceptions.py   # Custom exceptions
```

**models.py:**
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """User domain model."""
    id: str
    email: str
    name: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.email or '@' not in self.email:
            raise ValueError("Invalid email address")
```

**repository.py:**
```python
from typing import Optional, List
from .models import User

class UserRepository:
    """Repository for User persistence."""

    def __init__(self):
        self._users: dict[str, User] = {}

    def find_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID."""
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def save(self, user: User) -> User:
        """Save or update user."""
        self._users[user.id] = user
        return user

    def delete(self, user_id: str) -> bool:
        """Delete user by ID."""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def list_all(self) -> List[User]:
        """List all users."""
        return list(self._users.values())
```

**service.py:**
```python
from datetime import datetime
from typing import Optional
import uuid

from .models import User
from .repository import UserRepository
from .exceptions import UserAlreadyExistsError, UserNotFoundError

class UserService:
    """Service layer for user operations."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, email: str, name: str) -> User:
        """Create a new user."""
        # Check if user already exists
        existing = self.repository.find_by_email(email)
        if existing:
            raise UserAlreadyExistsError(f"User with email {email} already exists")

        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            name=name,
            created_at=datetime.now()
        )

        return self.repository.save(user)

    def get_user(self, user_id: str) -> User:
        """Get user by ID."""
        user = self.repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user

    def update_user(self, user_id: str, name: Optional[str] = None) -> User:
        """Update user information."""
        user = self.get_user(user_id)

        if name:
            user.name = name
        user.updated_at = datetime.now()

        return self.repository.save(user)

    def delete_user(self, user_id: str) -> None:
        """Delete user."""
        if not self.repository.delete(user_id):
            raise UserNotFoundError(f"User with id {user_id} not found")
```

**exceptions.py:**
```python
class UserServiceError(Exception):
    """Base exception for user service."""
    pass

class UserAlreadyExistsError(UserServiceError):
    """Raised when attempting to create duplicate user."""
    pass

class UserNotFoundError(UserServiceError):
    """Raised when user is not found."""
    pass
```

**__init__.py:**
```python
"""User service module."""

from .models import User
from .repository import UserRepository
from .service import UserService
from .exceptions import (
    UserServiceError,
    UserAlreadyExistsError,
    UserNotFoundError
)

__all__ = [
    'User',
    'UserRepository',
    'UserService',
    'UserServiceError',
    'UserAlreadyExistsError',
    'UserNotFoundError',
]
```

### Adapter Pattern Module

**Structure:**
```
notification_adapter/
├── __init__.py
├── interface.py    # Abstract interface
├── email.py        # Email implementation
├── sms.py          # SMS implementation
└── factory.py      # Factory for creating adapters
```

**interface.py:**
```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class NotificationAdapter(ABC):
    """Abstract interface for notification adapters."""

    @abstractmethod
    def send(self, recipient: str, message: str, metadata: Dict[str, Any] = None) -> bool:
        """Send notification to recipient."""
        pass

    @abstractmethod
    def validate_recipient(self, recipient: str) -> bool:
        """Validate recipient format."""
        pass
```

**email.py:**
```python
import re
from typing import Dict, Any
from .interface import NotificationAdapter

class EmailNotificationAdapter(NotificationAdapter):
    """Email notification adapter."""

    def __init__(self, smtp_host: str, smtp_port: int):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def send(self, recipient: str, message: str, metadata: Dict[str, Any] = None) -> bool:
        """Send email notification."""
        if not self.validate_recipient(recipient):
            raise ValueError(f"Invalid email address: {recipient}")

        # Simulate sending email
        print(f"Sending email to {recipient}: {message}")
        return True

    def validate_recipient(self, recipient: str) -> bool:
        """Validate email address format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, recipient))
```

**factory.py:**
```python
from typing import Dict, Any
from .interface import NotificationAdapter
from .email import EmailNotificationAdapter
from .sms import SMSNotificationAdapter

class NotificationAdapterFactory:
    """Factory for creating notification adapters."""

    @staticmethod
    def create(adapter_type: str, config: Dict[str, Any]) -> NotificationAdapter:
        """Create notification adapter based on type."""
        if adapter_type == 'email':
            return EmailNotificationAdapter(
                smtp_host=config.get('smtp_host', 'localhost'),
                smtp_port=config.get('smtp_port', 587)
            )
        elif adapter_type == 'sms':
            return SMSNotificationAdapter(
                api_key=config.get('api_key'),
                sender_id=config.get('sender_id')
            )
        else:
            raise ValueError(f"Unknown adapter type: {adapter_type}")
```

## Best Practices

### Type Hints
- Always include type hints for parameters and return values
- Use `Optional[T]` for nullable values
- Use `List[T]`, `Dict[K, V]` for collections
- Use `Protocol` for structural typing

### Documentation
- Include docstrings for all public classes and methods
- Use Google or NumPy docstring format
- Document exceptions that can be raised
- Include usage examples for complex APIs

### Error Handling
- Create custom exception classes for domain errors
- Validate inputs early
- Provide meaningful error messages
- Use specific exception types

### Dependency Injection
- Accept dependencies through constructor
- Use protocols/ABCs for loose coupling
- Make dependencies explicit
- Facilitate testing with mock implementations
