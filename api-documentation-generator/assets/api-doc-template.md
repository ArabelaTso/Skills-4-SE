# API Documentation Template

## Overview

Brief description of what this API does and who it's for.

## Base URL

```
https://api.example.com/v1
```

## Authentication

Describe authentication method (e.g., Bearer token, API key).

**Example:**
```
Authorization: Bearer YOUR_API_TOKEN
```

---

## Endpoints

### [Resource Name]

Brief description of this resource.

#### GET /resource

Retrieve a list of resources.

**Request:**

- **Method:** `GET`
- **Path:** `/resource`
- **Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | integer | No | Page number (default: 1) |
| `limit` | integer | No | Items per page (default: 20) |
| `filter` | string | No | Filter criteria |

**Response:**

- **Status:** `200 OK`
- **Body:**

```json
{
  "data": [
    {
      "id": 1,
      "name": "Example",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

**Example Request:**

```bash
curl -X GET "https://api.example.com/v1/resource?page=1&limit=20" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Example Response:**

```json
{
  "data": [
    {
      "id": 1,
      "name": "Example Resource",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

---

#### POST /resource

Create a new resource.

**Request:**

- **Method:** `POST`
- **Path:** `/resource`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_API_TOKEN`
- **Body:**

```json
{
  "name": "New Resource",
  "description": "Description of the resource"
}
```

**Request Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Name of the resource |
| `description` | string | No | Description |

**Response:**

- **Status:** `201 Created`
- **Headers:**
  - `Location: /resource/123`
- **Body:**

```json
{
  "id": 123,
  "name": "New Resource",
  "description": "Description of the resource",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Example Request:**

```bash
curl -X POST "https://api.example.com/v1/resource" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{
    "name": "New Resource",
    "description": "Description of the resource"
  }'
```

---

#### GET /resource/{id}

Retrieve a specific resource by ID.

**Request:**

- **Method:** `GET`
- **Path:** `/resource/{id}`
- **Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Resource ID |

**Response:**

- **Status:** `200 OK`
- **Body:**

```json
{
  "id": 123,
  "name": "Resource Name",
  "description": "Description",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**

- **Status:** `404 Not Found`
- **Body:**

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}
```

---

#### PUT /resource/{id}

Replace a resource entirely.

**Request:**

- **Method:** `PUT`
- **Path:** `/resource/{id}`
- **Body:**

```json
{
  "name": "Updated Name",
  "description": "Updated description"
}
```

**Response:**

- **Status:** `200 OK`
- **Body:**

```json
{
  "id": 123,
  "name": "Updated Name",
  "description": "Updated description",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

---

#### PATCH /resource/{id}

Partially update a resource.

**Request:**

- **Method:** `PATCH`
- **Path:** `/resource/{id}`
- **Body:**

```json
{
  "description": "New description"
}
```

**Response:**

- **Status:** `200 OK`
- **Body:**

```json
{
  "id": 123,
  "name": "Resource Name",
  "description": "New description",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

---

#### DELETE /resource/{id}

Delete a resource.

**Request:**

- **Method:** `DELETE`
- **Path:** `/resource/{id}`

**Response:**

- **Status:** `204 No Content`
- **Body:** (empty)

---

## Error Responses

All error responses follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": [
      {
        "field": "field_name",
        "message": "Field-specific error message"
      }
    ]
  }
}
```

### Common Error Codes

| Status Code | Error Code | Description |
|-------------|------------|-------------|
| 400 | `BAD_REQUEST` | Invalid request data |
| 401 | `UNAUTHORIZED` | Missing or invalid authentication |
| 403 | `FORBIDDEN` | Insufficient permissions |
| 404 | `NOT_FOUND` | Resource not found |
| 409 | `CONFLICT` | Resource conflict (e.g., duplicate) |
| 422 | `VALIDATION_ERROR` | Validation failed |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server error |

---

## Rate Limiting

API requests are rate-limited.

**Headers:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

**Limits:**
- 1000 requests per hour per API key
- 100 requests per minute per API key

---

## Pagination

Collection endpoints support pagination via query parameters:

- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

**Response includes pagination metadata:**

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

---

## Filtering & Sorting

### Filtering

Use query parameters to filter results:

```
GET /resource?status=active&type=premium
```

### Sorting

Use the `sort` parameter:

```
GET /resource?sort=created_at        # Ascending
GET /resource?sort=-created_at       # Descending
```

---

## Examples

### Complete Example: Creating and Retrieving a Resource

**1. Create a resource:**

```bash
curl -X POST "https://api.example.com/v1/resource" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{
    "name": "My Resource",
    "description": "This is my resource"
  }'
```

**Response:**

```json
{
  "id": 456,
  "name": "My Resource",
  "description": "This is my resource",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**2. Retrieve the resource:**

```bash
curl -X GET "https://api.example.com/v1/resource/456" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Response:**

```json
{
  "id": 456,
  "name": "My Resource",
  "description": "This is my resource",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

## Data Models

### Resource

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique identifier |
| `name` | string | Resource name |
| `description` | string | Resource description |
| `created_at` | datetime | Creation timestamp (ISO 8601) |
| `updated_at` | datetime | Last update timestamp (ISO 8601) |

---

## Webhooks

(If applicable) Document webhook endpoints and payloads.

---

## Changelog

(If applicable) Document API version changes and deprecations.
