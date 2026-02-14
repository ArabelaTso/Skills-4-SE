---
name: integration-test-generator
description: "Generate integration tests for multiple interacting components in Python. Use when testing interactions between: (1) Multiple services or APIs (REST/GraphQL endpoints, microservices), (2) Database operations with repositories/ORMs (SQLAlchemy, Django ORM), (3) External services (payment gateways, email services, third-party APIs), (4) Message queues and event-driven systems, (5) Full stack workflows (API + database + business logic). Provides test structure templates, fixtures, test data builders, and patterns for pytest-based integration testing."
---

# Integration Test Generator

Generate comprehensive integration tests for Python applications that test multiple interacting components together.

## When to Use Integration Tests

Integration tests verify that multiple components work correctly together:

- **Service Integration**: REST/GraphQL APIs communicating with each other
- **Database Integration**: Repositories, ORM models, transaction handling
- **External Services**: Payment gateways, email services, third-party APIs
- **Event-Driven**: Message queues, event publishers/consumers
- **Full Stack**: Complete workflows through multiple layers (API → business logic → database)

## Test Structure

### Basic Integration Test Template

```python
import pytest
from myapp.services import ServiceA, ServiceB

class TestServiceIntegration:
    """Test integration between ServiceA and ServiceB."""

    @pytest.fixture
    def service_a(self):
        """Setup ServiceA with test configuration."""
        return ServiceA(config={"mode": "test"})

    @pytest.fixture
    def service_b(self, service_a):
        """Setup ServiceB that depends on ServiceA."""
        return ServiceB(service_a=service_a)

    def test_services_communicate_correctly(self, service_a, service_b):
        """Test that ServiceB correctly uses ServiceA."""
        # Arrange
        test_data = {"key": "value"}

        # Act
        service_a.store(test_data)
        result = service_b.process()

        # Assert
        assert result["key"] == "value"
        assert result["processed"] is True
```

### Test Fixtures Pattern

Use fixtures to set up and tear down test dependencies:

```python
@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session  # Test runs here

    session.close()

@pytest.fixture
def test_user(db_session):
    """Create a test user and clean up after test."""
    user = User(username="testuser", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    yield user

    db_session.delete(user)
    db_session.commit()
```

## Common Integration Test Patterns

### API Integration Tests

Test multiple API endpoints working together:

```python
def test_create_user_then_create_order(test_client):
    # Create user
    user_response = test_client.post("/api/users", json={"username": "test"})
    user_id = user_response.json()["id"]

    # Create order for user
    order_response = test_client.post(
        "/api/orders",
        json={"user_id": user_id, "items": [...]}
    )

    # Verify integration
    assert order_response.status_code == 201
    assert order_response.json()["user_id"] == user_id
```

### Database Integration Tests

Test repository interactions and transactions:

```python
def test_user_order_relationship(db_session, user_repo, order_repo):
    # Create user
    user = user_repo.create(username="test")
    db_session.commit()

    # Create orders
    order1 = order_repo.create(user_id=user.id, total=50.00)
    order2 = order_repo.create(user_id=user.id, total=75.00)
    db_session.commit()

    # Verify relationship
    retrieved_user = user_repo.get_by_id(user.id)
    assert len(retrieved_user.orders) == 2
```

### External Service Integration

Test integration with external APIs using mocks:

```python
import responses

@responses.activate
def test_payment_integration():
    # Mock external payment API
    responses.add(
        responses.POST,
        "https://api.payment.com/charge",
        json={"transaction_id": "txn_123", "status": "success"},
        status=200
    )

    # Test integration
    payment_service = PaymentService()
    result = payment_service.charge(amount=99.99, card_token="tok_test")

    assert result["status"] == "success"
    assert len(responses.calls) == 1
```

## Detailed Patterns and Examples

For comprehensive integration test patterns, see:

**[patterns.md](references/patterns.md)** - Detailed examples for:
- REST and GraphQL API integration
- Database and repository integration
- Transaction testing
- Message queue integration
- Full stack integration tests
- External service mocking

**[test_data.md](references/test_data.md)** - Test data builders and fixtures:
- Builder pattern for test data
- Database fixtures
- Factory pattern usage
- API response builders

## Best Practices

### 1. Test Isolation

Each test should be independent:

```python
@pytest.fixture(scope="function")  # New instance per test
def db_session():
    # Fresh database for each test
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    # ...
```

### 2. Setup and Teardown

Always clean up test data:

```python
@pytest.fixture
def test_resource():
    # Setup
    resource = create_resource()

    yield resource

    # Teardown - always runs even if test fails
    delete_resource(resource)
```

### 3. Use Test Builders

Create reusable test data builders:

```python
def make_user(username="test", **kwargs):
    defaults = {"email": f"{username}@example.com", "is_active": True}
    return User(**{**defaults, **kwargs, "username": username})

# Usage
admin = make_user("admin", role="admin")
inactive = make_user("inactive", is_active=False)
```

### 4. Test Real Scenarios

Test complete user workflows:

```python
def test_complete_checkout_workflow(test_client, db_session):
    # 1. Create user
    user = create_test_user()

    # 2. Add items to cart
    add_to_cart(user.id, product_id=1, quantity=2)

    # 3. Checkout
    order = checkout(user.id, payment_method="credit_card")

    # 4. Verify all integrations
    assert order.status == "confirmed"
    assert order.user_id == user.id
    assert len(order.items) == 1
    assert get_cart(user.id).items == []  # Cart emptied
```

### 5. Mock External Dependencies

Use mocks for external services to avoid network calls:

```python
from unittest.mock import Mock, patch

def test_with_mocked_email_service():
    with patch('myapp.services.EmailService') as mock_email:
        mock_email.send.return_value = {"message_id": "123"}

        # Test code that uses email service
        result = send_confirmation_email("user@example.com")

        # Verify mock was called correctly
        mock_email.send.assert_called_once()
        assert result["message_id"] == "123"
```

## Quick Reference

### pytest Commands

```bash
# Run all integration tests
pytest tests/integration/

# Run specific test file
pytest tests/integration/test_user_order.py

# Run tests matching pattern
pytest -k "test_integration"

# Run with verbose output
pytest -v tests/integration/

# Run with coverage
pytest --cov=myapp tests/integration/
```

### Common Fixtures

```python
# Database session
@pytest.fixture(scope="function")
def db_session():
    """Fresh database for each test."""

# Test client for API testing
@pytest.fixture
def test_client():
    """Test client for FastAPI/Flask app."""
    with TestClient(app) as client:
        yield client

# Mock external service
@pytest.fixture
def mock_payment_gateway():
    with patch('myapp.services.PaymentGateway') as mock:
        yield mock
```

### Assertion Patterns

```python
# Verify status codes
assert response.status_code == 201

# Verify data structure
assert "id" in response.json()
assert len(response.json()["items"]) == 2

# Verify relationships
assert order.user_id == user.id
assert user.orders[0].id == order.id

# Verify side effects
assert email_service.send.called
assert db_session.query(Order).count() == 1
```
