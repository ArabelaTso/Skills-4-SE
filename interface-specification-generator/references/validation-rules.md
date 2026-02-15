# Validation Rules Reference

This document provides common validation patterns for API specifications.

## String Validations

### Email
```yaml
type: string
format: email
pattern: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
maxLength: 254
```

### Phone Number (International)
```yaml
type: string
pattern: ^\+?[1-9]\d{1,14}$
example: "+14155552671"
```

### URL
```yaml
type: string
format: uri
pattern: ^https?://
maxLength: 2048
```

### UUID
```yaml
type: string
format: uuid
pattern: ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$
```

### ISO 8601 Date
```yaml
type: string
format: date
pattern: ^\d{4}-\d{2}-\d{2}$
example: "2024-01-15"
```

### ISO 8601 DateTime
```yaml
type: string
format: date-time
pattern: ^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$
example: "2024-01-15T14:30:00Z"
```

### Password
```yaml
type: string
format: password
minLength: 8
maxLength: 128
pattern: ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]
description: Must contain at least one uppercase letter, one lowercase letter, one number, and one special character
```

### Slug/Identifier
```yaml
type: string
pattern: ^[a-z0-9]+(?:-[a-z0-9]+)*$
minLength: 1
maxLength: 100
example: "my-resource-name"
```

## Numeric Validations

### Positive Integer
```yaml
type: integer
minimum: 1
```

### Non-negative Integer
```yaml
type: integer
minimum: 0
```

### Percentage
```yaml
type: number
minimum: 0
maximum: 100
```

### Price/Currency
```yaml
type: number
format: double
minimum: 0
multipleOf: 0.01
example: 19.99
```

### Latitude
```yaml
type: number
format: double
minimum: -90
maximum: 90
```

### Longitude
```yaml
type: number
format: double
minimum: -180
maximum: 180
```

## Array Validations

### Non-empty Array
```yaml
type: array
minItems: 1
items:
  type: string
```

### Bounded Array
```yaml
type: array
minItems: 1
maxItems: 100
items:
  type: string
```

### Unique Items
```yaml
type: array
uniqueItems: true
items:
  type: string
```

## Object Validations

### Required Properties
```yaml
type: object
required:
  - id
  - name
  - email
properties:
  id:
    type: string
  name:
    type: string
  email:
    type: string
```

### Additional Properties
```yaml
type: object
additionalProperties: false  # Strict - no extra properties allowed
properties:
  name:
    type: string
```

```yaml
type: object
additionalProperties: true  # Allow any extra properties
properties:
  name:
    type: string
```

```yaml
type: object
additionalProperties:  # Allow extra properties of specific type
  type: string
properties:
  name:
    type: string
```

## Enum Validations

### String Enum
```yaml
type: string
enum:
  - active
  - inactive
  - pending
```

### Numeric Enum
```yaml
type: integer
enum:
  - 1
  - 2
  - 3
```

## Conditional Validations

### OneOf (Exactly one schema must match)
```yaml
oneOf:
  - type: object
    required: [email]
    properties:
      email:
        type: string
        format: email
  - type: object
    required: [phone]
    properties:
      phone:
        type: string
```

### AnyOf (At least one schema must match)
```yaml
anyOf:
  - type: string
  - type: number
```

### AllOf (All schemas must match - used for composition)
```yaml
allOf:
  - $ref: '#/components/schemas/BaseEntity'
  - type: object
    properties:
      specificField:
        type: string
```

## Common Validation Combinations

### Username
```yaml
type: string
pattern: ^[a-zA-Z0-9_-]{3,20}$
minLength: 3
maxLength: 20
```

### Credit Card Number
```yaml
type: string
pattern: ^\d{13,19}$
minLength: 13
maxLength: 19
```

### IP Address (IPv4)
```yaml
type: string
format: ipv4
pattern: ^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$
```

### Semantic Version
```yaml
type: string
pattern: ^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$
example: "1.0.0"
```

### File Size (in bytes)
```yaml
type: integer
minimum: 0
maximum: 10485760  # 10MB
```

### Color Hex Code
```yaml
type: string
pattern: ^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$
example: "#FF5733"
```
