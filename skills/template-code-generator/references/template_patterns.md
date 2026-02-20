# Project Template Patterns

## Table of Contents
- [React/TypeScript Application](#reacttypescript-application)
- [FastAPI Backend](#fastapi-backend)
- [Express/TypeScript API](#expresstypescript-api)
- [Python CLI Tool](#python-cli-tool)
- [Full-Stack Monorepo](#full-stack-monorepo)

---

## React/TypeScript Application

### Project Structure
```
react-app/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Modal.tsx
│   │   └── layout/
│   │       ├── Header.tsx
│   │       ├── Footer.tsx
│   │       └── Sidebar.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── About.tsx
│   │   └── NotFound.tsx
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useFetch.ts
│   │   └── useLocalStorage.ts
│   ├── utils/
│   │   ├── api.ts
│   │   ├── constants.ts
│   │   └── helpers.ts
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   └── main.tsx
├── public/
│   └── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .env.example
```

### Core Files

**src/main.tsx**
```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

**src/App.tsx**
```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import NotFound from './pages/NotFound';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

**src/hooks/useFetch.ts**
```typescript
import { useState, useEffect } from 'react';

interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

export function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        const json = await response.json();
        setData(json);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}
```

**src/utils/api.ts**
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}
```

---

## FastAPI Backend

### Project Structure
```
fastapi-app/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── users.py
│   │       │   ├── items.py
│   │       │   └── auth.py
│   │       └── router.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── user.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api/
│       └── test_users.py
├── requirements.txt
├── .env.example
└── alembic.ini
```

### Core Files

**app/main.py**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**app/core/config.py**
```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI App"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
```

**app/api/v1/endpoints/users.py**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas.user import User, UserCreate, UserUpdate
from app.crud import user as crud_user

router = APIRouter()

@router.get("/", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=User)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(deps.get_db)
):
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud_user.create(db, obj_in=user_in)
    return user

@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db)
):
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

**app/crud/base.py**
```python
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
```

---

## Express/TypeScript API

### Project Structure
```
express-app/
├── src/
│   ├── config/
│   │   ├── database.ts
│   │   └── env.ts
│   ├── controllers/
│   │   ├── userController.ts
│   │   └── authController.ts
│   ├── middleware/
│   │   ├── auth.ts
│   │   ├── errorHandler.ts
│   │   └── validation.ts
│   ├── models/
│   │   ├── User.ts
│   │   └── index.ts
│   ├── routes/
│   │   ├── userRoutes.ts
│   │   ├── authRoutes.ts
│   │   └── index.ts
│   ├── services/
│   │   ├── userService.ts
│   │   └── authService.ts
│   ├── utils/
│   │   ├── logger.ts
│   │   └── helpers.ts
│   ├── types/
│   │   └── index.ts
│   ├── app.ts
│   └── server.ts
├── tests/
│   └── unit/
│       └── userService.test.ts
├── package.json
├── tsconfig.json
└── .env.example
```

### Core Files

**src/server.ts**
```typescript
import app from './app';
import { config } from './config/env';
import logger from './utils/logger';

const PORT = config.port || 3000;

app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
});
```

**src/app.ts**
```typescript
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import routes from './routes';
import { errorHandler } from './middleware/errorHandler';

const app = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/api', routes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// Error handling
app.use(errorHandler);

export default app;
```

**src/controllers/userController.ts**
```typescript
import { Request, Response, NextFunction } from 'express';
import { userService } from '../services/userService';

export class UserController {
  async getAll(req: Request, res: Response, next: NextFunction) {
    try {
      const users = await userService.findAll();
      res.json(users);
    } catch (error) {
      next(error);
    }
  }

  async getById(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      const user = await userService.findById(parseInt(id));
      if (!user) {
        return res.status(404).json({ message: 'User not found' });
      }
      res.json(user);
    } catch (error) {
      next(error);
    }
  }

  async create(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await userService.create(req.body);
      res.status(201).json(user);
    } catch (error) {
      next(error);
    }
  }

  async update(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      const user = await userService.update(parseInt(id), req.body);
      res.json(user);
    } catch (error) {
      next(error);
    }
  }

  async delete(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      await userService.delete(parseInt(id));
      res.status(204).send();
    } catch (error) {
      next(error);
    }
  }
}

