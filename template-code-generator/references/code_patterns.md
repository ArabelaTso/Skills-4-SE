# Code Generation Patterns

## Class Generators

### TypeScript Class with Interface
```typescript
// Pattern: Domain model with interface
export interface {{ModelName}} {
  id: number;
  {{#each fields}}
  {{name}}: {{type}};
  {{/each}}
  createdAt: Date;
  updatedAt: Date;
}

export class {{ModelName}}Model implements {{ModelName}} {
  constructor(
    public id: number,
    {{#each fields}}
    public {{name}}: {{type}},
    {{/each}}
    public createdAt: Date = new Date(),
    public updatedAt: Date = new Date()
  ) {}

  update(data: Partial<{{ModelName}}>): void {
    Object.assign(this, data);
    this.updatedAt = new Date();
  }

  toJSON(): {{ModelName}} {
    return {
      id: this.id,
      {{#each fields}}
      {{name}}: this.{{name}},
      {{/each}}
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}
```

### Python Dataclass
```python
# Pattern: Python dataclass with validation
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class {{ClassName}}:
    """{{description}}"""
    {{#each fields}}
    {{name}}: {{type}}
    {{/each}}
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def validate(self) -> bool:
        """Validate the data."""
        {{#each validations}}
        if {{condition}}:
            raise ValueError("{{message}}")
        {{/each}}
        return True

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            {{#each fields}}
            "{{name}}": self.{{name}},
            {{/each}}
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
```

## API Endpoint Generators

### REST CRUD Endpoints (Express)
```typescript
// Pattern: Complete CRUD REST endpoints
import { Router } from 'express';
import { {{modelName}}Controller } from '../controllers/{{modelName}}Controller';
import { validate } from '../middleware/validation';
import { {{modelName}}Schema } from '../schemas/{{modelName}}';

const router = Router();

router.get('/', {{modelName}}Controller.getAll);
router.get('/:id', {{modelName}}Controller.getById);
router.post('/', validate({{modelName}}Schema), {{modelName}}Controller.create);
router.put('/:id', validate({{modelName}}Schema), {{modelName}}Controller.update);
router.patch('/:id', {{modelName}}Controller.partialUpdate);
router.delete('/:id', {{modelName}}Controller.delete);

export default router;
```

### GraphQL Resolvers
```typescript
// Pattern: GraphQL resolver with queries and mutations
export const {{modelName}}Resolvers = {
  Query: {
    {{modelNameLower}}: async (_: any, { id }: { id: number }, context: Context) => {
      return context.db.{{modelNameLower}}.findUnique({ where: { id } });
    },
    {{modelNameLower}}s: async (_: any, args: any, context: Context) => {
      return context.db.{{modelNameLower}}.findMany();
    },
  },
  Mutation: {
    create{{modelName}}: async (_: any, { input }: { input: {{modelName}}Input }, context: Context) => {
      return context.db.{{modelNameLower}}.create({ data: input });
    },
    update{{modelName}}: async (_: any, { id, input }: { id: number; input: {{modelName}}Input }, context: Context) => {
      return context.db.{{modelNameLower}}.update({ where: { id }, data: input });
    },
    delete{{modelName}}: async (_: any, { id }: { id: number }, context: Context) => {
      return context.db.{{modelNameLower}}.delete({ where: { id } });
    },
  },
};
```

## Component Generators

### React Component (TypeScript)
```typescript
// Pattern: React functional component with props
import React from 'react';
import styles from './{{ComponentName}}.module.css';

interface {{ComponentName}}Props {
  {{#each props}}
  {{name}}: {{type}};
  {{/each}}
}

export const {{ComponentName}}: React.FC<{{ComponentName}}Props> = ({
  {{#each props}}
  {{name}},
  {{/each}}
}) => {
  return (
    <div className={styles.container}>
      <h2>{{ComponentName}}</h2>
      {/* Component content */}
    </div>
  );
};
```

### React Hook
```typescript
// Pattern: Custom React hook
import { useState, useEffect } from 'react';

interface Use{{HookName}}Result {
  {{#each returnValues}}
  {{name}}: {{type}};
  {{/each}}
}

export function use{{HookName}}({{#each params}}{{name}}: {{type}}{{#unless @last}}, {{/unless}}{{/each}}): Use{{HookName}}Result {
  {{#each state}}
  const [{{name}}, set{{nameCapitalized}}] = useState<{{type}}>({{defaultValue}});
  {{/each}}

  useEffect(() => {
    // Effect logic
  }, [{{#each dependencies}}{{name}}{{#unless @last}}, {{/unless}}{{/each}}]);

  return {
    {{#each returnValues}}
    {{name}},
    {{/each}}
  };
}
```

## Test Generators

### Jest Unit Test
```typescript
// Pattern: Jest test suite
import { {{functionName}} } from '../{{moduleName}}';

describe('{{functionName}}', () => {
  it('should {{testDescription}}', () => {
    // Arrange
    const input = {{inputValue}};
    const expected = {{expectedValue}};

    // Act
    const result = {{functionName}}(input);

    // Assert
    expect(result).toEqual(expected);
  });

  it('should handle edge case: {{edgeCaseDescription}}', () => {
    const input = {{edgeCaseInput}};
    expect(() => {{functionName}}(input)).toThrow();
  });
});
```

