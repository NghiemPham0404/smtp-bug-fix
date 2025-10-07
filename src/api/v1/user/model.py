from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime


# Sorting Enum
class UserSortBy(str, Enum):
    joined_date_asc = "joined_date_asc"
    joined_date_desc = "joined_date_desc"
    last_login_asc = "last_login_asc"
    last_login_desc = "last_login_desc"
    name_asc = "name_asc"
    name_desc = "name_desc"
    email_asc = "email_asc"
    email_desc = "email_desc"


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = True
    role_id: Optional[int] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email : Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None


class UserResponse(UserBase):
    id: int
    name: str
    email: EmailStr
    avatar: Optional[str] = None
    is_active: Optional[bool] = True
    role_id: Optional[int] = None
    last_login: Optional[datetime] = None
    joined_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)



