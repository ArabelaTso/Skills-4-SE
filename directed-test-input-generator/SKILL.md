---
name: directed-test-input-generator
description: "Generate targeted test inputs to reach specific code paths and hard-to-reach behaviors in Python code. Use when: (1) Targeting uncovered branches or specific execution paths, (2) Need coverage-guided test generation, (3) Want to leverage LLM understanding of code semantics for meaningful test inputs, (4) Testing boundary conditions and edge cases systematically, (5) Combining symbolic reasoning with fuzzing. Provides path analysis, constraint solving, coverage-guided strategies, and LLM-driven semantic generation for comprehensive test input creation."
---

# Directed Test Input Generator

Generate test inputs that target specific code paths and hard-to-reach behaviors using program analysis, coverage feedback, and LLM-driven semantic understanding.

## Overview

Directed test input generation combines multiple techniques to create test inputs that explore specific execution paths:

1. **Path Analysis**: Extract control flow paths and their constraints
2. **Constraint Solving**: Generate inputs satisfying path conditions
3. **Coverage Guidance**: Use coverage feedback to iteratively reach new paths
4. **LLM Semantic Understanding**: Leverage code understanding for meaningful inputs

## Quick Start

### Basic Workflow

```python
# 1. Analyze code to extract paths
from scripts.path_analyzer import analyze_code_paths

paths = analyze_code_paths(source_code)

# 2. Generate inputs for each path
from scripts.input_generator import generate_test_suite

test_suite = generate_test_suite(paths)

# 3. Execute tests and measure coverage
for path_id, test_data in test_suite.items():
    result = execute_test(function, test_data['inputs'])
    verify_coverage(result, test_data['target_line'])
```

## Core Techniques

### 1. Path Analysis and Extraction

Extract execution paths and their constraints from code:

```python
from scripts.path_analyzer import analyze_code_paths, print_paths

source = """
def validate_age(age, country):
    if age < 0:
        raise ValueError("Invalid age")
    if age < 18:
        return "minor"
    if age >= 65 and country == "US":
        return "senior_us"
    return "adult"
"""

paths = analyze_code_paths(source)
print_paths(paths)

# Output:
# Path #0: exception handler (ValueError) (line 3)
#   Conditions:
#     - age < 0
#
# Path #1: if branch (line 5)
#   Conditions:
#     - age >= 0
#     - age < 18
#
# Path #2: if branch (line 7)
#   Conditions:
#     - age >= 0
#     - age >= 18
#     - age >= 65
#     - country == US
```

### 2. Constraint-Based Input Generation

Generate inputs that satisfy specific path constraints:

```python
from scripts.input_generator import TestInputGenerator

generator = TestInputGenerator()

# Generate input for path: age >= 65 AND country == "US"
constraints = {
    "age": ["age >= 65"],
    "country": ["country == US"]
}

inputs = generator.generate_for_path(constraints)
# Result: {"age": 65, "country": "US"}
```

### 3. Edge Case Generation

Generate boundary values systematically:

```python
from scripts.input_generator import EdgeCaseGenerator

# Generate edge cases for integer type
edge_cases = EdgeCaseGenerator.generate_edge_cases(int)
# [0, -1, 1, -2147483648, 2147483647, ...]

# Generate boundary values around a threshold
boundaries = EdgeCaseGenerator.generate_boundary_values(">", 65)
# [64, 65, 66, 67] - values around the boundary
```

### 4. Coverage-Guided Generation

Iteratively generate inputs to maximize coverage:

```python
def coverage_guided_testing(function, max_iterations=100):
    """
    Generate test inputs guided by coverage feedback.
    """
    covered_lines = set()
    test_corpus = []

    # Start with initial inputs
    current_inputs = generate_seed_inputs(function)

    for i in range(max_iterations):
        # Execute and measure coverage
        new_coverage = execute_with_coverage(function, current_inputs)

        if new_coverage - covered_lines:
            # New coverage reached - save inputs
            test_corpus.append(current_inputs)
            covered_lines.update(new_coverage)

        # Mutate inputs to explore new paths
        current_inputs = mutate_toward_uncovered(current_inputs, covered_lines)

    return test_corpus
```

