# Code Scanning Patterns

Patterns and conventions for annotating code with requirement references and scanning techniques.

## Table of Contents

1. [Annotation Conventions](#annotation-conventions)
2. [Python Scanning](#python-scanning)
3. [Java Scanning](#java-scanning)
4. [JavaScript/TypeScript Scanning](#javascripttypescript-scanning)
5. [Multi-Language Scanner](#multi-language-scanner)

---

## Annotation Conventions

### Standard Keywords

Use these keywords in comments/docstrings to indicate requirement implementation:

- `Implements:` - Primary implementation of requirement
- `Satisfies:` - Fulfills requirement
- `Covers:` - Addresses requirement
- `Relates to:` - Related but not direct implementation
- `@implements` - JavaDoc-style annotation

### ID Format

Use consistent ID format: `PREFIX-CATEGORY-NUMBER`

Examples:
- `REQ-AUTH-001`
- `US-123`
- `FEAT-SEARCH-005`

### Multiple Requirements

Separate multiple IDs with commas:
```
Implements: REQ-001, REQ-002, REQ-AUTH-001
```

---

## Python Scanning

### Docstring Annotations

```python
def authenticate_user(email, password):
    """Authenticate user with credentials.

    Implements: REQ-AUTH-001, REQ-LOGIN-001

    Args:
        email: User email
        password: User password

    Returns:
        Token if successful, None otherwise
    """
    pass
```

### Class-Level Annotations

```python
class AuthenticationService:
    """User authentication service.

    Implements: REQ-AUTH-001
    Satisfies: REQ-SECURITY-003
    """

    def login(self, email, password):
        """Login method. Implements: REQ-LOGIN-001"""
        pass
```

### Inline Comments

```python
# Implements: REQ-VALIDATION-001
def validate_email(email):
    return '@' in email and '.' in email
```

### Scanning Script

```python
import ast
import re
from pathlib import Path

def scan_python_file(file_path):
    """Scan Python file for requirement references."""
    implementations = []

    with open(file_path, 'r') as f:
        content = f.read()

    try:
        tree = ast.parse(content)

        for node in ast.walk(tree):
            # Check functions
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    req_ids = extract_requirement_ids(docstring)
                    if req_ids:
                        implementations.append({
                            'file': str(file_path),
                            'type': 'function',
                            'name': node.name,
                            'line': node.lineno,
                            'requirements': req_ids
                        })

            # Check classes
            elif isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    req_ids = extract_requirement_ids(docstring)
                    if req_ids:
                        implementations.append({
                            'file': str(file_path),
                            'type': 'class',
                            'name': node.name,
                            'line': node.lineno,
                            'requirements': req_ids
                        })

    except SyntaxError:
        # Fallback to regex if AST parsing fails
        pass

    # Also scan inline comments
    for i, line in enumerate(content.split('\n'), 1):
        if '#' in line and any(kw in line for kw in ['Implements:', 'Satisfies:', 'Covers:']):
            req_ids = extract_requirement_ids(line)
            if req_ids:
                implementations.append({
                    'file': str(file_path),
                    'type': 'comment',
                    'line': i,
                    'requirements': req_ids
                })

    return implementations

def extract_requirement_ids(text):
    """Extract requirement IDs from text."""
    pattern = r'(?:Implements?|Satisfies|Covers|Relates to):\s*([A-Z]+-[A-Z0-9-]+(?:,\s*[A-Z]+-[A-Z0-9-]+)*)'
    matches = re.findall(pattern, text, re.IGNORECASE)

    if matches:
        # Split comma-separated IDs
        ids = []
        for match in matches:
            ids.extend([req_id.strip() for req_id in match.split(',')])
        return ids

    return []
```

---

## Java Scanning

### JavaDoc Annotations

```java
/**
 * Authentication service for user login.
 *
 * @implements REQ-AUTH-001 User authentication
 * @implements REQ-LOGIN-001 Email/password login
 * @author Security Team
 */
public class AuthenticationService {
    /**
     * Authenticate user credentials.
     *
     * @implements REQ-LOGIN-001
     * @param email User email address
     * @param password User password
     * @return Authentication token
     */
    public Token authenticate(String email, String password) {
        // Implementation
    }
}
```

### Standard Comment Annotations

```java
// Implements: REQ-VALIDATION-001
public boolean validateEmail(String email) {
    return email.contains("@") && email.contains(".");
}
```

### Scanning Script

```python
import re
from pathlib import Path

def scan_java_file(file_path):
    """Scan Java file for requirement references."""
    implementations = []

    with open(file_path, 'r') as f:
        content = f.read()

    # Pattern to find classes
    class_pattern = r'/\*\*(.+?)\*/\s*(?:public|private|protected)?\s*class\s+(\w+)'

    for match in re.finditer(class_pattern, content, re.DOTALL):
        javadoc = match.group(1)
        class_name = match.group(2)

        req_ids = extract_requirement_ids(javadoc)
        if req_ids:
            implementations.append({
                'file': str(file_path),
                'type': 'class',
                'name': class_name,
                'requirements': req_ids
            })

    # Pattern to find methods
    method_pattern = r'/\*\*(.+?)\*/\s*(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\('

    for match in re.finditer(method_pattern, content, re.DOTALL):
        javadoc = match.group(1)
        method_name = match.group(2)

        req_ids = extract_requirement_ids(javadoc)
        if req_ids:
            implementations.append({
                'file': str(file_path),
                'type': 'method',
                'name': method_name,
                'requirements': req_ids
            })

    # Scan inline comments
    for i, line in enumerate(content.split('\n'), 1):
        if '//' in line:
            req_ids = extract_requirement_ids(line)
            if req_ids:
                implementations.append({
                    'file': str(file_path),
                    'type': 'comment',
                    'line': i,
                    'requirements': req_ids
                })

    return implementations
```

---

## JavaScript/TypeScript Scanning

### JSDoc Annotations

```javascript
/**
 * User authentication service.
 *
 * @implements REQ-AUTH-001
 * @implements REQ-LOGIN-001
 */
class AuthService {
    /**
     * Authenticate user credentials.
     *
     * @implements REQ-LOGIN-001
     * @param {string} email - User email
     * @param {string} password - User password
     * @returns {Promise<Token>} Authentication token
     */
    async authenticate(email, password) {
        // Implementation
    }
}
```

### Function Comments

```javascript
/**
 * Validate email format.
 * Implements: REQ-VALIDATION-001
 */
function validateEmail(email) {
    return email.includes('@') && email.includes('.');
}
```

### Scanning Script

```python
import re
from pathlib import Path

def scan_javascript_file(file_path):
    """Scan JavaScript/TypeScript file for requirement references."""
    implementations = []

    with open(file_path, 'r') as f:
        content = f.read()

    # Pattern to find classes
    class_pattern = r'/\*\*(.+?)\*/\s*(?:export\s+)?class\s+(\w+)'

    for match in re.finditer(class_pattern, content, re.DOTALL):
        jsdoc = match.group(1)
        class_name = match.group(2)

        req_ids = extract_requirement_ids(jsdoc)
        if req_ids:
            implementations.append({
                'file': str(file_path),
                'type': 'class',
                'name': class_name,
                'requirements': req_ids
            })

    # Pattern to find functions
    function_pattern = r'/\*\*(.+?)\*/\s*(?:async\s+)?(?:function\s+)?(\w+)\s*\('

    for match in re.finditer(function_pattern, content, re.DOTALL):
        jsdoc = match.group(1)
        function_name = match.group(2)

        req_ids = extract_requirement_ids(jsdoc)
        if req_ids:
            implementations.append({
                'file': str(file_path),
                'type': 'function',
                'name': function_name,
                'requirements': req_ids
            })

    return implementations
```

---

## Multi-Language Scanner

### Universal Scanner

```python
from pathlib import Path

def scan_codebase(code_dir, languages=['py', 'java', 'js', 'ts']):
    """Scan entire codebase for requirement references."""
    all_implementations = []

    scanners = {
        'py': scan_python_file,
        'java': scan_java_file,
        'js': scan_javascript_file,
        'ts': scan_javascript_file,  # TypeScript uses same patterns
    }

    for lang in languages:
        pattern = f'*.{lang}'
        for file_path in Path(code_dir).rglob(pattern):
            scanner = scanners.get(lang)
            if scanner:
                try:
                    implementations = scanner(file_path)
                    all_implementations.extend(implementations)
                except Exception as e:
                    print(f"Error scanning {file_path}: {e}")

    return all_implementations
```

### With Progress Reporting

```python
from tqdm import tqdm

def scan_codebase_with_progress(code_dir, languages=['py', 'java', 'js']):
    """Scan codebase with progress bar."""
    # Collect all files first
    files_to_scan = []
    for lang in languages:
        files_to_scan.extend(Path(code_dir).rglob(f'*.{lang}'))

    implementations = []

    with tqdm(total=len(files_to_scan), desc="Scanning files") as pbar:
        for file_path in files_to_scan:
            ext = file_path.suffix[1:]  # Remove leading dot
            scanner = get_scanner_for_extension(ext)

            if scanner:
                try:
                    impls = scanner(file_path)
                    implementations.extend(impls)
                except Exception as e:
                    print(f"Error: {file_path}: {e}")

            pbar.update(1)

    return implementations
```

---

## Advanced Patterns

### Requirement Metadata in Code

```python
class UserAuthentication:
    """User authentication module.

    Implements:
        - REQ-AUTH-001: OAuth 2.0 support
        - REQ-AUTH-002: Session management
        - REQ-SECURITY-001: Password hashing

    Related:
        - REQ-DATA-001: User data storage
    """
    pass
```

**Extraction:**
```python
def extract_detailed_requirements(docstring):
    """Extract requirements with metadata."""
    requirements = []

    # Pattern: - REQ-XXX: Description
    pattern = r'-\s*([A-Z]+-[0-9A-Z-]+):\s*(.+?)(?=\n\s*-|\n\n|\Z)'

    for match in re.finditer(pattern, docstring, re.DOTALL):
        requirements.append({
            'id': match.group(1),
            'description': match.group(2).strip()
        })

    return requirements
```

### Conditional Implementation

```python
def process_payment(amount, method):
    """Process payment.

    Implements:
        - REQ-PAY-001 (if method == 'credit_card')
        - REQ-PAY-002 (if method == 'paypal')
    """
    if method == 'credit_card':
        # REQ-PAY-001 implementation
        pass
    elif method == 'paypal':
        # REQ-PAY-002 implementation
        pass
```

### Orphaned Code Detection

```python
def find_orphaned_code(implementations, requirements):
    """Find code that doesn't reference any requirements."""
    orphaned = []

    # Collect all files with implementations
    files_with_reqs = {impl['file'] for impl in implementations}

    # Scan for code without requirement tags
    # (This is a simplified example)
    for impl in implementations:
        if not impl.get('requirements'):
            orphaned.append(impl)

    return orphaned
```

---

## Validation

### Validate Implementation References

```python
def validate_implementation_references(implementations, requirements):
    """Validate that all referenced requirements exist."""
    errors = []
    valid_req_ids = {req['id'] for req in requirements}

    for impl in implementations:
        for req_id in impl.get('requirements', []):
            if req_id not in valid_req_ids:
                errors.append({
                    'file': impl['file'],
                    'element': impl.get('name', impl.get('line', 'unknown')),
                    'error': f"References non-existent requirement: {req_id}"
                })

    return errors
```

---

## Tips

1. **Consistent Keywords**: Enforce standard keywords in code reviews
2. **Auto-completion**: Add IDE snippets for requirement annotations
3. **Linting**: Create custom linter rules to require annotations
4. **Git Hooks**: Check for requirement tags in new code
5. **Documentation**: Document annotation conventions in CONTRIBUTING.md
6. **Regular Scans**: Run scanner on every commit via CI/CD
7. **False Positives**: Filter out test fixtures and example code
