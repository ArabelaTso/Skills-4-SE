# Prioritization Algorithms

Detailed algorithms and formulas for calculating test priority scores.

## Table of Contents

1. [Basic Priority Score Algorithm](#basic-priority-score-algorithm)
2. [Advanced Scoring Formulas](#advanced-scoring-formulas)
3. [Coverage Analysis Methods](#coverage-analysis-methods)
4. [Dependency Graph Analysis](#dependency-graph-analysis)
5. [Time-Based Optimization](#time-based-optimization)

---

## Basic Priority Score Algorithm

### Simple Change-Impact Score

```python
def calculate_basic_priority(test_info, changed_files):
    """
    Calculate basic priority score for a test.

    Args:
        test_info: Dict with keys: 'file', 'imports', 'type'
        changed_files: Set of changed file paths

    Returns:
        Priority score (0-100)
    """
    score = 0

    # Direct test file changed
    if test_info['file'] in changed_files:
        score += 20

    # Test imports changed file
    for imported in test_info['imports']:
        if imported in changed_files:
            score += 10
            break

    # Test type bonus
    if test_info['type'] == 'unit':
        score += 5  # Fast feedback
    elif test_info['type'] == 'integration':
        score += 3  # Medium coverage
    elif test_info['type'] == 'e2e':
        score += 1  # Comprehensive but slow

    return min(score, 100)


# Example usage
test = {
    'file': 'tests/test_auth.py',
    'imports': ['src/auth/login.py', 'src/models/user.py'],
    'type': 'unit'
}
changed = {'src/auth/login.py'}

priority = calculate_basic_priority(test, changed)
# Returns: 10 (imports changed file) + 5 (unit test) = 15
```

### Weighted Multi-Factor Score

```python
def calculate_weighted_priority(test_info, context):
    """
    Calculate priority using multiple weighted factors.

    Args:
        test_info: Test metadata
        context: Dict with 'changed_files', 'critical_paths', 'failure_history'

    Returns:
        Priority score with breakdown
    """
    weights = {
        'direct_coverage': 10.0,
        'indirect_coverage': 5.0,
        'critical_path': 1.5,    # Multiplier
        'failure_history': 1.3,   # Multiplier
        'test_speed': 0.2,        # Bonus per second saved
    }

    base_score = 0
    multipliers = 1.0

    # Direct coverage
    if test_info['tests_file'] in context['changed_files']:
        base_score += weights['direct_coverage']

    # Indirect coverage (imports)
    for imported in test_info['imports']:
        if imported in context['changed_files']:
            base_score += weights['indirect_coverage']
            break

    # Critical path multiplier
    for critical_file in context['critical_paths']:
        if critical_file in test_info['imports']:
            multipliers *= weights['critical_path']
            break

    # Failure history multiplier
    failure_rate = context['failure_history'].get(test_info['name'], 0)
    if failure_rate > 0.1:  # >10% failure rate
        multipliers *= weights['failure_history']

    # Speed bonus (prefer fast tests for quick feedback)
    if test_info['duration'] < 1.0:  # Under 1 second
        base_score += weights['test_speed'] * (1.0 - test_info['duration'])

    final_score = base_score * multipliers

    return {
        'score': final_score,
        'base': base_score,
        'multipliers': multipliers,
        'breakdown': {
            'direct': test_info['tests_file'] in context['changed_files'],
            'indirect': any(i in context['changed_files'] for i in test_info['imports']),
            'critical': any(c in test_info['imports'] for c in context['critical_paths']),
            'flaky': failure_rate > 0.1,
            'fast': test_info['duration'] < 1.0,
        }
    }
```

---

## Advanced Scoring Formulas

### Risk-Weighted Priority

```python
def calculate_risk_priority(test, risk_factors):
    """
    Prioritize based on risk assessment.

    Risk factors:
    - business_impact: 0-10 (10 = critical to business)
    - technical_complexity: 0-10 (10 = very complex)
    - change_frequency: 0-1 (1 = changes very often)
    - user_facing: boolean
    """
    # Base risk score
    risk_score = (
        risk_factors['business_impact'] * 2.0 +
        risk_factors['technical_complexity'] * 1.5 +
        risk_factors['change_frequency'] * 10.0
    )

    # User-facing multiplier
    if risk_factors['user_facing']:
        risk_score *= 1.3

    # Combine with change impact
    change_impact = get_change_impact(test)

    priority = risk_score * change_impact

    return priority


# Example
risk = {
    'business_impact': 9,      # Payment processing
    'technical_complexity': 7,  # Moderate complexity
    'change_frequency': 0.2,    # Changes occasionally
    'user_facing': True
}

score = calculate_risk_priority(test, risk)
```

### Coverage-Weighted Priority

```python
def calculate_coverage_priority(test, coverage_data):
    """
    Prioritize based on code coverage overlap.

    Higher priority for tests that:
    - Cover more changed lines
    - Are the only test covering changed code
    - Cover critical paths
    """
    changed_lines = coverage_data['changed_lines']
    test_coverage = coverage_data['test_coverage'][test['name']]
    all_tests_coverage = coverage_data['all_tests_coverage']

    # Calculate coverage overlap
    covered_changed_lines = set(test_coverage) & set(changed_lines)
    coverage_percentage = len(covered_changed_lines) / len(changed_lines)

    # Base score from coverage
    base_score = coverage_percentage * 100

    # Unique coverage bonus
    unique_lines = 0
    for line in covered_changed_lines:
        tests_covering_line = [
            t for t in all_tests_coverage
            if line in all_tests_coverage[t]
        ]
        if len(tests_covering_line) == 1:
            unique_lines += 1

    uniqueness_bonus = (unique_lines / len(changed_lines)) * 50

    final_score = base_score + uniqueness_bonus

    return {
        'score': final_score,
        'coverage_pct': coverage_percentage * 100,
        'unique_coverage': unique_lines,
        'total_covered': len(covered_changed_lines)
    }
```

---

## Coverage Analysis Methods

### Static Import Analysis

```python
import ast
import os

def analyze_test_imports(test_file_path):
    """
    Extract imports from a Python test file.

    Returns:
        Set of imported module paths
    """
    with open(test_file_path, 'r') as f:
        tree = ast.parse(f.read())

    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)

    # Convert module names to file paths
    file_paths = set()
    for module in imports:
        file_path = module.replace('.', os.sep) + '.py'
        file_paths.add(file_path)

    return file_paths


def map_tests_to_code(test_dir, src_dir):
    """
    Create mapping of tests to source code files.

    Returns:
        Dict: {test_file: set(source_files)}
    """
    mapping = {}

    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.startswith('test_') and file.endswith('.py'):
                test_path = os.path.join(root, file)
                imports = analyze_test_imports(test_path)

                # Filter to only source files
                src_imports = {
                    imp for imp in imports
                    if imp.startswith(src_dir.replace(os.sep, '.'))
                }

                mapping[test_path] = src_imports

    return mapping
```

### Coverage.py Integration

```python
import json

def load_coverage_data(coverage_file='.coverage'):
    """
    Load coverage data from coverage.py run.

    Returns:
        Dict: {test_name: [covered_lines]}
    """
    # Convert .coverage to JSON
    os.system(f'coverage json -o coverage.json')

    with open('coverage.json', 'r') as f:
        data = json.load(f)

    coverage_map = {}

    for file_path, file_data in data['files'].items():
        covered_lines = file_data['executed_lines']
        coverage_map[file_path] = covered_lines

    return coverage_map


def tests_covering_lines(coverage_data, target_lines, file_path):
    """
    Find tests that cover specific lines in a file.

    Args:
        coverage_data: Coverage data from coverage.py
        target_lines: Set of line numbers to find coverage for
        file_path: Path to source file

    Returns:
        List of test names covering those lines
    """
    # This requires running tests individually to track which test
    # covers which lines. Pseudo-implementation:

    covering_tests = []

    # Would need to run: pytest --cov --cov-report=json
    # for each test individually and track line coverage

    return covering_tests
```

---

## Dependency Graph Analysis

### Build Dependency Graph

```python
from collections import defaultdict, deque

def build_dependency_graph(source_files):
    """
    Build directed graph of file dependencies.

    Returns:
        Dict: {file: set(dependencies)}
    """
    graph = defaultdict(set)

    for file_path in source_files:
        imports = analyze_test_imports(file_path)
        graph[file_path] = imports

    return graph


def find_transitive_dependencies(graph, changed_files):
    """
    Find all files affected by changes (transitive closure).

    Returns:
        Set of all files that depend on changed files
    """
    affected = set(changed_files)
    queue = deque(changed_files)

    # Reverse graph to find dependents
    reverse_graph = defaultdict(set)
    for file, deps in graph.items():
        for dep in deps:
            reverse_graph[dep].add(file)

    # BFS to find all affected files
    while queue:
        file = queue.popleft()

        for dependent in reverse_graph[file]:
            if dependent not in affected:
                affected.add(dependent)
                queue.append(dependent)

    return affected


def prioritize_by_dependency_depth(graph, changed_files):
    """
    Prioritize tests by dependency distance from changes.

    Closer dependencies = higher priority
    """
    priorities = {}

    # BFS from changed files
    queue = deque((f, 0) for f in changed_files)
    visited = set()

    while queue:
        file, depth = queue.popleft()

        if file in visited:
            continue
        visited.add(file)

        # Priority inversely proportional to depth
        priorities[file] = 10 - min(depth, 9)

        # Add dependencies
        for dep in graph.get(file, []):
            if dep not in visited:
                queue.append((dep, depth + 1))

    return priorities
```

---

## Time-Based Optimization

### Optimize for Time Budget

```python
def select_tests_for_time_budget(tests, budget_seconds):
    """
    Select highest priority tests that fit in time budget.

    Uses greedy knapsack algorithm.

    Args:
        tests: List of dicts with 'priority', 'duration', 'name'
        budget_seconds: Maximum time available

    Returns:
        List of selected tests
    """
    # Sort by priority/duration ratio (bang for buck)
    tests_sorted = sorted(
        tests,
        key=lambda t: t['priority'] / max(t['duration'], 0.1),
        reverse=True
    )

    selected = []
    total_time = 0

    for test in tests_sorted:
        if total_time + test['duration'] <= budget_seconds:
            selected.append(test)
            total_time += test['duration']

    return selected, total_time


# Example
tests = [
    {'name': 'test_auth', 'priority': 15, 'duration': 0.5},
    {'name': 'test_payment', 'priority': 15, 'duration': 0.8},
    {'name': 'test_e2e', 'priority': 10, 'duration': 5.0},
    {'name': 'test_ui', 'priority': 3, 'duration': 2.0},
]

selected, time = select_tests_for_time_budget(tests, budget_seconds=2.0)
# Returns: test_auth, test_payment (total: 1.3 seconds)
```

### Multi-Objective Optimization

```python
from typing import List, Tuple

def pareto_optimal_selection(tests, objectives):
    """
    Select tests optimizing multiple objectives:
    - Maximize priority
    - Minimize time
    - Maximize coverage

    Returns Pareto-optimal set.
    """
    def dominates(test1, test2):
        """Test1 dominates test2 if it's better in all objectives."""
        better_priority = test1['priority'] >= test2['priority']
        better_time = test1['duration'] <= test2['duration']
        better_coverage = test1['coverage'] >= test2['coverage']

        strictly_better = (
            test1['priority'] > test2['priority'] or
            test1['duration'] < test2['duration'] or
            test1['coverage'] > test2['coverage']
        )

        return (better_priority and better_time and better_coverage
                and strictly_better)

    pareto_set = []

    for test in tests:
        dominated = False

        for other in tests:
            if dominates(other, test):
                dominated = True
                break

        if not dominated:
            pareto_set.append(test)

    return pareto_set
```

### Dynamic Time Allocation

```python
def allocate_time_by_priority_tiers(tests, total_budget):
    """
    Allocate time budget across priority tiers.

    Strategy:
    - 50% of time for critical tests (score ≥ 15)
    - 30% of time for high priority (score 10-14)
    - 20% of time for medium priority (score 5-9)
    """
    # Categorize tests
    critical = [t for t in tests if t['priority'] >= 15]
    high = [t for t in tests if 10 <= t['priority'] < 15]
    medium = [t for t in tests if 5 <= t['priority'] < 10]

    # Allocate budgets
    budgets = {
        'critical': total_budget * 0.5,
        'high': total_budget * 0.3,
        'medium': total_budget * 0.2
    }

    # Select from each tier
    selected = {}
    selected['critical'], _ = select_tests_for_time_budget(
        critical, budgets['critical']
    )
    selected['high'], _ = select_tests_for_time_budget(
        high, budgets['high']
    )
    selected['medium'], _ = select_tests_for_time_budget(
        medium, budgets['medium']
    )

    return selected
```

## Complete Example: End-to-End Prioritization

```python
def prioritize_test_suite(changed_files, test_directory):
    """
    Complete test prioritization workflow.
    """
    # 1. Discover all tests
    tests = discover_tests(test_directory)

    # 2. Build dependency graph
    graph = build_dependency_graph(tests)

    # 3. Find affected tests
    affected_files = find_transitive_dependencies(graph, changed_files)

    # 4. Calculate priorities
    priorities = []
    for test in tests:
        # Calculate change impact
        impact = calculate_weighted_priority(
            test,
            {
                'changed_files': changed_files,
                'critical_paths': ['auth', 'payment', 'user'],
                'failure_history': load_failure_history()
            }
        )

        priorities.append({
            'name': test['name'],
            'file': test['file'],
            'priority': impact['score'],
            'duration': test.get('duration', 1.0),
            'breakdown': impact['breakdown']
        })

    # 5. Sort by priority
    priorities.sort(key=lambda x: x['priority'], reverse=True)

    # 6. Group by tiers
    tiers = {
        'critical': [p for p in priorities if p['priority'] >= 15],
        'high': [p for p in priorities if 10 <= p['priority'] < 15],
        'medium': [p for p in priorities if 5 <= p['priority'] < 10],
        'low': [p for p in priorities if p['priority'] < 5]
    }

    return {
        'priorities': priorities,
        'tiers': tiers,
        'total_tests': len(tests),
        'affected_tests': len([p for p in priorities if p['priority'] > 0])
    }
```
