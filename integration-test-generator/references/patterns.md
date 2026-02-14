# Integration Test Patterns

## API Integration Tests

### REST API Integration

```python
import pytest
import requests
from typing import Dict, Any

class TestUserOrderIntegration:
    """Test user service and order service integration."""

    @pytest.fixture
    def base_url(self):
        return "http://localhost:8000"

    @pytest.fixture
    def test_user(self, base_url):
        """Create a test user and clean up after test."""
        # Setup
        user_data = {"username": "testuser", "email": "test@example.com"}
        response = requests.post(f"{base_url}/users", json=user_data)
        user_id = response.json()["id"]

        yield user_id

        # Cleanup
        requests.delete(f"{base_url}/users/{user_id}")

    def test_create_order_for_user(self, base_url, test_user):
        """Test creating an order for a user integrates correctly."""
        # Arrange
        order_data = {
            "user_id": test_user,
            "items": [{"product_id": 1, "quantity": 2}],
            "total": 99.98
        }

        # Act
        response = requests.post(f"{base_url}/orders", json=order_data)
        order = response.json()

        # Assert - verify order created
        assert response.status_code == 201
        assert order["user_id"] == test_user
        assert order["status"] == "pending"

        # Assert - verify user's order list updated
        user_response = requests.get(f"{base_url}/users/{test_user}/orders")
        user_orders = user_response.json()
        assert len(user_orders) == 1
        assert user_orders[0]["id"] == order["id"]
```

### GraphQL API Integration

```python
import pytest
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class TestGraphQLIntegration:
    """Test GraphQL API with multiple related entities."""

    @pytest.fixture
    def gql_client(self):
        transport = RequestsHTTPTransport(url="http://localhost:4000/graphql")
        return Client(transport=transport, fetch_schema_from_transport=True)

    def test_create_post_with_author_integration(self, gql_client):
        """Test creating a post properly links to author."""
        # Create author
        create_author = gql("""
            mutation CreateAuthor($name: String!) {
                createAuthor(name: $name) {
                    id
                    name
                }
            }
        """)
        author_result = gql_client.execute(create_author, variable_values={"name": "John Doe"})
        author_id = author_result["createAuthor"]["id"]

        # Create post for author
        create_post = gql("""
            mutation CreatePost($title: String!, $authorId: ID!) {
                createPost(title: $title, authorId: $authorId) {
                    id
                    title
                    author {
                        id
                        name
                    }
                }
            }
        """)
        post_result = gql_client.execute(
            create_post,
            variable_values={"title": "Test Post", "authorId": author_id}
        )

        # Verify integration
        assert post_result["createPost"]["author"]["id"] == author_id
        assert post_result["createPost"]["author"]["name"] == "John Doe"
```

## Database Integration Tests

### Repository Pattern Integration

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.models import Base, User, Order
from myapp.repositories import UserRepository, OrderRepository

class TestDatabaseIntegration:
    """Test repository interactions with real database."""

    @pytest.fixture(scope="function")
    def db_session(self):
        """Create a clean database session for each test."""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        yield session

        session.close()

    @pytest.fixture
    def user_repo(self, db_session):
        return UserRepository(db_session)

    @pytest.fixture
    def order_repo(self, db_session):
        return OrderRepository(db_session)

    def test_user_order_relationship(self, db_session, user_repo, order_repo):
        """Test user-order relationship persists correctly."""
        # Create user
        user = user_repo.create(username="testuser", email="test@example.com")
        db_session.commit()

        # Create orders for user
        order1 = order_repo.create(user_id=user.id, total=50.00)
        order2 = order_repo.create(user_id=user.id, total=75.00)
        db_session.commit()

        # Verify relationship
        retrieved_user = user_repo.get_by_id(user.id)
        assert len(retrieved_user.orders) == 2
        assert sum(o.total for o in retrieved_user.orders) == 125.00

        # Verify cascade behavior
        user_repo.delete(user.id)
        db_session.commit()

        assert order_repo.get_by_id(order1.id) is None
        assert order_repo.get_by_id(order2.id) is None
```

### Transaction Integration

```python
import pytest
from myapp.services import PaymentService, InventoryService, OrderService
from myapp.models import InsufficientInventoryError

