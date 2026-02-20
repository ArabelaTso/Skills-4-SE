# Test Patterns for Killing Mutants

## Overview

This guide provides proven test patterns and strategies for killing specific types of mutants. Each pattern addresses common mutation scenarios and provides concrete examples.

## Pattern 1: Boundary Value Testing

**Use Case:** Kill relational operator and conditional boundary mutants

**Mutants Killed:**
- `<` ↔ `<=`
- `>` ↔ `>=`
- Off-by-one errors

**Pattern:**
```java
// Code under test
public boolean isEligible(int age) {
    return age >= 18;
}

// Weak test (doesn't kill boundary mutant)
@Test
public void testEligibility() {
    assertTrue(isEligible(20));   // Passes for both >= and >
    assertFalse(isEligible(15));  // Passes for both >= and >
}

// Strong test (kills boundary mutant)
@Test
public void testEligibilityBoundary() {
    assertTrue(isEligible(18));   // Kills mutant: >= changed to >
    assertTrue(isEligible(19));   // Above boundary
    assertFalse(isEligible(17));  // Below boundary
}
```

**Strategy:**
1. Identify boundary value in condition
2. Test exact boundary (18)
3. Test one above boundary (19)
4. Test one below boundary (17)

## Pattern 2: Exact Value Assertions

**Use Case:** Kill arithmetic operator and return value mutants

**Mutants Killed:**
- `+` → `-`, `*`, `/`
- Return value changes
- Constant mutations

**Pattern:**
```python
# Code under test
def calculate_total(price, quantity):
    return price * quantity

# Weak test (doesn't kill mutants)
def test_calculate_total_weak():
    result = calculate_total(10, 5)
    assert result > 0  # Too weak: passes for many mutations

# Strong test (kills mutants)
def test_calculate_total_strong():
    result = calculate_total(10, 5)
    assert result == 50  # Exact value: kills +, -, / mutations

    result = calculate_total(7, 3)
    assert result == 21  # Different values produce different results
```

**Strategy:**
1. Assert exact expected values, not ranges
2. Use inputs where different operators produce different results
3. Avoid inputs like 0, 1 where operations may be equivalent

## Pattern 3: Boolean Logic Truth Tables

**Use Case:** Kill logical operator mutants

**Mutants Killed:**
- `&&` ↔ `||`
- `!` insertion/removal
- Boolean expression changes

**Pattern:**
```javascript
// Code under test
function canAccess(isAuthenticated, hasPermission) {
    return isAuthenticated && hasPermission;
}

// Weak test (doesn't kill OR mutant)
test('user can access when authenticated and has permission', () => {
    expect(canAccess(true, true)).toBe(true);
});

// Strong test (kills AND/OR mutants)
test('access requires both authentication and permission', () => {
    expect(canAccess(true, true)).toBe(true);    // T && T = T
    expect(canAccess(true, false)).toBe(false);  // T && F = F (kills OR)
    expect(canAccess(false, true)).toBe(false);  // F && T = F (kills OR)
    expect(canAccess(false, false)).toBe(false); // F && F = F
});
```

**Strategy:**
1. Test all four boolean combinations (T/T, T/F, F/T, F/F)
2. Verify correct logical operator behavior
3. Use truth table to guide test cases

## Pattern 4: Side Effect Verification

**Use Case:** Kill void method call removal mutants

**Mutants Killed:**
- Removed method calls
- Statement deletions
- Missing side effects

**Pattern:**
```java
// Code under test
public class UserService {
    private Database db;
    private EmailService email;

    public void registerUser(User user) {
        db.save(user);
        email.sendWelcome(user);
    }
}

// Weak test (doesn't verify side effects)
@Test
public void testRegisterUser_weak() {
    UserService service = new UserService(db, email);
    service.registerUser(user);
    // No verification - mutant removing calls survives
}

// Strong test (kills method removal mutants)
@Test
public void testRegisterUser_strong() {
    UserService service = new UserService(db, email);
    service.registerUser(user);

    verify(db).save(user);           // Kills mutant removing db.save()
    verify(email).sendWelcome(user); // Kills mutant removing email.send()
}
```

**Strategy:**
1. Use mocks/spies to verify method calls
2. Check database state changes
3. Verify external interactions
4. Assert on observable side effects

## Pattern 5: State Transition Testing

**Use Case:** Kill mutants affecting state changes

**Mutants Killed:**
- Assignment mutations
- State update changes
- Increment/decrement mutations

**Pattern:**
```python
# Code under test
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

# Weak test (doesn't verify state)
def test_counter_weak():
    counter = Counter()
    counter.increment()
    # No assertion - mutant survives

# Strong test (kills state mutants)
def test_counter_strong():
    counter = Counter()
    assert counter.count == 0  # Initial state

    counter.increment()
    assert counter.count == 1  # Kills mutant: += changed to -=

    counter.increment()
    assert counter.count == 2  # Kills mutant: += changed to =

    counter.decrement()
    assert counter.count == 1  # Kills decrement mutants
```

