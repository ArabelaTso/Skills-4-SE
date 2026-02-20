---
name: test-oracle-generator
description: >
  Generates automated test oracles to verify correct software behavior. Creates assertion-based
  oracles (expected values), property-based oracles (invariants), differential oracles (comparing
  implementations), and metamorphic oracles (input transformations). Use when you need to generate
  assertions for test cases, identify invariants that should always hold, compare new vs legacy
  implementations, create metamorphic test relationships, validate function correctness, or improve
  test coverage with better verification strategies. Supports Python (pytest, unittest, hypothesis)
  and Java (JUnit, property testing).
---

# Test Oracle Generator

Generate automated test oracles to verify correct software behavior across multiple oracle types.

## Oracle Types

1. **Assertion-based**: Compare actual vs expected output
2. **Property-based**: Verify invariants that should always hold
3. **Differential**: Compare new implementation against reference
4. **Metamorphic**: Test input-output transformations

## Workflow

### Step 1: Analyze the Function Under Test

Understand what the function does and its expected behavior.

**Checklist:**
- [ ] Read function signature and docstring
- [ ] Identify input parameters and types
- [ ] Identify return type and possible values
- [ ] Note preconditions and postconditions
- [ ] Check for edge cases (empty input, null, boundary values)

**Example Analysis:**

```python
# Python
def calculate_discount(price: float, discount_percent: int) -> float:
    """Calculate discounted price.

    Args:
        price: Original price (must be positive)
        discount_percent: Discount percentage (0-100)

    Returns:
        Discounted price
    """
    return price * (1 - discount_percent / 100)
```

**Analysis:**
- Inputs: `price` (float, must be > 0), `discount_percent` (int, 0-100)
- Output: float (discounted price)
- Invariants: Result should be ≤ original price, result should be ≥ 0
- Edge cases: 0% discount, 100% discount, boundary values

### Step 2: Generate Assertion-Based Oracles

Create explicit expected value assertions for common cases.

**Template:**

```python
# Python (pytest)
def test_<function>_<scenario>():
    # Arrange
    input1 = <value>
    input2 = <value>
    expected = <calculated_expected_value>

    # Act
    actual = function_under_test(input1, input2)

    # Assert
    assert actual == expected, f"Expected {expected}, got {actual}"
```

```java
// Java (JUnit)
@Test
public void test<Function><Scenario>() {
    // Arrange
    Type input1 = <value>;
    Type input2 = <value>;
    Type expected = <calculated_expected_value>;

    // Act
    Type actual = functionUnderTest(input1, input2);

    // Assert
    assertEquals(expected, actual, "Expected and actual should match");
}
```

**Example:**

```python
def test_calculate_discount_50_percent():
    # Arrange
    price = 100.0
    discount = 50
    expected = 50.0

    # Act
    actual = calculate_discount(price, discount)

    # Assert
    assert actual == expected
    assert abs(actual - expected) < 0.01  # For floating point
```

**Generate oracles for:**
- ✓ Typical cases (middle of valid range)
- ✓ Boundary values (min/max)
- ✓ Edge cases (empty, zero, null)
- ✓ Special values (negative, infinity for numeric types)

### Step 3: Generate Property-Based Oracles

Identify invariants and properties that should always hold.

**Common Properties:**

1. **Range properties**: Output within expected range
2. **Relationship properties**: Output relates to input in specific way
3. **Conservation properties**: Something is preserved (e.g., list length)
4. **Idempotence**: Applying function twice gives same result as once
5. **Commutativity**: Order of inputs doesn't matter
6. **Associativity**: Grouping doesn't matter

**Template (Python with hypothesis):**

```python
from hypothesis import given, strategies as st

@given(st.floats(min_value=0.01, max_value=10000),
       st.integers(min_value=0, max_value=100))
def test_discount_properties(price, discount_percent):
    result = calculate_discount(price, discount_percent)

    # Property: Result should never exceed original price
    assert result <= price, "Discount should not increase price"

    # Property: Result should be non-negative
    assert result >= 0, "Price cannot be negative"

    # Property: 0% discount returns original price
    if discount_percent == 0:
        assert abs(result - price) < 0.01

    # Property: 100% discount returns 0
    if discount_percent == 100:
        assert abs(result) < 0.01
```

**Template (Java with JUnit Theories):**

