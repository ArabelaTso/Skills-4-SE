---
name: traceability-matrix-generator
description: >
  Builds traceability matrices connecting requirements to design documents to source code
  implementation, tracking the complete development lifecycle. Use when you need to verify
  implementation completeness, ensure all requirements are implemented in code, generate
  compliance documentation, audit requirement coverage, identify orphaned code, or create
  traceability reports for stakeholders. Supports parsing requirements from Markdown, Word,
  and PDFs; extracting design from architecture docs and API specs; and scanning source code
  for implementations. Outputs to Markdown tables, Excel/CSV, and HTML visualizations.
---

# Traceability Matrix Generator

Build comprehensive traceability matrices linking requirements → design → implementation across the software development lifecycle.

## What is a Traceability Matrix?

A traceability matrix documents relationships between:
- **Requirements**: What the system must do (user stories, specs, features)
- **Design**: How the system will be structured (architecture, APIs, components)
- **Implementation**: Where requirements are coded (functions, classes, modules)

**Benefits:**
- Ensure all requirements are implemented
- Identify missing implementations or tests
- Support compliance and auditing
- Track impact of requirement changes
- Find orphaned code without requirements

## Workflow

### Step 1: Identify and Collect Artifacts

Gather all traceability sources from the project.

**Requirements Sources:**
- `requirements.md`, `REQUIREMENTS.txt`
- User story documents
- Issue tracker exports (Jira, GitHub Issues)
- Product requirement documents (PRDs)
- Feature specifications

**Design Sources:**
- `DESIGN.md`, architecture documents
- API specifications (OpenAPI, Swagger)
- Database schemas
- UML diagrams, architecture diagrams
- Design decision records (ADRs)

**Implementation Sources:**
- Source code files (`*.py`, `*.java`, `*.js`, etc.)
- Module docstrings
- Function/class comments with requirement IDs
- Configuration files

**Checklist:**
- [ ] Locate requirements documents
- [ ] Find design documentation
- [ ] Identify source code directories
- [ ] Check for existing ID/tagging conventions
- [ ] Verify file access and permissions

### Step 2: Extract Requirements

Parse requirements and assign unique identifiers.

**Common Requirement Formats:**

**Markdown with IDs:**
```markdown
## REQ-001: User Authentication
The system shall allow users to log in with email and password.

## REQ-002: Password Reset
Users shall be able to reset forgotten passwords via email.
```

**User Stories:**
```markdown
### US-123: As a user, I want to search products
So that I can find items quickly

**Acceptance Criteria:**
- Search box on homepage
- Results display in < 1 second
- Filter by category
```

**Numbered Lists:**
```markdown
1. **REQ-AUTH-001**: System must support OAuth 2.0
2. **REQ-AUTH-002**: Sessions expire after 24 hours
3. **REQ-DATA-001**: Data must be encrypted at rest
```

**Extraction Script (Python):**

```python
import re
from pathlib import Path

def extract_requirements(file_path):
    """Extract requirements with IDs from markdown file."""
    requirements = []

    with open(file_path, 'r') as f:
        content = f.read()

    # Pattern: REQ-XXX or US-XXX or similar
    pattern = r'^#+\s*([A-Z]+-[A-Z0-9-]+):\s*(.+?)$'

    for match in re.finditer(pattern, content, re.MULTILINE):
        req_id = match.group(1)
        req_title = match.group(2)

        requirements.append({
            'id': req_id,
            'title': req_title,
            'source': file_path.name,
            'type': 'requirement'
        })

    return requirements

# Usage
reqs = extract_requirements(Path('requirements.md'))
for req in reqs:
    print(f"{req['id']}: {req['title']}")
```

**Manual Extraction:**

If documents lack IDs, assign them:

```
Original: "Users can filter search results"
→ Assign: REQ-SEARCH-001: Users can filter search results
```

For detailed requirement extraction patterns, see [references/extraction_patterns.md](references/extraction_patterns.md).

### Step 3: Extract Design Artifacts

Identify design elements and link to requirements.

**Design Linking Patterns:**

**Explicit References in Design Docs:**
```markdown
## Authentication Service (REQ-001, REQ-002)

**Architecture:**
- OAuth 2.0 provider integration (REQ-AUTH-001)
- Session management module (REQ-AUTH-002)
- Password reset workflow (REQ-002)

**API Endpoints:**
- `POST /auth/login` - Implements REQ-001
- `POST /auth/reset` - Implements REQ-002
```

