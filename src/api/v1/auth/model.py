from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone

from .enum import TokenTypeEnum, ProviderName

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str


class AuthProviderCreate(BaseModel):
    provider_id : str
    provider_name : str
    created_at : Optional[datetime] = datetime.now(timezone.utc)
    user_id : int


class TokenCreate(BaseModel):
    plain_token : str
    type : TokenTypeEnum
    revoked : Optional[bool] = False
    expires_at : datetime
    created_at : Optional[datetime] = datetime.now(timezone.utc)


class LoginByProviderModel(BaseModel):
    provider_id : str
    provider_name : str
    name : str
    email : str
    avatar : Optional[str]


class RequestOtpIn(BaseModel):
    email: EmailStr


class VerifyOtpIn(BaseModel):
    email: EmailStr
    otp: str

class SignUpByEmailModel(BaseModel):
    email : str
    name : str
    password : str
    avatar : Optional[str] = None

class LoginByEmailModel(BaseModel):
    email : str
    password : str


class RefreshTokenBody(BaseModel):
    refresh_token: str