class TestTransactionIntegration:
    """Test transactional behavior across services."""

    @pytest.fixture
    def services(self, db_session):
        return {
            "payment": PaymentService(db_session),
            "inventory": InventoryService(db_session),
            "order": OrderService(db_session)
        }

    def test_order_rollback_on_payment_failure(self, db_session, services):
        """Test order creation rolls back when payment fails."""
        # Setup inventory
        services["inventory"].add_stock(product_id=1, quantity=10)
        db_session.commit()

        # Attempt order with invalid payment
        with pytest.raises(Exception) as exc_info:
            services["order"].create_order(
                user_id=1,
                items=[{"product_id": 1, "quantity": 2}],
                payment_method="invalid_card"
            )

        # Verify rollback - inventory unchanged
        inventory = services["inventory"].get_stock(product_id=1)
        assert inventory == 10

        # Verify rollback - no order created
        orders = services["order"].get_orders_by_user(user_id=1)
        assert len(orders) == 0
```

## Message Queue Integration Tests

### Event-Driven Integration

```python
import pytest
import json
from unittest.mock import Mock
from myapp.publishers import EventPublisher
from myapp.consumers import OrderConsumer, NotificationConsumer

class TestEventDrivenIntegration:
    """Test message queue integration between services."""

    @pytest.fixture
    def message_queue(self):
        """In-memory message queue for testing."""
        return {}

    @pytest.fixture
    def event_publisher(self, message_queue):
        publisher = EventPublisher()
        publisher._queue = message_queue  # Inject test queue
        return publisher

    def test_order_event_triggers_notification(self, event_publisher, message_queue):
        """Test order creation event triggers notification."""
        # Setup consumer
        notification_handler = Mock()
        consumer = NotificationConsumer(message_queue)
        consumer.register_handler("order.created", notification_handler)

        # Publish order created event
        event_data = {
            "order_id": "123",
            "user_email": "user@example.com",
            "total": 99.99
        }
        event_publisher.publish("order.created", event_data)

        # Process messages
        consumer.process_messages()

        # Verify notification handler called
        notification_handler.assert_called_once()
        call_args = notification_handler.call_args[0][0]
        assert call_args["order_id"] == "123"
        assert call_args["user_email"] == "user@example.com"
```

## Multi-Component Integration Tests

### Full Stack Integration

```python
import pytest
from fastapi.testclient import TestClient
from myapp.main import app
from myapp.database import get_db
from myapp.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestFullStackIntegration:
    """Test complete request flow through all layers."""

    @pytest.fixture(scope="function")
    def test_client(self):
        # Setup test database
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        TestingSessionLocal = sessionmaker(bind=engine)

        def override_get_db():
            db = TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db

        with TestClient(app) as client:
            yield client

    def test_complete_order_workflow(self, test_client):
        """Test complete order creation workflow."""
        # Step 1: Create user
        user_response = test_client.post(
            "/api/users",
            json={"username": "testuser", "email": "test@example.com"}
        )
        assert user_response.status_code == 201
        user_id = user_response.json()["id"]

        # Step 2: Add items to cart
        cart_response = test_client.post(
            f"/api/users/{user_id}/cart",
            json={"items": [{"product_id": 1, "quantity": 2}]}
        )
        assert cart_response.status_code == 200

        # Step 3: Create order from cart
        order_response = test_client.post(
            f"/api/users/{user_id}/orders",
            json={"payment_method": "credit_card"}
        )
        assert order_response.status_code == 201
        order = order_response.json()

        # Step 4: Verify order details
        order_details = test_client.get(f"/api/orders/{order['id']}")
        assert order_details.status_code == 200
        assert order_details.json()["status"] == "confirmed"

        # Step 5: Verify cart is emptied
        cart_check = test_client.get(f"/api/users/{user_id}/cart")
        assert cart_check.json()["items"] == []
```

## External Service Integration Tests

### Third-Party API Integration

```python
import pytest
import responses
from myapp.services import PaymentGateway, EmailService

class TestExternalServiceIntegration:
    """Test integration with external services using mocks."""

    @responses.activate
    def test_payment_and_email_integration(self):
        """Test payment processing triggers confirmation email."""
        # Mock payment gateway
        responses.add(
            responses.POST,
            "https://api.payment-gateway.com/charge",
            json={"transaction_id": "txn_123", "status": "success"},
            status=200
        )

        # Mock email service
        responses.add(
            responses.POST,
            "https://api.email-service.com/send",
            json={"message_id": "msg_456"},
            status=200
        )

        # Execute integration flow
        payment_gateway = PaymentGateway()
        email_service = EmailService()

        # Process payment
        payment_result = payment_gateway.charge(
            amount=99.99,
            card_token="tok_test"
        )
        assert payment_result["status"] == "success"

        # Send confirmation email
        email_result = email_service.send_confirmation(
            to="user@example.com",
            transaction_id=payment_result["transaction_id"],
            amount=99.99
        )
        assert email_result["message_id"] == "msg_456"

        # Verify both services were called
        assert len(responses.calls) == 2
```
