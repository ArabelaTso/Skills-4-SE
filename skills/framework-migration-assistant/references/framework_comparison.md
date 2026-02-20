# Framework Comparison Reference

## Flask vs FastAPI

### Architecture

| Aspect | Flask | FastAPI |
|--------|-------|---------|
| **Type** | WSGI framework | ASGI framework |
| **Async Support** | Limited (via extensions) | Native async/await |
| **Type Hints** | Optional | Required for validation |
| **Data Validation** | Manual or via extensions | Built-in (Pydantic) |
| **Documentation** | Manual | Auto-generated (OpenAPI) |
| **Performance** | Moderate | High |

### Routing

**Flask:**
```python
@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
def user_handler(user_id):
    if request.method == 'GET':
        return get_user(user_id)
    else:
        return create_user(user_id)
```

**FastAPI:**
```python
@app.get('/users/{user_id}')
async def get_user(user_id: int):
    return await fetch_user(user_id)

@app.post('/users/{user_id}')
async def create_user(user_id: int, user: UserCreate):
    return await save_user(user_id, user)
```

### Request Handling

| Feature | Flask | FastAPI |
|---------|-------|---------|
| **Query params** | `request.args.get('key')` | Function parameter with type hint |
| **Path params** | `<type:name>` in route | `{name}` in path + type hint |
| **Request body** | `request.json` | Pydantic model parameter |
| **Form data** | `request.form.get('key')` | `Form()` parameter |
| **Files** | `request.files['key']` | `File()` or `UploadFile` parameter |
| **Headers** | `request.headers.get('key')` | `Header()` parameter |
| **Cookies** | `request.cookies.get('key')` | `Cookie()` parameter |

### Response Handling

| Feature | Flask | FastAPI |
|---------|-------|---------|
| **JSON** | `jsonify(data)` | Return dict/model directly |
| **Status code** | `return data, 404` | `Response(status_code=404)` or raise `HTTPException` |
| **Headers** | `response.headers['key'] = 'value'` | `Response(headers={'key': 'value'})` |
| **Cookies** | `response.set_cookie('key', 'value')` | `response.set_cookie('key', 'value')` |
| **Redirect** | `redirect(url)` | `RedirectResponse(url)` |
| **File** | `send_file(path)` | `FileResponse(path)` |
| **Stream** | `Response(generator)` | `StreamingResponse(generator)` |

### Dependency Injection

**Flask:**
```python
# Using g object
from flask import g

@app.before_request
def get_db():
    g.db = connect_db()

@app.route('/users')
def get_users():
    return g.db.query(User).all()
```

**FastAPI:**
```python
# Using dependencies
from fastapi import Depends

def get_db():
    db = connect_db()
    try:
        yield db
    finally:
        db.close()

@app.get('/users')
async def get_users(db = Depends(get_db)):
    return db.query(User).all()
```

### Error Handling

**Flask:**
```python
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404

@app.errorhandler(Exception)
def handle_exception(error):
    return {'error': str(error)}, 500
```

**FastAPI:**
```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={'error': 'Not found'}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={'error': str(exc)}
    )
```

### Testing

**Flask:**
```python
def test_get_user():
    client = app.test_client()
    response = client.get('/users/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
```

**FastAPI:**
```python
from fastapi.testclient import TestClient

def test_get_user():
    client = TestClient(app)
    response = client.get('/users/1')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
```

## Django vs FastAPI

### Architecture

| Aspect | Django | FastAPI |
|--------|--------|---------|
| **Type** | Full-stack framework | API framework |
| **ORM** | Django ORM | Bring your own (SQLAlchemy, etc.) |
| **Admin** | Built-in admin panel | None (use third-party) |
| **Templates** | Built-in template engine | None (API-focused) |
| **Auth** | Built-in auth system | Bring your own |
| **Async** | Limited support | Native async/await |

### URL Routing

**Django:**
```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/<int:user_id>/', views.get_user),
    path('users/', views.list_users),
]
```

**FastAPI:**
```python
@app.get('/users/{user_id}')
async def get_user(user_id: int):
    return await fetch_user(user_id)

@app.get('/users/')
async def list_users():
    return await fetch_all_users()
```

### Views/Handlers

**Django Function-Based View:**
```python
from django.http import JsonResponse

def get_user(request, user_id):
    user = User.objects.get(id=user_id)
    return JsonResponse({
        'id': user.id,
        'name': user.name
    })
```

**Django Class-Based View:**
```python
from django.views import View
from django.http import JsonResponse

class UserView(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        return JsonResponse({
            'id': user.id,
            'name': user.name
        })
```

**FastAPI:**
```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str

@app.get('/users/{user_id}')
async def get_user(user_id: int) -> UserResponse:
    user = await fetch_user(user_id)
    return UserResponse(id=user.id, name=user.name)
```

### Models and Serialization

**Django:**
```python
# models.py
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

# serializers.py (Django REST Framework)
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']
```

**FastAPI:**
```python
# models.py (SQLAlchemy)
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))

# schemas.py (Pydantic)
from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True
```

### Middleware

**Django:**
```python
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Before view
        response = self.get_response(request)
        # After view
        return response
```

**FastAPI:**
```python
@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    # Before endpoint
    response = await call_next(request)
    # After endpoint
    return response
```

## Performance Comparison

### Requests per Second (Approximate)

| Framework | Sync | Async |
|-----------|------|-------|
| Flask | 1,000 | N/A |
| Django | 800 | 1,200 |
| FastAPI | N/A | 10,000+ |

*Note: Actual performance depends on application complexity and hardware.*

### When to Use Each Framework

**Use Flask when:**
- Building small to medium applications
- Need simple, straightforward routing
- Don't need async support
- Want minimal boilerplate
- Have existing Flask knowledge

**Use Django when:**
- Building full-stack applications
- Need built-in admin panel
- Want comprehensive ORM
- Need built-in authentication
- Building content-heavy sites

**Use FastAPI when:**
- Building modern APIs
- Need high performance
- Want automatic API documentation
- Need async/await support
- Want built-in data validation
- Building microservices
