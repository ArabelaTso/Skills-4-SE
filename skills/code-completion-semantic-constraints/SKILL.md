---
name: code-completion-semantic-constraints
description: Automatically complete partial code snippets while satisfying semantic constraints including variable types, invariants, pre/post-conditions, interface contracts, and expected input/output behavior. Use when users provide incomplete code with specific requirements like "complete this function that takes a list and returns sorted unique elements" or "fill in this method body that must maintain the invariant that x stays positive" or "implement this interface method with these type constraints." Produces compilable, executable code with tests and a constraint satisfaction report.
---

# Code Completion with Semantic Constraints

## Overview

Complete partial code snippets while satisfying specified semantic constraints. Produces compilable code, verification tests, and a detailed report explaining how each constraint was satisfied.

## Workflow

### 1. Parse Input

Extract and categorize the provided information:

**Partial Code**: Identify the incomplete code structure (function signature, class skeleton, method stub, etc.)

**Semantic Constraints**: Categorize constraints by type:
- **Type constraints**: Variable types, return types, generic bounds
- **Invariants**: Pre-conditions, post-conditions, loop invariants
- **Behavioral constraints**: Expected input/output pairs, edge case handling
- **Interface contracts**: Method signatures, protocol conformance
- **Performance constraints**: Time/space complexity requirements

### 2. Analyze Constraints

For each constraint:
- Determine if it's satisfiable
- Identify dependencies between constraints
- Note any conflicts or ambiguities
- If constraints are unclear or conflicting, ask for clarification before proceeding

### 3. Complete the Code

Generate code that:
- Compiles without errors in the target language
- Satisfies all specified constraints
- Follows language idioms and best practices
- Includes necessary imports, type annotations, and error handling
- Uses minimal complexity (avoid over-engineering)

### 4. Generate Verification Tests

Create minimal test cases that verify:
- Type constraints are respected
- Pre-conditions and post-conditions hold
- Expected input/output behavior is correct
- Edge cases are handled properly
- Performance constraints are met (if specified)

### 5. Produce Constraint Satisfaction Report

Document how each constraint was satisfied:
- Map each constraint to the code that satisfies it
- Explain the reasoning for implementation choices
- Note any assumptions made
- Highlight any constraints that required trade-offs

## Examples

### Example 1: Type and Behavioral Constraints

**Input:**
```python
def process_items(items):
    # TODO: complete this function
    pass
```

**Constraints:**
- `items` is a list of integers
- Return a list of unique integers in ascending order
- Handle empty list (return empty list)
- Time complexity: O(n log n)

**Output:** Completed function with sorting logic, tests for empty/normal/duplicate cases, and report explaining constraint satisfaction.

### Example 2: Interface Contract

**Input:**
```java
public class DataCache implements Cache {
    // TODO: implement required methods
}
```

**Constraints:**
- Implement `Cache` interface (get, put, remove methods)
- Thread-safe operations
- LRU eviction policy with max size 100
- Return null for missing keys

**Output:** Complete class implementation, concurrency tests, and report mapping each interface method to implementation.

### Example 3: Invariant Preservation

**Input:**
```c
void update_balance(Account* acc, int amount) {
    // TODO: complete
}
```

**Constraints:**
- Pre-condition: `acc != NULL && acc->balance >= 0`
- Post-condition: `acc->balance >= 0` (balance never negative)
- If `amount` would make balance negative, set to 0 instead

**Output:** Implementation with bounds checking, tests for edge cases, and report showing invariant preservation.

## Output Format

Provide three components:

**1. Completed Code**
- Fully compilable and executable
- Includes necessary imports, type annotations, error handling
- Follows language conventions

**2. Verification Tests**
- Minimal test suite covering constraint verification
- Include edge cases and boundary conditions
- Use appropriate testing framework for the language

**3. Constraint Satisfaction Report**
- Table or list mapping each constraint to implementation details
- Explanation of design choices
- Any assumptions or trade-offs made

## Language Support

This skill works with any programming language. Adapt constraint types and verification approaches to language-specific features (e.g., type systems, contract programming, assertion libraries).
