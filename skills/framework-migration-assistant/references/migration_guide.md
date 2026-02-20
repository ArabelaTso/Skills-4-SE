# Framework Migration Guide

## Overview

This guide provides detailed information on migrating between different web frameworks. The migration process is automated but understanding the changes helps ensure a smooth transition.

## Supported Migration Paths

### Python Web Frameworks

#### Flask → FastAPI

**Key Changes:**
- Route decorators: `@app.route()` → `@app.get()`, `@app.post()`, etc.
- Request handling: `request.args` → `request.query_params`
- Response handling: `jsonify()` → direct return of Python objects
- Async support: All route handlers become async by default
- Type hints: Pydantic models for request/response validation

**Example:**

Flask:
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.get_user(user_id)
    return jsonify(user)
```

FastAPI:
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str

@app.get('/users/{user_id}')
async def get_user(user_id: int) -> User:
    user = await db.get_user(user_id)
    return user
```

#### Django → FastAPI

**Key Changes:**
- URL patterns → FastAPI path operations
- Django views → FastAPI path operation functions
- Django ORM → SQLAlchemy or other ORMs
- Settings module → Pydantic Settings
- Middleware → FastAPI middleware
- Django templates → Frontend framework or Jinja2

**Example:**

Django:
```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/<int:user_id>/', views.get_user),
]

# views.py
from django.http import JsonResponse

def get_user(request, user_id):
    user = User.objects.get(id=user_id)
    return JsonResponse({'id': user.id, 'name': user.name})
```

FastAPI:
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserResponse(BaseModel):
    id: int
    name: str

@app.get('/users/{user_id}')
async def get_user(user_id: int) -> UserResponse:
    user = await get_user_from_db(user_id)
    return UserResponse(id=user.id, name=user.name)
```

## Migration Process

### Phase 1: Preparation

1. **Backup your repository**
   ```bash
   git checkout -b backup-before-migration
   git push origin backup-before-migration
   ```

2. **Review current codebase**
   - Identify all routes and handlers
   - Document custom middleware
   - List all dependencies
   - Note any framework-specific features

3. **Run existing tests**
   ```bash
   pytest  # or your test command
   ```
   Ensure all tests pass before migration.

### Phase 2: Dependency Migration

The migration tool automatically updates:
- `requirements.txt`
- `pyproject.toml`
- `setup.py` (if present)

**Manual review needed for:**
- Custom extensions
- Third-party integrations
- Database drivers
- Authentication libraries

### Phase 3: Code Migration

#### Routes and Handlers

**Automatic transformations:**
- Route decorator syntax
- HTTP method specification
- Path parameter syntax
- Request/response handling

**Manual review needed for:**
- Complex request validation
- Custom response formatting
- Error handling patterns
- Streaming responses

#### Configuration

**Automatic transformations:**
- Environment variables
- Basic settings
- CORS configuration
- Middleware setup

**Manual review needed for:**
- Database connection strings
- Custom configuration loaders
- Secret management
- Feature flags

#### Dependency Injection

**Flask → FastAPI:**
- Flask's `g` object → FastAPI dependencies
- Flask extensions → FastAPI dependencies
- Request context → Dependency injection

**Django → FastAPI:**
- Django's middleware → FastAPI dependencies
- Django's context processors → Dependencies
- Django's signals → Event handlers

### Phase 4: Test Migration

**Automatic transformations:**
- Test client initialization
- Request methods
- Response assertions
- Basic test structure

**Manual review needed for:**
- Database fixtures
- Mock objects
- Integration tests
- End-to-end tests

### Phase 5: Verification

1. **Run migrated tests**
   ```bash
   pytest
   ```

2. **Manual testing**
   - Test all endpoints
   - Verify authentication
   - Check error handling
   - Test edge cases

3. **Performance testing**
   - Compare response times
   - Check memory usage
   - Verify concurrent request handling

## Common Migration Patterns

### Request Handling

**Query Parameters:**
```python
# Flask
value = request.args.get('key')

# FastAPI
@app.get('/endpoint')
async def endpoint(key: str = None):
    value = key
```

**Request Body:**
```python
# Flask
data = request.json

# FastAPI
class RequestModel(BaseModel):
    field: str

@app.post('/endpoint')
async def endpoint(data: RequestModel):
    value = data.field
```

**Form Data:**
```python
# Flask
value = request.form.get('key')

# FastAPI
from fastapi import Form

@app.post('/endpoint')
async def endpoint(key: str = Form(...)):
    value = key
```

### Response Handling

**JSON Response:**
```python
# Flask
return jsonify({'key': 'value'})

# FastAPI
return {'key': 'value'}
```

**Custom Status Code:**
```python
# Flask
return jsonify({'error': 'Not found'}), 404

# FastAPI
from fastapi import HTTPException

raise HTTPException(status_code=404, detail='Not found')
```

**File Response:**
```python
# Flask
return send_file('path/to/file')

# FastAPI
from fastapi.responses import FileResponse

return FileResponse('path/to/file')
```

### Error Handling

**Flask:**
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404
```

**FastAPI:**
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={'error': 'Not found'}
    )
```

### Middleware

**Flask:**
```python
@app.before_request
def before_request():
    # Do something before request

@app.after_request
def after_request(response):
    # Do something after request
    return response
```

**FastAPI:**
```python
from fastapi import Request

@app.middleware("http")
async def add_middleware(request: Request, call_next):
    # Do something before request
    response = await call_next(request)
    # Do something after request
    return response
```

## Post-Migration Checklist

- [ ] All tests pass
- [ ] All endpoints respond correctly
- [ ] Authentication works
- [ ] Database connections work
- [ ] Environment variables are set
- [ ] Logging is configured
- [ ] Error handling works
- [ ] CORS is configured (if needed)
- [ ] Documentation is updated
- [ ] Deployment configuration is updated

## Troubleshooting

### Common Issues

**Issue: Import errors after migration**
- Solution: Run `pip install -r requirements.txt` to install new dependencies

**Issue: Tests fail with async errors**
- Solution: Add `@pytest.mark.asyncio` to async tests and install `pytest-asyncio`

**Issue: Request validation fails**
- Solution: Add proper Pydantic models for request bodies

**Issue: Database connections fail**
- Solution: Update database connection strings for SQLAlchemy format

**Issue: CORS errors**
- Solution: Configure CORS middleware properly

### Getting Help

If you encounter issues:
1. Check the migration summary for warnings
2. Review the git commits to see what changed
3. Consult framework documentation
4. Test endpoints individually
5. Check logs for detailed error messages
