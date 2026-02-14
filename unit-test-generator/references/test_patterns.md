# Test Patterns

Complete examples for common testing scenarios across Python and Java.

## Table of Contents

1. [Simple Function Tests](#simple-function-tests)
2. [Mocking Dependencies](#mocking-dependencies)
3. [Testing Stateful Classes](#testing-stateful-classes)
4. [Async/Concurrent Code](#asyncconcurrent-code)
5. [Database Operations](#database-operations)
6. [File I/O Operations](#file-io-operations)
7. [Parameterized Tests](#parameterized-tests)

---

## Simple Function Tests

### Python (pytest) - Complete Example

```python
import pytest
from your_module import calculate_discount


class TestCalculateDiscount:
    """Tests for calculate_discount function."""

    # Happy path tests
    def test_calculate_discount_with_normal_values(self):
        """Should calculate correct discount for typical inputs."""
        # Arrange
        price = 100.0
        discount_percent = 20.0

        # Act
        result = calculate_discount(price, discount_percent)

        # Assert
        assert result == 80.0

    def test_calculate_discount_with_zero_discount(self):
        """Should return original price when discount is zero."""
        result = calculate_discount(100.0, 0.0)
        assert result == 100.0

    def test_calculate_discount_with_full_discount(self):
        """Should return zero when discount is 100%."""
        result = calculate_discount(100.0, 100.0)
        assert result == 0.0

    # Edge case tests
    def test_calculate_discount_with_zero_price(self):
        """Should handle zero price correctly."""
        result = calculate_discount(0.0, 50.0)
        assert result == 0.0

    def test_calculate_discount_with_small_discount(self):
        """Should handle small discount percentages accurately."""
        result = calculate_discount(100.0, 0.01)
        assert result == pytest.approx(99.99)

    def test_calculate_discount_with_large_price(self):
        """Should handle large prices correctly."""
        result = calculate_discount(1000000.0, 15.0)
        assert result == 850000.0

    # Error condition tests
    def test_calculate_discount_with_negative_price_raises_error(self):
        """Should raise ValueError for negative price."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            calculate_discount(-10.0, 20.0)

    def test_calculate_discount_with_discount_above_100_raises_error(self):
        """Should raise ValueError for discount > 100."""
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            calculate_discount(100.0, 101.0)

    def test_calculate_discount_with_negative_discount_raises_error(self):
        """Should raise ValueError for negative discount."""
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            calculate_discount(100.0, -5.0)
```

### Java (JUnit 4) - Complete Example

```java
import org.junit.Test;
import static org.junit.Assert.*;

public class DiscountCalculatorTest {

    // Happy path tests
    @Test
    public void testCalculateDiscountWithNormalValues() {
        // given
        DiscountCalculator calculator = new DiscountCalculator();
        double price = 100.0;
        double discountPercent = 20.0;

        // when
        double result = calculator.calculateDiscount(price, discountPercent);

        // then
        assertEquals(80.0, result, 0.001);
    }

    @Test
    public void testCalculateDiscountWithZeroDiscount() {
        DiscountCalculator calculator = new DiscountCalculator();
        assertEquals(100.0, calculator.calculateDiscount(100.0, 0.0), 0.001);
    }

    @Test
    public void testCalculateDiscountWithFullDiscount() {
        DiscountCalculator calculator = new DiscountCalculator();
        assertEquals(0.0, calculator.calculateDiscount(100.0, 100.0), 0.001);
    }

    // Edge case tests
    @Test
    public void testCalculateDiscountWithZeroPrice() {
        DiscountCalculator calculator = new DiscountCalculator();
        assertEquals(0.0, calculator.calculateDiscount(0.0, 50.0), 0.001);
    }

    @Test
    public void testCalculateDiscountWithSmallDiscount() {
        DiscountCalculator calculator = new DiscountCalculator();
        assertEquals(99.99, calculator.calculateDiscount(100.0, 0.01), 0.001);
    }

    // Error condition tests
    @Test(expected = IllegalArgumentException.class)
    public void testCalculateDiscountWithNegativePriceThrowsException() {
        DiscountCalculator calculator = new DiscountCalculator();
        calculator.calculateDiscount(-10.0, 20.0);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCalculateDiscountWithDiscountAbove100ThrowsException() {
        DiscountCalculator calculator = new DiscountCalculator();
        calculator.calculateDiscount(100.0, 101.0);
    }
}
```

---

## Mocking Dependencies

### Python (pytest with unittest.mock)

```python
import pytest
from unittest.mock import Mock, patch
from your_module import UserService


class TestUserService:
    """Tests for UserService with mocked dependencies."""

    @pytest.fixture
    def mock_database(self):
        """Mock database dependency."""
        return Mock()

    @pytest.fixture
    def mock_email_service(self):
        """Mock email service dependency."""
        return Mock()

    @pytest.fixture
    def user_service(self, mock_database, mock_email_service):
        """UserService instance with mocked dependencies."""
        return UserService(mock_database, mock_email_service)

    def test_create_user_saves_to_database(self, user_service, mock_database):
        """Should save user data to database."""
        # Arrange
        email = "alice@example.com"
        name = "Alice"
        expected_user = Mock(id=1, email=email, name=name)
        mock_database.save_user.return_value = expected_user

        # Act
        result = user_service.create_user(email, name)

        # Assert
        mock_database.save_user.assert_called_once_with({
            "email": email,
            "name": name
        })
        assert result.id == 1
        assert result.email == email

    def test_create_user_sends_welcome_email(self, user_service, mock_email_service, mock_database):
        """Should send welcome email after creating user."""
        # Arrange
        user = Mock(email="alice@example.com")
        mock_database.save_user.return_value = user

        # Act
        user_service.create_user("alice@example.com", "Alice")

        # Assert
        mock_email_service.send_welcome_email.assert_called_once_with("alice@example.com")

    def test_create_user_handles_database_error(self, user_service, mock_database):
        """Should propagate database errors."""
        # Arrange
        mock_database.save_user.side_effect = Exception("DB connection failed")

        # Act & Assert
        with pytest.raises(Exception, match="DB connection failed"):
            user_service.create_user("test@example.com", "Test")

    @patch('your_module.external_api')
    def test_fetch_user_data_calls_external_api(self, mock_api, user_service):
        """Should call external API to fetch user data."""
        # Arrange
        mock_api.get_user.return_value = {"id": 1, "name": "Alice"}

        # Act
        result = user_service.fetch_user_data(1)

        # Assert
        mock_api.get_user.assert_called_once_with(1)
        assert result["name"] == "Alice"
```

### Java (JUnit with Mockito)

```java
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.mockito.Mockito.*;
import static org.junit.Assert.*;

public class UserServiceTest {

    @Mock
    private Database database;

    @Mock
    private EmailService emailService;

    private UserService userService;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
        userService = new UserService(database, emailService);
    }

    @Test
    public void testCreateUserSavesToDatabase() {
        // given
        String email = "alice@example.com";
        String name = "Alice";
        User expectedUser = new User(1, email, name);
        when(database.saveUser(any(UserData.class))).thenReturn(expectedUser);

        // when
        User result = userService.createUser(email, name);

        // then
        verify(database).saveUser(argThat(data ->
            data.getEmail().equals(email) && data.getName().equals(name)
        ));
        assertEquals(1, result.getId());
        assertEquals(email, result.getEmail());
    }

    @Test
    public void testCreateUserSendsWelcomeEmail() {
        // given
        User user = new User(1, "alice@example.com", "Alice");
        when(database.saveUser(any(UserData.class))).thenReturn(user);

        // when
        userService.createUser("alice@example.com", "Alice");

        // then
        verify(emailService).sendWelcomeEmail("alice@example.com");
    }

    @Test(expected = DatabaseException.class)
    public void testCreateUserHandlesDatabaseError() {
        // given
        when(database.saveUser(any(UserData.class)))
            .thenThrow(new DatabaseException("Connection failed"));

        // when
        userService.createUser("test@example.com", "Test");
    }

    @Test
    public void testCreateUserVerifyInteractionOrder() {
        // given
        User user = new User(1, "alice@example.com", "Alice");
        when(database.saveUser(any(UserData.class))).thenReturn(user);

        // when
        userService.createUser("alice@example.com", "Alice");

        // then - verify order of operations
        InOrder inOrder = inOrder(database, emailService);
        inOrder.verify(database).saveUser(any(UserData.class));
        inOrder.verify(emailService).sendWelcomeEmail("alice@example.com");
    }
}
```

---

## Testing Stateful Classes

### Python Example - Shopping Cart

```python
import pytest
from unittest.mock import Mock
from your_module import ShoppingCart


class TestShoppingCart:
    """Tests for ShoppingCart class."""

    @pytest.fixture
    def cart(self):
        """Fresh shopping cart for each test."""
        return ShoppingCart()

    @pytest.fixture
    def sample_item(self):
        """Sample product item."""
        return Mock(id=1, name="Test Item", price=10.0)

    @pytest.fixture
    def expensive_item(self):
        """Expensive product item."""
        return Mock(id=2, name="Expensive Item", price=100.0)

    # Basic operations
    def test_new_cart_is_empty(self, cart):
        """New cart should have no items."""
        assert len(cart.items) == 0
        assert cart.get_total() == 0.0

    def test_add_item_increases_cart_size(self, cart, sample_item):
        """Adding item should increase cart size."""
        # Act
        cart.add_item(sample_item)

        # Assert
        assert len(cart.items) == 1

    def test_add_item_with_quantity(self, cart, sample_item):
        """Should add item with specified quantity."""
        # Act
        cart.add_item(sample_item, quantity=3)

        # Assert
        assert cart.items[0]["item"] == sample_item
        assert cart.items[0]["quantity"] == 3

    # State transitions
    def test_add_multiple_items(self, cart, sample_item, expensive_item):
        """Should handle multiple different items."""
        # Act
        cart.add_item(sample_item, quantity=2)
        cart.add_item(expensive_item, quantity=1)

        # Assert
        assert len(cart.items) == 2

    def test_remove_item_decreases_cart_size(self, cart, sample_item):
        """Removing item should decrease cart size."""
        # Arrange
        cart.add_item(sample_item)

        # Act
        cart.remove_item(sample_item.id)

        # Assert
        assert len(cart.items) == 0

    # Calculations
    def test_get_total_with_single_item(self, cart, sample_item):
        """Should calculate total for single item."""
        # Arrange
        cart.add_item(sample_item, quantity=2)

        # Act
        total = cart.get_total()

        # Assert
        assert total == 20.0  # 10.0 * 2

    def test_get_total_with_multiple_items(self, cart, sample_item, expensive_item):
        """Should calculate total for multiple items."""
        # Arrange
        cart.add_item(sample_item, quantity=2)
        cart.add_item(expensive_item, quantity=1)

        # Act
        total = cart.get_total()

        # Assert
        assert total == 120.0  # (10*2) + (100*1)

    # State cleanup
    def test_clear_empties_cart(self, cart, sample_item):
        """Clear should remove all items."""
        # Arrange
        cart.add_item(sample_item)
        cart.add_item(sample_item)

        # Act
        cart.clear()

        # Assert
        assert len(cart.items) == 0
        assert cart.get_total() == 0.0

    # Edge cases
    def test_add_item_with_zero_quantity_raises_error(self, cart, sample_item):
        """Should reject zero quantity."""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            cart.add_item(sample_item, quantity=0)

    def test_remove_nonexistent_item_raises_error(self, cart):
        """Should raise error when removing item not in cart."""
        with pytest.raises(KeyError, match="Item not found"):
            cart.remove_item(999)
```

### Java Example - Shopping Cart

```java
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ShoppingCartTest {

    private ShoppingCart cart;
    private Product sampleItem;
    private Product expensiveItem;

    @Before
    public void setUp() {
        cart = new ShoppingCart();
        sampleItem = new Product(1, "Test Item", 10.0);
        expensiveItem = new Product(2, "Expensive Item", 100.0);
    }

    @Test
    public void testNewCartIsEmpty() {
        assertEquals(0, cart.getItemCount());
        assertEquals(0.0, cart.getTotal(), 0.001);
    }

    @Test
    public void testAddItemIncreasesCartSize() {
        cart.addItem(sampleItem, 1);
        assertEquals(1, cart.getItemCount());
    }

    @Test
    public void testAddItemWithQuantity() {
        cart.addItem(sampleItem, 3);
        assertEquals(3, cart.getQuantity(sampleItem.getId()));
    }

    @Test
    public void testAddMultipleItems() {
        cart.addItem(sampleItem, 2);
        cart.addItem(expensiveItem, 1);
        assertEquals(2, cart.getItemCount());
    }

    @Test
    public void testGetTotalWithSingleItem() {
        cart.addItem(sampleItem, 2);
        assertEquals(20.0, cart.getTotal(), 0.001);
    }

    @Test
    public void testGetTotalWithMultipleItems() {
        cart.addItem(sampleItem, 2);
        cart.addItem(expensiveItem, 1);
        assertEquals(120.0, cart.getTotal(), 0.001);
    }

    @Test
    public void testClearEmptiesCart() {
        cart.addItem(sampleItem, 1);
        cart.clear();
        assertEquals(0, cart.getItemCount());
        assertEquals(0.0, cart.getTotal(), 0.001);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testAddItemWithZeroQuantityThrowsException() {
        cart.addItem(sampleItem, 0);
    }

    @Test(expected = ItemNotFoundException.class)
    public void testRemoveNonexistentItemThrowsException() {
        cart.removeItem(999);
    }
}
```

---

## Async/Concurrent Code

### Python (pytest-asyncio)

```python
import pytest
import asyncio
from your_module import AsyncDataFetcher


class TestAsyncDataFetcher:
    """Tests for async data fetcher."""

    @pytest.fixture
    def fetcher(self):
        return AsyncDataFetcher()

    @pytest.mark.asyncio
    async def test_fetch_data_returns_result(self, fetcher):
        """Should fetch data asynchronously."""
        # Act
        result = await fetcher.fetch_data("https://api.example.com")

        # Assert
        assert result is not None
        assert "data" in result

    @pytest.mark.asyncio
    async def test_fetch_data_handles_timeout(self, fetcher):
        """Should handle timeout gracefully."""
        # Act & Assert
        with pytest.raises(asyncio.TimeoutError):
            await fetcher.fetch_data("https://slow-api.example.com", timeout=0.1)

    @pytest.mark.asyncio
    async def test_fetch_multiple_urls_concurrently(self, fetcher):
        """Should fetch multiple URLs concurrently."""
        # Arrange
        urls = [
            "https://api1.example.com",
            "https://api2.example.com",
            "https://api3.example.com"
        ]

        # Act
        results = await fetcher.fetch_all(urls)

        # Assert
        assert len(results) == 3
        assert all(r is not None for r in results)

    @pytest.mark.asyncio
    async def test_fetch_with_retry(self, fetcher, mocker):
        """Should retry on failure."""
        # Arrange
        mock_fetch = mocker.patch.object(fetcher, '_do_fetch')
        mock_fetch.side_effect = [
            Exception("Network error"),
            Exception("Network error"),
            {"data": "success"}
        ]

        # Act
        result = await fetcher.fetch_with_retry("https://api.example.com", retries=3)

        # Assert
        assert result["data"] == "success"
        assert mock_fetch.call_count == 3
```

### Java (JUnit with CompletableFuture)

```java
import org.junit.Test;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import static org.junit.Assert.*;

public class AsyncDataFetcherTest {

    @Test
    public void testFetchDataReturnsResult() throws Exception {
        // given
        AsyncDataFetcher fetcher = new AsyncDataFetcher();

        // when
        CompletableFuture<Data> future = fetcher.fetchData("https://api.example.com");
        Data result = future.get();

        // then
        assertNotNull(result);
        assertNotNull(result.getValue());
    }

    @Test
    public void testFetchMultipleUrlsConcurrently() throws Exception {
        // given
        AsyncDataFetcher fetcher = new AsyncDataFetcher();
        String[] urls = {
            "https://api1.example.com",
            "https://api2.example.com",
            "https://api3.example.com"
        };

        // when
        CompletableFuture<Data>[] futures = fetcher.fetchAll(urls);
        CompletableFuture.allOf(futures).get();

        // then
        for (CompletableFuture<Data> future : futures) {
            assertNotNull(future.get());
        }
    }

    @Test(expected = ExecutionException.class)
    public void testFetchDataHandlesError() throws Exception {
        // given
        AsyncDataFetcher fetcher = new AsyncDataFetcher();

        // when
        CompletableFuture<Data> future = fetcher.fetchData("https://invalid-url");
        future.get();  // Should throw
    }
}
```

---

## Database Operations

### Python (pytest with database fixtures)

```python
import pytest
from your_module import UserRepository, User


@pytest.fixture(scope="function")
def db_connection():
    """Create test database connection."""
    conn = create_test_database()
    yield conn
    conn.rollback()
    conn.close()


@pytest.fixture
def user_repo(db_connection):
    """UserRepository with test database."""
    return UserRepository(db_connection)


class TestUserRepository:
    """Tests for database operations."""

    def test_save_user_inserts_into_database(self, user_repo, db_connection):
        """Should insert user into database."""
        # Arrange
        user = User(name="Alice", email="alice@example.com")

        # Act
        saved_user = user_repo.save(user)

        # Assert
        assert saved_user.id is not None
        # Verify in database
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (saved_user.id,))
        row = cursor.fetchone()
        assert row is not None
        assert row["email"] == "alice@example.com"

    def test_find_by_id_returns_user(self, user_repo):
        """Should find user by ID."""
        # Arrange
        user = user_repo.save(User(name="Bob", email="bob@example.com"))

        # Act
        found_user = user_repo.find_by_id(user.id)

        # Assert
        assert found_user is not None
        assert found_user.email == "bob@example.com"

    def test_find_by_id_returns_none_for_nonexistent(self, user_repo):
        """Should return None for nonexistent ID."""
        # Act
        result = user_repo.find_by_id(99999)

        # Assert
        assert result is None

    def test_update_user_modifies_database(self, user_repo):
        """Should update existing user."""
        # Arrange
        user = user_repo.save(User(name="Charlie", email="charlie@example.com"))
        user.name = "Charles"

        # Act
        user_repo.update(user)

        # Assert
        updated_user = user_repo.find_by_id(user.id)
        assert updated_user.name == "Charles"

    def test_delete_user_removes_from_database(self, user_repo):
        """Should delete user from database."""
        # Arrange
        user = user_repo.save(User(name="Dave", email="dave@example.com"))

        # Act
        user_repo.delete(user.id)

        # Assert
        assert user_repo.find_by_id(user.id) is None
```

---

## File I/O Operations

### Python Example

```python
import pytest
import os
from pathlib import Path
from your_module import FileProcessor


@pytest.fixture
def temp_file(tmp_path):
    """Create temporary file for testing."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    return file_path


class TestFileProcessor:
    """Tests for file operations."""

    def test_read_file_returns_content(self, temp_file):
        """Should read file content."""
        # Arrange
        processor = FileProcessor()

        # Act
        content = processor.read_file(temp_file)

        # Assert
        assert content == "test content"

    def test_write_file_creates_file(self, tmp_path):
        """Should write content to file."""
        # Arrange
        processor = FileProcessor()
        file_path = tmp_path / "output.txt"

        # Act
        processor.write_file(file_path, "new content")

        # Assert
        assert file_path.exists()
        assert file_path.read_text() == "new content"

    def test_read_nonexistent_file_raises_error(self):
        """Should raise error for nonexistent file."""
        # Arrange
        processor = FileProcessor()

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            processor.read_file("nonexistent.txt")

    def test_process_large_file(self, tmp_path):
        """Should handle large files."""
        # Arrange
        processor = FileProcessor()
        large_file = tmp_path / "large.txt"
        large_file.write_text("line\\n" * 10000)

        # Act
        line_count = processor.count_lines(large_file)

        # Assert
        assert line_count == 10000
```

---

## Parameterized Tests

### Python (pytest)

```python
import pytest


@pytest.mark.parametrize("price,discount,expected", [
    (100, 20, 80),
    (100, 0, 100),
    (100, 100, 0),
    (50, 10, 45),
    (200, 25, 150),
    (75, 33.33, 50.0025),
])
def test_calculate_discount_various_inputs(price, discount, expected):
    """Test discount calculation with various valid inputs."""
    result = calculate_discount(price, discount)
    assert result == pytest.approx(expected, abs=0.01)


@pytest.mark.parametrize("price,discount,error_message", [
    (-10, 20, "Price cannot be negative"),
    (100, 101, "Discount must be between 0 and 100"),
    (100, -5, "Discount must be between 0 and 100"),
])
def test_calculate_discount_invalid_inputs(price, discount, error_message):
    """Test that invalid inputs raise appropriate errors."""
    with pytest.raises(ValueError, match=error_message):
        calculate_discount(price, discount)
```

### Java (JUnit 5)

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;
import static org.junit.jupiter.api.Assertions.*;

public class ParameterizedTestExamples {

    @ParameterizedTest
    @CsvSource({
        "100.0, 20.0, 80.0",
        "100.0, 0.0, 100.0",
        "100.0, 100.0, 0.0",
        "50.0, 10.0, 45.0",
        "200.0, 25.0, 150.0"
    })
    void testCalculateDiscountVariousInputs(double price, double discount, double expected) {
        DiscountCalculator calculator = new DiscountCalculator();
        double result = calculator.calculateDiscount(price, discount);
        assertEquals(expected, result, 0.001);
    }

    @ParameterizedTest
    @ValueSource(doubles = {-10.0, 101.0, -5.0})
    void testCalculateDiscountInvalidDiscounts(double invalidDiscount) {
        DiscountCalculator calculator = new DiscountCalculator();
        assertThrows(IllegalArgumentException.class,
            () -> calculator.calculateDiscount(100.0, invalidDiscount));
    }
}
```
