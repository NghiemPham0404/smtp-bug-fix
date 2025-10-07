from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func
from ..database.core import Base

class EmailOTP(Base):
    __tablename__ = "email_otps"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    otp_hash = Column(String, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)