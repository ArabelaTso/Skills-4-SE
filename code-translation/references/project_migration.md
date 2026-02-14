# Project Migration Guide

## Overview

Migrating entire projects requires translating not just code, but also build systems, dependency management, project structure, and configuration files.

## Migration Phases

### Phase 1: Assessment and Planning

**1. Inventory Source Project**
- List all source files and their dependencies
- Identify external libraries and their equivalents in target language
- Document build/deployment processes
- Note language-specific features used

**2. Identify Challenges**
- Libraries without direct equivalents
- Language-specific features requiring significant rework
- Performance-critical sections
- Integration points with other systems

**3. Create Migration Strategy**
- Decide: Big bang vs incremental migration
- Plan testing strategy
- Set up parallel development if needed

### Phase 2: Environment Setup

**Create Target Project Structure**

**Python → Node.js**
```
python-project/          →    nodejs-project/
├── src/                      ├── src/
│   ├── __init__.py          │   └── index.ts
│   └── main.py              ├── package.json
├── tests/                    ├── tsconfig.json
│   └── test_main.py         └── tests/
├── requirements.txt              └── main.test.ts
└── setup.py
```

**Java → Python**
```
java-project/            →    python-project/
├── src/                      ├── src/
│   └── main/                 │   ├── __init__.py
│       └── java/             │   └── main.py
│           └── com/          ├── tests/
│               └── app/      │   └── test_main.py
├── pom.xml                   ├── setup.py
└── build.gradle              └── requirements.txt
```

**Go → Rust**
```
go-project/              →    rust-project/
├── main.go                   ├── src/
├── go.mod                    │   ├── main.rs
├── pkg/                      │   └── lib.rs
│   └── module/               ├── Cargo.toml
└── cmd/                      └── tests/
                                  └── integration_test.rs
```

### Phase 3: Dependency Translation

**Map Dependencies to Target Language**

**Python → JavaScript**
```python
# requirements.txt
requests==2.28.0
flask==2.3.0
pytest==7.3.0
numpy==1.24.0
```

```json
// package.json
{
  "dependencies": {
    "axios": "^1.4.0",
    "express": "^4.18.0"
  },
  "devDependencies": {
    "jest": "^29.5.0",
    "mathjs": "^11.8.0"
  }
}
```

**Java → Python**
```xml
<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
    </dependency>
    <dependency>
        <groupId>com.google.guava</groupId>
        <artifactId>guava</artifactId>
    </dependency>
</dependencies>
```

```python
# requirements.txt
# Apache Commons Lang → built-in Python string methods
# Google Guava → built-in Python collections + itertools
```

**Common Library Mappings**

| Python | JavaScript | Java | Go | Rust |
|--------|-----------|------|-----|------|
| requests | axios/fetch | HttpClient | net/http | reqwest |
| flask/django | express | Spring | gin/echo | actix-web |
| pytest | jest/mocha | JUnit | testing | cargo test |
| numpy | mathjs | Apache Commons Math | gonum | ndarray |
| pandas | - | - | - | polars |

### Phase 4: Code Translation

**1. Start with Core Logic**

Translate business logic first, leaving framework-specific code for later.

**Python Core Logic**
```python
def calculate_discount(price: float, customer_tier: str) -> float:
    """Calculate discount based on customer tier."""
    discounts = {
        "gold": 0.20,
        "silver": 0.10,
        "bronze": 0.05
    }
    discount_rate = discounts.get(customer_tier, 0)
    return price * (1 - discount_rate)
```

**TypeScript Translation**
```typescript
function calculateDiscount(price: number, customerTier: string): number {
    const discounts: Record<string, number> = {
        gold: 0.20,
        silver: 0.10,
        bronze: 0.05
    };
    const discountRate = discounts[customerTier] ?? 0;
    return price * (1 - discountRate);
}
```

**2. Translate Module by Module**

Work through modules in dependency order (lowest dependencies first).

**3. Adapt Framework Code**

**Flask → Express**
```python
# Python Flask
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = database.get_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "Not found"}), 404
```

```typescript
// TypeScript Express
import express from 'express';

const app = express();

app.get('/api/users/:userId', (req, res) => {
    const userId = parseInt(req.params.userId);
    const user = database.getUser(userId);
    if (user) {
        res.json(user);
    } else {
        res.status(404).json({ error: "Not found" });
    }
});
```

### Phase 5: Testing Strategy

**1. Port Existing Tests**

Translate unit tests alongside code:

**Python pytest**
```python
import pytest

def test_calculate_discount_gold():
    result = calculate_discount(100, "gold")
    assert result == 80.0

def test_calculate_discount_invalid():
    result = calculate_discount(100, "invalid")
    assert result == 100.0
```

**JavaScript Jest**
```javascript
describe('calculateDiscount', () => {
    test('gold tier receives 20% discount', () => {
        const result = calculateDiscount(100, 'gold');
        expect(result).toBe(80.0);
    });

    test('invalid tier receives no discount', () => {
        const result = calculateDiscount(100, 'invalid');
        expect(result).toBe(100.0);
    });
});
```

**2. Add Integration Tests**

Test that translated code integrates correctly with new framework:

```typescript
// Integration test for Express API
import request from 'supertest';
import app from './app';

describe('GET /api/users/:userId', () => {
    test('returns user when exists', async () => {
        const response = await request(app)
            .get('/api/users/1')
            .expect(200);

        expect(response.body).toHaveProperty('id', 1);
    });

    test('returns 404 when user not found', async () => {
        await request(app)
            .get('/api/users/999')
            .expect(404);
    });
});
```