export const userController = new UserController();
```

**src/middleware/errorHandler.ts**
```typescript
import { Request, Response, NextFunction } from 'express';
import logger from '../utils/logger';

export class AppError extends Error {
  statusCode: number;

  constructor(message: string, statusCode: number = 500) {
    super(message);
    this.statusCode = statusCode;
    Error.captureStackTrace(this, this.constructor);
  }
}

export function errorHandler(
  err: Error | AppError,
  req: Request,
  res: Response,
  next: NextFunction
) {
  logger.error(err);

  const statusCode = err instanceof AppError ? err.statusCode : 500;
  const message = err.message || 'Internal Server Error';

  res.status(statusCode).json({
    status: 'error',
    statusCode,
    message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  });
}
```

---

## Python CLI Tool

### Project Structure
```
cli-tool/
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── init.py
│   │   ├── build.py
│   │   └── deploy.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── helpers.py
│   └── core/
│       ├── __init__.py
│       └── manager.py
├── tests/
│   ├── __init__.py
│   └── test_cli.py
├── setup.py
├── requirements.txt
└── README.md
```

### Core Files

**src/cli.py**
```python
import click
from src.commands import init, build, deploy

@click.group()
@click.version_option()
def cli():
    """My CLI Tool - Description of what it does."""
    pass

cli.add_command(init.init_command)
cli.add_command(build.build_command)
cli.add_command(deploy.deploy_command)

if __name__ == '__main__':
    cli()
```

**src/commands/init.py**
```python
import click
from pathlib import Path

@click.command('init')
@click.argument('name')
@click.option('--template', default='basic', help='Project template to use')
@click.option('--path', default='.', help='Path to create project')
def init_command(name: str, template: str, path: str):
    """Initialize a new project."""
    project_path = Path(path) / name

    click.echo(f"Creating project: {name}")
    click.echo(f"Template: {template}")

    try:
        project_path.mkdir(parents=True, exist_ok=False)

        # Create project structure
        (project_path / 'src').mkdir()
        (project_path / 'tests').mkdir()

        # Create initial files
        (project_path / 'README.md').write_text(f"# {name}\n")
        (project_path / '.gitignore').write_text("__pycache__/\n*.pyc\n")

        click.secho(f"✓ Project created successfully at {project_path}", fg='green')
    except FileExistsError:
        click.secho(f"Error: Directory {name} already exists", fg='red', err=True)
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red', err=True)
```

**setup.py**
```python
from setuptools import setup, find_packages

setup(
    name='my-cli-tool',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'mycli=src.cli:cli',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A CLI tool for doing things',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my-cli-tool',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)
```

---

## Full-Stack Monorepo

### Project Structure
```
monorepo/
├── apps/
│   ├── web/                 # React frontend
│   │   ├── src/
│   │   ├── package.json
│   │   └── vite.config.ts
│   └── api/                 # Backend API
│       ├── src/
│       ├── package.json
│       └── tsconfig.json
├── packages/
│   ├── shared/              # Shared code
│   │   ├── src/
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── ui/                  # Shared UI components
│       ├── src/
│       ├── package.json
│       └── tsconfig.json
├── package.json             # Root package.json
├── turbo.json              # Turborepo config
├── tsconfig.json           # Base TypeScript config
└── .gitignore
```

### Root package.json
```json
{
  "name": "monorepo",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "test": "turbo run test",
    "lint": "turbo run lint"
  },
  "devDependencies": {
    "turbo": "latest",
    "typescript": "^5.0.0"
  }
}
```

### turbo.json
```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": []
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```
