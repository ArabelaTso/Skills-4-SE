# Java Implementation Patterns

## Interface Implementation

### Simple Interface Implementation

**From Interface:**
```java
public interface DataRepository {
    Optional<Map<String, Object>> get(String id);
    String save(Map<String, Object> data);
    boolean delete(String id);
}
```

**Implementation:**
```java
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * In-memory implementation of DataRepository.
 */
public class InMemoryDataRepository implements DataRepository {
    private final Map<String, Map<String, Object>> storage;

    public InMemoryDataRepository() {
        this.storage = new ConcurrentHashMap<>();
    }

    @Override
    public Optional<Map<String, Object>> get(String id) {
        Objects.requireNonNull(id, "ID cannot be null");
        return Optional.ofNullable(storage.get(id))
                .map(HashMap::new); // Return copy
    }

    @Override
    public String save(Map<String, Object> data) {
        Objects.requireNonNull(data, "Data cannot be null");

        String id = (String) data.getOrDefault("id", UUID.randomUUID().toString());
        storage.put(id, new HashMap<>(data));
        return id;
    }

    @Override
    public boolean delete(String id) {
        Objects.requireNonNull(id, "ID cannot be null");
        return storage.remove(id) != null;
    }
}
```

### Abstract Class Implementation

**From Abstract Class:**
```java
public abstract class PaymentProcessor {
    public abstract String processPayment(double amount, String currency);
    public abstract boolean refund(String transactionId);

    protected void validateAmount(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
    }
}
```

**Implementation:**
```java
import java.util.*;

/**
 * Stripe implementation of PaymentProcessor.
 */
public class StripePaymentProcessor extends PaymentProcessor {
    private final String apiKey;
    private final Map<String, Transaction> transactions;

    public StripePaymentProcessor(String apiKey) {
        this.apiKey = Objects.requireNonNull(apiKey, "API key cannot be null");
        this.transactions = new HashMap<>();
    }

    @Override
    public String processPayment(double amount, String currency) {
        validateAmount(amount);
        validateCurrency(currency);

        String transactionId = UUID.randomUUID().toString();
        Transaction transaction = new Transaction(transactionId, amount, currency, "COMPLETED");
        transactions.put(transactionId, transaction);

        return transactionId;
    }

    @Override
    public boolean refund(String transactionId) {
        Objects.requireNonNull(transactionId, "Transaction ID cannot be null");

        Transaction transaction = transactions.get(transactionId);
        if (transaction == null || !transaction.getStatus().equals("COMPLETED")) {
            return false;
        }

        transaction.setStatus("REFUNDED");
        return true;
    }

    private void validateCurrency(String currency) {
        Set<String> supportedCurrencies = Set.of("USD", "EUR", "GBP");
        if (!supportedCurrencies.contains(currency)) {
            throw new IllegalArgumentException("Unsupported currency: " + currency);
        }
    }

    private static class Transaction {
        private final String id;
        private final double amount;
        private final String currency;
        private String status;

        public Transaction(String id, double amount, String currency, String status) {
            this.id = id;
            this.amount = amount;
            this.currency = currency;
            this.status = status;
        }

        public String getStatus() {
            return status;
        }

        public void setStatus(String status) {
            this.status = status;
        }
    }
}
```

## Module Structure Patterns

### Service Layer Module

**Structure:**
```
com.example.user/
├── model/
│   └── User.java
├── repository/
│   └── UserRepository.java
├── service/
│   └── UserService.java
└── exception/
    ├── UserServiceException.java
    ├── UserAlreadyExistsException.java
    └── UserNotFoundException.java
```

**User.java:**
```java
package com.example.user.model;

import java.time.LocalDateTime;
import java.util.Objects;

/**
 * User domain model.
 */
public class User {
    private final String id;
    private final String email;
    private String name;
    private final LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public User(String id, String email, String name, LocalDateTime createdAt) {
        this.id = Objects.requireNonNull(id, "ID cannot be null");
        this.email = validateEmail(email);
        this.name = Objects.requireNonNull(name, "Name cannot be null");
        this.createdAt = Objects.requireNonNull(createdAt, "Created date cannot be null");
    }

    private String validateEmail(String email) {
        Objects.requireNonNull(email, "Email cannot be null");
        if (!email.contains("@")) {
            throw new IllegalArgumentException("Invalid email address");
        }
        return email;
    }

    // Getters
    public String getId() { return id; }
    public String getEmail() { return email; }
    public String getName() { return name; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }

    // Setters
    public void setName(String name) {
        this.name = Objects.requireNonNull(name, "Name cannot be null");
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        User user = (User) o;
        return Objects.equals(id, user.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
```

**UserRepository.java:**
```java
package com.example.user.repository;

import com.example.user.model.User;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Repository for User persistence.
 */
public class UserRepository {
    private final Map<String, User> users;

    public UserRepository() {
        this.users = new ConcurrentHashMap<>();
    }

    public Optional<User> findById(String userId) {
        Objects.requireNonNull(userId, "User ID cannot be null");
        return Optional.ofNullable(users.get(userId));
    }

    public Optional<User> findByEmail(String email) {
        Objects.requireNonNull(email, "Email cannot be null");
        return users.values().stream()
                .filter(user -> user.getEmail().equals(email))
                .findFirst();
    }

    public User save(User user) {
        Objects.requireNonNull(user, "User cannot be null");
        users.put(user.getId(), user);
        return user;
    }

    public boolean delete(String userId) {
        Objects.requireNonNull(userId, "User ID cannot be null");
        return users.remove(userId) != null;
    }

    public List<User> findAll() {
        return new ArrayList<>(users.values());
    }
}
```

