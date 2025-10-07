# schemas/permission.py
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class PermissionOut(BaseModel):
    id: int
    name: str
    role_ids: List[int]

    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = []


class RoleUpdate(RoleBase):
    permission_ids: Optional[List[int]] = []


class RoleOut(RoleBase):
    id: int
    name: str
    permissions_ids: Optional[List] = []

    model_config = ConfigDict(from_attributes=True)


class PermissionOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
