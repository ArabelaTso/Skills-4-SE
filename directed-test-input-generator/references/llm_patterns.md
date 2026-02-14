# LLM-Driven Test Input Generation Patterns

## Overview

LLM-driven generation leverages the language model's understanding of code semantics, naming conventions, and domain knowledge to generate contextually meaningful test inputs. Unlike random fuzzing, LLM-driven generation produces inputs that make semantic sense for the code being tested.

## Pattern 1: Semantic Input Generation

Use LLM to understand parameter semantics from names and generate appropriate values.

### Example Prompt Template

```
Analyze this function and generate test inputs:

```python
{function_source_code}
```

For each parameter, determine:
1. Expected type and format
2. Valid value ranges
3. Edge cases specific to the parameter's semantic meaning

Generate 5 diverse test cases covering:
- Typical valid inputs
- Boundary values
- Invalid inputs that should trigger errors
- Edge cases based on parameter semantics

Format as Python dictionary.
```

### Sample Response

For a function:
```python
def book_flight(passenger_age, departure_date, destination_country, is_premium):
    # ... booking logic
```

LLM generates:
```python
test_cases = [
    # Typical case
    {
        "passenger_age": 35,
        "departure_date": "2026-06-15",
        "destination_country": "US",
        "is_premium": False
    },
    # Child passenger
    {
        "passenger_age": 8,
        "departure_date": "2026-07-01",
        "destination_country": "UK",
        "is_premium": False
    },
    # Senior citizen
    {
        "passenger_age": 72,
        "departure_date": "2026-08-10",
        "destination_country": "CA",
        "is_premium": True
    },
    # Infant (edge case)
    {
        "passenger_age": 1,
        "departure_date": "2026-05-20",
        "destination_country": "FR",
        "is_premium": False
    },
    # Invalid age (should error)
    {
        "passenger_age": -5,
        "departure_date": "2026-06-01",
        "destination_country": "DE",
        "is_premium": False
    }
]
```

## Pattern 2: Path-Directed Input Generation

Provide LLM with path constraints and ask it to generate inputs that satisfy those constraints.

### Example Prompt Template

```
I need test inputs to reach this specific code path:

Target path conditions:
{path_conditions}

Function to test:
```python
{function_source_code}
```

Generate input values that will:
1. Satisfy all the path conditions
2. Be realistic/meaningful values (not just arbitrary numbers)

Explain your reasoning and provide the test input as a dictionary.
```

### Sample Usage

For path conditions:
```
age > 65 AND is_premium == True AND country == "US"
```

LLM generates:
```python
{
    "age": 70,  # Senior citizen (> 65)
    "is_premium": True,  # Premium membership
    "country": "US"  # United States
}

# Reasoning: Generated age 70 as a realistic senior citizen age,
# rather than edge value like 66. This tests the business logic
# path for premium US senior citizens.
```

## Pattern 3: Constraint-Aware Mutation

Use LLM to mutate existing inputs while maintaining semantic validity.

### Example Prompt Template

```
Given this test input:
{current_input}

And these path constraints that are NOT yet covered:
{uncovered_constraints}

Suggest mutations to the input that:
1. Might help cover the uncovered constraints
2. Maintain semantic validity
3. Are realistic test scenarios

Provide 3 mutation suggestions with reasoning.
```

### Sample Response

Current input:
```python
{"age": 30, "is_premium": False, "country": "UK"}
```

Uncovered constraint: `age < 18`

LLM suggests:
```python
mutations = [
    {
        "age": 16,
        "is_premium": False,
        "country": "UK",
        "reasoning": "Test teenage passenger scenario"
    },
    {
        "age": 10,
        "is_premium": True,
        "country": "US",
        "reasoning": "Test premium child passenger"
    },
    {
        "age": 0,
        "is_premium": False,
        "country": "CA",
        "reasoning": "Test infant (boundary case)"
    }
]
```

## Pattern 4: Domain Knowledge Integration

Use LLM's domain knowledge to generate realistic test scenarios.

