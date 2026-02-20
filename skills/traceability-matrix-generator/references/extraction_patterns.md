# Requirement Extraction Patterns

Patterns for parsing requirements from various document formats and sources.

## Table of Contents

1. [Markdown Formats](#markdown-formats)
2. [Issue Tracker Exports](#issue-tracker-exports)
3. [Word Documents](#word-documents)
4. [Excel Spreadsheets](#excel-spreadsheets)
5. [PDF Documents](#pdf-documents)

---

## Markdown Formats

### Heading-Based Requirements

```markdown
## REQ-001: User Authentication
The system shall support user authentication via email and password.

### REQ-002: Password Strength
Passwords must be at least 8 characters with mixed case and numbers.
```

**Extraction Pattern:**
```python
pattern = r'^#+\s*([A-Z]+-[0-9A-Z-]+):\s*(.+?)$'
```

### Numbered List Requirements

```markdown
1. **REQ-AUTH-001**: OAuth 2.0 support required
2. **REQ-AUTH-002**: Session timeout after 30 minutes
3. **REQ-DATA-001**: Encrypt sensitive data at rest
```

**Extraction Pattern:**
```python
pattern = r'^\d+\.\s*\*\*([A-Z]+-[0-9A-Z-]+)\*\*:\s*(.+)$'
```

### Table-Based Requirements

```markdown
| ID | Title | Priority | Status |
|----|-------|----------|--------|
| REQ-001 | User Login | High | Approved |
| REQ-002 | Password Reset | Medium | Draft |
```

**Extraction Pattern:**
```python
# Skip header rows, parse data rows
pattern = r'\|\s*([A-Z]+-[0-9]+)\s*\|\s*(.+?)\s*\|'
```

### User Story Format

```markdown
### US-123: Search Products
**As a** customer
**I want to** search for products by name
**So that** I can find items quickly

**Acceptance Criteria:**
- Search box on homepage
- Auto-complete suggestions
- Results in < 1 second
```

**Extraction Pattern:**
```python
pattern = r'#+\s*(US-[0-9]+):\s*(.+?)\n\*\*As a\*\*\s+(.+?)\n\*\*I want to\*\*\s+(.+?)\n\*\*So that\*\*\s+(.+?)(?:\n|$)'
```

---

## Issue Tracker Exports

### Jira CSV Export

```csv
Issue Key,Summary,Description,Status,Priority
PROJ-123,User Authentication,Implement OAuth login,In Progress,High
PROJ-124,Dashboard UI,Create dashboard view,To Do,Medium
```

**Extraction Script:**
```python
import csv

def extract_from_jira_csv(csv_file):
    requirements = []

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            requirements.append({
                'id': row['Issue Key'],
                'title': row['Summary'],
                'description': row.get('Description', ''),
                'status': row.get('Status', ''),
                'priority': row.get('Priority', ''),
                'type': 'requirement',
                'source': csv_file
            })

    return requirements
```

### GitHub Issues JSON Export

```json
[
  {
    "number": 42,
    "title": "Add user authentication",
    "body": "Implement OAuth 2.0 login",
    "labels": ["feature", "authentication"],
    "state": "open"
  }
]
```

**Extraction Script:**
```python
import json

def extract_from_github_issues(json_file):
    requirements = []

    with open(json_file, 'r') as f:
        issues = json.load(f)

    for issue in issues:
        # Create ID from issue number
        req_id = f"GH-{issue['number']}"

        requirements.append({
            'id': req_id,
            'title': issue['title'],
            'description': issue.get('body', ''),
            'labels': issue.get('labels', []),
            'status': issue.get('state', ''),
            'type': 'requirement',
            'source': json_file
        })

    return requirements
```

---

## Word Documents

### Using python-docx

```python
from docx import Document

def extract_from_word(docx_file):
    """Extract requirements from Word document."""
    requirements = []
    doc = Document(docx_file)

    for para in doc.paragraphs:
        # Check for requirement ID pattern
        match = re.match(r'^([A-Z]+-[0-9A-Z-]+):\s*(.+)$', para.text)
        if match:
            requirements.append({
                'id': match.group(1),
                'title': match.group(2),
                'source': docx_file,
                'type': 'requirement'
            })

    return requirements
```

### Heading-Based Extraction

```python
def extract_from_word_headings(docx_file):
    """Extract requirements from Word document headings."""
    requirements = []
    doc = Document(docx_file)

    for para in doc.paragraphs:
        # Check if paragraph is a heading
        if para.style.name.startswith('Heading'):
            match = re.match(r'^([A-Z]+-[0-9A-Z-]+):\s*(.+)$', para.text)
            if match:
                requirements.append({
                    'id': match.group(1),
                    'title': match.group(2),
                    'level': para.style.name,
                    'source': docx_file,
                    'type': 'requirement'
                })

    return requirements
```

---

## Excel Spreadsheets

### Using openpyxl

```python
from openpyxl import load_workbook

def extract_from_excel(excel_file, sheet_name='Requirements'):
    """Extract requirements from Excel spreadsheet."""
    requirements = []
    wb = load_workbook(excel_file)
    ws = wb[sheet_name]

    # Assume first row is header
    headers = [cell.value for cell in ws[1]]

    # Find column indices
    id_col = headers.index('ID')
    title_col = headers.index('Title')
    desc_col = headers.index('Description') if 'Description' in headers else None

    # Process data rows
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[id_col]:  # Skip empty rows
            req = {
                'id': row[id_col],
                'title': row[title_col],
                'source': excel_file,
                'type': 'requirement'
            }

            if desc_col and row[desc_col]:
                req['description'] = row[desc_col]

            requirements.append(req)

    return requirements
```

---

## PDF Documents

### Using PyPDF2

```python
import PyPDF2
import re

def extract_from_pdf(pdf_file):
    """Extract requirements from PDF document."""
    requirements = []

    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)

        text = ''
        for page in reader.pages:
            text += page.extract_text()

    # Extract requirements using pattern matching
    pattern = r'([A-Z]+-[0-9A-Z-]+):\s*(.+?)(?=\n[A-Z]+-[0-9A-Z-]+:|\Z)'

    for match in re.finditer(pattern, text, re.DOTALL):
        req_id = match.group(1)
        req_text = match.group(2).strip()

        requirements.append({
            'id': req_id,
            'title': req_text.split('\n')[0],  # First line as title
            'description': req_text,
            'source': pdf_file,
            'type': 'requirement'
        })

    return requirements
```

---

## Advanced Patterns

### Requirements with Metadata

```markdown
## REQ-AUTH-001: OAuth 2.0 Support
**Priority:** High
**Status:** Approved
**Owner:** Security Team
**Dependencies:** REQ-DATA-001, REQ-NET-003

The system shall support OAuth 2.0 authentication protocol.
```

**Extraction:**
```python
def extract_with_metadata(file_path):
    requirements = []

    with open(file_path, 'r') as f:
        content = f.read()

    # Pattern to match requirement block
    pattern = r'#+\s*([A-Z]+-[0-9A-Z-]+):\s*(.+?)\n((?:\*\*.+?\*\*:.+?\n)+)(.+?)(?=\n#+|$)'

    for match in re.finditer(pattern, content, re.DOTALL):
        req_id = match.group(1)
        title = match.group(2)
        metadata_block = match.group(3)
        description = match.group(4).strip()

        # Parse metadata
        metadata = {}
        for meta_line in metadata_block.split('\n'):
            meta_match = re.match(r'\*\*(.+?)\*\*:\s*(.+)', meta_line)
            if meta_match:
                metadata[meta_match.group(1)] = meta_match.group(2)

        requirements.append({
            'id': req_id,
            'title': title,
            'description': description,
            'metadata': metadata,
            'type': 'requirement'
        })

    return requirements
```

### Hierarchical Requirements

```markdown
# 1. Authentication (REQ-AUTH)
## 1.1 Login (REQ-AUTH-LOGIN)
### 1.1.1 Email Login (REQ-AUTH-LOGIN-001)
### 1.1.2 Social Login (REQ-AUTH-LOGIN-002)
## 1.2 Password Reset (REQ-AUTH-RESET)
```

**Extraction with Hierarchy:**
```python
def extract_hierarchical(file_path):
    requirements = []

    with open(file_path, 'r') as f:
        lines = f.readlines()

    hierarchy = []

    for line in lines:
        # Count heading level
        heading_match = re.match(r'^(#+)\s*(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)

            # Extract ID if present
            id_match = re.search(r'\(([A-Z]+-[0-9A-Z-]+)\)', text)
            if id_match:
                req_id = id_match.group(1)
                title = re.sub(r'\s*\([A-Z]+-[0-9A-Z-]+\)', '', text).strip()

                # Update hierarchy
                hierarchy = hierarchy[:level-1] + [req_id]

                requirements.append({
                    'id': req_id,
                    'title': title,
                    'level': level,
                    'parent': hierarchy[-2] if len(hierarchy) > 1 else None,
                    'path': ' > '.join(hierarchy),
                    'type': 'requirement'
                })

    return requirements
```

---

## Validation

### Validate Extracted Requirements

```python
def validate_requirements(requirements):
    """Validate extracted requirements."""
    errors = []
    seen_ids = set()

    for req in requirements:
        # Check for required fields
        if not req.get('id'):
            errors.append(f"Missing ID in requirement: {req}")

        if not req.get('title'):
            errors.append(f"Missing title for {req.get('id', 'unknown')}")

        # Check for duplicates
        if req['id'] in seen_ids:
            errors.append(f"Duplicate ID: {req['id']}")
        seen_ids.add(req['id'])

        # Validate ID format
        if not re.match(r'^[A-Z]+-[0-9A-Z-]+$', req['id']):
            errors.append(f"Invalid ID format: {req['id']}")

    return errors
```

---

## Tips

1. **Normalize IDs**: Convert all IDs to uppercase for consistency
2. **Handle Whitespace**: Strip leading/trailing whitespace from extracted text
3. **Preserve Context**: Keep surrounding text for better understanding
4. **Track Source**: Always record which file/line the requirement came from
5. **Validate Early**: Check ID format and uniqueness during extraction
6. **Support Multiple Formats**: Try multiple patterns if first fails
7. **Log Extraction**: Keep track of what was extracted vs skipped
