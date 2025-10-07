from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey
from ..database.core import Base
from sqlalchemy.orm import relationship


class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    format = Column(String(50))
    type = Column(String, nullable=False)  # IMAGE, VIDEO, AUDIO
    size = Column(BigInteger)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    # flat relationships
    feedbacks = relationship(
        "Feedback",
        secondary="feedback_media_files",
        back_populates="media_files"
    )

    attributes = relationship("SpotAttribute", secondary="spot_attribute_media_files", back_populates="media_files")
