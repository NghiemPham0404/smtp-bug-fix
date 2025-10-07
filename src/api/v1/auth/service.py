from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
import hashlib, random
from datetime import datetime, timedelta, timezone
from fastapi_mail import MessageSchema
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi import HTTPException
import smtplib
import dns.resolver
from email_validator import validate_email

from .model import AuthResponse, TokenTypeEnum, SignUpByEmailModel

from ....entities.auth import Token, AuthProvider
from ....entities.user import User
from ....security.authentication import *
from ....entities.email_otp import EmailOTP
from ....core.email import fm, templates


class AuthService:
   def authenticate_user(self, user_id : int, role_id : int, db:Session) -> AuthResponse:
      access_token = create_access_token(user_id=user_id, role_id = role_id)
      refresh_token = create_refresh_token(user_id=user_id)
      self.create_db_token(user_id=user_id, token=access_token, type = TokenTypeEnum.access, db = db)
      self.create_db_token(user_id=user_id, token=refresh_token, type = TokenTypeEnum.refresh, db = db)
      return AuthResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

   def create_db_token(self, user_id : int, token : str, type : TokenTypeEnum, db : Session):
      if type == TokenTypeEnum.access:
         expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      elif type == TokenTypeEnum.refresh:
         expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

      token_db = Token(
         hashed_token = hash_token(token),
         type = type.value,
         expires_at = expires_at,
         user_id = user_id,
         created_at = datetime.now(timezone.utc)
      )
      db.add(token_db)
      db.commit()
      db.refresh(token_db)
      return token_db
   
   def create_auth_provider(self, user_id : int, provider_id : str, provider_name : str, db:Session):
      auth_provider = AuthProvider(
         user_id = user_id,
         provider_id = provider_id,
         provider_name = provider_name,
         created_at = datetime.now(timezone.utc)
      )
      db.add(auth_provider)
      db.commit()
      db.refresh(auth_provider)
      return auth_provider


   def create_user_profile(self, name : str, email : str, avatar : str, role_id : int, db : Session):
      user = User(
         name=name, 
         email=email, 
         avatar=avatar, 
         joined_date=datetime.now(timezone.utc), 
         last_login=datetime.now(timezone.utc), 
         role_id = role_id
      )
      db.add(user)
      db.commit()
      db.refresh(user)
      return user

   def get_auth_provider(self, provider_id : str, provider_name, db : Session):
      return db.query(AuthProvider).filter(and_(AuthProvider.provider_id == provider_id, 
                                                AuthProvider.provider_name == provider_name)).first()

   def login_by_provider(self, 
                         provider_id : str, 
                         provider_name : str, 
                         name : str, 
                         email : str, 
                         avatar  : str,
                         db : Session):
      
      auth_provider = self.get_auth_provider(provider_id=provider_id, provider_name=provider_name)
      if auth_provider is None:
         user = self.create_user_profile(name=name, email=email, avatar=avatar, role_id=5, db=db)
         auth_provider = self.create_auth_provider(user_id=user.id, provider_id=provider_id, provider_name=provider_name, db=db)
      
      user = db.query(User).filter(User.id == auth_provider.user_id).first()
      if not user:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
      return self.authenticate_user(user_id=user.id, role_id=user.role_id, db=db)

   
   def sign_up_by_email(self, db: Session, signup_model: SignUpByEmailModel):
      user = User(
         name=signup_model.name, 
         email= signup_model.email, 
         avatar= signup_model.avatar, 
         joined_date=datetime.now(timezone.utc), 
         last_login=datetime.now(timezone.utc), 
         role_id = 1,
         hashed_password = generate_hashed_password(signup_model.password)
      )
      db.add(user)
      db.commit()
      db.refresh(user)
      return self.authenticate_user(user_id=user.id, role_id=user.role_id, db=db)
   
   def revoke_all_tokens_of_user(self, db: Session, user_id: int):
        db.query(Token).filter(
            Token.user_id == user_id,
            Token.revoked == False
        ).update({"revoked": True})
        db.commit()
      

auth_service = AuthService()


class EmailService:
   async def is_email_valid(self, email: str) -> bool:
      try:
         # Step 1: syntax check
         valid = validate_email(email)
         domain = valid["domain"]

         # Step 2: MX record check
         records = dns.resolver.resolve(domain, "MX")
         mx_record = str(records[0].exchange)

         # Step 3: Try connecting SMTP (optional, skip in dev)
         server = smtplib.SMTP(timeout=5)
         server.connect(mx_record)
         server.quit()
         return True
      except Exception:
         return False

   def generate_otp(self) -> str:
      return f"{random.randint(0, 999999):06d}"

   def hash_otp(self, otp: str) -> str:
      return hashlib.sha256(otp.encode("utf-8")).hexdigest()

   def create_otp(self, db: Session, email: str, expire_minutes: int = 10) -> str:
      otp = self.generate_otp()
      otp_hash = self.hash_otp(otp)
      expires_at = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

      record = EmailOTP(email=email, otp_hash=otp_hash, expires_at=expires_at)
      db.add(record)
      db.commit()
      db.refresh(record)
      return otp

   def verify_otp(self, db: Session, email: str, otp: str):
      otp_hash = self.hash_otp(otp)
      record = (
         db.query(EmailOTP)
         .filter(EmailOTP.email == email, EmailOTP.otp_hash == otp_hash)
         .order_by(EmailOTP.created_at.desc())
         .first()
      )
      if record.is_used:
        raise HTTPException(status_code=400, detail="OTP already used")
      if record and not record.is_used and record.expires_at > datetime.now(timezone.utc):
         record.is_used = True
         db.commit()
         return record
      return None



   async def send_email(self, subject: str, recipients: list[EmailStr], template_name: str, context: dict):
      """Render Jinja2 template and send email"""
      template = templates.get_template(template_name)
      html_body = template.render(context)

      message = MessageSchema(
         subject=subject,  # e.g. "Your OTP Code: 123456"
         recipients=recipients,
         body=html_body,
         subtype="html",
      )
      await fm.send_message(message)

email_service = EmailService()