### Example Prompt Template

```
Generate test inputs for this function that test realistic edge cases
based on domain knowledge:

```python
{function_source_code}
```

Consider:
- Common real-world scenarios
- Typical edge cases in this domain
- Invalid inputs users might actually provide
- Business rule violations

Generate 5 test cases with descriptions.
```

### Sample Response

For payment processing function:
```python
def process_payment(amount, currency, card_number, cvv):
    # ... payment logic
```

LLM generates:
```python
test_cases = [
    {
        "description": "Micro-transaction (common mobile payment)",
        "amount": 0.99,
        "currency": "USD",
        "card_number": "4111111111111111",
        "cvv": "123"
    },
    {
        "description": "Large purchase (fraud detection trigger)",
        "amount": 9999.99,
        "currency": "USD",
        "card_number": "5500000000000004",
        "cvv": "456"
    },
    {
        "description": "International currency",
        "amount": 50.00,
        "currency": "EUR",
        "card_number": "340000000000009",
        "cvv": "789"
    },
    {
        "description": "Invalid CVV (common user error)",
        "amount": 25.00,
        "currency": "USD",
        "card_number": "4111111111111111",
        "cvv": "12"  # Too short
    },
    {
        "description": "Zero amount (edge case)",
        "amount": 0.00,
        "currency": "USD",
        "card_number": "4111111111111111",
        "cvv": "123"
    }
]
```

## Pattern 5: Multi-Step Scenario Generation

Generate complex test scenarios involving multiple function calls.

### Example Prompt Template

```
Create a test scenario that exercises this sequence of operations:

Functions:
```python
{function_1_source}
{function_2_source}
{function_3_source}
```

Target behavior: {target_behavior_description}

Generate:
1. Initial state/inputs
2. Sequence of function calls
3. Expected state transitions
4. Final expected outcome
```

### Sample Response

Target: Test shopping cart checkout flow

```python
scenario = {
    "description": "Premium user checkout with discount",
    "steps": [
        {
            "function": "create_cart",
            "inputs": {"user_id": 123, "is_premium": True},
            "expected_state": {"cart_id": 1, "items": [], "total": 0}
        },
        {
            "function": "add_item",
            "inputs": {"cart_id": 1, "product_id": 5, "quantity": 2},
            "expected_state": {"cart_id": 1, "items": [{"product_id": 5, "quantity": 2}], "total": 50.00}
        },
        {
            "function": "apply_discount",
            "inputs": {"cart_id": 1, "code": "PREMIUM10"},
            "expected_state": {"total": 45.00, "discount_applied": "PREMIUM10"}
        },
        {
            "function": "checkout",
            "inputs": {"cart_id": 1, "payment_method": "credit_card"},
            "expected_outcome": {"status": "success", "order_id": 456, "amount_charged": 45.00}
        }
    ]
}
```

## Pattern 6: Adversarial Input Generation

Use LLM to generate inputs designed to break the code or find bugs.

### Example Prompt Template

```
Act as a security tester. Generate adversarial test inputs for this function
that might expose bugs or vulnerabilities:

```python
{function_source_code}
```

Generate inputs that test:
1. Type confusion
2. Boundary violations
3. Injection attacks
4. Resource exhaustion
5. Logic errors

Provide 5 adversarial test cases.
```

### Sample Response

For user validation function:
```python
adversarial_tests = [
    {
        "description": "SQL injection attempt",
        "username": "admin' OR '1'='1",
        "email": "test@test.com"
    },
    {
        "description": "XSS attempt",
        "username": "<script>alert('xss')</script>",
        "email": "malicious@evil.com"
    },
    {
        "description": "Extremely long input (DoS)",
        "username": "A" * 1000000,
        "email": "test@example.com"
    },
    {
        "description": "Unicode edge cases",
        "username": "𝓤𝓷𝓲𝓬𝓸𝓭𝓮",
        "email": "unicode@例え.jp"
    },
    {
        "description": "Null byte injection",
        "username": "admin\x00hidden",
        "email": "test\x00@fake.com"
    }
]
```

