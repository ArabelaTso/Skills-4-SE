# OpenAPI 3.0 Specification Template

## Basic Structure

```yaml
openapi: 3.0.0
info:
  title: API Name
  description: API description
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

paths:
  /resource:
    # Endpoints defined here

components:
  schemas:
    # Data models defined here
  securitySchemes:
    # Auth methods defined here
  parameters:
    # Reusable parameters
  responses:
    # Reusable responses

security:
  - bearerAuth: []
```

## Path Examples

### GET Collection
```yaml
/users:
  get:
    summary: List all users
    description: Retrieve a paginated list of users
    tags:
      - Users
    parameters:
      - name: page
        in: query
        description: Page number
        schema:
          type: integer
          default: 1
      - name: limit
        in: query
        description: Items per page
        schema:
          type: integer
          default: 20
          maximum: 100
      - name: status
        in: query
        description: Filter by status
        schema:
          type: string
          enum: [active, inactive, pending]
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
                  $ref: '#/components/schemas/Pagination'
      '400':
        $ref: '#/components/responses/BadRequest'
      '401':
        $ref: '#/components/responses/Unauthorized'
```

### GET Single Resource
```yaml
/users/{userId}:
  get:
    summary: Get user by ID
    description: Retrieve a specific user
    tags:
      - Users
    parameters:
      - name: userId
        in: path
        required: true
        description: User ID
        schema:
          type: integer
    responses:
      '200':
        description: Successful response
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      '404':
        $ref: '#/components/responses/NotFound'
```

### POST Create Resource
```yaml
/users:
  post:
    summary: Create a new user
    description: Create a new user account
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - email
            properties:
              name:
                type: string
                example: John Doe
              email:
                type: string
                format: email
                example: john@example.com
              role:
                type: string
                enum: [admin, user, guest]
                default: user
    responses:
      '201':
        description: User created successfully
        headers:
          Location:
            description: URL of created resource
            schema:
              type: string
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      '400':
        $ref: '#/components/responses/BadRequest'
      '409':
        description: User already exists
```

### PUT Update Resource
```yaml
/users/{userId}:
  put:
    summary: Replace user
    description: Replace entire user resource
    tags:
      - Users
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/UserInput'
    responses:
      '200':
        description: User updated successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      '404':
        $ref: '#/components/responses/NotFound'
```

### PATCH Partial Update
```yaml
/users/{userId}:
  patch:
    summary: Update user fields
    description: Partially update user resource
    tags:
      - Users
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              email:
                type: string
                format: email
              status:
                type: string
                enum: [active, inactive]
    responses:
      '200':
        description: User updated successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
```

### DELETE Resource
```yaml
/users/{userId}:
  delete:
    summary: Delete user
    description: Remove user from system
    tags:
      - Users
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: integer
    responses:
      '204':
        description: User deleted successfully
      '404':
        $ref: '#/components/responses/NotFound'
```

## Schema Components

### Basic Model
```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - name
        - email
      properties:
        id:
          type: integer
          format: int64
          example: 123
        name:
          type: string
          example: John Doe
        email:
          type: string
          format: email
          example: john@example.com
        role:
          type: string
          enum: [admin, user, guest]
          example: user
        created_at:
          type: string
          format: date-time
          example: '2024-01-15T10:30:00Z'
        updated_at:
          type: string
          format: date-time
          example: '2024-01-15T10:30:00Z'
```

### Nested Objects
```yaml
Order:
  type: object
  properties:
    id:
      type: integer
    customer:
      $ref: '#/components/schemas/Customer'
    items:
      type: array
      items:
        $ref: '#/components/schemas/OrderItem'
    total:
      type: number
      format: decimal
```

### Pagination
```yaml
Pagination:
  type: object
  properties:
    page:
      type: integer
      example: 1
    limit:
      type: integer
      example: 20
    total:
      type: integer
      example: 150
    total_pages:
      type: integer
      example: 8
```

### Error Response
```yaml
Error:
  type: object
  required:
    - code
    - message
  properties:
    code:
      type: string
      example: VALIDATION_ERROR
    message:
      type: string
      example: Invalid input data
    details:
      type: array
      items:
        type: object
        properties:
          field:
            type: string
          message:
            type: string
```

## Reusable Components

### Parameters
```yaml
components:
  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        default: 1
    LimitParam:
      name: limit
      in: query
      schema:
        type: integer
        default: 20
        maximum: 100
    UserIdParam:
      name: userId
      in: path
      required: true
      schema:
        type: integer
```

### Responses
```yaml
components:
  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Missing or invalid authentication
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

## Security Schemes

### Bearer Token (JWT)
```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token authentication
```

### API Key
```yaml
components:
  securitySchemes:
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for authentication
```

### OAuth2
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
```

## Complete Example

```yaml
openapi: 3.0.0
info:
  title: User Management API
  version: 1.0.0

servers:
  - url: https://api.example.com/v1

paths:
  /users:
    get:
      summary: List users
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Success
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
                    $ref: '#/components/schemas/Pagination'

    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserInput'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

  /users/{userId}:
    get:
      summary: Get user
      parameters:
        - $ref: '#/components/parameters/UserIdParam'
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email
        created_at:
          type: string
          format: date-time

    UserInput:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
        email:
          type: string
          format: email

    Pagination:
      type: object
      properties:
        page:
          type: integer
        total:
          type: integer

  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        default: 1

    LimitParam:
      name: limit
      in: query
      schema:
        type: integer
        default: 20

    UserIdParam:
      name: userId
      in: path
      required: true
      schema:
        type: integer

  responses:
    NotFound:
      description: Resource not found

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer

security:
  - bearerAuth: []
```
