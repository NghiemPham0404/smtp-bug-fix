# GENERAL PROMPTING FOR CRUD FASTAPI APPLICATION   

**ROLE:** backend developer
**Description:** Create a CRUD module for FastAPI Application
**Instruction:**
- Use clean architecture
- Write in a clear, runnable, performance, security, maintainable and scalable code
- Use nested query for if needed but make sure its doesn't violate clean arcgutecture
- example architect: 
```bash
 
├── v1/
│   ├── user/
    │   ├── __init__.py
    │   ├── controller.py
    │   ├── service.py
    │   ├── exceptions.py
    │   └── models.py
    └── todo/
    │   ├── __init__.py
    │   ├── controller.py
    │   ├── service.py
    │   ├── exceptions.py
    │   └── models.py
├── entities.py
    ├── user.py
    └── todo.py
├── database.py
├── main.py
```

Example code:
- entities
``` python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# /entities/user.py
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    todos = relationship("Todo", back_populates="owner")

# /entities/todo.py
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")
```

- exception

```python
from fastapi import HTTPException, status

# A base class for all custom API exceptions
class ApiException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail=detail)

# /user/exceptions.py
class UserNotFoundException(ApiException):
    def __init__(self):
        super().__init__(detail="User not found.")

# /todo/exceptions.py
class TodoNotFoundException(ApiException):
    def __init__(self):
        super().__init__(detail="Todo not found.")
```
- models
```python
# /todo/models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1)
    complete: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# /user/models.py
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    todos: List[Todo] = []

    class Config:
        orm_mode = True
```
- service
```python
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from .. import schemas, models

def get_todos(
    db: Session,
    page: int,
    limit: int,
    sort: Optional[str],
    query: Optional[str]
) -> Dict[str, Any]:
    """
    Handles the database query logic for listing todos with pagination, sorting, and filtering.
    """
    db_query = db.query(models.Todo)

    if query:
        db_query = db_query.filter(models.Todo.title.ilike(f"%{query}%"))

    total_results = db_query.count()
    total_pages = (total_results + limit - 1) // limit

    if sort:
        if sort == "id":
            db_query = db_query.order_by(models.Todo.id)
        elif sort == "title":
            db_query = db_query.order_by(models.Todo.title)
        elif sort == "complete":
            db_query = db_query.order_by(models.Todo.complete)

    offset = (page - 1) * limit
    todos = db_query.offset(offset).limit(limit).all()

    return {
        "results": todos,
        "page": page,
        "total_pages": total_pages,
        "total_results": total_results
    }
    
def get_todo(db: Session, todo_id: int):
    """
    Handles the database query for getting a single todo by its ID.
    """
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    
def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    """
    Handles the database query for creating a new todo.
    """
    db_todo = models.Todo(**todo.dict(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo_update: schemas.TodoUpdate):
    """
    Handles the database query for updating an existing todo.
    """
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    
    update_data = todo_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    """
    Handles the database query for deleting a todo.
    """
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    
    db.delete(db_todo)
    db.commit()
    return db_todo

```
- controller
```python
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import schemas
from ..database import get_db
from ..exceptions import TodoNotFoundException, UserNotFoundException
from ..services import todos as todo_service, users as user_service

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=schemas.PaginatedTodos)
def list_todos_controller(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort: Optional[str] = Query("id", regex="^(id|title|complete)$"),
    query: Optional[str] = None
):
    """
    List all todos with pagination, sorting, and filtering.
    """
    return todo_service.get_todos(db, page, limit, sort, query)
    
@router.get("/{todo_id}", response_model=schemas.Todo)
def get_todo_controller(
    todo_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single todo by its ID.
    """
    db_todo = todo_service.get_todo(db, todo_id)
    if db_todo is None:
        raise TodoNotFoundException()
    return db_todo

@router.post("/", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_todo_controller(
    todo: schemas.TodoCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Create a new todo for a specific user.
    """
    db_user = user_service.get_user(db, user_id)
    if db_user is None:
        raise UserNotFoundException()
        
    return todo_service.create_todo(db, todo, user_id)

@router.put("/{todo_id}", response_model=schemas.Todo)
def update_todo_controller(
    todo_id: int,
    todo_update: schemas.TodoUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing todo by its ID.
    """
    db_todo = todo_service.update_todo(db, todo_id, todo_update)
    if db_todo is None:
        raise TodoNotFoundException()
    return db_todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_controller(
    todo_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a todo by its ID.
    """
    db_todo = todo_service.delete_todo(db, todo_id)
    if db_todo is None:
        raise TodoNotFoundException()
    return

```