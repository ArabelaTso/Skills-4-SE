# Code Change Patterns and Test Generation Strategies

Catalog of common code changes and corresponding regression test generation strategies.

## Table of Contents
- [Method Signature Changes](#method-signature-changes)
- [New Methods Added](#new-methods-added)
- [Method Logic Modified](#method-logic-modified)
- [Class Structure Changes](#class-structure-changes)
- [Dependency Changes](#dependency-changes)
- [Removed Methods](#removed-methods)

## Method Signature Changes

### Pattern: Parameter Added

**Old Code**:
```java
public int calculateDiscount(int price) {
    return price * 10 / 100;
}
```

**New Code**:
```java
public int calculateDiscount(int price, int discountPercent) {
    return price * discountPercent / 100;
}
```

**Old Test**:
```java
@Test
public void testCalculateDiscount() {
    assertEquals(10, calculator.calculateDiscount(100));
}
```

**Test Generation Strategy**:
1. **Update existing test**: Migrate old test to use new signature with default/equivalent parameter
2. **Add new tests**: Generate tests for new parameter variations

**Generated Tests**:
```java
@Test
public void testCalculateDiscount_WithDefaultPercent() {
    // Migrated from old test - preserves original behavior
    assertEquals(10, calculator.calculateDiscount(100, 10));
}

@Test
public void testCalculateDiscount_WithCustomPercent() {
    // New test for added parameter
    assertEquals(25, calculator.calculateDiscount(100, 25));
    assertEquals(50, calculator.calculateDiscount(200, 25));
}

@Test
public void testCalculateDiscount_WithZeroPercent() {
    // Edge case for new parameter
    assertEquals(0, calculator.calculateDiscount(100, 0));
}
```

### Pattern: Return Type Changed

**Old Code**:
```java
public int getUserAge(String userId) {
    return database.getAge(userId);
}
```

**New Code**:
```java
public Optional<Integer> getUserAge(String userId) {
    return Optional.ofNullable(database.getAge(userId));
}
```

**Test Generation Strategy**:
1. **Update existing tests**: Wrap assertions to handle Optional
2. **Add null-case tests**: Test empty Optional scenarios

**Generated Tests**:
```java
@Test
public void testGetUserAge_ExistingUser() {
    // Migrated test
    Optional<Integer> age = service.getUserAge("user123");
    assertTrue(age.isPresent());
    assertEquals(25, age.get());
}

@Test
public void testGetUserAge_NonExistentUser() {
    // New test for Optional.empty() case
    Optional<Integer> age = service.getUserAge("unknown");
    assertFalse(age.isPresent());
}
```

## New Methods Added

### Pattern: New Public Method

**New Code**:
```java
public class UserService {
    // Existing method
    public User getUser(String id) { ... }

    // New method added
    public List<User> getUsersByRole(String role) {
        return users.stream()
            .filter(u -> u.getRole().equals(role))
            .collect(Collectors.toList());
    }
}
```

**Test Generation Strategy**:
1. **Generate basic functionality test**: Test normal case
2. **Generate edge case tests**: Empty results, null inputs
3. **Generate boundary tests**: Multiple results

**Generated Tests**:
```java
@Test
public void testGetUsersByRole_WithMatchingUsers() {
    // Setup
    when(userRepository.findAll()).thenReturn(Arrays.asList(
        new User("1", "admin"),
        new User("2", "user"),
        new User("3", "admin")
    ));

    // Execute
    List<User> admins = service.getUsersByRole("admin");

    // Verify
    assertEquals(2, admins.size());
    assertTrue(admins.stream().allMatch(u -> u.getRole().equals("admin")));
}

@Test
public void testGetUsersByRole_NoMatches() {
    when(userRepository.findAll()).thenReturn(Arrays.asList(
        new User("1", "user")
    ));

    List<User> admins = service.getUsersByRole("admin");

    assertTrue(admins.isEmpty());
}

@Test
public void testGetUsersByRole_NullRole() {
    assertThrows(NullPointerException.class, () -> {
        service.getUsersByRole(null);
    });
}
```

## Method Logic Modified

### Pattern: Algorithm Changed

**Old Code**:
```java
public boolean isPrime(int n) {
    if (n <= 1) return false;
    for (int i = 2; i < n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}
```

**New Code**:
```java
public boolean isPrime(int n) {
    if (n <= 1) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    // Optimized: only check odd divisors up to sqrt(n)
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}
```

**Old Tests**:
```java
@Test
public void testIsPrime() {
    assertTrue(isPrime(2));
    assertTrue(isPrime(7));
    assertFalse(isPrime(4));
}
```

**Test Generation Strategy**:
1. **Preserve existing tests**: Keep all old tests (behavior should be identical)
2. **Add performance tests**: Verify optimization works for large inputs
3. **Add edge cases**: Test boundary conditions of new logic

**Generated Tests**:
```java
// Existing tests preserved
@Test
public void testIsPrime_SmallPrimes() {
    assertTrue(isPrime(2));
    assertTrue(isPrime(3));
    assertTrue(isPrime(7));
}

@Test
public void testIsPrime_Composites() {
    assertFalse(isPrime(4));
    assertFalse(isPrime(9));
}

// New tests for optimized algorithm
@Test
public void testIsPrime_LargePrime() {
    // Tests optimization path
    assertTrue(isPrime(97));
    assertTrue(isPrime(1009));
}

@Test
public void testIsPrime_EvenNumbers() {
    // Tests early even-number check
    assertFalse(isPrime(100));
    assertFalse(isPrime(1000));
}
```

### Pattern: Error Handling Added

**Old Code**:
```java
public double divide(int a, int b) {
    return (double) a / b;
}
```

**New Code**:
```java
public double divide(int a, int b) {
    if (b == 0) {
        throw new IllegalArgumentException("Division by zero");
    }
    return (double) a / b;
}
```

**Test Generation Strategy**:
1. **Preserve existing tests**: Keep valid division tests
2. **Add exception tests**: Test new error handling

**Generated Tests**:
```java
@Test
public void testDivide_ValidInputs() {
    // Preserved test
    assertEquals(2.0, calculator.divide(10, 5), 0.001);
}

@Test
public void testDivide_ByZero() {
    // New test for error handling
    IllegalArgumentException ex = assertThrows(
        IllegalArgumentException.class,
        () -> calculator.divide(10, 0)
    );
    assertEquals("Division by zero", ex.getMessage());
}
```

## Class Structure Changes

### Pattern: Field Added

**Old Code**:
```java
public class Order {
    private String orderId;
    private double amount;

    public Order(String orderId, double amount) {
        this.orderId = orderId;
        this.amount = amount;
    }
}
```

**New Code**:
```java
public class Order {
    private String orderId;
    private double amount;
    private LocalDateTime createdAt;  // New field

    public Order(String orderId, double amount, LocalDateTime createdAt) {
        this.orderId = orderId;
        this.amount = amount;
        this.createdAt = createdAt;
    }
}
```

**Test Generation Strategy**:
1. **Update constructor calls**: Add new parameter to existing tests
2. **Add field-specific tests**: Test new field behavior

**Generated Tests**:
```java
@Test
public void testOrderCreation() {
    // Updated test with new parameter
    LocalDateTime now = LocalDateTime.now();
    Order order = new Order("ORD-123", 99.99, now);

    assertEquals("ORD-123", order.getOrderId());
    assertEquals(99.99, order.getAmount(), 0.01);
    assertEquals(now, order.getCreatedAt());  // New assertion
}

@Test
public void testOrderCreation_WithNullTimestamp() {
    // New test for edge case
    assertThrows(NullPointerException.class, () -> {
        new Order("ORD-123", 99.99, null);
    });
}
```

### Pattern: Inheritance Changed

**Old Code**:
```java
public class EmailNotifier {
    public void send(String message) { ... }
}
```

**New Code**:
```java
public interface Notifier {
    void send(String message);
}

public class EmailNotifier implements Notifier {
    @Override
    public void send(String message) { ... }
}
```

**Test Generation Strategy**:
1. **Preserve existing tests**: Concrete class tests remain valid
2. **Add interface tests**: Test polymorphic behavior

**Generated Tests**:
```java
@Test
public void testEmailNotifier_Send() {
    // Preserved test
    EmailNotifier notifier = new EmailNotifier();
    notifier.send("Test message");
    verify(emailService).sendEmail("Test message");
}

@Test
public void testNotifier_Polymorphism() {
    // New test for interface
    Notifier notifier = new EmailNotifier();
    notifier.send("Test message");
    verify(emailService).sendEmail("Test message");
}
```

## Dependency Changes

### Pattern: Dependency Injection Added

**Old Code**:
```java
public class OrderService {
    private PaymentProcessor processor = new PaymentProcessor();

    public void processOrder(Order order) {
        processor.process(order.getAmount());
    }
}
```

**New Code**:
```java
public class OrderService {
    private final PaymentProcessor processor;

    public OrderService(PaymentProcessor processor) {
        this.processor = processor;
    }

    public void processOrder(Order order) {
        processor.process(order.getAmount());
    }
}
```

**Test Generation Strategy**:
1. **Update test setup**: Use constructor injection with mocks
2. **Preserve test logic**: Behavior verification remains the same

**Generated Tests**:
```java
@Test
public void testProcessOrder() {
    // Updated setup with DI
    PaymentProcessor mockProcessor = mock(PaymentProcessor.class);
    OrderService service = new OrderService(mockProcessor);

    Order order = new Order("ORD-123", 99.99);
    service.processOrder(order);

    // Preserved verification
    verify(mockProcessor).process(99.99);
}
```

## Removed Methods

### Pattern: Method Deleted

**Old Code**:
```java
public class Calculator {
    public int add(int a, int b) { return a + b; }
    public int subtract(int a, int b) { return a - b; }
}
```

**New Code**:
```java
public class Calculator {
    public int add(int a, int b) { return a + b; }
    // subtract method removed
}
```

**Test Generation Strategy**:
1. **Mark tests as obsolete**: Comment out or remove tests for deleted methods
2. **Check for replacement**: If functionality moved elsewhere, suggest migration

**Action**:
```java
// Test removed or commented:
// @Test
// public void testSubtract() {
//     assertEquals(5, calculator.subtract(10, 5));
// }
// Reason: subtract() method removed in new version
```

## Test Generation Decision Matrix

| Change Type | Preserve Old Tests | Update Old Tests | Generate New Tests |
|-------------|-------------------|------------------|-------------------|
| Parameter added | ✓ (migrate) | ✓ (add param) | ✓ (new param cases) |
| Return type changed | ✗ | ✓ (adapt assertions) | ✓ (new type cases) |
| New method | N/A | N/A | ✓ (full coverage) |
| Logic optimized | ✓ | ✗ | ✓ (edge cases) |
| Error handling added | ✓ | ✗ | ✓ (exception cases) |
| Field added | ✗ | ✓ (update setup) | ✓ (field tests) |
| Method removed | ✗ (delete) | N/A | N/A |
| Dependency injection | ✗ | ✓ (update setup) | ✗ |