See **[coverage_strategies.md](references/coverage_strategies.md)** for detailed coverage-guided strategies.

### 5. LLM-Driven Semantic Generation

Use LLM understanding of code semantics to generate meaningful inputs:

```python
# Example: LLM generates semantically appropriate inputs
function_code = """
def book_flight(passenger_age, departure_date, destination_country):
    # ... booking logic
"""

# LLM understands parameter semantics and generates realistic inputs:
llm_generated = [
    {
        "passenger_age": 35,           # Adult
        "departure_date": "2026-06-15",  # Future date
        "destination_country": "US"      # Valid country code
    },
    {
        "passenger_age": 8,            # Child passenger
        "departure_date": "2026-07-20",
        "destination_country": "UK"
    },
    {
        "passenger_age": 72,           # Senior citizen
        "departure_date": "2026-08-10",
        "destination_country": "CA"
    }
]
```

See **[llm_patterns.md](references/llm_patterns.md)** for comprehensive LLM-driven generation patterns.

## Common Use Cases

### Use Case 1: Target Specific Branch

Generate input to reach an uncovered branch:

```python
# Target: age > 100 branch
def check_age(age):
    if age > 100:
        return "exceptionally_old"  # Want to test this
    return "normal"

# Analyze paths
paths = analyze_code_paths(check_age_source)
target_path = paths[0]  # age > 100 path

# Generate input
generator = TestInputGenerator()
constraints = target_path.get_constraints()
test_input = generator.generate_for_path(constraints)
# Result: {"age": 101}

# Test
assert check_age(**test_input) == "exceptionally_old"
```

### Use Case 2: Systematic Boundary Testing

Test all boundaries in a function:

```python
def calculate_discount(age, is_premium):
    if age < 18:
        return 0.0
    elif age < 65:
        return 0.1 if is_premium else 0.05
    else:
        return 0.2 if is_premium else 0.15

# Generate boundary test suite
boundaries = [
    {"age": 17, "is_premium": False},  # Just below 18
    {"age": 18, "is_premium": False},  # Exactly 18
    {"age": 19, "is_premium": True},   # Just above 18
    {"age": 64, "is_premium": False},  # Just below 65
    {"age": 65, "is_premium": True},   # Exactly 65
    {"age": 66, "is_premium": False},  # Just above 65
]

for inputs in boundaries:
    result = calculate_discount(**inputs)
    print(f"{inputs} -> {result}")
```

### Use Case 3: Coverage-Driven Exploration

Maximize code coverage through iterative generation:

```python
def complex_function(x, y, z):
    if x > 10:
        if y < 5:
            if z == 0:
                return "path_A"  # Hard to reach
    elif x < 0:
        if y > 10:
            return "path_B"
    return "default"

# Coverage-guided approach
covered = set()
test_inputs = []

# Iteration 1: Try random input
input_1 = {"x": 5, "y": 3, "z": 1}
coverage_1 = execute_with_coverage(complex_function, input_1)
# Covers: default path

# Iteration 2: Mutate toward uncovered (x > 10)
input_2 = {"x": 11, "y": 7, "z": 1}
coverage_2 = execute_with_coverage(complex_function, input_2)
# Covers: x > 10 but not y < 5

# Iteration 3: Refine toward (y < 5)
input_3 = {"x": 11, "y": 4, "z": 1}
coverage_3 = execute_with_coverage(complex_function, input_3)
# Covers: x > 10 and y < 5 but not z == 0

# Iteration 4: Target (z == 0)
input_4 = {"x": 11, "y": 4, "z": 0}
result = complex_function(**input_4)
# SUCCESS: Reached "path_A"
```

## Advanced Strategies

### Hybrid Approach: Combining Techniques

