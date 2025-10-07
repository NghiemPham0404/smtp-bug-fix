from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .exception import *
from .model import *
from .service import user_service

from ....core.response import ListResponse, MessageResponse
from ....database.core import get_db
from ....security.authentication import get_current_user
from ....security.authorization import get_current_permissions
from ....core.exception import ForbidenException


router = APIRouter(prefix="/users", tags=["Users"])



@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if user is None:
        return UserNotFoundException(user_id)
    return user


@router.get("/", response_model=ListResponse[UserResponse])
def list_users(
    page: int = 1,
    limit: int = 20,
    sort_by: UserSortBy = UserSortBy.joined_date_asc,
    is_active: bool | None = None,
    role_id: int | None = None,
    db: Session = Depends(get_db),
):
    return user_service.list_users(db, page, limit, sort_by, is_active, role_id)


@router.post("/", response_model=UserResponse)
def create_user(user_create : UserCreate, 
                db: Session = Depends(get_db), 
                current_user = Depends(get_current_user)):
    permissions = get_current_permissions(current_user.role_id)
    if 'manage_users' not in permissions:
        raise ForbidenException()
    return user_service.create_user(db, user_create)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, 
                user_update : UserUpdate,
                db: Session = Depends(get_db),
                current_user = Depends(get_current_user)):
    permissions = get_current_permissions(current_user.role_id)
    if current_user.id != user_id and 'manage_users' not in permissions:
        raise ForbidenException()
    
    if (user_update.role_id is not None) and 'manage_users' not in permissions:
        raise ForbidenException()
    
    db_user = user_service.get_user(db, user_id)
    if db_user is None:
        raise UserNotFoundException(user_id)
    
    return user_service.update_user(db, db_user, user_update)


@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(user_id: int, 
                db: Session = Depends(get_db),
                current_user = Depends(get_current_user)):
    permissions = get_current_permissions(current_user.role_id)
    if current_user.id != user_id and 'manage_users' not in permissions:
        raise ForbidenException()
    
    db_user = user_service.get_user(db, user_id)
    if db_user is None:
        raise UserNotFoundException(user_id)

    user_service.delete_user(db, db_user)
    return MessageResponse(detail=f"User with id {user_id} deleted successfully")
