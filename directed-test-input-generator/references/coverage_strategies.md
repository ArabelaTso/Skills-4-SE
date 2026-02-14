# Coverage-Guided Test Generation Strategies

## Overview

Coverage-guided generation iteratively creates test inputs that explore uncovered code paths. This document provides strategies for using coverage feedback to guide test input generation toward hard-to-reach behaviors.

## Basic Coverage-Guided Workflow

```python
def coverage_guided_generation(function, iterations=100):
    """
    Generate test inputs guided by coverage feedback.

    1. Start with random/baseline inputs
    2. Execute and measure coverage
    3. Mutate inputs that reach new coverage
    4. Repeat until coverage goal reached
    """
    covered_lines = set()
    test_corpus = []

    # Initial seed inputs
    current_inputs = generate_seed_inputs(function)

    for i in range(iterations):
        # Execute with coverage tracking
        new_coverage = execute_with_coverage(function, current_inputs)

        # Check if new coverage was reached
        if new_coverage - covered_lines:
            # Save inputs that reached new coverage
            test_corpus.append(current_inputs)
            covered_lines.update(new_coverage)

        # Mutate inputs to explore new paths
        current_inputs = mutate_inputs(current_inputs, covered_lines)

    return test_corpus
```

## Strategy 1: Branch Distance Minimization

Use branch distance to guide input generation toward uncovered branches.

```python
def calculate_branch_distance(condition, actual_value):
    """
    Calculate how "close" an input is to satisfying a branch condition.

    Lower distance = closer to satisfying the condition
    """
    if condition.operator == "<":
        if actual_value < condition.value:
            return 0  # Condition satisfied
        else:
            return actual_value - condition.value + 1

    elif condition.operator == ">":
        if actual_value > condition.value:
            return 0
        else:
            return condition.value - actual_value + 1

    elif condition.operator == "==":
        if actual_value == condition.value:
            return 0
        else:
            return abs(actual_value - condition.value)

    elif condition.operator == "!=":
        if actual_value != condition.value:
            return 0
        else:
            return 1  # Need any different value

    return float('inf')


def guided_input_mutation(current_input, uncovered_branch):
    """
    Mutate input to minimize branch distance to uncovered branch.

    Example:
        Uncovered branch: x > 100
        Current input: x = 50
        Branch distance: 100 - 50 + 1 = 51

        Mutation strategy: Increase x toward 101
        New input: x = 101
    """
    variable = uncovered_branch.variable
    current_value = current_input[variable]

    if uncovered_branch.operator == ">":
        # Need value greater than threshold
        new_value = uncovered_branch.value + 1
    elif uncovered_branch.operator == "<":
        # Need value less than threshold
        new_value = uncovered_branch.value - 1
    elif uncovered_branch.operator == "==":
        # Need exact value
        new_value = uncovered_branch.value
    elif uncovered_branch.operator == ">=":
        new_value = uncovered_branch.value
    elif uncovered_branch.operator == "<=":
        new_value = uncovered_branch.value
    else:
        new_value = current_value

    mutated_input = current_input.copy()
    mutated_input[variable] = new_value
    return mutated_input
```

## Strategy 2: Gradient-Based Input Adjustment

Use numeric gradients to iteratively adjust inputs toward coverage goals.

```python
def gradient_based_generation(function, target_branch, max_iterations=50):
    """
    Use gradient descent to generate inputs that reach target branch.

    This works well for numeric inputs where we can measure
    "distance" to satisfying the branch condition.
    """
    # Start with random input
    current_input = initialize_random_input()

    for iteration in range(max_iterations):
        # Calculate branch distance
        distance = evaluate_branch_distance(function, current_input, target_branch)

        if distance == 0:
            # Target reached!
            return current_input

        # Compute gradient (how changing input affects distance)
        gradient = compute_gradient(function, current_input, target_branch)

        # Update input in direction that reduces distance
        current_input = update_input(current_input, gradient, learning_rate=0.1)

    return current_input


def compute_gradient(function, input_values, target_branch):
    """
    Compute numerical gradient showing how input changes affect branch distance.
    """
    gradient = {}
    epsilon = 0.01  # Small perturbation

    base_distance = evaluate_branch_distance(function, input_values, target_branch)

    for param_name, param_value in input_values.items():
        if not isinstance(param_value, (int, float)):
            continue

        # Perturb parameter slightly
        perturbed = input_values.copy()
        perturbed[param_name] = param_value + epsilon

        # Measure change in distance
        new_distance = evaluate_branch_distance(function, perturbed, target_branch)

        # Gradient = change in distance / change in parameter
        gradient[param_name] = (new_distance - base_distance) / epsilon

    return gradient
```

