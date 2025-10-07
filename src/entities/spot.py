from sqlalchemy import (
    Column, Integer, String, Text, Float, ForeignKey, DateTime, Index, UniqueConstraint
)
from sqlalchemy.orm import relationship
from ..database.core import Base


class ScenicSpot(Base):
    __tablename__ = "scenic_spots"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="SET NULL"), index=True)
    name = Column(String(255), nullable=False, index=True)
    address = Column(String(255), nullable=False)
    description = Column(Text)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    radius = Column(Float, nullable=False)
    status = Column(String, nullable=False)  # DRAFT, APPROVAL-PENDING, ACTIVE, CLOSED
    thumb_img = Column(String)
    type = Column(Integer, ForeignKey("spot_types.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    assignee_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_at = Column(DateTime(timezone=True))
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    __table_args__ = (
        Index("idx_spot_name", "name"),
        Index("idx_spot_status", "status"),
    )


class SpotType(Base):
    __tablename__ = "spot_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    icon_url = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))


class SpotAttribute(Base):
    __tablename__ = "spot_attributes"

    id = Column(Integer, primary_key=True)
    spot_id = Column(Integer, ForeignKey("scenic_spots.id", ondelete="CASCADE"))
    name = Column(String(50), nullable=False)
    description = Column(Text)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True))
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("spot_id", "name", name="uq_spot_attribute_name_per_spot"),
    )

    media_files = relationship(
        "MediaFile",
        secondary="spot_attribute_media_files",
        back_populates="attributes"
    )


class SpotAttributeMediaFile(Base):
    __tablename__ = "spot_attribute_media_files"

    spot_attribute_id = Column(Integer, ForeignKey("spot_attributes.id", ondelete="CASCADE"), primary_key=True)
    media_file_id = Column(Integer, ForeignKey("media_files.id", ondelete="CASCADE"), primary_key=True)


class UserSpot(Base):
    __tablename__ = "user_spots"

    spot_id = Column(Integer, ForeignKey("scenic_spots.id", ondelete="CASCADE"), primary_key=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    type = Column(String, primary_key=True, index=True)  # VISITED, SAVED, VIEWED, FAVORITE

    __table_args__ = (
        # Explicit unique constraint (redundant with PK, but allowed)
        UniqueConstraint("spot_id", "created_by", "type", name="uq_user_spots_spot_id_created_by_type"),
    )


class SpotMediaFile(Base):
    __tablename__ = "spot_media_files"

    spot_id = Column(Integer, ForeignKey("scenic_spots.id", ondelete="CASCADE"), primary_key=True)
    media_file_id = Column(Integer, ForeignKey("media_files.id", ondelete="CASCADE"), primary_key=True)
