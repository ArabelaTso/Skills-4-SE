# Property-Based Oracle Patterns

Catalog of common property patterns for generating property-based test oracles.

## Table of Contents

1. [Numeric Properties](#numeric-properties)
2. [Collection Properties](#collection-properties)
3. [String Properties](#string-properties)
4. [Relational Properties](#relational-properties)
5. [State Properties](#state-properties)

---

## Numeric Properties

### Range Properties

**Pattern**: Output must fall within specific bounds.

```python
@given(st.floats(min_value=0, max_value=1000))
def test_square_root_range(x):
    result = sqrt(x)
    assert 0 <= result <= x, "Square root should be between 0 and input"
```

```java
@Theory
public void squareRootRange(@ForAll @InRange(min="0", max="1000") double x) {
    double result = Math.sqrt(x);
    assertTrue(0 <= result && result <= x);
}
```

### Monotonicity

**Pattern**: As input increases, output increases (or decreases consistently).

```python
@given(st.floats(min_value=0, max_value=100))
def test_tax_monotonic(income):
    if income < 100:
        tax1 = calculate_tax(income)
        tax2 = calculate_tax(income + 1)
        assert tax2 >= tax1, "Tax should not decrease with higher income"
```

### Non-Negativity

**Pattern**: Output is never negative.

```python
@given(st.lists(st.integers()))
def test_count_non_negative(items):
    count = len(items)
    assert count >= 0, "Count should never be negative"
```

### Symmetry

**Pattern**: f(x, y) = f(y, x)

```python
@given(st.integers(), st.integers())
def test_addition_symmetry(a, b):
    assert add(a, b) == add(b, a), "Addition should be commutative"
```

---

## Collection Properties

### Length Preservation

**Pattern**: Operation preserves collection length.

```python
@given(st.lists(st.integers()))
def test_reverse_preserves_length(lst):
    reversed_lst = reverse(lst)
    assert len(reversed_lst) == len(lst), "Reverse should preserve length"
```

### Element Preservation

**Pattern**: All elements are preserved (no additions/deletions).

```python
@given(st.lists(st.integers()))
def test_sort_preserves_elements(lst):
    sorted_lst = sort(lst)
    assert sorted(lst) == sorted_lst, "Sort should preserve all elements"
    assert set(lst) == set(sorted_lst), "Same unique elements"
```

### Ordering Property

**Pattern**: Result is sorted/ordered correctly.

```python
@given(st.lists(st.integers()))
def test_sort_is_ordered(lst):
    sorted_lst = sort(lst)
    for i in range(len(sorted_lst) - 1):
        assert sorted_lst[i] <= sorted_lst[i + 1], "Should be in ascending order"
```

### Subset Property

**Pattern**: Result is subset of input or vice versa.

```python
@given(st.lists(st.integers()), st.integers())
def test_filter_is_subset(lst, threshold):
    filtered = filter_greater_than(lst, threshold)
    assert set(filtered).issubset(set(lst)), "Filtered list should be subset"
```

### Empty Input

**Pattern**: Empty input produces empty output (or specific default).

```python
@given(st.just([]))
def test_sort_empty_list(lst):
    assert sort(lst) == [], "Sorting empty list should return empty list"
```

---

## String Properties

### Length Bounds

**Pattern**: Output length relates to input length.

```python
@given(st.text())
def test_trim_length(text):
    trimmed = trim(text)
    assert len(trimmed) <= len(text), "Trim should not increase length"
```

### Character Preservation

**Pattern**: Same characters, possibly reordered.

```python
@given(st.text())
def test_reverse_preserves_chars(text):
    reversed_text = reverse(text)
    assert sorted(text) == sorted(reversed_text), "Same characters"
```

### Case Transformation

**Pattern**: Case change properties.

```python
@given(st.text())
def test_upper_idempotent(text):
    upper1 = text.upper()
    upper2 = upper1.upper()
    assert upper1 == upper2, "Upper is idempotent"
```

### Concatenation

**Pattern**: Parts combine to whole.

```python
@given(st.text(), st.text())
def test_concat_length(s1, s2):
    result = concat(s1, s2)
    assert len(result) == len(s1) + len(s2), "Concat length is sum"
```

---

## Relational Properties

### Idempotence

**Pattern**: f(f(x)) = f(x)

```python
@given(st.lists(st.integers()))
def test_sort_idempotent(lst):
    sorted_once = sort(lst)
    sorted_twice = sort(sorted_once)
    assert sorted_once == sorted_twice, "Sorting twice is same as once"
```

### Inverse

**Pattern**: f(g(x)) = x and g(f(x)) = x

```python
@given(st.text())
def test_encode_decode_inverse(text):
    encoded = encode(text)
    decoded = decode(encoded)
    assert decoded == text, "Decode should reverse encode"
```

### Consistency

**Pattern**: Multiple calls with same input produce same output.

```python
@given(st.integers())
def test_hash_consistent(value):
    hash1 = hash_function(value)
    hash2 = hash_function(value)
    assert hash1 == hash2, "Hash should be deterministic"
```

### Transitivity

**Pattern**: If a R b and b R c, then a R c.

```python
@given(st.lists(st.integers(), min_size=3))
def test_comparison_transitive(lst):
    a, b, c = lst[0], lst[1], lst[2]
    if a <= b and b <= c:
        assert a <= c, "Comparison should be transitive"
```

---

## State Properties

### Precondition-Postcondition

**Pattern**: State changes follow specific rules.

```python
@given(st.integers(min_value=0))
def test_withdraw_postcondition(initial_balance):
    account = Account(initial_balance)
    amount = min(10, initial_balance)
    account.withdraw(amount)
    assert account.balance == initial_balance - amount
```

### Invariants

**Pattern**: Certain properties always hold regardless of operations.

```python
@given(st.lists(st.integers()))
def test_stack_size_invariant(operations):
    stack = Stack()
    for op in operations:
        if op > 0:
            stack.push(op)
        elif not stack.is_empty():
            stack.pop()
        # Invariant: size should never be negative
        assert stack.size() >= 0
```

### Conservation

**Pattern**: Total quantity is conserved.

```python
@given(st.integers(min_value=0), st.integers(min_value=0))
def test_transfer_conservation(amount1, amount2):
    total_before = amount1 + amount2
    # Transfer some money
    transfer_amount = min(amount1, 10)
    amount1 -= transfer_amount
    amount2 += transfer_amount
    total_after = amount1 + amount2
    assert total_before == total_after, "Total should be conserved"
```

---

## Domain-Specific Patterns

### Mathematical Functions

```python
# Commutativity
@given(st.floats(), st.floats())
def test_multiply_commutative(a, b):
    assert multiply(a, b) == multiply(b, a)

# Associativity
@given(st.floats(), st.floats(), st.floats())
def test_add_associative(a, b, c):
    assert add(add(a, b), c) == add(a, add(b, c))

# Identity element
@given(st.floats())
def test_multiply_identity(a):
    assert multiply(a, 1) == a
```

### Data Transformations

```python
# Serialization/Deserialization
@given(st.dictionaries(st.text(), st.integers()))
def test_json_roundtrip(data):
    serialized = to_json(data)
    deserialized = from_json(serialized)
    assert deserialized == data

# Encoding/Decoding
@given(st.binary())
def test_base64_roundtrip(data):
    encoded = base64_encode(data)
    decoded = base64_decode(encoded)
    assert decoded == data
```

### Business Logic

```python
# Discount never exceeds price
@given(st.floats(min_value=0), st.floats(min_value=0, max_value=1))
def test_discount_bounds(price, discount_rate):
    discounted = apply_discount(price, discount_rate)
    assert 0 <= discounted <= price

# Quantity constraints
@given(st.integers(min_value=0))
def test_inventory_non_negative(initial_stock):
    inventory = Inventory(initial_stock)
    sold = min(initial_stock, 5)
    inventory.sell(sold)
    assert inventory.stock >= 0
```

---

## Tips for Identifying Properties

Ask these questions:

1. **What can I say about the output without computing it?**
   - Range, bounds, constraints

2. **How does output relate to input?**
   - Length, size, elements, ordering

3. **What should never happen?**
   - Negative values, null results, exceptions

4. **What operations are reversible?**
   - Encode/decode, compress/decompress

5. **What operations don't change the result?**
   - Idempotent operations

6. **What should be preserved?**
   - Total count, sum, unique elements

7. **What relationships hold between multiple calls?**
   - Consistency, commutativity, associativity