### Python pytest
```python
# Pattern: pytest test suite
import pytest
from {{module_name}} import {{function_name}}

class Test{{FunctionName}}:
    """Test suite for {{function_name}}."""

    def test_{{test_name}}(self):
        """Test {{description}}."""
        # Arrange
        input_data = {{input_value}}
        expected = {{expected_value}}

        # Act
        result = {{function_name}}(input_data)

        # Assert
        assert result == expected

    def test_{{error_case}}(self):
        """Test error handling for {{error_description}}."""
        with pytest.raises({{ExceptionType}}):
            {{function_name}}({{invalid_input}})

    @pytest.fixture
    def sample_data(self):
        """Provide sample data for tests."""
        return {{fixture_data}}
```

## Database Generators

### TypeORM Entity
```typescript
// Pattern: TypeORM entity with relations
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, {{#if hasRelations}}ManyToOne, OneToMany, {{/if}}}} from 'typeorm';
{{#each relations}}
import { {{relatedEntity}} } from './{{relatedEntity}}';
{{/each}}

@Entity('{{tableName}}')
export class {{EntityName}} {
  @PrimaryGeneratedColumn()
  id: number;

  {{#each columns}}
  @Column({{#if options}}{{{options}}}{{/if}})
  {{name}}: {{type}};

  {{/each}}
  {{#each relations}}
  @{{relationType}}(() => {{relatedEntity}}{{#if inverse}}, {{inverseProperty}}{{/if}})
  {{name}}: {{relatedEntity}}{{#if isArray}}[]{{/if}};

  {{/each}}
  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

### SQLAlchemy Model
```python
# Pattern: SQLAlchemy model with relationships
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class {{ModelName}}(Base):
    """{{description}}"""
    __tablename__ = '{{table_name}}'

    id = Column(Integer, primary_key=True)
    {{#each columns}}
    {{name}} = Column({{type}}{{#if nullable}}, nullable=True{{/if}})
    {{/each}}
    {{#each foreignKeys}}
    {{name}}_id = Column(Integer, ForeignKey('{{referencedTable}}.id'))
    {{name}} = relationship("{{RelatedModel}}", back_populates="{{backPopulates}}")
    {{/each}}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<{{ModelName}}(id={self.id})>"
```

## Configuration Generators

### Environment Configuration
```typescript
// Pattern: Type-safe environment configuration
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.string().transform(Number),
  DATABASE_URL: z.string().url(),
  {{#each envVars}}
  {{name}}: z.{{zodType}}(){{#if optional}}.optional(){{/if}},
  {{/each}}
});

export const env = envSchema.parse(process.env);

export type Env = z.infer<typeof envSchema>;
```

## Service Generators

### Generic Service Class
```typescript
// Pattern: Generic service with CRUD operations
export class {{ServiceName}}Service {
  constructor(private repository: {{EntityName}}Repository) {}

  async findAll(): Promise<{{EntityName}}[]> {
    return this.repository.find();
  }

  async findById(id: number): Promise<{{EntityName}} | null> {
    return this.repository.findOne({ where: { id } });
  }

  async create(data: Create{{EntityName}}Dto): Promise<{{EntityName}}> {
    const entity = this.repository.create(data);
    return this.repository.save(entity);
  }

  async update(id: number, data: Update{{EntityName}}Dto): Promise<{{EntityName}}> {
    await this.repository.update(id, data);
    const updated = await this.findById(id);
    if (!updated) {
      throw new NotFoundException(`{{EntityName}} with id ${id} not found`);
    }
    return updated;
  }

  async delete(id: number): Promise<void> {
    await this.repository.delete(id);
  }
}
```

## Middleware Generators

### Express Middleware
```typescript
// Pattern: Express middleware function
import { Request, Response, NextFunction } from 'express';

export function {{middlewareName}}({{#each params}}{{name}}: {{type}}{{#unless @last}}, {{/unless}}{{/each}}) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      // Middleware logic
      {{#each checks}}
      if ({{condition}}) {
        return res.status({{statusCode}}).json({ message: '{{message}}' });
      }
      {{/each}}

      next();
    } catch (error) {
      next(error);
    }
  };
}
```

## Validation Generators

### Zod Schema
```typescript
// Pattern: Zod validation schema
import { z } from 'zod';

export const {{schemaName}}Schema = z.object({
  {{#each fields}}
  {{name}}: z.{{zodType}}(){{#if validation}}.{{validation}}(){{/if}}{{#if optional}}.optional(){{/if}},
  {{/each}}
});

export type {{SchemaName}} = z.infer<typeof {{schemaName}}Schema>;
```

### Pydantic Model
```python
# Pattern: Pydantic validation model
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class {{ModelName}}(BaseModel):
    """{{description}}"""
    {{#each fields}}
    {{name}}: {{type}}{{#if hasDefault}} = Field({{defaultValue}}, description="{{description}}"){{/if}}
    {{/each}}

    {{#each validators}}
    @validator('{{fieldName}}')
    def {{validatorName}}(cls, v):
        if {{condition}}:
            raise ValueError('{{errorMessage}}')
        return v
    {{/each}}

    class Config:
        orm_mode = True
```
