from datetime import datetime, timezone
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from ....core.response import MessageResponse

from .exception import ExpiredOtpException, InvalidOtpException

from ....entities.user import User

from ....core.exception import UnAuthorizedException

from .service import (auth_service, verify_token, create_signup_token, verify_password,
                      decode_refresh_token, validate_signup_token, email_service)
from .model import (AuthResponse, RefreshTokenBody, LoginByProviderModel,
                     RequestOtpIn, VerifyOtpIn, SignUpByEmailModel, LoginByEmailModel)

from ....database.core import get_db

router = APIRouter(prefix="/auth", tags=['authentication'])

@router.post("/request-otp", response_model=MessageResponse)
async def request_otp(payload: RequestOtpIn, db: Session = Depends(get_db)):
    otp = email_service.create_otp(db, payload.email)

    email = payload.email

    # 1️⃣ Check existing user
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="This email is already registered.")

    # 2️⃣ Validate email (SMTP + MX check)
    if not await email_service.is_email_valid(email):
        raise HTTPException(status_code=400, detail="Invalid or unreachable email address.")

    # ✅ Send email with Jinja2 template
    await email_service.send_email(
        subject=f"Your OTP Code  : {otp}",
        recipients=[payload.email],
        template_name="emails/otp.html",
        context={"otp": otp},
    )

    return MessageResponse(detail= "OTP sent to your email")

@router.post("/verify-otp", response_model=AuthResponse)
def verify_otp_endpoint(payload: VerifyOtpIn, db: Session = Depends(get_db)):
    record = email_service.verify_otp(db, payload.email, payload.otp)
    if not record:
        raise InvalidOtpException()
    if record.expires_at < datetime.now(timezone.utc):
        raise ExpiredOtpException()
    return {"access_token": create_signup_token(payload.email, payload.otp), "refresh_token": None, "token_type": "bearer"}


@router.post("/regis_by_email", response_model = AuthResponse)
def regist_by_email(db : Annotated[Session, Depends(get_db)], signup_model : SignUpByEmailModel, valid : bool = Depends(validate_signup_token)):
    if valid:
        return auth_service.sign_up_by_email(db=db, signup_model=signup_model)
    else:
        return UnAuthorizedException()


@router.post("/login_by_email", response_model = AuthResponse)
def login_by_email(db : Annotated[Session, Depends(get_db)],
                login_model : LoginByEmailModel,
                ):
    user = db.query(User).filter(User.email == login_model.email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if  verify_password(login_model.password, user.hashed_password):
        return auth_service.authenticate_user(user_id=user.id, role_id=user.role_id, db=db)
    
    return UnAuthorizedException()




@router.post("/login_by_provider", response_model = AuthResponse)
def login_provider(db : Annotated[Session, Depends(get_db)],
                login_model : LoginByProviderModel,
                ):
    return auth_service.login_by_provider(
        provider_id= login_model.provider_id, 
        provider_name= login_model.provider_name, 
        name= login_model.name, 
        email=login_model.email, 
        avatar= login_model.avatar, 
        db=db)


@router.post("/refresh-token", response_model = AuthResponse)
def refresh_token(db : Annotated[Session, Depends(get_db)], refresh_token_body : RefreshTokenBody):
    payload = decode_refresh_token(refresh_token_body.refresh_token)
    auth_service.revoke_all_tokens_of_user(db=db, user_id=payload.sub)
    return auth_service.authenticate_user(user_id=payload.sub, role_id=None, db=db)