**API Specifications:**
```yaml
# openapi.yaml
paths:
  /auth/login:
    post:
      summary: User login endpoint
      x-requirements: [REQ-001, REQ-AUTH-001]
      description: Implements user authentication
```

**Architecture Diagrams:**
```markdown
[Component Diagram]
- AuthService → Implements REQ-001, REQ-002
- UserDatabase → Supports REQ-DATA-001
- EmailService → Enables REQ-002
```

**Extraction Example:**

```python
def extract_design_links(design_file):
    """Extract design artifacts and linked requirements."""
    design_artifacts = []

    with open(design_file, 'r') as f:
        content = f.read()

    # Find headers with requirement references
    pattern = r'^#+\s*(.+?)\s*\((.+?)\)$'

    for match in re.finditer(pattern, content, re.MULTILINE):
        artifact_name = match.group(1)
        req_refs = match.group(2)

        # Parse requirement IDs
        req_ids = re.findall(r'[A-Z]+-[A-Z0-9-]+', req_refs)

        design_artifacts.append({
            'name': artifact_name,
            'requirements': req_ids,
            'source': design_file.name,
            'type': 'design'
        })

    return design_artifacts
```

### Step 4: Scan Implementation

Search source code for requirement references.

**Code Annotation Patterns:**

**Docstrings (Python):**
```python
def authenticate_user(email, password):
    """Authenticate user credentials.

    Implements: REQ-001, REQ-AUTH-001

    Args:
        email: User email address
        password: User password

    Returns:
        Authentication token if successful
    """
    # Implementation...
```

**Comments (Java):**
```java
/**
 * User authentication service
 * @implements REQ-001 User login
 * @implements REQ-AUTH-001 OAuth support
 */
public class AuthenticationService {
    // Implementation...
}
```

**Comments (JavaScript):**
```javascript
/**
 * Password reset functionality
 * Implements: REQ-002
 */
function resetPassword(email) {
    // Implementation...
}
```

**Scanning Script:**

```python
def scan_code_for_requirements(code_dir):
    """Scan source code for requirement references."""
    implementations = []

    for file_path in Path(code_dir).rglob('*.py'):
        with open(file_path, 'r') as f:
            content = f.read()

        # Find requirement references in comments/docstrings
        matches = re.finditer(
            r'(?:Implements?|Satisfies|Covers):\s*([A-Z]+-[A-Z0-9-]+(?:,\s*[A-Z]+-[A-Z0-9-]+)*)',
            content,
            re.IGNORECASE
        )

        for match in matches:
            req_ids = [r.strip() for r in match.group(1).split(',')]

            # Find containing function/class
            lines_before = content[:match.start()].split('\n')
            for i in range(len(lines_before) - 1, -1, -1):
                if 'def ' in lines_before[i] or 'class ' in lines_before[i]:
                    code_element = lines_before[i].strip()
                    break
            else:
                code_element = "Unknown"

            implementations.append({
                'file': str(file_path),
                'element': code_element,
                'requirements': req_ids,
                'type': 'implementation'
            })

    return implementations
```

For comprehensive code scanning patterns, see [references/code_scanning.md](references/code_scanning.md).

### Step 5: Build the Traceability Matrix

Combine all extracted data into a structured matrix.

**Data Structure:**

```python
traceability_matrix = {
    'REQ-001': {
        'requirement': {
            'id': 'REQ-001',
            'title': 'User Authentication',
            'source': 'requirements.md'
        },
        'design': [
            {
                'name': 'Authentication Service',
                'source': 'design.md'
            }
        ],
        'implementation': [
            {
                'file': 'auth/service.py',
                'element': 'def authenticate_user()'
            }
        ]
    },
    # ... more requirements
}
```

**Building Script:**

```python
def build_traceability_matrix(requirements, design_artifacts, implementations):
    """Build complete traceability matrix."""
    matrix = {}

    # Initialize with requirements
    for req in requirements:
        matrix[req['id']] = {
            'requirement': req,
            'design': [],
            'implementation': []
        }

    # Link design artifacts
    for design in design_artifacts:
        for req_id in design.get('requirements', []):
            if req_id in matrix:
                matrix[req_id]['design'].append(design)

    # Link implementations
    for impl in implementations:
        for req_id in impl.get('requirements', []):
            if req_id in matrix:
                matrix[req_id]['implementation'].append(impl)

    return matrix
```

