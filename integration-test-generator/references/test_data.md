# Test Data Builders

## User Test Data

```python
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class UserBuilder:
    """Builder for creating test user data."""
    username: str = "testuser"
    email: str = "test@example.com"
    first_name: str = "Test"
    last_name: str = "User"
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    roles: List[str] = field(default_factory=list)

    def with_username(self, username: str) -> 'UserBuilder':
        self.username = username
        return self

    def with_email(self, email: str) -> 'UserBuilder':
        self.email = email
        return self

    def with_role(self, role: str) -> 'UserBuilder':
        self.roles.append(role)
        return self

    def as_admin(self) -> 'UserBuilder':
        self.roles = ["admin"]
        return self

    def inactive(self) -> 'UserBuilder':
        self.is_active = False
        return self

    def build(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "roles": self.roles
        }

# Usage example
admin_user = UserBuilder().with_username("admin").as_admin().build()
inactive_user = UserBuilder().with_email("inactive@example.com").inactive().build()
```

## Order Test Data

```python
from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal

@dataclass
class OrderItemBuilder:
    """Builder for order items."""
    product_id: int = 1
    quantity: int = 1
    price: Decimal = Decimal("10.00")

    def with_product(self, product_id: int) -> 'OrderItemBuilder':
        self.product_id = product_id
        return self

    def with_quantity(self, quantity: int) -> 'OrderItemBuilder':
        self.quantity = quantity
        return self

    def with_price(self, price: float) -> 'OrderItemBuilder':
        self.price = Decimal(str(price))
        return self

    def build(self) -> dict:
        return {
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": float(self.price),
            "subtotal": float(self.price * self.quantity)
        }

@dataclass
class OrderBuilder:
    """Builder for creating test order data."""
    user_id: int = 1
    status: str = "pending"
    items: List[dict] = field(default_factory=list)
    shipping_address: Optional[dict] = None
    payment_method: str = "credit_card"

    def for_user(self, user_id: int) -> 'OrderBuilder':
        self.user_id = user_id
        return self

    def with_status(self, status: str) -> 'OrderBuilder':
        self.status = status
        return self

    def add_item(self, product_id: int, quantity: int = 1, price: float = 10.00) -> 'OrderBuilder':
        item = (OrderItemBuilder()
                .with_product(product_id)
                .with_quantity(quantity)
                .with_price(price)
                .build())
        self.items.append(item)
        return self

    def with_shipping(self, address: dict) -> 'OrderBuilder':
        self.shipping_address = address
        return self

    def confirmed(self) -> 'OrderBuilder':
        self.status = "confirmed"
        return self

    def build(self) -> dict:
        total = sum(item["subtotal"] for item in self.items)
        return {
            "user_id": self.user_id,
            "status": self.status,
            "items": self.items,
            "total": total,
            "shipping_address": self.shipping_address,
            "payment_method": self.payment_method
        }

# Usage example
order = (OrderBuilder()
         .for_user(123)
         .add_item(product_id=1, quantity=2, price=25.00)
         .add_item(product_id=2, quantity=1, price=50.00)
         .confirmed()
         .build())
```

## Database Fixtures

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.models import Base, User, Product, Order

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def sample_users(db_session):
    """Create sample users for testing."""
    users = [
        User(username="alice", email="alice@example.com", role="admin"),
        User(username="bob", email="bob@example.com", role="user"),
        User(username="charlie", email="charlie@example.com", role="user"),
    ]
    db_session.add_all(users)
    db_session.commit()
    return users

@pytest.fixture
def sample_products(db_session):
    """Create sample products for testing."""
    products = [
        Product(name="Widget", price=10.00, stock=100),
        Product(name="Gadget", price=25.00, stock=50),
        Product(name="Doohickey", price=15.00, stock=75),
    ]
    db_session.add_all(products)
    db_session.commit()
    return products

@pytest.fixture
def order_with_items(db_session, sample_users, sample_products):
    """Create an order with items for testing."""
    user = sample_users[0]
    order = Order(user_id=user.id, status="pending")
    db_session.add(order)
    db_session.flush()

    from myapp.models import OrderItem
    items = [
        OrderItem(order_id=order.id, product_id=sample_products[0].id, quantity=2),
        OrderItem(order_id=order.id, product_id=sample_products[1].id, quantity=1),
    ]
    db_session.add_all(items)
    db_session.commit()
    return order
