# Metamorphic Relation Patterns

Catalog of metamorphic relations for generating metamorphic test oracles.

## What Are Metamorphic Relations?

Metamorphic relations describe how changes to input should predictably change the output, without needing to know the exact expected output. Format: "If input changes in way X, output should change in way Y."

---

## Table of Contents

1. [Arithmetic Relations](#arithmetic-relations)
2. [Collection Relations](#collection-relations)
3. [Transformation Relations](#transformation-relations)
4. [Equivalence Relations](#equivalence-relations)
5. [Domain-Specific Relations](#domain-specific-relations)

---

## Arithmetic Relations

### Additive Relation

**Pattern**: f(x + k) = f(x) + k or similar additive relationship.

```python
def test_temperature_conversion_additive():
    """Adding to Celsius adds proportionally to Fahrenheit."""
    temp_c = 0
    f1 = celsius_to_fahrenheit(temp_c)
    f2 = celsius_to_fahrenheit(temp_c + 10)

    # 10°C increase = 18°F increase
    assert abs((f2 - f1) - 18) < 0.01
```

### Multiplicative Relation

**Pattern**: f(k × x) = k × f(x)

```python
def test_area_scaling():
    """Doubling dimensions quadruples area."""
    radius = 5
    area1 = circle_area(radius)
    area2 = circle_area(radius * 2)

    assert abs(area2 - 4 * area1) < 0.01
```

### Distributive Relation

**Pattern**: f(x) + f(y) = f(x + y)

```python
def test_discount_distributive():
    """Total discount equals sum of individual discounts."""
    items = [100, 50, 30]
    discount_rate = 0.1

    # Method 1: Discount total
    total = sum(items)
    discount1 = apply_discount(total, discount_rate)

    # Method 2: Sum of discounts
    discount2 = sum(apply_discount(item, discount_rate) for item in items)

    assert abs(discount1 - discount2) < 0.01
```

### Inverse Relation

**Pattern**: f(1/x) = 1/f(x) or f(-x) = -f(x)

```python
def test_reciprocal_relation():
    """Reciprocal of input gives reciprocal of output."""
    x = 5
    f_x = some_function(x)
    f_inv_x = some_function(1/x)

    assert abs(f_inv_x - 1/f_x) < 0.01
```

---

## Collection Relations

### Permutation Invariance

**Pattern**: f(permute(x)) = f(x) - order doesn't matter.

```python
def test_sum_permutation_invariant():
    """Sum is same regardless of order."""
    lst = [1, 2, 3, 4, 5]
    shuffled = [3, 1, 5, 2, 4]

    assert sum_list(lst) == sum_list(shuffled)

def test_sort_permutation_invariant():
    """Sorting any permutation gives same result."""
    lst = [3, 1, 4, 1, 5, 9]
    reversed_lst = list(reversed(lst))

    assert sort(lst) == sort(reversed_lst)
```

### Subset Relation

**Pattern**: f(subset(x)) ⊆ f(x)

```python
def test_search_subset():
    """Searching in subset yields subset of full results."""
    full_data = [1, 2, 3, 4, 5, 6, 7, 8]
    subset_data = [1, 2, 3, 4]
    query = lambda x: x > 2

    full_results = search(full_data, query)
    subset_results = search(subset_data, query)

    assert set(subset_results).issubset(set(full_results))
```

### Duplication Relation

**Pattern**: f(x + x) relates predictably to f(x).

```python
def test_sort_duplication():
    """Sorting duplicated list gives sorted original, doubled."""
    lst = [3, 1, 4]
    duplicated = lst + lst

    result = sort(duplicated)
    expected = sort(lst) + sort(lst)

    assert result == expected
```

### Concatenation Relation

**Pattern**: f(x + y) relates to f(x) and f(y).

```python
def test_max_concatenation():
    """Max of concatenated lists is max of individual maxes."""
    list1 = [1, 3, 5]
    list2 = [2, 4, 6]

    max_combined = max_value(list1 + list2)
    max_individuals = max(max_value(list1), max_value(list2))

    assert max_combined == max_individuals
```

---

## Transformation Relations

### Reversal Relation

**Pattern**: Certain operations are unchanged by reversal.

```python
def test_palindrome_reversal():
    """Palindrome check same after reversal."""
    text = "racecar"
    reversed_text = text[::-1]

    assert is_palindrome(text) == is_palindrome(reversed_text)

def test_max_reversal():
    """Max is same after reversing."""
    lst = [1, 3, 5, 2, 4]
    reversed_lst = list(reversed(lst))

    assert max_value(lst) == max_value(reversed_lst)
```

### Negation Relation

**Pattern**: f(-x) = -f(x) or similar negation relationship.

```python
def test_average_negation():
    """Average of negated values is negation of average."""
    values = [10, 20, 30, 40]
    negated = [-v for v in values]

    assert abs(average(negated) - (-average(values))) < 0.01
```

### Case Transformation

**Pattern**: Case changes don't affect certain operations.

```python
def test_search_case_insensitive():
    """Case change in query preserves result count."""
    data = ["Apple", "Banana", "apricot"]

    results_lower = search(data, "app")
    results_upper = search(data, "APP")

    assert len(results_lower) == len(results_upper)
```

---

## Equivalence Relations

### Alternative Paths

**Pattern**: Different ways to compute should give same result.

```python
def test_power_alternative_paths():
    """x^4 via (x^2)^2 equals x^4 directly."""
    x = 7

    # Path 1: Direct
    result1 = power(x, 4)

    # Path 2: Via intermediate
    intermediate = power(x, 2)
    result2 = power(intermediate, 2)

    assert result1 == result2
```

### Associativity

**Pattern**: (a op b) op c = a op (b op c)

```python
def test_string_concat_associative():
    """Concatenation order doesn't matter."""
    s1, s2, s3 = "hello", " ", "world"

    result1 = concat(concat(s1, s2), s3)
    result2 = concat(s1, concat(s2, s3))

    assert result1 == result2
```

### Commutativity

**Pattern**: f(x, y) = f(y, x)

```python
def test_intersection_commutative():
    """Set intersection is commutative."""
    set1 = {1, 2, 3, 4}
    set2 = {3, 4, 5, 6}

    assert intersection(set1, set2) == intersection(set2, set1)
```

---

## Domain-Specific Relations

### Image Processing

```python
def test_brightness_additive():
    """Increasing brightness twice equals one large increase."""
    image = load_image("test.jpg")

    # Two small increases
    result1 = increase_brightness(image, 10)
    result1 = increase_brightness(result1, 10)

    # One large increase
    result2 = increase_brightness(image, 20)

    assert images_similar(result1, result2, tolerance=0.01)

def test_rotation_additive():
    """Rotating 90° four times equals 360°."""
    image = load_image("test.jpg")

    rotated = image
    for _ in range(4):
        rotated = rotate(rotated, 90)

    assert images_equal(rotated, image)
```

### Search and Retrieval

```python
def test_search_query_expansion():
    """More specific query yields subset of general query."""
    general_query = "python"
    specific_query = "python tutorial"

    general_results = search(general_query)
    specific_results = search(specific_query)

    assert len(specific_results) <= len(general_results)

def test_filter_composition():
    """Applying two filters equals applying combined filter."""
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Two separate filters
    result1 = filter_even(data)
    result1 = filter_greater_than(result1, 5)

    # Combined filter
    result2 = filter_even_and_greater_than(data, 5)

    assert result1 == result2
```

### Mathematical Functions

```python
def test_sin_periodicity():
    """sin(x) = sin(x + 2π)"""
    import math
    x = 1.5

    sin1 = math.sin(x)
    sin2 = math.sin(x + 2 * math.pi)

    assert abs(sin1 - sin2) < 0.0001

def test_log_product():
    """log(a * b) = log(a) + log(b)"""
    import math
    a, b = 10, 20

    log_product = math.log(a * b)
    sum_logs = math.log(a) + math.log(b)

    assert abs(log_product - sum_logs) < 0.0001
```

### Data Structures

```python
def test_stack_push_pop():
    """Pushing then popping returns original state."""
    stack = Stack([1, 2, 3])
    original_size = stack.size()

    stack.push(4)
    stack.pop()

    assert stack.size() == original_size

def test_tree_traversal():
    """Inorder of BST gives sorted result."""
    tree = BST([3, 1, 4, 1, 5, 9, 2, 6])

    inorder = tree.inorder_traversal()
    sorted_values = sorted([3, 1, 4, 1, 5, 9, 2, 6])

    assert inorder == sorted_values
```

### Compiler/Interpreter

```python
def test_optimization_equivalence():
    """Optimized code produces same output as unoptimized."""
    source_code = "x = 1 + 2 + 3"

    result_unopt = execute(source_code, optimize=False)
    result_opt = execute(source_code, optimize=True)

    assert result_unopt == result_opt

def test_constant_folding():
    """Precomputed constants give same result."""
    # Original
    result1 = evaluate("2 + 3 * 4")

    # With constant folding
    result2 = evaluate("2 + 12")  # 3*4 precomputed

    assert result1 == result2
```

---

## Identifying Metamorphic Relations

### Questions to Ask

1. **What happens if I apply the operation twice?**
   - Idempotence, accumulation, cycling

2. **What happens if I reverse/negate/invert the input?**
   - Symmetry, inverse relations

3. **What if I change the order of elements?**
   - Permutation invariance, commutativity

4. **What if I split or combine inputs?**
   - Distributive, additive properties

5. **What if I scale the input?**
   - Multiplicative relations, proportionality

6. **Are there alternative ways to compute the same thing?**
   - Equivalent paths, different algorithms

7. **What if I add/remove a subset?**
   - Subset relations, incremental changes

### Common Patterns Summary

| Pattern | Relation | Example |
|---------|----------|---------|
| Additive | f(x+k) relates to f(x) | Temperature conversion |
| Multiplicative | f(k×x) = k×f(x) | Area scaling |
| Permutation | f(permute(x)) = f(x) | Sum, max invariant to order |
| Subset | f(subset(x)) ⊆ f(x) | Search results |
| Inverse | f(f⁻¹(x)) = x | Encode/decode |
| Idempotent | f(f(x)) = f(x) | Sorting, normalization |
| Commutative | f(x,y) = f(y,x) | Symmetric operations |
| Associative | f(f(a,b),c) = f(a,f(b,c)) | Concatenation |
| Distributive | f(x)+f(y) = f(x+y) | Linear operations |
| Negation | f(-x) = -f(x) | Odd functions |

---

## Tips for Creating Metamorphic Tests

1. **Start with mathematical properties**: They often have well-known relations
2. **Think about data transformations**: Encode/decode, compress/decompress
3. **Consider user workflows**: Different paths to same goal
4. **Look for symmetries**: Operations that preserve certain qualities
5. **Test with follow-up operations**: What happens after the first operation?
6. **Combine simple relations**: Build complex relations from simpler ones
