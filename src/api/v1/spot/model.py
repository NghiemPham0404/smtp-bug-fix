from pydantic import BaseModel, ConfigDict
from datetime import datetime, timezone
from typing import List, Optional

from .enum import SpotStatusEnum


class SpotBase(BaseModel):
    city_id: Optional[int] = None
    name: str
    address: Optional[str] = None
    description: Optional[str] = None
    longitude: float
    latitude: float
    radius: float
    status: Optional[SpotStatusEnum] = SpotStatusEnum.draft
    thumb_img: Optional[str] = None
    type: Optional[int] = None
    assignee_id: Optional[int] = None

    spot_tag_ids : Optional[List[int]] = None


class SpotCreate(SpotBase):
    created_at : Optional[datetime] = datetime.now(timezone.utc) 


class SpotUpdate(SpotBase):
    updated_at : Optional[datetime] = datetime.now(timezone.utc)


class SpotResponse(BaseModel):
    id: int
    city_id: Optional[int] = None
    name: str
    address: str
    description: Optional[str] = None
    longitude: float
    latitude: float
    radius: float
    status: str
    thumb_img: Optional[str] = None
    type: Optional[int] = None
    created_at: datetime
    created_by: int
    assignee_id: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    viewed_count: int = 0
    visited_count: int = 0
    favorite_count: int = 0
    saved_count: int = 0
    average_rating : Optional[float] = None
    feedbacks_count : Optional[int] = None
    spot_tag_ids: Optional[List[int]] = []
    spot_attributes_ids: Optional[List[int]] = []

    model_config = ConfigDict(from_attributes=True) 
