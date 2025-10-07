from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from ..database.core import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    thumb_image = Column(String)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    radius = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    __table_args__ = (
        Index("idx_city_name", "name"),
    )
