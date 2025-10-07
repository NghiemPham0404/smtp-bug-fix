from ..database.core import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from ..entities.role import *

DEFAULT_PERMISSIONS = ["trial"]

roles_permissions : dict[int, list[str]] = {}


def get_roles_permissions_map(db : Session):
    roles = db.query(Role).all()
    for role in roles:
        roles_permissions[role.id] = get_permissions_of_role(role.id, db)
    print(roles)


def get_permissions_of_role(role_id : int,  db:Session):
    permissions = []
    user_permissions = (db.query(Permission)
                        .join(RolePermission, onclause= Permission.id == RolePermission.permission_id)
                        .join(Role, onclause= RolePermission.role_id == Role.id)
                        .filter(Role.id == role_id)
                        .all())
    if user_permissions:
        for permission in user_permissions:
            permissions.append(permission.name)
    return permissions

def get_current_permissions(role_id : int):
    if role_id is None or role_id not in roles_permissions:
        return DEFAULT_PERMISSIONS
    return roles_permissions[role_id]


def refresh(db : Session):
    get_roles_permissions_map(db = db)