## Strategy 3: Symbolic Execution-Inspired Generation

Use symbolic reasoning to solve path constraints.

```python
def symbolic_constraint_solving(path_conditions):
    """
    Solve path constraints to generate inputs that satisfy specific paths.

    This strategy analyzes the logical conditions required to reach a path
    and generates inputs that satisfy those conditions.
    """
    # Group constraints by variable
    constraints_by_var = {}
    for condition in path_conditions:
        var = condition.variable
        if var not in constraints_by_var:
            constraints_by_var[var] = []
        constraints_by_var[var].append(condition)

    # Solve constraints for each variable
    solution = {}
    for var, constraints in constraints_by_var.items():
        solution[var] = solve_variable_constraints(var, constraints)

    return solution


def solve_variable_constraints(variable, constraints):
    """
    Find a value that satisfies all constraints on a variable.

    Example:
        Constraints: x > 10, x < 100, x != 50
        Solution: x = 11 (satisfies all constraints)
    """
    # Track bounds
    lower_bound = float('-inf')
    upper_bound = float('inf')
    excluded_values = set()
    required_value = None

    for constraint in constraints:
        op = constraint.operator
        val = constraint.value

        if constraint.negated:
            # Invert operator
            op = invert_operator(op)

        if op == ">":
            lower_bound = max(lower_bound, val + 0.001)
        elif op == ">=":
            lower_bound = max(lower_bound, val)
        elif op == "<":
            upper_bound = min(upper_bound, val - 0.001)
        elif op == "<=":
            upper_bound = min(upper_bound, val)
        elif op == "==":
            required_value = val
        elif op == "!=":
            excluded_values.add(val)

    # Generate value satisfying constraints
    if required_value is not None:
        return required_value

    # Find value in valid range
    if isinstance(lower_bound, int) and isinstance(upper_bound, int):
        # Integer value
        candidate = int(lower_bound) + 1
        while candidate in excluded_values and candidate < upper_bound:
            candidate += 1
        return candidate
    else:
        # Float value
        return (lower_bound + upper_bound) / 2


def invert_operator(op):
    """Invert a comparison operator."""
    inversions = {
        "<": ">=",
        "<=": ">",
        ">": "<=",
        ">=": "<",
        "==": "!=",
        "!=": "=="
    }
    return inversions.get(op, op)
```

## Strategy 4: Mutation-Based Fuzzing

Mutate existing inputs to explore new code paths.

```python
class InputMutator:
    """Mutates test inputs to explore new code paths."""

    def mutate(self, input_value, mutation_rate=0.3):
        """Apply random mutations to input."""
        if isinstance(input_value, dict):
            return self.mutate_dict(input_value, mutation_rate)
        else:
            return self.mutate_single_value(input_value)

    def mutate_single_value(self, value):
        """Mutate a single value based on its type."""
        if isinstance(value, int):
            return self.mutate_int(value)
        elif isinstance(value, float):
            return self.mutate_float(value)
        elif isinstance(value, str):
            return self.mutate_string(value)
        elif isinstance(value, bool):
            return not value
        elif isinstance(value, list):
            return self.mutate_list(value)
        else:
            return value

    def mutate_int(self, value):
        """Mutate integer value."""
        mutations = [
            value + 1,
            value - 1,
            value * 2,
            value // 2,
            -value,
            0,
            value + random.randint(-10, 10)
        ]
        return random.choice(mutations)

    def mutate_float(self, value):
        """Mutate float value."""
        mutations = [
            value + 0.1,
            value - 0.1,
            value * 1.1,
            value * 0.9,
            -value,
            0.0
        ]
        return random.choice(mutations)

    def mutate_string(self, value):
        """Mutate string value."""
        if not value:
            return "a"

        mutations = [
            value + "x",              # Append
            value[:-1],               # Truncate
            value.upper(),            # Case change
            value.lower(),
            value[::-1],              # Reverse
            value.replace(value[0], 'X') if value else value,  # Replace char
            ""                        # Empty string
        ]
        return random.choice(mutations)

    def mutate_list(self, value):
        """Mutate list value."""
        if not value:
            return [0]

        mutations = [
            value + [0],              # Append
            value[:-1],               # Remove last
            value[::-1],              # Reverse
            value * 2,                # Duplicate
            []                        # Empty
        ]
        return random.choice(mutations)

    def mutate_dict(self, value, mutation_rate):
        """Mutate dictionary of input parameters."""
        mutated = value.copy()

        for key in list(mutated.keys()):
            if random.random() < mutation_rate:
                mutated[key] = self.mutate_single_value(mutated[key])

        return mutated
```

