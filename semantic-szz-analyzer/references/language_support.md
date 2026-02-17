# Language Support

## Overview

Semantic SZZ Analyzer supports multiple programming languages through language-specific parsers and analyzers. This document describes the support level and configuration for each language.

## Supported Languages

### Python (Full Support)

**Parser**: Built-in `ast` module

**Features**:
- Complete AST parsing
- Control-flow analysis
- Data-flow analysis
- Semantic equivalence detection

**Example Usage**:
```python
from semantic_analyzer import SemanticAnalyzer

analyzer = SemanticAnalyzer()
result = analyzer.analyze_commit_pair(repo_path, 'file.py', commit1, commit2)
```

**Limitations**:
- Dynamic features (eval, exec) not fully analyzed
- Type information limited without type hints

### Java (Full Support)

**Parser**: `javalang` or `tree-sitter-java`

**Installation**:
```bash
pip install javalang
# OR
pip install tree-sitter tree-sitter-java
```

**Features**:
- Complete AST parsing
- Type-aware analysis
- Method signature comparison
- Class hierarchy analysis

**Example**:
```java
// Semantic change detected
// Version 1
public int calculate(int x) {
    return x * 2;
}

// Version 2
public int calculate(int x) {
    return x * 3;  // Semantic change
}

// Refactoring detected
// Version 1
public int calculate(int x) {
    return x * 2;
}

// Version 2
public int calculate(int x) {
    int result = x * 2;
    return result;  // Refactoring only
}
```

### C/C++ (Partial Support)

**Parser**: `pycparser` (C) or `tree-sitter-cpp` (C++)

**Installation**:
```bash
pip install pycparser
# OR
pip install tree-sitter tree-sitter-cpp
```

**Features**:
- AST parsing (requires preprocessed code for pycparser)
- Basic control-flow analysis
- Pointer analysis (limited)

**Limitations**:
- Preprocessor directives require special handling
- Template metaprogramming not fully supported
- Macro expansion needed for accurate analysis

**Configuration**:
```python
# For pycparser, preprocess first
import subprocess

def preprocess_c_file(file_path):
    result = subprocess.run(['gcc', '-E', file_path],
                          capture_output=True, text=True)
    return result.stdout
```

### JavaScript/TypeScript (Full Support)

**Parser**: `esprima` (JavaScript) or `typescript` (TypeScript)

**Installation**:
```bash
pip install esprima
# OR
npm install -g typescript
```

**Features**:
- Complete AST parsing
- ES6+ syntax support
- Async/await analysis
- Module dependency tracking

**Example**:
```javascript
// Semantic change
// Version 1
function process(data) {
    return data.filter(x => x > 0);
}

// Version 2
function process(data) {
    return data.filter(x => x >= 0);  // Semantic change
}

// Refactoring
// Version 1
function process(data) {
    return data.filter(x => x > 0);
}

// Version 2
const isPositive = x => x > 0;
function process(data) {
    return data.filter(isPositive);  // Refactoring
}
```

### Go (Partial Support)

**Parser**: `tree-sitter-go`

**Installation**:
```bash
pip install tree-sitter tree-sitter-go
```

**Features**:
- AST parsing
- Goroutine detection
- Interface analysis

**Limitations**:
- Concurrent behavior analysis limited
- Reflection not fully analyzed

### Ruby (Partial Support)

**Parser**: `tree-sitter-ruby`

**Installation**:
```bash
pip install tree-sitter tree-sitter-ruby
```

**Features**:
- AST parsing
- Basic metaprogramming detection

**Limitations**:
- Dynamic method definitions challenging
- Eval and instance_eval not fully analyzed

## Language Detection

The analyzer automatically detects language based on file extension:

```python
LANGUAGE_MAP = {
    '.py': 'python',
    '.java': 'java',
    '.c': 'c',
    '.cpp': 'cpp',
    '.cc': 'cpp',
    '.h': 'c',
    '.hpp': 'cpp',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.go': 'go',
    '.rb': 'ruby',
}
```

## Parser Configuration

### Using Tree-sitter (Recommended for Multi-Language)

Tree-sitter provides consistent parsing across languages:

```python
from tree_sitter import Language, Parser

# Build language library
Language.build_library(
    'build/languages.so',
    [
        'vendor/tree-sitter-python',
        'vendor/tree-sitter-java',
        'vendor/tree-sitter-cpp',
    ]
)

# Load language
PY_LANGUAGE = Language('build/languages.so', 'python')

# Create parser
parser = Parser()
parser.set_language(PY_LANGUAGE)

# Parse code
tree = parser.parse(bytes(code, 'utf8'))
```