**3. Behavioral Testing**

Run same test scenarios against both old and new implementations:

```python
# test_scenarios.json
[
    {
        "input": {"price": 100, "tier": "gold"},
        "expected_output": 80.0
    },
    {
        "input": {"price": 50, "tier": "silver"},
        "expected_output": 45.0
    }
]
```

### Phase 6: Build System Translation

**Python (setup.py) → Node.js (package.json)**

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="myapp",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "flask>=2.3.0",
    ],
    extras_require={
        "dev": ["pytest>=7.3.0"]
    }
)
```

```json
// package.json
{
    "name": "myapp",
    "version": "1.0.0",
    "main": "dist/index.js",
    "scripts": {
        "build": "tsc",
        "test": "jest",
        "start": "node dist/index.js"
    },
    "dependencies": {
        "axios": "^1.4.0",
        "express": "^4.18.0"
    },
    "devDependencies": {
        "jest": "^29.5.0",
        "typescript": "^5.0.0"
    }
}
```

**Java (Maven) → Go (go.mod)**

```xml
<!-- pom.xml -->
<project>
    <groupId>com.example</groupId>
    <artifactId>myapp</artifactId>
    <version>1.0.0</version>

    <dependencies>
        <dependency>
            <groupId>com.google.code.gson</groupId>
            <artifactId>gson</artifactId>
            <version>2.10</version>
        </dependency>
    </dependencies>
</project>
```

```go
// go.mod
module github.com/example/myapp

go 1.20

require (
    github.com/gin-gonic/gin v1.9.0
)
```

### Phase 7: Configuration Translation

**Environment Variables**

Maintain same environment variables for easier migration:

```bash
# .env (same across languages)
DATABASE_URL=postgresql://localhost/mydb
API_KEY=secret123
PORT=8000
```

**Configuration Files**

**Python config.py → Node.js config.ts**
```python
# config.py
import os

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    API_KEY = os.getenv("API_KEY")
    PORT = int(os.getenv("PORT", 8000))
```

```typescript
// config.ts
interface Config {
    databaseUrl: string;
    apiKey: string;
    port: number;
}

export const config: Config = {
    databaseUrl: process.env.DATABASE_URL!,
    apiKey: process.env.API_KEY!,
    port: parseInt(process.env.PORT ?? "8000")
};
```

### Phase 8: Deployment

**Docker Translation**

**Python Dockerfile**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

**Node.js Dockerfile**
```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build
CMD ["node", "dist/index.js"]
```

**CI/CD Translation**

**Python GitHub Actions → Node.js GitHub Actions**
```yaml
# .github/workflows/test.yml (Python)
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
```

```yaml
# .github/workflows/test.yml (Node.js)
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm test
```

## Migration Checklist

### Pre-Migration
- [ ] Document current architecture
- [ ] List all dependencies
- [ ] Identify equivalent libraries in target language
- [ ] Plan testing strategy
- [ ] Set up target project structure

### During Migration
- [ ] Translate core business logic first
- [ ] Port tests alongside code
- [ ] Adapt framework-specific code
- [ ] Translate build configuration
- [ ] Migrate database schemas/queries if needed
- [ ] Update documentation

### Post-Migration
- [ ] Run full test suite
- [ ] Performance testing
- [ ] Security audit
- [ ] Deploy to staging
- [ ] Monitor for issues
- [ ] Update deployment docs

## Common Migration Challenges

### Challenge: No Direct Library Equivalent

**Solution**: Implement abstraction layer

```python
# Python using library X
from library_x import SpecialFeature

def process_data(data):
    return SpecialFeature.process(data)
```

```typescript
// TypeScript without equivalent - implement interface
interface DataProcessor {
    process(data: any): any;
}

class CustomProcessor implements DataProcessor {
    process(data: any): any {
        // Implement equivalent functionality
        return data;
    }
}
```

### Challenge: Different Concurrency Models

**Python asyncio → Go goroutines**

```python
# Python
async def fetch_all(urls):
    tasks = [fetch(url) for url in urls]
    return await asyncio.gather(*tasks)
```

```go
// Go
func fetchAll(urls []string) []Result {
    results := make([]Result, len(urls))
    var wg sync.WaitGroup

    for i, url := range urls {
        wg.Add(1)
        go func(idx int, u string) {
            defer wg.Done()
            results[idx] = fetch(u)
        }(i, url)
    }

    wg.Wait()
    return results
}
```

### Challenge: Different Type Systems

**Dynamic (Python) → Static (TypeScript)**

Add type definitions incrementally:

```python
# Python (dynamic)
def process_user(user):
    return {"name": user["name"].upper()}
```

```typescript
// TypeScript (static)
interface User {
    name: string;
    email?: string;
}

interface ProcessedUser {
    name: string;
}

function processUser(user: User): ProcessedUser {
    return { name: user.name.toUpperCase() };
}
```

## Incremental Migration Strategy

For large projects, consider incremental migration:

1. **Create API boundaries**: Wrap modules behind APIs
2. **Translate module by module**: One at a time
3. **Run both versions in parallel**: Gradually shift traffic
4. **Validate behavior**: Compare outputs between versions
5. **Complete cutover**: When confident in new version