## Strategy 5: Hybrid Coverage-Guided + LLM

Combine coverage feedback with LLM's semantic understanding.

```python
def hybrid_generation_strategy(function, uncovered_paths):
    """
    Hybrid approach: Use LLM to understand program semantics,
    then use coverage feedback to refine inputs.

    Workflow:
    1. LLM analyzes function and suggests initial inputs for uncovered paths
    2. Execute and measure coverage
    3. Use coverage feedback to refine inputs
    4. LLM suggests new variations based on what worked
    """

    # Phase 1: LLM generates initial inputs based on code understanding
    llm_inputs = llm_generate_initial_inputs(function, uncovered_paths)

    # Phase 2: Coverage-guided refinement
    refined_inputs = []
    for path_id, initial_input in llm_inputs.items():
        # Execute and measure coverage
        coverage = execute_with_coverage(function, initial_input)

        # Check if target path was reached
        if path_id in coverage:
            refined_inputs.append(initial_input)
        else:
            # Use gradient descent to refine
            refined = gradient_refine(function, initial_input, path_id)
            refined_inputs.append(refined)

    # Phase 3: LLM suggests mutations for paths still uncovered
    still_uncovered = [p for p in uncovered_paths if not is_covered(p, refined_inputs)]
    if still_uncovered:
        mutations = llm_suggest_mutations(function, refined_inputs, still_uncovered)
        refined_inputs.extend(mutations)

    return refined_inputs


def llm_generate_initial_inputs(function, uncovered_paths):
    """
    LLM analyzes function semantics and generates inputs likely to
    reach uncovered paths.

    The LLM understands:
    - Variable naming conventions (e.g., "age" likely needs numeric value)
    - Business logic (e.g., "premium_user" likely boolean)
    - Common patterns (e.g., "country_code" likely 2-letter string)
    """
    # This would interface with LLM API
    # Pseudocode for illustration
    pass


def llm_suggest_mutations(function, current_inputs, uncovered_paths):
    """
    LLM suggests semantically meaningful mutations.

    Instead of random mutations, LLM suggests:
    - "Try age = 17 to test underage path"
    - "Try country = 'XX' to test invalid country code"
    - "Try empty string to test validation error"
    """
    pass
```

## Practical Tips

### 1. Start with Seed Corpus
Always start with a diverse set of seed inputs:
- Edge cases (0, -1, None, empty string)
- Typical values
- Boundary values

### 2. Prioritize Uncovered Branches
Focus generation on branches that haven't been covered yet:
```python
def prioritize_generation(uncovered_branches, covered_branches):
    # Focus on branches furthest from current coverage
    priority = []
    for branch in uncovered_branches:
        distance = min_distance_to_covered(branch, covered_branches)
        priority.append((distance, branch))

    # Generate inputs for highest priority first
    priority.sort(reverse=True)
    return [b for _, b in priority]
```

### 3. Track Coverage Progress
Monitor coverage improvement to know when to try new strategies:
```python
coverage_history = []
for iteration in range(max_iterations):
    inputs = generate_inputs(...)
    coverage = measure_coverage(inputs)
    coverage_history.append(coverage)

    # If no improvement in 10 iterations, change strategy
    if len(coverage_history) > 10:
        recent_improvement = coverage_history[-1] - coverage_history[-10]
        if recent_improvement < 0.01:
            switch_to_different_strategy()
```

### 4. Combine Multiple Strategies
Different strategies work better for different code patterns:
- **Simple numeric conditions**: Gradient-based or symbolic
- **Complex business logic**: LLM-based semantic understanding
- **String/list manipulation**: Mutation-based fuzzing
- **Unknown territory**: Coverage-guided exploration