### Step 6: Generate Output Formats

Export matrix in multiple formats for different audiences.

**Markdown Table:**

```markdown
# Traceability Matrix

| Requirement | Title | Design | Implementation | Status |
|-------------|-------|--------|----------------|--------|
| REQ-001 | User Authentication | Authentication Service | auth/service.py::authenticate_user() | ✓ Complete |
| REQ-002 | Password Reset | Auth Service | auth/service.py::reset_password() | ✓ Complete |
| REQ-003 | Data Encryption | - | - | ⚠ Missing |
```

**Generation Script:**

```python
def generate_markdown_table(matrix):
    """Generate markdown traceability table."""
    lines = [
        "# Traceability Matrix\n",
        "| Requirement | Title | Design | Implementation | Status |",
        "|-------------|-------|--------|----------------|--------|"
    ]

    for req_id, data in sorted(matrix.items()):
        req = data['requirement']
        design = ', '.join([d['name'] for d in data['design']]) or '-'
        impl = ', '.join([f"{i['file']}::{i['element']}" for i in data['implementation']]) or '-'

        # Determine status
        if data['design'] and data['implementation']:
            status = '✓ Complete'
        elif data['design'] or data['implementation']:
            status = '⚠ Partial'
        else:
            status = '❌ Missing'

        lines.append(f"| {req_id} | {req['title']} | {design} | {impl} | {status} |")

    return '\n'.join(lines)
```

**CSV Export:**

```python
import csv

def generate_csv(matrix, output_file):
    """Generate CSV traceability matrix."""
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'Requirement ID',
            'Title',
            'Source',
            'Design Artifacts',
            'Implementation Files',
            'Status'
        ])

        # Data rows
        for req_id, data in sorted(matrix.items()):
            req = data['requirement']
            design_str = '; '.join([d['name'] for d in data['design']])
            impl_str = '; '.join([f"{i['file']}" for i in data['implementation']])

            if data['design'] and data['implementation']:
                status = 'Complete'
            elif data['design'] or data['implementation']:
                status = 'Partial'
            else:
                status = 'Missing'

            writer.writerow([
                req_id,
                req['title'],
                req['source'],
                design_str,
                impl_str,
                status
            ])
```

**HTML Interactive Visualization:**

```python
def generate_html_visualization(matrix, output_file):
    """Generate interactive HTML traceability matrix."""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Traceability Matrix</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .complete { color: green; }
        .partial { color: orange; }
        .missing { color: red; }
        .filter { margin: 20px 0; }
    </style>
</head>
<body>
    <h1>Traceability Matrix</h1>

    <div class="filter">
        <label>Filter by status:</label>
        <select id="statusFilter" onchange="filterTable()">
            <option value="all">All</option>
            <option value="complete">Complete</option>
            <option value="partial">Partial</option>
            <option value="missing">Missing</option>
        </select>
    </div>

    <table id="matrixTable">
        <thead>
            <tr>
                <th>Requirement</th>
                <th>Title</th>
                <th>Design</th>
                <th>Implementation</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
"""

    for req_id, data in sorted(matrix.items()):
        req = data['requirement']
        design = '<br>'.join([d['name'] for d in data['design']]) or '-'
        impl = '<br>'.join([f"{i['file']}" for i in data['implementation']]) or '-'

        if data['design'] and data['implementation']:
            status_class = 'complete'
            status_text = '✓ Complete'
        elif data['design'] or data['implementation']:
            status_class = 'partial'
            status_text = '⚠ Partial'
        else:
            status_class = 'missing'
            status_text = '❌ Missing'

        html += f"""
            <tr class="{status_class}">
                <td>{req_id}</td>
                <td>{req['title']}</td>
                <td>{design}</td>
                <td>{impl}</td>
                <td class="{status_class}">{status_text}</td>
            </tr>
"""

    html += """
        </tbody>
    </table>

    <script>
        function filterTable() {
            var filter = document.getElementById('statusFilter').value;
            var rows = document.querySelectorAll('#matrixTable tbody tr');

            rows.forEach(function(row) {
                if (filter === 'all' || row.classList.contains(filter)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""

    with open(output_file, 'w') as f:
        f.write(html)
```

### Step 7: Analyze and Report Gaps

Identify incomplete traceability and generate recommendations.

**Gap Analysis:**

