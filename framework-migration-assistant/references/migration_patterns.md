# Common Migration Patterns

## Table of Contents

1. [Route Migration Patterns](#route-migration-patterns)
2. [Request Handling Patterns](#request-handling-patterns)
3. [Response Patterns](#response-patterns)
4. [Authentication Patterns](#authentication-patterns)
5. [Database Patterns](#database-patterns)
6. [Testing Patterns](#testing-patterns)

## Route Migration Patterns

### Pattern 1: Simple GET Route

**Flask:**
```python
@app.route('/items')
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])
```

**FastAPI:**
```python
from typing import List

@app.get('/items')
async def get_items() -> List[ItemSchema]:
    items = await db.query(Item).all()
    return items
```

### Pattern 2: Route with Path Parameters

**Flask:**
```python
@app.route('/items/<int:item_id>')
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())
```

**FastAPI:**
```python
from fastapi import HTTPException

@app.get('/items/{item_id}')
async def get_item(item_id: int) -> ItemSchema:
    item = await db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

### Pattern 3: POST Route with Request Body

**Flask:**
```python
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    item = Item(**data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201
```

**FastAPI:**
```python
from fastapi import status

@app.post('/items', status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate) -> ItemSchema:
    new_item = Item(**item.dict())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item
```

### Pattern 4: Multiple HTTP Methods

**Flask:**
```python
@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def item_handler(item_id):
    if request.method == 'GET':
        return get_item(item_id)
    elif request.method == 'PUT':
        return update_item(item_id)
    elif request.method == 'DELETE':
        return delete_item(item_id)
```

**FastAPI:**
```python
@app.get('/items/{item_id}')
async def get_item(item_id: int) -> ItemSchema:
    # Implementation

@app.put('/items/{item_id}')
async def update_item(item_id: int, item: ItemUpdate) -> ItemSchema:
    # Implementation

@app.delete('/items/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    # Implementation
```

## Request Handling Patterns

### Pattern 1: Query Parameters

**Flask:**
```python
@app.route('/search')
def search():
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)
    results = search_items(query, limit)
    return jsonify(results)
```

**FastAPI:**
```python
from typing import Optional

@app.get('/search')
async def search(q: str = '', limit: int = 10) -> List[ItemSchema]:
    results = await search_items(q, limit)
    return results
```

### Pattern 2: Request Headers

**Flask:**
```python
@app.route('/protected')
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    user = verify_token(token)
    return jsonify({'user': user})
```

**FastAPI:**
```python
from fastapi import Header, HTTPException

@app.get('/protected')
async def protected(authorization: str = Header(None)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = await verify_token(authorization)
    return {'user': user}
```

### Pattern 3: File Upload

**Flask:**
```python
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify({'filename': filename})
```

**FastAPI:**
```python
from fastapi import File, UploadFile

@app.post('/upload')
async def upload_file(file: UploadFile = File(...)) -> dict:
    contents = await file.read()
    filename = file.filename
    # Save file
    with open(f"uploads/{filename}", "wb") as f:
        f.write(contents)
    return {'filename': filename}
```

### Pattern 4: Form Data

**Flask:**
```python
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = authenticate(username, password)
    return jsonify({'token': user.token})
```

**FastAPI:**
```python
from fastapi import Form

@app.post('/login')
async def login(
    username: str = Form(...),
    password: str = Form(...)
) -> dict:
    user = await authenticate(username, password)
    return {'token': user.token}
```

## Response Patterns

### Pattern 1: Custom Status Code

**Flask:**
```python
@app.route('/items', methods=['POST'])
def create_item():
    item = create_new_item(request.json)
    return jsonify(item), 201
```

**FastAPI:**
```python
from fastapi import status

@app.post('/items', status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate) -> ItemSchema:
    new_item = await create_new_item(item)
    return new_item
```

### Pattern 2: Custom Headers

**Flask:**
```python
@app.route('/items/<int:item_id>')
def get_item(item_id):
    item = get_item_by_id(item_id)
    response = jsonify(item)
    response.headers['X-Custom-Header'] = 'value'
    return response
```

**FastAPI:**
```python
from fastapi import Response

@app.get('/items/{item_id}')
async def get_item(item_id: int, response: Response) -> ItemSchema:
    item = await get_item_by_id(item_id)
    response.headers['X-Custom-Header'] = 'value'
    return item
```

### Pattern 3: Redirect

**Flask:**
```python
@app.route('/old-path')
def old_path():
    return redirect('/new-path')
```

**FastAPI:**
```python
from fastapi.responses import RedirectResponse

@app.get('/old-path')
async def old_path():
    return RedirectResponse(url='/new-path')
```

### Pattern 4: Streaming Response

**Flask:**
```python
@app.route('/stream')
def stream():
    def generate():
        for i in range(10):
            yield f"data: {i}\n\n"
    return Response(generate(), mimetype='text/event-stream')
```

**FastAPI:**
```python
from fastapi.responses import StreamingResponse

@app.get('/stream')
async def stream():
    async def generate():
        for i in range(10):
            yield f"data: {i}\n\n"
    return StreamingResponse(generate(), media_type='text/event-stream')
```

## Authentication Patterns

### Pattern 1: Token-Based Auth

**Flask:**
```python
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not verify_token(token):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/protected')
@require_auth
def protected():
    return jsonify({'message': 'Success'})
```

**FastAPI:**
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    token = credentials.credentials
    if not await is_valid_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.get('/protected')
async def protected(token: str = Depends(verify_token)):
    return {'message': 'Success'}
```

### Pattern 2: Session-Based Auth

**Flask:**
```python
@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.json)
    session['user_id'] = user.id
    return jsonify({'success': True})

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    user = get_user(session['user_id'])
    return jsonify(user)
```

**FastAPI:**
```python
from fastapi import Cookie, HTTPException

@app.post('/login')
async def login(credentials: LoginCredentials, response: Response):
    user = await authenticate(credentials)
    response.set_cookie(key="session_id", value=user.session_id)
    return {'success': True}

@app.get('/profile')
async def profile(session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = await get_user_by_session(session_id)
    return user
```

## Database Patterns

### Pattern 1: Query All

**Flask (SQLAlchemy):**
```python
@app.route('/items')
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])
```

**FastAPI (SQLAlchemy):**
```python
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def get_db():
    async with AsyncSession() as session:
        yield session

@app.get('/items')
async def get_items(db: AsyncSession = Depends(get_db)) -> List[ItemSchema]:
    result = await db.execute(select(Item))
    items = result.scalars().all()
    return items
```

### Pattern 2: Filter Query

**Flask:**
```python
@app.route('/items/active')
def get_active_items():
    items = Item.query.filter_by(active=True).all()
    return jsonify([item.to_dict() for item in items])
```

**FastAPI:**
```python
@app.get('/items/active')
async def get_active_items(db: AsyncSession = Depends(get_db)) -> List[ItemSchema]:
    result = await db.execute(select(Item).where(Item.active == True))
    items = result.scalars().all()
    return items
```

## Testing Patterns

### Pattern 1: Basic Test

**Flask:**
```python
def test_get_items():
    client = app.test_client()
    response = client.get('/items')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
```

**FastAPI:**
```python
from fastapi.testclient import TestClient

def test_get_items():
    client = TestClient(app)
    response = client.get('/items')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
```

### Pattern 2: POST Request Test

**Flask:**
```python
def test_create_item():
    client = app.test_client()
    response = client.post('/items', json={'name': 'Test'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test'
```

**FastAPI:**
```python
def test_create_item():
    client = TestClient(app)
    response = client.post('/items', json={'name': 'Test'})
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Test'
```

### Pattern 3: Authenticated Request Test

**Flask:**
```python
def test_protected_endpoint():
    client = app.test_client()
    headers = {'Authorization': 'Bearer test-token'}
    response = client.get('/protected', headers=headers)
    assert response.status_code == 200
```

**FastAPI:**
```python
def test_protected_endpoint():
    client = TestClient(app)
    headers = {'Authorization': 'Bearer test-token'}
    response = client.get('/protected', headers=headers)
    assert response.status_code == 200
```
