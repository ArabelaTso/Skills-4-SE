---
name: api-documentation-generator
description: Generate comprehensive API documentation from repository sources including OpenAPI specs, code comments, docstrings, and existing documentation. Use when documenting APIs, creating API reference guides, or summarizing API functionality from codebases. Extracts endpoint details, request/response schemas, authentication methods, and generates code examples. Triggers when users ask to document APIs, generate API docs, create API reference, or summarize API endpoints from a repository.
---

# API Documentation Generator

## Overview

Analyze a repository to extract and generate comprehensive API documentation, including endpoints, request/response schemas, authentication, and usage examples organized in a clear, multi-file structure.

## Workflow

### 1. Discover API Information Sources

Scan the repository to identify all sources of API information:

**Primary sources (in priority order):**

1. **OpenAPI/Swagger specifications** (`.yaml`, `.yml`, `.json`)
   - Look in: root directory, `/docs`, `/api`, `/spec`, `/openapi`
   - Files named: `openapi.yaml`, `swagger.json`, `api-spec.yaml`, etc.

2. **Code files with docstrings/comments**
   - Python: Flask/FastAPI route decorators, docstrings
   - JavaScript/TypeScript: Express routes, JSDoc comments
   - Java: Spring annotations, Javadoc
   - Go: HTTP handler comments
   - Ruby: Rails routes, YARD comments

3. **Existing documentation**
   - Markdown files in `/docs`, `/documentation`, `/api-docs`
   - README files with API sections
   - Wiki pages or doc site content

4. **Configuration files**
   - `routes.rb`, `urls.py`, `routes.js`
   - API gateway configurations

**Discovery approach:**

```bash
# Find OpenAPI specs
find . -name "openapi.*" -o -name "swagger.*" -o -name "*api-spec*"

# Find API route definitions
grep -r "@app.route\|@router\|app.get\|app.post" --include="*.py" --include="*.js"

# Find documentation
find . -path "*/docs/*" -name "*.md" -o -path "*/api/*" -name "*.md"
```

### 2. Extract API Information

Based on discovered sources, extract key information:

#### From OpenAPI Specs

Parse YAML/JSON to extract:
- Base URL and server information
- All paths and operations (GET, POST, PUT, PATCH, DELETE)
- Request parameters (path, query, header, body)
- Response schemas and status codes
- Authentication/security schemes
- Data models/schemas
- Tags and operation groupings

#### From Code Comments/Docstrings

Look for patterns like:

**Python (FastAPI/Flask):**
```python
@app.post("/users")
async def create_user(user: UserCreate):
    """
    Create a new user.

    Args:
        user: User creation data

    Returns:
        Created user object
    """
```

**JavaScript (Express):**
```javascript
/**
 * GET /users
 * List all users
 * @param {number} page - Page number
 * @param {number} limit - Items per page
 * @returns {Array<User>} List of users
 */
app.get('/users', (req, res) => { ... })
```

Extract:
- HTTP method and path
- Description from docstring/comment
- Parameters and types
- Return types
- Example usage if present

#### From Existing Documentation

Parse markdown files to extract:
- Endpoint descriptions
- Request/response examples
- Authentication details
- Rate limiting information
- Error codes

### 3. Organize Documentation Structure

Create a multi-file documentation structure organized by resource or API area:

```
docs/
├── README.md                 # Overview, authentication, getting started
├── endpoints/
│   ├── users.md             # User-related endpoints
│   ├── products.md          # Product-related endpoints
│   ├── orders.md            # Order-related endpoints
│   └── ...
├── models/
│   └── schemas.md           # Data models and schemas
├── errors.md                # Error codes and handling
└── examples.md              # Complete usage examples
```

**Grouping strategy:**
- Group by resource (users, products, orders)
- Group by OpenAPI tags if available
- Group by URL prefix if no tags
- Keep authentication, errors, and models separate

### 4. Generate Documentation Files

For each file, use the template from [assets/api-doc-template.md](assets/api-doc-template.md) as a guide.

#### README.md (Main Overview)

```markdown
# API Documentation

## Overview
[Brief description of the API and its purpose]

## Base URL
https://api.example.com/v1

## Authentication
[Describe auth method: Bearer tokens, API keys, OAuth2]

## Quick Start
[Simple example showing how to make first API call]

## Endpoints

- [Users](endpoints/users.md) - User management endpoints
- [Products](endpoints/products.md) - Product catalog endpoints
- [Orders](endpoints/orders.md) - Order processing endpoints

## Resources

- [Data Models](models/schemas.md) - Request/response schemas
- [Errors](errors.md) - Error codes and handling
- [Examples](examples.md) - Complete usage examples

## Rate Limiting
[Rate limit details if applicable]

## Versioning
[API versioning strategy if applicable]
```

#### Endpoint Files (e.g., `endpoints/users.md`)

For each endpoint, document:

**Endpoint header:**
```markdown
### POST /users

Create a new user account.
```

**Request details:**
```markdown
**Request:**

- **Method:** `POST`
- **Path:** `/users`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_TOKEN`

**Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | User's full name |
| email | string | Yes | User's email address |
| role | string | No | User role (default: user) |

**Example:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "admin"
}
```
```

**Response details:**
```markdown
**Response:**

- **Status:** `201 Created`
- **Headers:**
  - `Location: /users/123`

**Body:**

```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "admin",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**

- `400 Bad Request` - Invalid input data
- `409 Conflict` - Email already exists
```

**Code examples:**
```markdown
**Example Request:**

```bash
curl -X POST "https://api.example.com/v1/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

```python
import requests

