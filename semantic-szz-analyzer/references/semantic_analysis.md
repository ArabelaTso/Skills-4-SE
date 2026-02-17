# Semantic Analysis Techniques

## Overview

Semantic analysis examines the meaning and behavior of code rather than just its textual representation. This document describes the techniques used in Semantic SZZ to distinguish semantic changes from refactorings.

## Abstract Syntax Tree (AST) Analysis

### What is AST?

An Abstract Syntax Tree represents the syntactic structure of code in a tree format, abstracting away formatting details like whitespace and comments.

### Example

```python
# Code
def add(x, y):
    return x + y

# AST Structure
Module
└── FunctionDef(name='add')
    ├── arguments
    │   ├── arg(arg='x')
    │   └── arg(arg='y')
    └── Return
        └── BinOp
            ├── Name(id='x')
            ├── Add
            └── Name(id='y')
```

### AST Similarity Computation

**Method**: Compare AST node sequences using sequence matching algorithms.

```python
def compute_ast_similarity(tree1, tree2):
    nodes1 = extract_node_types(tree1)  # ['Module', 'FunctionDef', 'Return', ...]
    nodes2 = extract_node_types(tree2)
    return sequence_matcher(nodes1, nodes2)
```

**Use Case**: Detect when code structure is preserved despite textual changes.

### AST-Based Refactoring Detection

**Refactoring indicators**:
- High AST similarity (>0.8) despite textual differences
- Same node types in different order (code movement)
- Identical subtrees in different locations (extract method)

## Control-Flow Graph (CFG) Analysis

### What is CFG?

A Control-Flow Graph represents all possible execution paths through a program, showing how control flows between statements.

### Example

```python
# Code
def check(x):
    if x > 0:
        return "positive"
    else:
        return "negative"

# CFG
[Entry]
   ↓
[if x > 0]
   ↓     ↓
[return] [return]
"positive" "negative"
   ↓     ↓
  [Exit]
```

### CFG Similarity Computation

**Method**: Extract control flow patterns and compare them.

```python
def extract_control_flow(code):
    patterns = set()
    for node in ast.walk(parse(code)):
        if isinstance(node, ast.If):
            patterns.add('If')
        elif isinstance(node, ast.While):
            patterns.add('While')
        elif isinstance(node, ast.For):
            patterns.add('For')
    return patterns

def compute_cfg_similarity(code1, code2):
    cfg1 = extract_control_flow(code1)
    cfg2 = extract_control_flow(code2)
    return jaccard_similarity(cfg1, cfg2)
```

### CFG-Based Change Detection

**Semantic changes**:
- New conditional branches (if/else added)
- Loop structure changes (for → while)
- Different branching logic

**Refactorings**:
- Same control flow patterns
- Reordered but equivalent branches
- Guard clauses vs. nested ifs (equivalent)

## Data-Flow Graph (DFG) Analysis

### What is DFG?

A Data-Flow Graph tracks how data flows through a program, showing variable definitions, uses, and dependencies.

### Example

```python
# Code
def calculate(x, y):
    z = x + y
    result = z * 2
    return result

# DFG
x ──┐
    ├──> z ──> result ──> return
y ──┘
```

### DFG Similarity Computation

**Method**: Extract variable usage patterns and dependencies.

```python
def extract_variable_usage(code):
    usage = set()
    for node in ast.walk(parse(code)):
        if isinstance(node, ast.Name):
            usage.add(node.id)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                usage.add(f'assign:{target.id}')
    return usage

def compute_dfg_similarity(code1, code2):
    dfg1 = extract_variable_usage(code1)
    dfg2 = extract_variable_usage(code2)
    return jaccard_similarity(dfg1, dfg2)
```

### DFG-Based Change Detection

**Semantic changes**:
- New variables introduced
- Different variable dependencies
- Changed computation order affecting results

**Refactorings**:
- Variable renaming (same usage pattern)
- Intermediate variables added/removed
- Equivalent expressions (x*2 vs. x+x)

## Semantic Equivalence Detection

### Normalization Techniques

**Purpose**: Identify semantically equivalent code with different syntax.

**Techniques**:

1. **Whitespace Normalization**: Remove all whitespace and compare
2. **Comment Removal**: Strip comments before comparison
3. **Variable Renaming**: Normalize variable names to canonical forms
4. **Expression Canonicalization**: Convert equivalent expressions to standard form

### Example

```python
# Version 1
def foo(x):
    # Calculate double
    result = x * 2
    return result

# Version 2
def foo(y):
    return y + y

# After normalization
def foo(VAR1):
    return VAR1 * 2  # Both normalize to this
```

## Combined Semantic Analysis

### Multi-Metric Approach

Semantic SZZ combines multiple metrics for robust analysis:

```python
def is_semantic_change(code1, code2):
    ast_sim = compute_ast_similarity(code1, code2)
    cfg_sim = compute_cfg_similarity(code1, code2)
    dfg_sim = compute_dfg_similarity(code1, code2)

    # Weighted combination
    semantic_score = (ast_sim * 0.4 + cfg_sim * 0.3 + dfg_sim * 0.3)

    # Thresholds
    if semantic_score > 0.8:
        return False  # Likely refactoring
    elif semantic_score < 0.5:
        return True   # Definite semantic change
    else:
        return "uncertain"  # Requires manual review
```

### Decision Rules

**High Confidence Semantic Change**:
- AST similarity < 0.5
- CFG similarity < 0.5
- DFG similarity < 0.5

**High Confidence Refactoring**:
- AST similarity > 0.8
- CFG similarity > 0.8
- Normalized code is identical

**Uncertain Cases**:
- Mixed signals from different metrics
- Moderate similarity scores (0.5-0.8)
- Requires additional analysis or manual review

## Advanced Techniques

### Program Slicing

Extract code slices relevant to specific variables or statements to focus analysis.

```python
# Original code
def process(x, y):
    a = x + 1
    b = y * 2
    c = a + b
    return c

# Slice for variable 'c'
def process(x, y):
    a = x + 1
    b = y * 2
    c = a + b
    return c
```

### Symbolic Execution

Execute code symbolically to determine if different code versions produce equivalent outputs.

### Clone Detection

Identify code clones (duplicated code) to track code movement across files.

## Limitations

### 1. Language-Specific Challenges

Different languages require different parsing and analysis approaches:
- Dynamic languages (Python, JavaScript): Runtime behavior harder to analyze
- Static languages (Java, C++): More amenable to static analysis

### 2. Complex Refactorings

Some refactorings are difficult to detect:
- Extract superclass
- Introduce design pattern
- Algorithm replacement

### 3. Semantic Equivalence

Determining true semantic equivalence is undecidable in general:
- Infinite loops
- Non-deterministic behavior
- External dependencies

## Best Practices

1. **Use Multiple Metrics**: Don't rely on a single similarity measure
2. **Tune Thresholds**: Adjust thresholds based on project characteristics
3. **Manual Validation**: Review uncertain cases manually
4. **Language-Specific Analysis**: Use appropriate parsers and analyzers for each language
5. **Incremental Analysis**: Analyze changes incrementally rather than entire files

## References

- Ferrante, J., et al. (1987). "The program dependence graph and its use in optimization"
- Komondoor, R., & Horwitz, S. (2001). "Using slicing to identify duplication in source code"
- Gabel, M., & Su, Z. (2008). "Javert: Fully automatic mining of general temporal properties"
- Kim, M., et al. (2010). "An empirical study of code clone genealogies"