**Strategy:**
1. Assert state before operation
2. Assert state after each operation
3. Test multiple state transitions
4. Verify accumulated effects

## Pattern 6: Exception and Error Handling

**Use Case:** Kill mutants in error handling paths

**Mutants Killed:**
- Exception handler removal
- Throw statement changes
- Error condition mutations

**Pattern:**
```java
// Code under test
public int divide(int a, int b) {
    if (b == 0) {
        throw new IllegalArgumentException("Division by zero");
    }
    return a / b;
}

// Weak test (doesn't test error case)
@Test
public void testDivide_weak() {
    assertEquals(5, divide(10, 2));
}

// Strong test (kills error handling mutants)
@Test
public void testDivide_strong() {
    assertEquals(5, divide(10, 2));  // Normal case

    assertThrows(IllegalArgumentException.class, () -> {
        divide(10, 0);  // Kills mutant removing exception
    });
}

@Test
public void testDivide_errorMessage() {
    Exception ex = assertThrows(IllegalArgumentException.class, () -> {
        divide(10, 0);
    });
    assertEquals("Division by zero", ex.getMessage());  // Verify message
}
```

**Strategy:**
1. Test both success and error paths
2. Verify exception types
3. Check exception messages
4. Test all error conditions

## Pattern 7: Null and Empty Input Testing

**Use Case:** Kill mutants in guard clauses and validation

**Mutants Killed:**
- Conditional removal
- Null check mutations
- Empty check mutations

**Pattern:**
```javascript
// Code under test
function processItems(items) {
    if (!items || items.length === 0) {
        return [];
    }
    return items.map(item => item.toUpperCase());
}

// Weak test (doesn't test edge cases)
test('processes items', () => {
    expect(processItems(['a', 'b'])).toEqual(['A', 'B']);
});

// Strong test (kills guard clause mutants)
test('handles null and empty inputs', () => {
    expect(processItems(null)).toEqual([]);      // Kills null check removal
    expect(processItems(undefined)).toEqual([]); // Kills undefined check
    expect(processItems([])).toEqual([]);        // Kills empty check removal
    expect(processItems(['a'])).toEqual(['A']); // Normal case
});
```

**Strategy:**
1. Test null/undefined inputs
2. Test empty collections
3. Test single-element collections
4. Test normal cases

## Pattern 8: Return Path Coverage

**Use Case:** Kill return value mutants in multiple return paths

**Mutants Killed:**
- Return value changes
- Return true/false mutations
- Early return mutations

**Pattern:**
```python
# Code under test
def get_discount(customer_type, amount):
    if customer_type == "VIP":
        return amount * 0.2
    elif customer_type == "REGULAR":
        return amount * 0.1
    else:
        return 0

# Weak test (doesn't cover all paths)
def test_discount_weak():
    assert get_discount("VIP", 100) > 0

# Strong test (kills return value mutants)
def test_discount_strong():
    assert get_discount("VIP", 100) == 20.0      # Exact VIP discount
    assert get_discount("REGULAR", 100) == 10.0  # Exact regular discount
    assert get_discount("GUEST", 100) == 0       # Exact no discount
    assert get_discount("UNKNOWN", 100) == 0     # Default case
```

**Strategy:**
1. Test all return paths
2. Assert exact return values
3. Cover all branches
4. Test default/else cases

## Pattern 9: Loop and Iteration Testing

**Use Case:** Kill mutants in loops

**Mutants Killed:**
- Loop boundary changes
- Iterator mutations
- Accumulator mutations

**Pattern:**
```java
// Code under test
public int sumArray(int[] arr) {
    int sum = 0;
    for (int i = 0; i < arr.length; i++) {
        sum += arr[i];
    }
    return sum;
}

// Weak test (doesn't catch off-by-one)
@Test
public void testSumArray_weak() {
    assertEquals(6, sumArray(new int[]{1, 2, 3}));
}

// Strong test (kills loop mutants)
@Test
public void testSumArray_strong() {
    assertEquals(0, sumArray(new int[]{}));           // Empty array
    assertEquals(5, sumArray(new int[]{5}));          // Single element
    assertEquals(6, sumArray(new int[]{1, 2, 3}));    // Multiple elements
    assertEquals(10, sumArray(new int[]{1, 2, 3, 4})); // Different sum

    // Use distinct values to catch index mutations
    assertEquals(14, sumArray(new int[]{2, 4, 8}));   // Powers of 2
}
```

**Strategy:**
1. Test empty collections
2. Test single-element collections
3. Use distinct values (not all same)
4. Verify complete iteration

## Pattern 10: Comparison and Equality Testing

**Use Case:** Kill equality operator mutants

