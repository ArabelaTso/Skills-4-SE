# FastAPI Example Application (Migrated from Flask)

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

# Database setup
DATABASE_URL = "sqlite+aiosqlite:///./app.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

app = FastAPI(title="Items API", version="1.0.0")


# Models
class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float)
    active = Column(Boolean, default=True)


# Pydantic schemas
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    active: bool = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    active: Optional[bool] = None


class ItemSchema(ItemBase):
    id: int

    class Config:
        from_attributes = True


# Dependency
async def get_db():
    async with async_session() as session:
        yield session


# Routes
@app.get('/items', response_model=List[ItemSchema])
async def get_items(db: AsyncSession = Depends(get_db)):
    """Get all items."""
    result = await db.execute(select(Item))
    items = result.scalars().all()
    return items


@app.get('/items/{item_id}', response_model=ItemSchema)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific item."""
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post('/items', response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    """Create a new item."""
    new_item = Item(**item.dict())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


@app.put('/items/{item_id}', response_model=ItemSchema)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing item."""
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = item_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return item


@app.delete('/items/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an item."""
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(item)
    await db.commit()
    return None


@app.get('/items/search', response_model=List[ItemSchema])
async def search_items(q: str = Query(''), db: AsyncSession = Depends(get_db)):
    """Search items by name."""
    result = await db.execute(select(Item).where(Item.name.contains(q)))
    items = result.scalars().all()
    return items


# Startup event
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
