# OpenAPI Patterns and Best Practices

## REST API Design Patterns

### CRUD Operations

Standard HTTP methods for resource operations:

```yaml
paths:
  /users:
    get:
      summary: List users
      parameters:
        - in: query
          name: page
          schema:
            type: integer
            minimum: 1
            default: 1
        - in: query
          name: limit
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/PaginationResponse'
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'

  /users/{userId}:
    parameters:
      - in: path
        name: userId
        required: true
        schema:
          type: string
          format: uuid
    get:
      summary: Get user by ID
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'
    put:
      summary: Update user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: User updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'
    patch:
      summary: Partially update user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchUserRequest'
      responses:
        '200':
          description: User updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
    delete:
      summary: Delete user
      responses:
        '204':
          description: User deleted
        '404':
          $ref: '#/components/responses/NotFound'
```

### Nested Resources

```yaml
paths:
  /users/{userId}/posts:
    parameters:
      - in: path
        name: userId
        required: true
        schema:
          type: string
    get:
      summary: List user's posts
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Post'
    post:
      summary: Create post for user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreatePostRequest'
      responses:
        '201':
          description: Post created
```

### Filtering and Sorting

```yaml
paths:
  /products:
    get:
      summary: List products with filtering and sorting
      parameters:
        - in: query
          name: category
          schema:
            type: string
          description: Filter by category
        - in: query
          name: minPrice
          schema:
            type: number
          description: Minimum price filter
        - in: query
          name: maxPrice
          schema:
            type: number
          description: Maximum price filter
        - in: query
          name: sortBy
          schema:
            type: string
            enum: [name, price, createdAt]
            default: createdAt
        - in: query
          name: sortOrder
          schema:
            type: string
            enum: [asc, desc]
            default: desc
        - in: query
          name: search
          schema:
            type: string
          description: Search query
      responses:
        '200':
          description: Successful response
```

### Bulk Operations

```yaml
paths:
  /users/bulk:
    post:
      summary: Create multiple users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - users
              properties:
                users:
                  type: array
                  minItems: 1
                  maxItems: 100
                  items:
                    $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: Users created
          content:
            application/json:
              schema:
                type: object
                properties:
                  created:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  failed:
                    type: array
                    items:
                      type: object
                      properties:
                        index:
                          type: integer
                        error:
                          $ref: '#/components/schemas/Error'
    delete:
      summary: Delete multiple users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - ids
              properties:
                ids:
                  type: array
                  minItems: 1
                  items:
                    type: string
      responses:
        '200':
          description: Deletion results
```

### Action Endpoints (Non-CRUD)

```yaml
paths:
  /users/{userId}/activate:
    post:
      summary: Activate user account
      parameters:
        - in: path
          name: userId
          required: true
          schema:
            type: string
      responses:
        '200':
          description: User activated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

  /orders/{orderId}/cancel:
    post:
      summary: Cancel order
      parameters:
        - in: path
          name: orderId
          required: true
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                reason:
                  type: string
      responses:
        '200':
          description: Order cancelled
```

## Authentication Patterns

### Bearer Token (JWT)

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []

paths:
  /auth/login:
    post:
      summary: Login
      security: []  # Override global security
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  format: password
      responses:
        '200':
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  token:
                    type: string
                  refreshToken:
                    type: string
                  expiresIn:
                    type: integer
```

### API Key

```yaml
components:
  securitySchemes:
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key

security:
  - apiKey: []
```

### OAuth 2.0

```yaml
components:
  securitySchemes:
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://example.com/oauth/authorize
          tokenUrl: https://example.com/oauth/token
          scopes:
            read: Read access
            write: Write access
            admin: Admin access

security:
  - oauth2: [read, write]
```

## Error Response Patterns

### Standard Error Format

```yaml
components:
  schemas:
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: Machine-readable error code
          example: "VALIDATION_ERROR"
        message:
          type: string
          description: Human-readable error message
          example: "Invalid input data"
        details:
          type: array
          description: Detailed error information
          items:
            type: object
            properties:
              field:
                type: string
                example: "email"
              message:
                type: string
                example: "Invalid email format"
              code:
                type: string
                example: "INVALID_FORMAT"
        timestamp:
          type: string
          format: date-time
        requestId:
          type: string
          format: uuid
```

### Validation Errors

```yaml
responses:
  '422':
    description: Validation error
    content:
      application/json:
        schema:
          type: object
          properties:
            code:
              type: string
              example: "VALIDATION_ERROR"
            message:
              type: string
              example: "Validation failed"
            errors:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string
                  value:
                    type: string
        example:
          code: "VALIDATION_ERROR"
          message: "Validation failed"
          errors:
            - field: "email"
              message: "Invalid email format"
              value: "invalid-email"
            - field: "age"
              message: "Must be at least 18"
              value: "15"
```

## Pagination Patterns

### Offset-based Pagination

```yaml
parameters:
  - in: query
    name: page
    schema:
      type: integer
      minimum: 1
      default: 1
  - in: query
    name: limit
    schema:
      type: integer
      minimum: 1
      maximum: 100
      default: 20

responses:
  '200':
    content:
      application/json:
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/components/schemas/Item'
            pagination:
              type: object
              properties:
                page:
                  type: integer
                limit:
                  type: integer
                total:
                  type: integer
                totalPages:
                  type: integer
```

### Cursor-based Pagination

```yaml
parameters:
  - in: query
    name: cursor
    schema:
      type: string
    description: Cursor for next page
  - in: query
    name: limit
    schema:
      type: integer
      minimum: 1
      maximum: 100
      default: 20

responses:
  '200':
    content:
      application/json:
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/components/schemas/Item'
            pagination:
              type: object
              properties:
                nextCursor:
                  type: string
                  nullable: true
                hasMore:
                  type: boolean
```

## Versioning Patterns

### URL Path Versioning

```yaml
servers:
  - url: https://api.example.com/v1
  - url: https://api.example.com/v2
```

### Header Versioning

```yaml
parameters:
  - in: header
    name: API-Version
    schema:
      type: string
      enum: ['1.0', '2.0']
    required: true
```

## File Upload Pattern

```yaml
paths:
  /upload:
    post:
      summary: Upload file
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              required:
                - file
              properties:
                file:
                  type: string
                  format: binary
                description:
                  type: string
      responses:
        '201':
          description: File uploaded
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                  url:
                    type: string
                  size:
                    type: integer
                  mimeType:
                    type: string
```

## Webhook Pattern

```yaml
paths:
  /webhooks:
    post:
      summary: Register webhook
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - url
                - events
              properties:
                url:
                  type: string
                  format: uri
                events:
                  type: array
                  items:
                    type: string
                    enum: [user.created, user.updated, user.deleted]
                secret:
                  type: string
                  description: Secret for webhook signature verification
      responses:
        '201':
          description: Webhook registered
```
