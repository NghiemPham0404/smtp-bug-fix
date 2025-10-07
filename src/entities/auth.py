from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from ..database.core import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    hashed_token = Column(String, nullable=False)
    type = Column(String, nullable=False)  # ACCESS, REFRESH
    revoked = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class AuthProvider(Base):
    __tablename__ = "auth_providers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    provider_id = Column(String, nullable=False)
    provider_name = Column(String, nullable=False)  # GOOGLE, FACEBOOK, APPLE
    created_at = Column(DateTime(timezone=True), nullable=False)