## Pattern 7: Property-Based Test Generation

Use LLM to identify invariants and generate property-based tests.

### Example Prompt Template

```
Analyze this function and identify invariants/properties that should always hold:

```python
{function_source_code}
```

Then generate test inputs that verify these properties across diverse inputs.
```

### Sample Response

For sorting function:
```python
properties = {
    "invariant_1": {
        "description": "Output length equals input length",
        "test_inputs": [
            [],
            [1],
            [3, 1, 2],
            list(range(100)),
            [1] * 50
        ]
    },
    "invariant_2": {
        "description": "Output is sorted in ascending order",
        "test_inputs": [
            [5, 2, 8, 1, 9],
            [-3, -1, -5],
            [1.5, 1.1, 1.9],
            ["c", "a", "b"]
        ]
    },
    "invariant_3": {
        "description": "Output contains same elements as input",
        "test_inputs": [
            [1, 2, 2, 3],
            [5, 5, 5],
            ["a", "b", "a"]
        ]
    }
}
```

## Implementation Helpers

### LLM Query Helper

```python
def query_llm_for_inputs(function_source, path_constraints, strategy="semantic"):
    """
    Query LLM to generate test inputs.

    Args:
        function_source: Source code of function to test
        path_constraints: Constraints for target path
        strategy: Generation strategy (semantic, adversarial, etc.)

    Returns:
        List of generated test inputs
    """
    prompts = {
        "semantic": semantic_generation_prompt,
        "path_directed": path_directed_prompt,
        "adversarial": adversarial_prompt,
        "property_based": property_based_prompt
    }

    prompt = prompts[strategy](function_source, path_constraints)

    # Call LLM API (pseudocode)
    response = call_llm_api(prompt)

    # Parse response to extract test inputs
    test_inputs = parse_llm_response(response)

    return test_inputs
```

### Response Parser

```python
import json
import re

def parse_llm_response(response_text):
    """
    Parse LLM response to extract test inputs.

    Handles various formats:
    - Python dict/list literals
    - JSON
    - Markdown code blocks
    """
    # Try to extract code block
    code_block_match = re.search(r'```python\s*(.*?)\s*```', response_text, re.DOTALL)
    if code_block_match:
        code = code_block_match.group(1)
        # Evaluate safely (consider using ast.literal_eval for safety)
        try:
            return eval(code)
        except:
            pass

    # Try JSON parsing
    json_match = re.search(r'\{.*\}|\[.*\]', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except:
            pass

    return None
```

## Best Practices

### 1. Validate LLM-Generated Inputs
Always validate that LLM-generated inputs are syntactically valid:
```python
def validate_inputs(inputs, function_signature):
    """Ensure generated inputs match function signature."""
    required_params = extract_parameters(function_signature)

    for param in required_params:
        if param not in inputs:
            raise ValueError(f"Missing parameter: {param}")

    return True
```

### 2. Combine with Traditional Methods
Use LLM generation alongside traditional techniques:
```python
def hybrid_generation(function):
    # LLM generates semantically meaningful inputs
    llm_inputs = query_llm_for_inputs(function)

    # Traditional fuzzer generates edge cases
    fuzzer_inputs = generate_edge_cases(function)

    # Combine both
    return llm_inputs + fuzzer_inputs
```

### 3. Iterate Based on Coverage
Use coverage feedback to refine LLM prompts:
```python
def iterative_llm_generation(function, max_iterations=5):
    all_inputs = []
    covered_paths = set()

    for i in range(max_iterations):
        # Ask LLM to target uncovered paths
        uncovered = get_uncovered_paths(function, covered_paths)
        new_inputs = query_llm_for_inputs(function, uncovered)

        # Measure coverage
        coverage = execute_with_coverage(function, new_inputs)
        covered_paths.update(coverage)

        all_inputs.extend(new_inputs)

    return all_inputs
```
