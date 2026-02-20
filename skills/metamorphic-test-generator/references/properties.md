# Metamorphic Properties Reference

## Overview

Metamorphic properties define relationships between inputs and outputs that should hold when transformations are applied. This guide explains built-in properties and how to define custom ones.

## Built-in Properties

### Permutation Property

**Concept**: Reordering inputs should not affect the output (or produce equivalent output).

**Use cases**: Sorting algorithms, set operations, commutative operations

**Example**:
- Input: `[3, 1, 2]` → Output: `[1, 2, 3]`
- Transformed: `[2, 3, 1]` → Output: `[1, 2, 3]`
- Relation: Outputs should be equal

### Addition Property

**Concept**: Adding elements should increase or maintain the result.

**Use cases**: Counting, aggregation, accumulation operations

**Example**:
- Input: `[1, 2, 3]` → Output: `6`
- Transformed: `[1, 2, 3, 1]` → Output: `7`
- Relation: `transformed_output >= original_output`

### Multiplication Property

**Concept**: Scaling inputs should scale outputs proportionally.

**Use cases**: Linear transformations, scaling operations, mathematical functions

**Example**:
- Input: `5` → Output: `10`
- Transformed: `10` (×2) → Output: `20` (×2)
- Relation: `transformed_output = original_output × factor`

### Inverse Property

**Concept**: Applying an inverse operation should return to the original state.

**Use cases**: Reversible operations, encoding/decoding, encryption/decryption

**Example**:
- Input: `[1, 2, 3]` → Output: `[3, 2, 1]`
- Transformed: `[3, 2, 1]` → Output: `[1, 2, 3]`
- Relation: Applying inverse twice returns original

### Monotonicity Property

**Concept**: Increasing input should not decrease output.

**Use cases**: Monotonic functions, ranking, scoring systems

**Example**:
- Input: `5` → Output: `25`
- Transformed: `6` → Output: `36`
- Relation: `transformed_output >= original_output`

### Equivalence Property

**Concept**: Different representations should yield the same result.

**Use cases**: Format conversions, normalization, equivalent inputs

**Example**:
- Input: `"hello"` → Output: `5`
- Transformed: `"hello "` (with trailing space) → Output: `5`
- Relation: Outputs should be equal

## Property Definition Format

When using a JSON file to define properties, use this format:

```json
{
  "properties": [
    "permutation",
    "addition",
    "inverse"
  ]
}
```

Or with parameters:

```json
{
  "properties": [
    {
      "name": "multiplication",
      "factor": 3.0
    },
    {
      "name": "permutation"
    }
  ]
}
```

## Selecting Properties

Choose properties based on program semantics:

1. **Identify invariants**: What relationships should always hold?
2. **Consider domain**: What transformations make sense for your domain?
3. **Start simple**: Begin with permutation and addition
4. **Iterate**: Add more complex properties as needed

## Property Violations

Violations indicate potential bugs:

- **Consistent violations**: Likely a real bug in the program
- **Occasional violations**: May indicate edge cases or floating-point issues
- **All violations**: Property may not apply to this program

## Custom Properties

To add custom properties, extend the `MetamorphicProperty` class in `generate.py`:

```python
class CustomProperty(MetamorphicProperty):
    def __init__(self):
        super().__init__("custom")

    def transform_input(self, input_data: Any) -> Any:
        # Define how to transform the input
        return transformed_input

    def verify_output(self, original_output: Any, transformed_output: Any,
                     original_input: Any, transformed_input: Any) -> Tuple[bool, str]:
        # Define the metamorphic relation
        is_valid = check_relation(original_output, transformed_output)
        message = "Description of the relation"
        return is_valid, message
```

## Tips

- Properties should be **deterministic** and **verifiable**
- Start with **domain-independent** properties (permutation, addition)
- Add **domain-specific** properties based on program semantics
- Document properties for future test maintenance
- Combine multiple properties for better coverage