```python
def hybrid_test_generation(function_source):
    """
    Combine multiple techniques for comprehensive coverage.
    """
    # 1. Symbolic analysis - extract paths
    paths = analyze_code_paths(function_source)

    # 2. Constraint solving - generate initial inputs
    symbolic_inputs = [generate_for_path(p.get_constraints()) for p in paths]

    # 3. Edge case generation - add boundary values
    edge_inputs = generate_edge_cases_for_function(function_source)

    # 4. LLM semantic generation - add realistic scenarios
    llm_inputs = query_llm_for_realistic_inputs(function_source)

    # 5. Coverage-guided refinement - fill gaps
    all_inputs = symbolic_inputs + edge_inputs + llm_inputs
    coverage = measure_coverage(all_inputs)

    # 6. Mutate to reach remaining uncovered paths
    refined_inputs = coverage_guided_mutation(all_inputs, coverage)

    return refined_inputs
```

### Branch Distance Minimization

Guide input generation toward uncovered branches:

```python
def minimize_branch_distance(target_condition, current_input):
    """
    Adjust input to get closer to satisfying target condition.

    Example:
        Target: x > 100
        Current: x = 50
        Distance: 100 - 50 + 1 = 51

        New input: x = 101 (distance = 0)
    """
    variable = target_condition.variable
    operator = target_condition.operator
    threshold = target_condition.value

    if operator == ">":
        return {**current_input, variable: threshold + 1}
    elif operator == "<":
        return {**current_input, variable: threshold - 1}
    elif operator == ">=":
        return {**current_input, variable: threshold}
    elif operator == "<=":
        return {**current_input, variable: threshold}
    elif operator == "==":
        return {**current_input, variable: threshold}

    return current_input
```

## Reference Documentation

### Detailed Coverage Strategies
See **[coverage_strategies.md](references/coverage_strategies.md)** for:
- Branch distance minimization
- Gradient-based input adjustment
- Symbolic constraint solving
- Mutation-based fuzzing
- Hybrid coverage-guided + LLM approaches

### LLM-Driven Patterns
See **[llm_patterns.md](references/llm_patterns.md)** for:
- Semantic input generation
- Path-directed generation with LLM
- Domain knowledge integration
- Adversarial input generation
- Property-based test generation
- Multi-step scenario generation

## Best Practices

### 1. Start with Symbolic Analysis
Extract paths first to understand what needs to be tested:
```python
paths = analyze_code_paths(source)
print(f"Found {len(paths)} paths to cover")
```

### 2. Generate Diverse Inputs
Combine multiple generation strategies:
- Constraint solving for known paths
- Edge cases for boundaries
- LLM for semantic realism
- Fuzzing for unexpected cases

### 3. Use Coverage Feedback
Monitor coverage and adjust strategy:
```python
if coverage_improvement < 0.01:
    # Switch from symbolic to fuzzing
    switch_to_mutation_based()
```

### 4. Validate Generated Inputs
Always check that generated inputs are valid:
```python
def validate_input(inputs, function_signature):
    required_params = get_parameters(function_signature)
    assert all(p in inputs for p in required_params)
```

### 5. Prioritize Hard-to-Reach Paths
Focus on paths requiring specific conditions:
```python
# Prioritize deeply nested conditions
priority_paths = [p for p in paths if len(p.conditions) > 3]
```

## Tools Reference

### Scripts

**path_analyzer.py** - Extract control flow paths and constraints from Python code
```bash
python scripts/path_analyzer.py < your_code.py
```

**input_generator.py** - Generate test inputs satisfying path constraints
```bash
python scripts/input_generator.py --paths paths.json
```

### Example Workflow

```python
from scripts.path_analyzer import analyze_code_paths
from scripts.input_generator import generate_test_suite

# 1. Analyze code
source = open("my_module.py").read()
paths = analyze_code_paths(source)

# 2. Generate inputs
test_suite = generate_test_suite(paths)

# 3. Run tests
for path_id, test_data in test_suite.items():
    print(f"Testing path {path_id}: {test_data['description']}")
    result = my_function(**test_data['inputs'])
    print(f"  Result: {result}")
```