response = requests.post(
    "https://api.example.com/v1/users",
    headers={"Authorization": "Bearer YOUR_TOKEN"},
    json={
        "name": "John Doe",
        "email": "john@example.com"
    }
)

user = response.json()
print(f"Created user: {user['id']}")
```
```

#### Data Models File (`models/schemas.md`)

Document all data structures:

```markdown
# Data Models

## User

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| name | string | User's full name |
| email | string | User's email address |
| role | string | User role (admin, user, guest) |
| created_at | datetime | Account creation timestamp |
| updated_at | datetime | Last update timestamp |

**Example:**

```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```
```

#### Error Reference (`errors.md`)

```markdown
# Error Handling

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message"
  }
}
```

## Error Codes

| Status | Code | Description |
|--------|------|-------------|
| 400 | BAD_REQUEST | Invalid request data |
| 401 | UNAUTHORIZED | Missing/invalid auth |
| 403 | FORBIDDEN | Insufficient permissions |
| 404 | NOT_FOUND | Resource not found |
| 409 | CONFLICT | Resource conflict |
| 422 | VALIDATION_ERROR | Validation failed |
| 429 | RATE_LIMIT_EXCEEDED | Too many requests |
| 500 | INTERNAL_ERROR | Server error |
```

### 5. Include Code Examples

For major use cases, provide complete code examples:

```markdown
# Examples

## Creating and Managing Users

### 1. Create a User

```bash
curl -X POST "https://api.example.com/v1/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

```python
import requests

# Create user
response = requests.post(
    "https://api.example.com/v1/users",
    headers={"Authorization": "Bearer YOUR_TOKEN"},
    json={"name": "John Doe", "email": "john@example.com"}
)

user_id = response.json()["id"]
```

### 2. Retrieve the User

```python
# Get user details
response = requests.get(
    f"https://api.example.com/v1/users/{user_id}",
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)

user = response.json()
print(f"User: {user['name']} ({user['email']})")
```
```

### 6. Handle Special Cases

#### No OpenAPI Spec Available

When no OpenAPI spec exists:
1. Thoroughly scan code files for route definitions
2. Extract information from docstrings and comments
3. Infer request/response structure from code
4. Note assumptions and recommend validation

#### Multiple API Versions

When multiple versions exist:
1. Document each version separately
2. Note differences between versions
3. Indicate which version is recommended
4. Document migration path if applicable

#### Incomplete Information

When information is missing:
1. Document what's known
2. Mark unknown sections with `[To be documented]`
3. Provide best-effort inferences with `(inferred from code)`
4. Suggest improvements to add missing details

#### GraphQL APIs

For GraphQL:
1. Extract schema from `.graphql` files or introspection
2. Document queries, mutations, and subscriptions
3. Include example queries with variables
4. Document input types and return types

### 7. Quality Checks

Before finalizing documentation:

- ✅ All endpoints documented with HTTP method and path
- ✅ Request parameters clearly specified (type, required/optional)
- ✅ Response schemas documented with examples
- ✅ Authentication method explained
- ✅ Error responses documented
- ✅ Code examples provided for main operations
- ✅ Files organized logically by resource
- ✅ Links between files work correctly
- ✅ Consistent formatting throughout
- ✅ Base URL and versioning strategy documented

## Example Workflows

### Example 1: Repository with OpenAPI Spec

**User request:**
> "Generate API documentation for this repository"

**Response approach:**

1. Search for OpenAPI spec files
2. Find `openapi.yaml` in `/docs` directory
3. Parse the spec to extract all endpoints, schemas, and auth
4. Organize by tags into separate files
5. Generate README with overview and navigation
6. Create endpoint files for each tag
7. Create schemas.md with all data models
8. Create errors.md with error codes
9. Add code examples in curl and Python

### Example 2: Flask API Without Spec

**User request:**
> "Document the API endpoints in this Flask application"

**Response approach:**

1. Search for Flask route decorators (`@app.route`, `@blueprint.route`)
2. Extract endpoints from route definitions
3. Parse docstrings for descriptions and parameter info
4. Infer request/response types from function signatures and code
5. Organize endpoints by blueprint or URL prefix
6. Generate documentation files
7. Note inferred information with disclaimers
8. Suggest creating OpenAPI spec for better docs

### Example 3: Multiple Sources

**User request:**
> "Summarize the API documentation from all available sources"

**Response approach:**

1. Find OpenAPI spec for base structure
2. Find existing markdown docs for additional context
3. Scan code for endpoints not in spec
4. Merge information from all sources
5. Prioritize OpenAPI spec for conflicts
6. Add code-derived info where spec is incomplete
7. Generate unified documentation
8. Note sources for each piece of information

## Tips for Effective Documentation

**Be comprehensive but concise:**
- Include all necessary details
- Avoid redundancy across files
- Use tables for structured data
- Use code blocks for examples

**Use consistent formatting:**
- Same structure for all endpoint docs
- Consistent naming (camelCase vs snake_case)
- Consistent status code documentation
- Consistent example format

**Make it navigable:**
- Clear table of contents in README
- Links between related sections
- Organized by resource or feature area
- Separate concerns (auth, errors, models)

**Provide context:**
- Explain what each endpoint does and why
- Show realistic use cases
- Include complete working examples
- Document edge cases and limitations

**Keep it current:**
- Extract from source of truth (code or spec)
- Note generated date
- Provide instructions for regenerating
- Flag areas needing manual review

## Template

Use the template in [assets/api-doc-template.md](assets/api-doc-template.md) as a starting point for each documentation file. Adapt the structure based on the specific API being documented.
