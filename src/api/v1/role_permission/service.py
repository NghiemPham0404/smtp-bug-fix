# services/role_service.py

from sqlalchemy import func
from sqlalchemy.orm import Session

from .model import RoleCreate, RoleUpdate, RoleOut

from ....entities import Role, RolePermission, Permission


class RoleService:


    def get_roles(self, db: Session):
        # Aggregate permission IDs per role
        query = (
            db.query(
                Role.id,
                Role.name,
                func.coalesce(func.array_agg(RolePermission.permission_id), []).label("permissions_ids")
            )
            .outerjoin(RolePermission, Role.id == RolePermission.role_id)
            .group_by(Role.id)
            .order_by(Role.id)
        )

        results = query.all()

        # Turn into dicts or Pydantic models depending on your schema
        return results


    def create_role(self, db: Session, role_data: RoleCreate):
        # Create role
        role = Role(name=role_data.name)
        db.add(role)
        db.commit()
        db.refresh(role)

        # Insert role-permissions mapping if provided
        if role_data.permission_ids:
            role_permissions = [
                RolePermission(role_id=role.id, permission_id=pid)
                for pid in role_data.permission_ids
            ]
            db.bulk_save_objects(role_permissions)
            db.commit()

        role.permissions_ids = role_data.permission_ids

        return role


    def get_role(self, db: Session, role_id: int):
        return db.query(Role).filter(Role.id == role_id).first()


    def update_role(self, db: Session, db_role: Role, role_data: RoleUpdate):

        db_role.name = role_data.name
        db.commit()
        db.refresh(db_role)

        if role_data.permission_ids is not None:
            # Remove old permissions
            db.query(RolePermission).filter(RolePermission.role_id == db_role.id).delete()
            db.commit()

            # Insert new permissions
            if role_data.permission_ids:
                role_permissions = [
                    RolePermission(role_id=db_role.id, permission_id=pid)
                    for pid in role_data.permission_ids
                ]
                db.bulk_save_objects(role_permissions)
                db.commit()

        db_role.permissions_ids = role_data.permission_ids

        return db_role


    def delete_role(self, db: Session, db_role: Role):
        # Cascades will handle role_permissions if DB schema is set correctly
        db.delete(db_role)
        db.commit()
        return True


role_service = RoleService()


class PermissionService:
    def get_permissions(self, db: Session):
        return db.query(Permission).all()
    
permission_service = PermissionService()