### Language-Specific Analyzers

Each language has a specialized analyzer:

```python
# semantic_analyzer.py
class LanguageAnalyzer:
    def __init__(self, language):
        self.language = language
        self.parser = self._get_parser(language)

    def _get_parser(self, language):
        if language == 'python':
            return PythonAnalyzer()
        elif language == 'java':
            return JavaAnalyzer()
        elif language == 'cpp':
            return CppAnalyzer()
        # ... etc
```

## Extending Language Support

### Adding a New Language

1. **Install Parser**:
```bash
pip install tree-sitter-<language>
```

2. **Create Language Analyzer**:
```python
# analyzers/new_language_analyzer.py
class NewLanguageAnalyzer(BaseAnalyzer):
    def parse(self, code):
        # Implement parsing logic
        pass

    def extract_cfg(self, tree):
        # Implement CFG extraction
        pass

    def extract_dfg(self, tree):
        # Implement DFG extraction
        pass
```

3. **Register Language**:
```python
# semantic_analyzer.py
LANGUAGE_ANALYZERS = {
    'python': PythonAnalyzer,
    'java': JavaAnalyzer,
    'new_language': NewLanguageAnalyzer,
}
```

4. **Add File Extension Mapping**:
```python
LANGUAGE_MAP['.newext'] = 'new_language'
```

## Language-Specific Considerations

### Python

**Dynamic Features**:
- `eval()` and `exec()`: Cannot be fully analyzed statically
- Dynamic imports: May miss dependencies
- Metaclasses: Complex behavior not fully captured

**Best Practices**:
- Use type hints for better analysis
- Avoid dynamic code generation when possible
- Document dynamic behavior in comments

### Java

**Type System**:
- Strong typing enables more accurate analysis
- Generics provide additional type information
- Reflection usage may limit analysis

**Best Practices**:
- Use explicit types over `var` for clarity
- Document reflection usage
- Prefer composition over complex inheritance

### C/C++

**Preprocessing**:
- Macros must be expanded before analysis
- Conditional compilation affects analysis
- Include paths must be configured

**Best Practices**:
```bash
# Preprocess before analysis
gcc -E -I/path/to/includes source.c > preprocessed.c
python scripts/semantic_szz.py --file preprocessed.c
```

### JavaScript

**Async Code**:
- Promises and async/await tracked
- Callback patterns detected
- Event handlers analyzed

**Best Practices**:
- Use async/await over callbacks
- Avoid deeply nested promises
- Document asynchronous behavior

## Performance Considerations

### Parser Performance

| Language | Parse Speed | Memory Usage |
|----------|-------------|--------------|
| Python   | Fast        | Low          |
| Java     | Medium      | Medium       |
| C/C++    | Slow*       | High         |
| JavaScript | Fast      | Low          |
| Go       | Fast        | Low          |

*C/C++ slow due to preprocessing requirements

### Optimization Tips

1. **Cache Parsed Trees**:
```python
tree_cache = {}

def get_parsed_tree(file_path, commit):
    key = f"{file_path}:{commit}"
    if key not in tree_cache:
        tree_cache[key] = parse_file(file_path, commit)
    return tree_cache[key]
```

2. **Parallel Processing**:
```python
from multiprocessing import Pool

def analyze_files_parallel(files):
    with Pool(processes=4) as pool:
        results = pool.map(analyze_file, files)
    return results
```

3. **Incremental Analysis**:
Only analyze changed functions/classes rather than entire files.

## Testing Language Support

### Test Suite

```bash
# Run language-specific tests
python tests/test_python_analyzer.py
python tests/test_java_analyzer.py
python tests/test_cpp_analyzer.py
```

### Validation

```python
# Validate parser installation
def validate_language_support():
    for lang, analyzer_class in LANGUAGE_ANALYZERS.items():
        try:
            analyzer = analyzer_class()
            print(f"✓ {lang}: Supported")
        except ImportError as e:
            print(f"✗ {lang}: Missing dependency - {e}")
```

## References

- Tree-sitter documentation: https://tree-sitter.github.io/tree-sitter/
- Python AST documentation: https://docs.python.org/3/library/ast.html
- Javalang: https://github.com/c2nes/javalang
- Esprima: https://esprima.org/