```java
@Theory
public void discountProperties(
    @ForAll @InRange(min = "0.01", max = "10000") double price,
    @ForAll @InRange(min = "0", max = "100") int discountPercent) {

    double result = calculateDiscount(price, discountPercent);

    // Property: Result should never exceed original price
    assertTrue(result <= price, "Discount should not increase price");

    // Property: Result should be non-negative
    assertTrue(result >= 0, "Price cannot be negative");
}
```

**Identify properties by asking:**
- What can I say about the output without computing it exactly?
- What relationships must hold between input and output?
- What constraints must the output satisfy?
- What should never happen?

For detailed property patterns, see [references/property_patterns.md](references/property_patterns.md).

### Step 4: Generate Differential Oracles

Compare new implementation against reference implementation.

**Use Cases:**
- Refactoring: New optimized version vs old version
- Migration: New library/language vs legacy system
- Bug fixes: Patched version vs unpatched version

**Template:**

```python
# Python
def test_new_vs_legacy_implementation():
    # Test data
    test_cases = [
        (100.0, 10),
        (50.0, 25),
        (200.0, 0),
        (75.0, 100),
    ]

    for price, discount in test_cases:
        # Compare outputs
        legacy_result = legacy_calculate_discount(price, discount)
        new_result = calculate_discount(price, discount)

        assert abs(legacy_result - new_result) < 0.01, \
            f"Mismatch for ({price}, {discount}): " \
            f"legacy={legacy_result}, new={new_result}"
```

```java
// Java
@Test
public void testNewVsLegacyImplementation() {
    Object[][] testCases = {
        {100.0, 10},
        {50.0, 25},
        {200.0, 0},
        {75.0, 100}
    };

    for (Object[] testCase : testCases) {
        double price = (double) testCase[0];
        int discount = (int) testCase[1];

        double legacyResult = LegacyClass.calculateDiscount(price, discount);
        double newResult = calculateDiscount(price, discount);

        assertEquals(legacyResult, newResult, 0.01,
            String.format("Mismatch for (%f, %d)", price, discount));
    }
}
```

**Best Practices:**
- Generate diverse test data (random, boundary, edge cases)
- Include both typical and unusual inputs
- Log differences for debugging
- Consider performance differences acceptable

### Step 5: Generate Metamorphic Oracles

Create test pairs where input transformation produces predictable output transformation.

**Metamorphic Relations:**

1. **Additive**: f(x) + f(y) = f(x + y)
2. **Multiplicative**: f(k × x) = k × f(x)
3. **Permutation**: f(permute(x)) = permute(f(x))
4. **Subset**: f(subset(x)) ⊆ f(x)
5. **Inverse**: f(f⁻¹(x)) = x

**Example for discount function:**

```python
# Python
def test_discount_metamorphic_double_price():
    """If price doubles, discount amount doubles."""
    price = 100.0
    discount_percent = 20

    result1 = calculate_discount(price, discount_percent)
    result2 = calculate_discount(price * 2, discount_percent)

    discount_amount1 = price - result1
    discount_amount2 = (price * 2) - result2

    # Metamorphic relation: doubling price doubles discount amount
    assert abs(discount_amount2 - 2 * discount_amount1) < 0.01

def test_discount_metamorphic_additive():
    """Applying discount to sum equals sum of individual discounts."""
    price1 = 50.0
    price2 = 30.0
    discount_percent = 15

    # Method 1: Discount on combined price
    combined_result = calculate_discount(price1 + price2, discount_percent)

    # Method 2: Sum of individual discounts
    individual_sum = (calculate_discount(price1, discount_percent) +
                      calculate_discount(price2, discount_percent))

    # Metamorphic relation: Should be equivalent
    assert abs(combined_result - individual_sum) < 0.01
```

**Example for sorting function:**

```python
def test_sort_metamorphic_reverse():
    """Reversing then sorting gives same result as sorting."""
    input_list = [3, 1, 4, 1, 5, 9, 2, 6]

    result1 = sort(input_list)
    result2 = sort(list(reversed(input_list)))

    assert result1 == result2

def test_sort_metamorphic_duplicate():
    """Sorting list with duplicated elements maintains order."""
    input_list = [3, 1, 4]
    duplicated = input_list + input_list

    result = sort(duplicated)

    # Should be sorted version of original, doubled
    expected = sorted(input_list) + sorted(input_list)
    assert result == sorted(expected)
```

For more metamorphic relation patterns, see [references/metamorphic_patterns.md](references/metamorphic_patterns.md).

### Step 6: Combine Oracles for Comprehensive Testing

