from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
import os
from datetime import timedelta, datetime, timezone
from pydantic import BaseModel
from sqlalchemy.orm import Session
import hashlib

from ..entities.email_otp import EmailOTP

from ..entities.user import User
from ..entities.auth import Token
from ..database.core import get_db


# http_bearer for authentication
http_bearer = HTTPBearer()

# bcrypt_context to hash password
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')


ALGORITHM=os.getenv('ALGORITHM')
SECRET_KEY=os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_SECRET_KEY=os.getenv('REFRESH_SECRET_KEY')
REFRESH_TOKEN_EXPIRE_DAYS=int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS'))
ISSUER = os.getenv('ISSUER') 


class TokenPayload(BaseModel):
    sub: int              # user_id
    role_id: Optional[int] = -1   # role is optional (not always in refresh token)
    iss: str              # issuer
    iat: int              # issued at (unix timestamp)
    exp: int      


# create access tokken
def create_access_token(user_id, role_id):
    to_encode = {'sub':f"{user_id}", 'role_id' : f"{role_id}"}
    expire = datetime.now(timezone.utc) +  timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(to_encode, expire, SECRET_KEY)


# create refresh token
def create_refresh_token(user_id):
    to_encode = {'sub': f"{user_id}"}
    expire = datetime.now(timezone.utc) +  timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return create_token(to_encode, expire, REFRESH_SECRET_KEY)


def create_token(to_encode, expire, key):
    to_encode.update({"exp": expire})
    to_encode.update(
        {
            "iat":  datetime.now(timezone.utc),
            "iss" : ISSUER,
        }
    )
    return jwt.encode(to_encode, key, algorithm=ALGORITHM)


# dependency that get current user
async def get_current_user(token_bearer: HTTPAuthorizationCredentials = Depends(http_bearer), 
                           db:Session= Depends(get_db)):
    try:
        print(token_bearer.credentials)
        token = token_bearer.credentials 
        payload = decode_access_token(token)

        if payload.iss != ISSUER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid issuer')
        
        if verify_token(token = token, db = db):
            user_id: int = payload.sub
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')


# decode access token
def decode_access_token(jwt_bearer_token:str):
    try:
        payload = jwt.decode(jwt_bearer_token, SECRET_KEY, algorithms=[ALGORITHM])
        payload['sub'] = int(payload['sub'])
        payload['role_id'] = int(payload['role_id'])
        return TokenPayload(**payload)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is expired or invalid')
    


# decode refresh token 
def decode_refresh_token(refresh_token:str):
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        payload['sub'] = int(payload['sub'])
        return TokenPayload(**payload)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is expired or invalid')
    

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def verify_token(token: str, db: Session) -> bool:
    # return True # only for testing
    token_db = db.query(Token).filter(Token.hashed_token == hash_token(token)).first()
    if token_db is None:
        return False
    return not token_db.revoked


def generate_hashed_password(raw_password: str) -> str:
    return bcrypt_context.hash(raw_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def create_signup_token(email: str, otp: str):
    payload = {
        "sub": email,
        "otp" : otp,
        "type": "SIGNUP",  # identify token type
        "iss": ISSUER,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# dependency that get current user
async def validate_signup_token(token_bearer: HTTPAuthorizationCredentials = Depends(http_bearer), 
                                db: Session = Depends(get_db)):
    try:
        token = token_bearer.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("iss") != ISSUER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid issuer")

        if payload.get("type") != "SIGNUP":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

        return True
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is expired or invalid")
