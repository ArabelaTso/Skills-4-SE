# API Design Best Practices

## REST API Principles

### Resource Naming
- Use **plural nouns** for collections: `/users`, `/products`, `/orders`
- Use **singular nouns** for single resources: `/users/{id}`, `/profile`
- Use **lowercase** and **hyphens** for multi-word resources: `/user-profiles`, `/order-items`
- Avoid verbs in URLs (except for actions that don't fit CRUD): `/convert`, `/search`

### HTTP Methods
- **GET**: Retrieve resource(s) - idempotent, cacheable
- **POST**: Create new resource - not idempotent
- **PUT**: Replace entire resource - idempotent
- **PATCH**: Partial update - not necessarily idempotent
- **DELETE**: Remove resource - idempotent

### Endpoint Patterns

**Collections:**
```
GET    /users           # List all users
POST   /users           # Create new user
GET    /users/{id}      # Get specific user
PUT    /users/{id}      # Replace user
PATCH  /users/{id}      # Update user fields
DELETE /users/{id}      # Delete user
```

**Nested resources:**
```
GET    /users/{id}/orders           # List user's orders
POST   /users/{id}/orders           # Create order for user
GET    /users/{id}/orders/{orderId} # Get specific order
```

**Actions that don't fit CRUD:**
```
POST   /users/{id}/activate         # Activate user
POST   /orders/{id}/cancel          # Cancel order
POST   /documents/{id}/convert      # Convert document
```

## Request Parameters

### Query Parameters
Use for filtering, sorting, pagination, and search:

```
GET /users?status=active&role=admin          # Filtering
GET /users?sort=created_at&order=desc        # Sorting
GET /users?page=2&limit=50                   # Pagination
GET /users?search=john                       # Search
GET /users?fields=id,name,email              # Field selection
```

### Path Parameters
Use for resource identification:
```
GET /users/{userId}
GET /users/{userId}/orders/{orderId}
```

### Request Body
Use for creating/updating resources:
```json
POST /users
{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "admin"
}
```

## Response Formats

### Successful Responses

**Single resource:**
```json
GET /users/123
200 OK
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Collection with pagination:**
```json
GET /users?page=1&limit=20
200 OK
{
  "data": [
    { "id": 1, "name": "User 1" },
    { "id": 2, "name": "User 2" }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

**Create response:**
```json
POST /users
201 Created
Location: /users/123
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Error Responses

**Standard error structure:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid"
      }
    ]
  }
}
```

**Common HTTP status codes:**
- **200 OK**: Successful GET, PUT, PATCH, DELETE
- **201 Created**: Successful POST creating resource
- **204 No Content**: Successful DELETE with no body
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource doesn't exist
- **409 Conflict**: Resource conflict (e.g., duplicate)
- **422 Unprocessable Entity**: Validation errors
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

## Authentication & Authorization

### Common patterns:
```
Authorization: Bearer <jwt-token>          # JWT tokens
Authorization: Basic <base64-credentials>  # Basic auth
X-API-Key: <api-key>                      # API keys
```

## Versioning

### URL versioning (most common):
```
GET /v1/users
GET /v2/users
```

### Header versioning:
```
Accept: application/vnd.api.v1+json
```

### Query parameter versioning:
```
GET /users?version=1
```

## Pagination Strategies

### Offset-based:
```
GET /users?offset=20&limit=10
```

### Page-based:
```
GET /users?page=3&limit=10
```

### Cursor-based (for large datasets):
```
GET /users?cursor=eyJpZCI6MTIzfQ&limit=10
```

## Filtering & Sorting

### Filtering:
```
GET /users?status=active&role=admin
GET /users?created_after=2024-01-01
GET /users?age_gt=18&age_lt=65
```

### Sorting:
```
GET /users?sort=created_at             # Ascending
GET /users?sort=-created_at            # Descending (minus prefix)
GET /users?sort=name,created_at        # Multiple fields
```

## Rate Limiting

### Response headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## HATEOAS (Hypermedia)

Include links to related resources:
```json
{
  "id": 123,
  "name": "John Doe",
  "_links": {
    "self": { "href": "/users/123" },
    "orders": { "href": "/users/123/orders" },
    "profile": { "href": "/users/123/profile" }
  }
}
```

## Data Types

### Common field types:
- **String**: Text data, emails, URLs
- **Integer**: Whole numbers, IDs, counts
- **Float/Decimal**: Prices, percentages, measurements
- **Boolean**: true/false flags
- **Date**: ISO 8601 format (e.g., "2024-01-15")
- **DateTime**: ISO 8601 with time (e.g., "2024-01-15T10:30:00Z")
- **Array**: Lists of items
- **Object**: Nested structures
- **Enum**: Fixed set of values

### Nullable vs Required:
- Mark fields as `required` or `optional`
- Use `null` for absent optional values
- Avoid returning `null` for required fields

## Security Best Practices

1. **Always use HTTPS** in production
2. **Validate all inputs** (type, format, range)
3. **Sanitize outputs** to prevent XSS
4. **Use authentication** for protected resources
5. **Implement rate limiting** to prevent abuse
6. **Don't expose sensitive data** in responses
7. **Use proper authorization** (role-based, resource-based)
8. **Log security events** (failed auth, rate limits)

## Idempotency

Safe methods (GET, HEAD, OPTIONS) and idempotent methods (PUT, DELETE) can be retried without side effects.

For POST requests that should be idempotent:
```
POST /orders
Idempotency-Key: uuid-12345
```

## Common Mistakes to Avoid

1. ❌ Using verbs in URLs: `/getUsers`, `/createOrder`
2. ❌ Inconsistent naming: `/user` vs `/users`
3. ❌ Ignoring HTTP methods: using only GET and POST
4. ❌ Returning wrong status codes
5. ❌ Not versioning APIs
6. ❌ Inconsistent error formats
7. ❌ Missing pagination for collections
8. ❌ Not handling partial updates (use PATCH)
9. ❌ Exposing internal IDs without validation
10. ❌ Not documenting breaking changes