```python
def analyze_gaps(matrix):
    """Identify gaps in traceability."""
    gaps = {
        'missing_design': [],      # Requirements without design
        'missing_implementation': [], # Requirements without code
        'complete': [],            # Fully traced requirements
        'orphaned_code': []        # Code without requirements (if tracked)
    }

    for req_id, data in matrix.items():
        req = data['requirement']

        if not data['design'] and not data['implementation']:
            # Completely untraced
            gaps['missing_design'].append(req_id)
            gaps['missing_implementation'].append(req_id)
        elif not data['design']:
            gaps['missing_design'].append(req_id)
        elif not data['implementation']:
            gaps['missing_implementation'].append(req_id)
        else:
            gaps['complete'].append(req_id)

    return gaps

def generate_gap_report(gaps):
    """Generate gap analysis report."""
    report = ["# Traceability Gap Analysis\n"]

    report.append(f"## Summary")
    report.append(f"- ✓ Complete: {len(gaps['complete'])} requirements")
    report.append(f"- ⚠ Missing Design: {len(gaps['missing_design'])} requirements")
    report.append(f"- ⚠ Missing Implementation: {len(gaps['missing_implementation'])} requirements\n")

    if gaps['missing_design']:
        report.append("## Requirements Without Design")
        for req_id in gaps['missing_design']:
            report.append(f"- {req_id}")
        report.append("")

    if gaps['missing_implementation']:
        report.append("## Requirements Without Implementation")
        for req_id in gaps['missing_implementation']:
            report.append(f"- {req_id}")
        report.append("")

    report.append("## Recommendations")
    if gaps['missing_design']:
        report.append("- Create design documents for undesigned requirements")
    if gaps['missing_implementation']:
        report.append("- Implement missing requirements or update requirement status")

    return '\n'.join(report)
```

**Coverage Metrics:**

```python
def calculate_coverage(matrix):
    """Calculate traceability coverage metrics."""
    total = len(matrix)
    with_design = sum(1 for data in matrix.values() if data['design'])
    with_impl = sum(1 for data in matrix.values() if data['implementation'])
    complete = sum(1 for data in matrix.values()
                   if data['design'] and data['implementation'])

    return {
        'total_requirements': total,
        'design_coverage': (with_design / total * 100) if total > 0 else 0,
        'implementation_coverage': (with_impl / total * 100) if total > 0 else 0,
        'complete_coverage': (complete / total * 100) if total > 0 else 0
    }
```

## Complete Example

```python
from pathlib import Path

# Step 1: Collect artifacts
req_file = Path('requirements.md')
design_file = Path('design.md')
code_dir = Path('src/')

# Step 2-4: Extract data
requirements = extract_requirements(req_file)
design_artifacts = extract_design_links(design_file)
implementations = scan_code_for_requirements(code_dir)

# Step 5: Build matrix
matrix = build_traceability_matrix(requirements, design_artifacts, implementations)

# Step 6: Generate outputs
with open('traceability.md', 'w') as f:
    f.write(generate_markdown_table(matrix))

generate_csv(matrix, 'traceability.csv')
generate_html_visualization(matrix, 'traceability.html')

# Step 7: Analyze gaps
gaps = analyze_gaps(matrix)
coverage = calculate_coverage(matrix)

print(f"Coverage: {coverage['complete_coverage']:.1f}% complete")
print(generate_gap_report(gaps))
```

## Tips

1. **Establish ID conventions early**: Use consistent prefixes (REQ-, US-, FEAT-)
2. **Automate where possible**: Use scripts for large codebases
3. **Keep matrix updated**: Regenerate when requirements or code changes
4. **Tag code consistently**: Enforce requirement references in code reviews
5. **Start simple**: Begin with requirements→implementation, add design later
6. **Use version control**: Track matrix changes alongside code changes
7. **Integrate with CI/CD**: Auto-generate matrix on commits

## Common Use Cases

**Compliance Auditing:**
- Demonstrate all requirements are implemented
- Provide evidence for regulatory reviews
- Track safety-critical requirement coverage

**Impact Analysis:**
- Identify affected code when requirements change
- Find which tests need updating
- Assess scope of feature modifications

**Quality Assurance:**
- Verify implementation completeness
- Ensure no orphaned code
- Track requirement fulfillment

## References

For detailed information:
- [references/extraction_patterns.md](references/extraction_patterns.md) - Requirement parsing patterns for various formats
- [references/code_scanning.md](references/code_scanning.md) - Code annotation conventions and scanning techniques
