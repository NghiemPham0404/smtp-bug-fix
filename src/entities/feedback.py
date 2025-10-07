from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, SmallInteger, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database.core import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True)
    spot_id = Column(Integer, ForeignKey("scenic_spots.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    rating = Column(SmallInteger, nullable=False)  # 1 -> 5
    text = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("user_id", "spot_id", name="uq_feedback_user_spot"),
    )

    user = relationship("User", back_populates="feedbacks")

    # directly link to MediaFile
    media_files = relationship(
        "MediaFile",
        secondary="feedback_media_files",
        back_populates="feedbacks",
        cascade="all, delete"
    )


class FeedbackMediaFile(Base):
    __tablename__ = "feedback_media_files"

    feedback_id = Column(Integer, ForeignKey("feedbacks.id", ondelete="CASCADE"), primary_key=True)
    media_id = Column(Integer, ForeignKey("media_files.id", ondelete="CASCADE"), primary_key=True)


class FeedbackLike(Base):
    __tablename__ = "feedback_likes"

    feedback_id = Column(Integer, ForeignKey("feedbacks.id", ondelete="CASCADE"), primary_key=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
