from fastapi import HTTPException


class RoleNotFound(HTTPException):
    def __init__(self, role_id: int):
        super().__init__(status_code=404, detail=f"Role with id {role_id} not found")


from fastapi import HTTPException


class PermissionNotFound(HTTPException):
    def __init__(self, permission_id: int):
        super().__init__(status_code=404, detail=f"Permission with id {permission_id} not found")