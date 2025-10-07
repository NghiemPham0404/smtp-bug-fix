from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Index
from ..database.core import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255), nullable=True)
    avatar = Column(String)
    joined_date = Column(Date, nullable=False)
    last_login = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    # Relationship
    feedbacks = relationship("Feedback", back_populates="user")

    __table_args__ = (
        Index("idx_user_name", "name"),
    )