```

## Factory Pattern for Test Data

```python
import factory
from factory.alchemy import SQLAlchemyModelFactory
from myapp.models import User, Product, Order, OrderItem

class UserFactory(SQLAlchemyModelFactory):
    """Factory for creating test users."""

    class Meta:
        model = User
        sqlalchemy_session = None  # Set in fixture
        sqlalchemy_session_persistence = "commit"

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True

class ProductFactory(SQLAlchemyModelFactory):
    """Factory for creating test products."""

    class Meta:
        model = Product
        sqlalchemy_session = None

    name = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=200)
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    stock = factory.Faker("random_int", min=0, max=1000)

class OrderItemFactory(SQLAlchemyModelFactory):
    """Factory for creating order items."""

    class Meta:
        model = OrderItem
        sqlalchemy_session = None

    order = factory.SubFactory("tests.factories.OrderFactory")
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("random_int", min=1, max=10)
    price = factory.LazyAttribute(lambda obj: obj.product.price)

class OrderFactory(SQLAlchemyModelFactory):
    """Factory for creating test orders."""

    class Meta:
        model = Order
        sqlalchemy_session = None

    user = factory.SubFactory(UserFactory)
    status = "pending"
    items = factory.RelatedFactoryList(
        OrderItemFactory,
        factory_related_name="order",
        size=2
    )

# Usage in tests
@pytest.fixture
def factories(db_session):
    """Configure factories with database session."""
    UserFactory._meta.sqlalchemy_session = db_session
    ProductFactory._meta.sqlalchemy_session = db_session
    OrderFactory._meta.sqlalchemy_session = db_session
    OrderItemFactory._meta.sqlalchemy_session = db_session
    return {
        "user": UserFactory,
        "product": ProductFactory,
        "order": OrderFactory,
        "order_item": OrderItemFactory,
    }

def test_example(factories):
    # Create test data easily
    user = factories["user"].create(username="testuser")
    order = factories["order"].create(user=user)
    assert len(order.items) == 2
```

## API Response Builders

```python
from typing import Dict, Any, Optional

class APIResponseBuilder:
    """Builder for creating mock API responses."""

    def __init__(self):
        self.status_code = 200
        self.data = {}
        self.errors = []
        self.metadata = {}

    def with_status(self, status_code: int) -> 'APIResponseBuilder':
        self.status_code = status_code
        return self

    def with_data(self, data: Dict[str, Any]) -> 'APIResponseBuilder':
        self.data = data
        return self

    def with_error(self, error_message: str, error_code: Optional[str] = None) -> 'APIResponseBuilder':
        error = {"message": error_message}
        if error_code:
            error["code"] = error_code
        self.errors.append(error)
        return self

    def with_pagination(self, page: int, per_page: int, total: int) -> 'APIResponseBuilder':
        self.metadata["pagination"] = {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page
        }
        return self

    def success(self) -> 'APIResponseBuilder':
        self.status_code = 200
        return self

    def not_found(self) -> 'APIResponseBuilder':
        self.status_code = 404
        self.with_error("Resource not found", "NOT_FOUND")
        return self

    def unauthorized(self) -> 'APIResponseBuilder':
        self.status_code = 401
        self.with_error("Unauthorized", "UNAUTHORIZED")
        return self

    def build(self) -> Dict[str, Any]:
        response = {
            "status": "success" if self.status_code < 400 else "error",
            "status_code": self.status_code,
        }
        if self.data:
            response["data"] = self.data
        if self.errors:
            response["errors"] = self.errors
        if self.metadata:
            response["metadata"] = self.metadata
        return response

# Usage example
success_response = (APIResponseBuilder()
                   .with_data({"user": {"id": 1, "name": "Test"}})
                   .with_pagination(page=1, per_page=10, total=100)
                   .build())

error_response = (APIResponseBuilder()
                 .not_found()
                 .build())
```
