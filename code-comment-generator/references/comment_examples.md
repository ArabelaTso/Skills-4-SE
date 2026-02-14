# Comment Examples

Comprehensive examples of well-commented code for various scenarios.

## Table of Contents

1. [Algorithms](#algorithms)
2. [API Clients](#api-clients)
3. [Data Processing](#data-processing)
4. [Business Logic](#business-logic)
5. [Database Operations](#database-operations)
6. [Configuration and Setup](#configuration-and-setup)

---

## Algorithms

### Binary Search (Python)

```python
def binary_search(arr: List[int], target: int) -> int:
    """
    Find the index of target value in sorted array using binary search.

    Binary search achieves O(log n) time complexity by repeatedly dividing
    the search interval in half. If the target is less than the middle element,
    search the left half; otherwise search the right half.

    Args:
        arr: Sorted list of integers to search
        target: Value to find in the array

    Returns:
        Index of target if found, -1 otherwise

    Example:
        >>> binary_search([1, 3, 5, 7, 9], 5)
        2
        >>> binary_search([1, 3, 5, 7, 9], 4)
        -1

    Note:
        Array must be sorted for correct results.
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        # Use (left + right) // 2 to avoid integer overflow in other languages
        # In Python, integers can be arbitrarily large, so this isn't strictly necessary
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            # Target is in right half - exclude mid since we already checked it
            left = mid + 1
        else:
            # Target is in left half - exclude mid
            right = mid - 1

    # Target not found in array
    return -1
```

### Quicksort (Java)

```java
/**
 * Sorts an array using the Quicksort algorithm.
 *
 * <p>Quicksort is a divide-and-conquer algorithm that works by selecting
 * a 'pivot' element and partitioning the array around it. Elements smaller
 * than the pivot go to the left, larger elements go to the right. The
 * process recursively sorts the sub-arrays.
 *
 * <p>Average time complexity: O(n log n)
 * <br>Worst case: O(n²) when array is already sorted
 * <br>Space complexity: O(log n) due to recursion stack
 *
 * @param arr the array to sort (modified in-place)
 * @param low starting index of the portion to sort
 * @param high ending index of the portion to sort
 */
public void quicksort(int[] arr, int low, int high) {
    if (low < high) {
        // Partition array and get pivot index
        // After partitioning: arr[low..pi-1] <= arr[pi] <= arr[pi+1..high]
        int pi = partition(arr, low, high);

        // Recursively sort elements before and after partition
        quicksort(arr, low, pi - 1);
        quicksort(arr, pi + 1, high);
    }
}

/**
 * Partitions array segment around a pivot element.
 *
 * <p>Uses the last element as pivot (Lomuto partition scheme).
 * Rearranges array so elements smaller than pivot are on the left,
 * and larger elements are on the right.
 *
 * @param arr the array to partition
 * @param low starting index
 * @param high ending index (used as pivot)
 * @return the final position of the pivot element
 */
private int partition(int[] arr, int low, int high) {
    // Choose rightmost element as pivot
    int pivot = arr[high];

    // Index of smaller element - indicates position where pivot should be placed
    int i = low - 1;

    // Move all elements smaller than pivot to the left side
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            // Swap arr[i] and arr[j]
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }

    // Place pivot in its correct position
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;

    return i + 1;
}
```

---

## API Clients

### REST API Client (Python)

```python
class PaymentAPIClient:
    """
    Client for interacting with the Payment Processing API.

    Handles authentication, request retry logic, and error handling
    for the third-party payment service. All monetary amounts are
    in USD cents to avoid floating-point precision issues.

    Attributes:
        api_key: API key for authentication
        base_url: Base URL for API endpoints
        timeout: Request timeout in seconds (default: 30)
        max_retries: Maximum number of retry attempts (default: 3)

    Example:
        >>> client = PaymentAPIClient(api_key="pk_live_...")
        >>> result = client.charge(amount=1000, token="tok_visa")
        >>> print(result['status'])
        'succeeded'
    """

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize payment API client.

        Args:
            api_key: Secret API key from payment provider dashboard
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = "https://api.payment-provider.com/v1"
        self.timeout = timeout
        # Retry on network errors and 5xx server errors, but not 4xx client errors
        self.max_retries = 3

    def charge(self, amount: int, token: str, description: str = "") -> dict:
        """
        Process a payment charge.

        Args:
            amount: Amount to charge in cents (e.g., 1000 = $10.00)
            token: Payment token from client-side tokenization
            description: Optional description for the charge

        Returns:
            Dictionary containing charge details with keys:
            - id: Unique charge identifier
            - status: 'succeeded', 'pending', or 'failed'
            - amount: Amount charged in cents

        Raises:
            PaymentError: If charge fails due to insufficient funds,
                         invalid card, or other payment issues
            APIError: If API request fails after retries

        Example:
            >>> charge = client.charge(amount=5000, token="tok_123")
            >>> if charge['status'] == 'succeeded':
            ...     send_confirmation_email()
        """
        endpoint = f"{self.base_url}/charges"
        payload = {
            "amount": amount,
            "token": token,
            "description": description,
            "currency": "usd",  # Currently only USD supported
        }

        # Retry logic for transient failures
        for attempt in range(self.max_retries):
            try:
                response = self._make_request("POST", endpoint, payload)
                return response

            except requests.exceptions.Timeout:
                # Timeout errors are retryable - payment may not have processed
                if attempt == self.max_retries - 1:
                    raise APIError("Request timed out after 3 attempts")
                # Exponential backoff: wait 1s, 2s, 4s between retries
                time.sleep(2 ** attempt)

            except requests.exceptions.HTTPError as e:
                # 4xx errors are client errors - don't retry
                if 400 <= e.response.status_code < 500:
                    raise PaymentError(f"Payment failed: {e.response.json()['error']}")
                # 5xx errors are server errors - retry
                if attempt == self.max_retries - 1:
                    raise APIError(f"Server error: {e.response.status_code}")
                time.sleep(2 ** attempt)

    def _make_request(self, method: str, url: str, data: dict = None) -> dict:
        """
        Make authenticated HTTP request to API.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Full URL to request
            data: Optional request payload

        Returns:
            Parsed JSON response

        Raises:
            requests.exceptions.HTTPError: On non-2xx status codes
            requests.exceptions.Timeout: On request timeout
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.request(
            method=method,
            url=url,
            json=data,
            headers=headers,
            timeout=self.timeout,
        )

        # Raise exception for 4xx/5xx status codes
        response.raise_for_status()

        return response.json()
```

---

## Data Processing

### CSV Data Transformer (Python)

```python
def transform_sales_data(input_file: str, output_file: str) -> dict:
    """
    Transform raw sales CSV data into aggregated monthly report.

    Reads sales transactions from CSV, calculates monthly totals by product
    category, and writes results to a new CSV file. Handles missing values
    and invalid data gracefully.

    Input CSV format:
        date,product,category,amount
        2024-01-15,Widget A,Electronics,150.00

    Output CSV format:
        month,category,total_sales,transaction_count
        2024-01,Electronics,45000.00,120

    Args:
        input_file: Path to input CSV file with sales transactions
        output_file: Path where aggregated report will be written

    Returns:
        Dictionary with processing stats:
        - rows_processed: Number of input rows read
        - rows_written: Number of output rows written
        - rows_skipped: Number of invalid rows skipped

    Raises:
        FileNotFoundError: If input file doesn't exist
        PermissionError: If output file can't be written

    Example:
        >>> stats = transform_sales_data('sales_2024.csv', 'report.csv')
        >>> print(f"Processed {stats['rows_processed']} transactions")
    """
    from collections import defaultdict
    from datetime import datetime

    # Track aggregated data: {(month, category): {'total': amount, 'count': n}}
    aggregates = defaultdict(lambda: {'total': 0.0, 'count': 0})

    rows_processed = 0
    rows_skipped = 0

    # Read and aggregate input data
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                # Parse date to extract month (format: YYYY-MM)
                date = datetime.strptime(row['date'], '%Y-%m-%d')
                month = date.strftime('%Y-%m')

                # Convert amount to float, handling missing/invalid values
                amount = float(row['amount'])

                # Skip negative amounts (likely data errors)
                if amount < 0:
                    rows_skipped += 1
                    continue

                category = row['category'].strip()

                # Aggregate by month and category
                key = (month, category)
                aggregates[key]['total'] += amount
                aggregates[key]['count'] += 1

                rows_processed += 1

            except (ValueError, KeyError) as e:
                # Skip rows with invalid dates or missing required fields
                # Log to stderr but continue processing
                print(f"Skipping invalid row: {e}", file=sys.stderr)
                rows_skipped += 1
                continue

    # Write aggregated results
    rows_written = 0
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['month', 'category', 'total_sales', 'transaction_count'])

        # Sort by month and category for consistent output
        for (month, category), data in sorted(aggregates.items()):
            writer.writerow([
                month,
                category,
                f"{data['total']:.2f}",  # Format to 2 decimal places
                data['count']
            ])
            rows_written += 1

    return {
        'rows_processed': rows_processed,
        'rows_written': rows_written,
        'rows_skipped': rows_skipped,
    }
```

---

## Business Logic

### Order Processing (Java)

```java
/**
 * Processes customer orders and manages inventory.
 *
 * <p>Handles the complete order workflow:
 * <ol>
 *   <li>Validates order items and quantities
 *   <li>Checks inventory availability
 *   <li>Reserves inventory
 *   <li>Calculates pricing with discounts and tax
 *   <li>Processes payment
 *   <li>Commits inventory changes
 *   <li>Sends confirmation email
 * </ol>
 *
 * <p>If any step fails, the entire transaction is rolled back to maintain
 * data consistency (inventory is released, payment is voided).
 *
 * @since 2.0
 */
public class OrderProcessor {

    private InventoryService inventoryService;
    private PaymentService paymentService;
    private EmailService emailService;

    /**
     * Processes a customer order from cart to confirmation.
     *
     * @param order the order to process
     * @return processed order with confirmation number
     * @throws InsufficientInventoryException if any item is out of stock
     * @throws PaymentFailedException if payment processing fails
     * @throws OrderValidationException if order data is invalid
     */
    public Order processOrder(Order order) throws OrderProcessingException {
        // Step 1: Validate order data
        validateOrder(order);

        // Step 2: Check inventory availability for all items
        // Throws exception if any item is out of stock - fail fast
        checkInventoryAvailability(order);

        // Step 3: Reserve inventory to prevent overselling
        // This locks the inventory until the order is committed or cancelled
        List<InventoryReservation> reservations = reserveInventory(order);

        try {
            // Step 4: Calculate total with applicable discounts and taxes
            OrderTotal total = calculateOrderTotal(order);
            order.setTotal(total);

            // Step 5: Process payment
            // If payment fails, inventory will be released in finally block
            PaymentResult payment = paymentService.charge(
                order.getCustomerId(),
                total.getGrandTotal()
            );
            order.setPaymentId(payment.getId());

            // Step 6: Commit inventory changes (remove reserved items from stock)
            inventoryService.commitReservations(reservations);

            // Step 7: Generate confirmation number and mark order as confirmed
            String confirmationNumber = generateConfirmationNumber();
            order.setConfirmationNumber(confirmationNumber);
            order.setStatus(OrderStatus.CONFIRMED);

            // Step 8: Send confirmation email asynchronously
            // Email failure shouldn't fail the order - log and continue
            try {
                emailService.sendOrderConfirmation(order);
            } catch (EmailException e) {
                // Log error but don't fail the order
                logger.error("Failed to send confirmation email for order {}",
                            order.getId(), e);
            }

            return order;

        } catch (PaymentFailedException e) {
            // Payment failed - release inventory reservations
            inventoryService.releaseReservations(reservations);
            throw new OrderProcessingException("Payment failed: " + e.getMessage(), e);

        } catch (Exception e) {
            // Unexpected error - rollback all changes
            inventoryService.releaseReservations(reservations);
            // Note: Payment void happens automatically via payment service
            throw new OrderProcessingException("Order processing failed", e);
        }
    }

    /**
     * Calculates order total including discounts and taxes.
     *
     * <p>Calculation order matters:
     * <ol>
     *   <li>Subtotal (sum of item prices × quantities)
     *   <li>Apply discount codes (percentage or fixed amount)
     *   <li>Calculate tax on discounted amount
     *   <li>Add shipping cost (not taxed in most states)
     * </ol>
     *
     * @param order the order with items and discount codes
     * @return order total breakdown
     */
    private OrderTotal calculateOrderTotal(Order order) {
        // Calculate subtotal from line items
        double subtotal = order.getItems().stream()
            .mapToDouble(item -> item.getPrice() * item.getQuantity())
            .sum();

        // Apply discount code if present
        double discount = 0.0;
        if (order.getDiscountCode() != null) {
            DiscountCode code = discountService.validate(order.getDiscountCode());
            if (code.getType() == DiscountType.PERCENTAGE) {
                // Percentage discount (e.g., 15% off)
                discount = subtotal * (code.getValue() / 100.0);
            } else {
                // Fixed amount discount (e.g., $10 off)
                discount = Math.min(code.getValue(), subtotal);
            }
        }

        double discountedAmount = subtotal - discount;

        // Calculate tax on discounted amount
        // Tax rate varies by shipping address - use appropriate rate
        double taxRate = taxService.getTaxRate(order.getShippingAddress());
        double tax = discountedAmount * taxRate;

        // Add shipping cost (not subject to tax in this jurisdiction)
        double shipping = shippingService.calculateCost(
            order.getItems(),
            order.getShippingAddress()
        );

        double grandTotal = discountedAmount + tax + shipping;

        return new OrderTotal(subtotal, discount, tax, shipping, grandTotal);
    }
}
```

---

## Database Operations

### User Repository (Python)

```python
class UserRepository:
    """
    Data access layer for user entities.

    Handles all database operations for user records including CRUD operations,
    queries, and transactional updates. Uses prepared statements to prevent
    SQL injection.

    Note:
        All methods automatically handle database connection from pool.
        Connections are returned to pool when method completes.
    """

    def __init__(self, db_pool: ConnectionPool):
        """
        Initialize repository with database connection pool.

        Args:
            db_pool: Database connection pool for executing queries
        """
        self.db_pool = db_pool

    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve user by unique ID.

        Args:
            user_id: Primary key of user to retrieve

        Returns:
            User object if found, None otherwise

        Example:
            >>> user = repo.find_by_id(123)
            >>> if user:
            ...     print(user.email)
        """
        conn = self.db_pool.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)

            # Use parameterized query to prevent SQL injection
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))

            row = cursor.fetchone()
            if row:
                return User.from_dict(row)
            return None

        finally:
            # Always return connection to pool, even if exception occurs
            conn.close()

    def save(self, user: User) -> User:
        """
        Insert new user or update existing user.

        Uses INSERT ... ON DUPLICATE KEY UPDATE pattern to handle both
        create and update in a single query. This is more efficient than
        separate SELECT + INSERT/UPDATE.

        Args:
            user: User object to persist

        Returns:
            User object with updated ID (for new records)

        Raises:
            DatabaseError: If save operation fails
            ValidationError: If user data is invalid

        Note:
            For new users, the ID field will be populated after save.
        """
        # Validate before saving
        user.validate()

        conn = self.db_pool.get_connection()
        try:
            cursor = conn.cursor()

            # Use upsert pattern (INSERT ... ON DUPLICATE KEY UPDATE)
            # This handles both new users and updates to existing users
            query = """
                INSERT INTO users (id, email, name, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    email = VALUES(email),
                    name = VALUES(name),
                    updated_at = VALUES(updated_at)
            """

            now = datetime.utcnow()
            cursor.execute(query, (
                user.id,
                user.email,
                user.name,
                user.created_at or now,
                now
            ))

            # For new records, get the auto-generated ID
            if user.id is None:
                user.id = cursor.lastrowid

            # Commit transaction
            conn.commit()

            return user

        except Exception as e:
            # Rollback on error to maintain database consistency
            conn.rollback()
            raise DatabaseError(f"Failed to save user: {e}")

        finally:
            conn.close()
```

---

## Configuration and Setup

### Application Configuration (Python)

```python
class Config:
    """
    Application configuration loaded from environment variables.

    Provides centralized access to all configuration values with
    sensible defaults and validation. Follows 12-factor app methodology
    by using environment variables for configuration.

    Environment variables:
        DATABASE_URL: PostgreSQL connection string (required)
        REDIS_URL: Redis connection string (default: localhost)
        SECRET_KEY: Secret key for session encryption (required)
        DEBUG: Enable debug mode (default: False)
        LOG_LEVEL: Logging level (default: INFO)

    Example:
        >>> config = Config.from_env()
        >>> print(config.database_url)
        'postgresql://user:pass@localhost/db'
    """

    def __init__(
        self,
        database_url: str,
        redis_url: str,
        secret_key: str,
        debug: bool = False,
        log_level: str = "INFO"
    ):
        self.database_url = database_url
        self.redis_url = redis_url
        self.secret_key = secret_key
        self.debug = debug
        self.log_level = log_level

    @classmethod
    def from_env(cls) -> "Config":
        """
        Load configuration from environment variables.

        Returns:
            Config instance populated from environment

        Raises:
            ConfigurationError: If required variables are missing or invalid

        Note:
            Use python-dotenv to load .env file in development.
        """
        # Required configuration - fail fast if missing
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise ConfigurationError("DATABASE_URL environment variable is required")

        secret_key = os.environ.get("SECRET_KEY")
        if not secret_key:
            raise ConfigurationError("SECRET_KEY environment variable is required")

        # Validate secret key length for security
        # Minimum 32 bytes for AES-256 encryption
        if len(secret_key) < 32:
            raise ConfigurationError("SECRET_KEY must be at least 32 characters")

        # Optional configuration with sensible defaults
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

        # Parse boolean from string (common in env vars)
        # Any of: "1", "true", "True", "yes", "Yes" -> True
        debug = os.environ.get("DEBUG", "").lower() in ("1", "true", "yes")

        # Validate log level
        log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if log_level not in valid_levels:
            raise ConfigurationError(
                f"LOG_LEVEL must be one of {valid_levels}, got {log_level}"
            )

        return cls(
            database_url=database_url,
            redis_url=redis_url,
            secret_key=secret_key,
            debug=debug,
            log_level=log_level,
        )
```