**UserService.java:**
```java
package com.example.user.service;

import com.example.user.model.User;
import com.example.user.repository.UserRepository;
import com.example.user.exception.*;

import java.time.LocalDateTime;
import java.util.Objects;
import java.util.UUID;

/**
 * Service layer for user operations.
 */
public class UserService {
    private final UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = Objects.requireNonNull(repository, "Repository cannot be null");
    }

    /**
     * Create a new user.
     *
     * @param email User email
     * @param name User name
     * @return Created user
     * @throws UserAlreadyExistsException if user with email already exists
     */
    public User createUser(String email, String name) {
        Objects.requireNonNull(email, "Email cannot be null");
        Objects.requireNonNull(name, "Name cannot be null");

        // Check if user already exists
        if (repository.findByEmail(email).isPresent()) {
            throw new UserAlreadyExistsException("User with email " + email + " already exists");
        }

        // Create new user
        User user = new User(
            UUID.randomUUID().toString(),
            email,
            name,
            LocalDateTime.now()
        );

        return repository.save(user);
    }

    /**
     * Get user by ID.
     *
     * @param userId User ID
     * @return User
     * @throws UserNotFoundException if user not found
     */
    public User getUser(String userId) {
        Objects.requireNonNull(userId, "User ID cannot be null");
        return repository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException("User with id " + userId + " not found"));
    }

    /**
     * Update user information.
     *
     * @param userId User ID
     * @param name New name (optional)
     * @return Updated user
     * @throws UserNotFoundException if user not found
     */
    public User updateUser(String userId, String name) {
        User user = getUser(userId);

        if (name != null) {
            user.setName(name);
        }
        user.setUpdatedAt(LocalDateTime.now());

        return repository.save(user);
    }

    /**
     * Delete user.
     *
     * @param userId User ID
     * @throws UserNotFoundException if user not found
     */
    public void deleteUser(String userId) {
        Objects.requireNonNull(userId, "User ID cannot be null");
        if (!repository.delete(userId)) {
            throw new UserNotFoundException("User with id " + userId + " not found");
        }
    }
}
```

**Exception Classes:**
```java
package com.example.user.exception;

public class UserServiceException extends RuntimeException {
    public UserServiceException(String message) {
        super(message);
    }
}

public class UserAlreadyExistsException extends UserServiceException {
    public UserAlreadyExistsException(String message) {
        super(message);
    }
}

public class UserNotFoundException extends UserServiceException {
    public UserNotFoundException(String message) {
        super(message);
    }
}
```

### Strategy Pattern Module

**Structure:**
```
com.example.notification/
├── NotificationStrategy.java (interface)
├── EmailNotificationStrategy.java
├── SMSNotificationStrategy.java
└── NotificationContext.java
```

**NotificationStrategy.java:**
```java
package com.example.notification;

import java.util.Map;

/**
 * Strategy interface for sending notifications.
 */
public interface NotificationStrategy {
    /**
     * Send notification to recipient.
     *
     * @param recipient Recipient identifier
     * @param message Message content
     * @param metadata Additional metadata
     * @return true if sent successfully
     */
    boolean send(String recipient, String message, Map<String, Object> metadata);

    /**
     * Validate recipient format.
     *
     * @param recipient Recipient identifier
     * @return true if valid
     */
    boolean validateRecipient(String recipient);
}
```

**EmailNotificationStrategy.java:**
```java
package com.example.notification;

import java.util.Map;
import java.util.Objects;
import java.util.regex.Pattern;

/**
 * Email notification strategy.
 */
public class EmailNotificationStrategy implements NotificationStrategy {
    private static final Pattern EMAIL_PATTERN =
        Pattern.compile("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$");

    private final String smtpHost;
    private final int smtpPort;

    public EmailNotificationStrategy(String smtpHost, int smtpPort) {
        this.smtpHost = Objects.requireNonNull(smtpHost, "SMTP host cannot be null");
        this.smtpPort = smtpPort;
    }

    @Override
    public boolean send(String recipient, String message, Map<String, Object> metadata) {
        Objects.requireNonNull(recipient, "Recipient cannot be null");
        Objects.requireNonNull(message, "Message cannot be null");

        if (!validateRecipient(recipient)) {
            throw new IllegalArgumentException("Invalid email address: " + recipient);
        }

        // Simulate sending email
        System.out.println("Sending email to " + recipient + ": " + message);
        return true;
    }

    @Override
    public boolean validateRecipient(String recipient) {
        return recipient != null && EMAIL_PATTERN.matcher(recipient).matches();
    }
}
```

## Best Practices

### Null Safety
- Use `Objects.requireNonNull()` for parameter validation
- Use `Optional<T>` for nullable return values
- Validate inputs early in public methods
- Document nullability in JavaDoc

### Immutability
- Make fields `final` when possible
- Return defensive copies of mutable objects
- Use immutable collections where appropriate
- Consider using records (Java 14+) for data classes

### Exception Handling
- Create custom exception hierarchy
- Use unchecked exceptions for programming errors
- Use checked exceptions for recoverable errors
- Provide meaningful exception messages

### Documentation
- Include JavaDoc for all public classes and methods
- Document parameters, return values, and exceptions
- Include usage examples for complex APIs
- Use `@param`, `@return`, `@throws` tags

### Dependency Injection
- Accept dependencies through constructor
- Use interfaces for loose coupling
- Make dependencies explicit and final
- Facilitate testing with mock implementations
