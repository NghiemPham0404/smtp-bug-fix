from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from ..database.core import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_at = Column(DateTime(timezone=True), nullable=True)


class SpotTag(Base):
    __tablename__ = "spot_tags"

    spot_id = Column(Integer, ForeignKey("scenic_spots.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