Use multiple oracle types together for robust verification.

**Example: Complete test suite for calculate_discount:**

```python
import pytest
from hypothesis import given, strategies as st

# Assertion-based oracles
class TestDiscountAssertions:
    def test_50_percent_discount(self):
        assert calculate_discount(100.0, 50) == 50.0

    def test_no_discount(self):
        assert calculate_discount(100.0, 0) == 100.0

    def test_full_discount(self):
        assert calculate_discount(100.0, 100) == 0.0

# Property-based oracles
class TestDiscountProperties:
    @given(st.floats(min_value=0.01, max_value=10000),
           st.integers(min_value=0, max_value=100))
    def test_result_within_bounds(self, price, discount):
        result = calculate_discount(price, discount)
        assert 0 <= result <= price

    @given(st.floats(min_value=0.01, max_value=10000),
           st.integers(min_value=0, max_value=100))
    def test_monotonic_in_discount(self, price, discount):
        """Higher discount percentage means lower price."""
        if discount < 100:
            result1 = calculate_discount(price, discount)
            result2 = calculate_discount(price, discount + 1)
            assert result2 <= result1

# Differential oracles
class TestDiscountDifferential:
    @pytest.mark.parametrize("price,discount", [
        (100.0, 10), (50.0, 25), (200.0, 50)
    ])
    def test_vs_manual_calculation(self, price, discount):
        result = calculate_discount(price, discount)
        expected = price * (1 - discount / 100)
        assert abs(result - expected) < 0.01

# Metamorphic oracles
class TestDiscountMetamorphic:
    def test_double_price_doubles_discount_amount(self):
        price = 100.0
        discount = 20

        discount_amt1 = price - calculate_discount(price, discount)
        discount_amt2 = (price * 2) - calculate_discount(price * 2, discount)

        assert abs(discount_amt2 - 2 * discount_amt1) < 0.01
```

### Step 7: Document and Validate Oracles

Ensure oracles are correct and well-documented.

**Oracle Documentation Template:**

```python
def test_function_oracle_type():
    """Brief description of what this oracle verifies.

    Oracle Type: [Assertion-based|Property-based|Differential|Metamorphic]

    Rationale: Explain why this property/assertion should hold.

    Edge Cases Covered:
    - Case 1
    - Case 2
    """
    # Test implementation
    pass
```

**Validation Checklist:**
- [ ] Oracle passes on correct implementation
- [ ] Oracle fails on intentionally broken implementation (mutation testing)
- [ ] Oracle is deterministic (same input → same result)
- [ ] Oracle is independent (doesn't rely on other test state)
- [ ] Oracle has clear failure messages
- [ ] Oracle is documented with rationale

**Mutation Testing (validate oracle effectiveness):**

```python
# Introduce deliberate bug to verify oracle catches it
def calculate_discount_buggy(price, discount_percent):
    # BUG: Wrong formula
    return price * discount_percent / 100  # Should be: price * (1 - discount_percent / 100)

# Oracle should fail on buggy version
def test_oracle_detects_bug():
    """Verify oracle catches the bug."""
    with pytest.raises(AssertionError):
        assert calculate_discount_buggy(100, 50) == 50.0  # This should fail
```

## Oracle Selection Guide

**Choose Assertion-based when:**
- Expected output is easily computable
- Testing specific known scenarios
- Regression testing with saved examples

**Choose Property-based when:**
- Expected output is hard to compute but properties are clear
- Want to test many random inputs
- Testing invariants that should always hold

**Choose Differential when:**
- Refactoring or optimizing existing code
- Migrating to new implementation
- Reference implementation exists

**Choose Metamorphic when:**
- Expected output is unknown or hard to compute
- No reference implementation available
- Want to test complex transformations

## Tips

1. **Start simple**: Begin with assertion-based oracles, add others as needed
2. **Combine oracles**: Use multiple types for robust verification
3. **Test the tests**: Use mutation testing to validate oracle effectiveness
4. **Document assumptions**: Explain why properties should hold
5. **Handle floating point**: Use tolerance for float comparisons
6. **Consider performance**: Property-based tests run many iterations
7. **Focus on important properties**: Not every function needs all oracle types

## Common Patterns

For detailed oracle patterns organized by domain, see:
- [references/property_patterns.md](references/property_patterns.md) - Common property-based oracle patterns
- [references/metamorphic_patterns.md](references/metamorphic_patterns.md) - Metamorphic relation catalog