**Mutants Killed:**
- `==` ↔ `!=`
- `equals()` mutations
- Comparison changes

**Pattern:**
```javascript
// Code under test
function findUser(users, targetId) {
    return users.find(user => user.id === targetId);
}

// Weak test (doesn't verify correct match)
test('finds user', () => {
    const users = [{id: 1, name: 'Alice'}];
    const result = findUser(users, 1);
    expect(result).toBeDefined();  // Too weak
});

// Strong test (kills equality mutants)
test('finds correct user by id', () => {
    const users = [
        {id: 1, name: 'Alice'},
        {id: 2, name: 'Bob'},
        {id: 3, name: 'Charlie'}
    ];

    const result = findUser(users, 2);
    expect(result.id).toBe(2);        // Exact match
    expect(result.name).toBe('Bob');  // Correct user

    expect(findUser(users, 99)).toBeUndefined();  // Not found case
});
```

**Strategy:**
1. Test exact matches
2. Test non-matches
3. Use multiple distinct values
4. Verify correct item selected

## Pattern 11: String and Collection Mutations

**Use Case:** Kill string and collection operation mutants

**Mutants Killed:**
- String method mutations
- Collection size changes
- Slice/substring mutations

**Pattern:**
```python
# Code under test
def get_first_n_items(items, n):
    return items[:n]

# Weak test
def test_get_items_weak():
    result = get_first_n_items([1, 2, 3, 4, 5], 3)
    assert len(result) == 3  # Doesn't verify content

# Strong test (kills slice mutants)
def test_get_items_strong():
    items = [10, 20, 30, 40, 50]

    result = get_first_n_items(items, 3)
    assert result == [10, 20, 30]  # Exact content, kills [:n] → [:n-1]

    result = get_first_n_items(items, 1)
    assert result == [10]  # Kills [:n] → [:n+1]

    result = get_first_n_items(items, 0)
    assert result == []  # Edge case

    result = get_first_n_items(items, 10)
    assert result == items  # Beyond length
```

**Strategy:**
1. Assert exact content, not just length
2. Use distinct values
3. Test boundary cases (0, 1, max)
4. Test beyond boundaries

## Pattern 12: Parameterized Testing

**Use Case:** Kill multiple mutants with data-driven tests

**Mutants Killed:**
- Multiple operator mutations
- Various input combinations
- Edge cases

**Pattern:**
```java
// Code under test
public String getGrade(int score) {
    if (score >= 90) return "A";
    if (score >= 80) return "B";
    if (score >= 70) return "C";
    if (score >= 60) return "D";
    return "F";
}

// Strong parameterized test
@ParameterizedTest
@CsvSource({
    "100, A",  // Max boundary
    "90, A",   // A boundary
    "89, B",   // Just below A
    "80, B",   // B boundary
    "79, C",   // Just below B
    "70, C",   // C boundary
    "69, D",   // Just below C
    "60, D",   // D boundary
    "59, F",   // Just below D
    "0, F"     // Min boundary
})
public void testGetGrade(int score, String expectedGrade) {
    assertEquals(expectedGrade, getGrade(score));
}
```

**Strategy:**
1. Test all boundaries
2. Test values just above and below boundaries
3. Test extreme values
4. Use parameterized tests for efficiency

## Anti-Patterns to Avoid

### Anti-Pattern 1: Testing Implementation

```java
// BAD: Tests implementation details
@Test
public void testSortUsesQuickSort() {
    // Checking algorithm choice, not behavior
}

// GOOD: Tests behavior
@Test
public void testSortOrdersElementsAscending() {
    List<Integer> result = sort(Arrays.asList(3, 1, 2));
    assertEquals(Arrays.asList(1, 2, 3), result);
}
```

### Anti-Pattern 2: Weak Assertions

```python
# BAD: Too weak
def test_calculate():
    result = calculate(5, 3)
    assert result is not None  # Survives most mutants

# GOOD: Specific assertion
def test_calculate():
    result = calculate(5, 3)
    assert result == 8  # Kills arithmetic mutants
```

### Anti-Pattern 3: Testing Only Happy Path

```javascript
// BAD: Only success case
test('processes data', () => {
    expect(process({valid: true})).toBe('success');
});

// GOOD: Tests error cases too
test('handles invalid data', () => {
    expect(() => process({valid: false})).toThrow();
    expect(() => process(null)).toThrow();
});
```

## Test Generation Checklist

When generating tests to kill mutants:

- [ ] Assert exact values, not ranges or types
- [ ] Test all boundary conditions
- [ ] Cover all branches and return paths
- [ ] Verify side effects and state changes
- [ ] Test null/empty/edge cases
- [ ] Use distinct input values
- [ ] Check exception handling
- [ ] Verify boolean logic with truth tables
- [ ] Test all combinations for logical operators
- [ ] Assert on observable behavior, not implementation
