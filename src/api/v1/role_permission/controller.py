# controllers/role_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .service import role_service, permission_service
from .model import RoleCreate, RoleUpdate, RoleOut, PermissionOut
from .exception import RoleNotFound

from ....database.core import get_db
from ....security.authentication import get_current_user
from ....security.authorization import refresh
from ....core.response import MessageResponse
from ....core.exception import ForbidenException

router = APIRouter(prefix="", tags=["Roles & Permissions"])

@router.get("/roles", response_model=List[RoleOut])
def list_roles(db: Session = Depends(get_db)):
    return role_service.get_roles(db)
    

@router.post("/roles", response_model=RoleOut)
def create_role(role_data: RoleCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role_id != 1 and user.role_id != 2:
        raise ForbidenException()
    role = role_service.create_role(db, role_data)
    refresh(db)
    return role


@router.put("/roles/{role_id}", response_model=RoleOut)
def update_role(role_id: int, role_data: RoleUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role_id != 1 and user.role_id != 2:
        raise ForbidenException()
    db_role = role_service.get_role(db, role_id)
    if not db_role:
        raise RoleNotFound(role_id)
    role = role_service.update_role(db, db_role, role_data)
    refresh(db)
    return role


@router.delete("/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role_id != 1 and user.role_id != 2:
        raise ForbidenException()
    db_role = role_service.get_role(db, role_id)
    if not db_role:
        raise RoleNotFound(role_id)
    role_service.delete_role(db, db_role)
    refresh(db)
    return MessageResponse(detail=f"role with id = {role_id} deleted successfully")
        


@router.get("/permissions", response_model=List[PermissionOut])
def list_permissions(db: Session = Depends(get_db)):
    permissions = permission_service.get_permissions(db)
    return [
        PermissionOut(id=p.id, name=p.name)
        for p in permissions
    ]
