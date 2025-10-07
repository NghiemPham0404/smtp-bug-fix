from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SpotTypeResponse(BaseModel):
    id: int
    name: str
    icon_url: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    spots_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)


class SpotTypeBase(BaseModel):
    icon_url: Optional[str] = None
    image_url: Optional[str] = None


class SpotTypeCreate(SpotTypeBase):
    name : str

class SpotTypeUpdate(SpotTypeBase):
    name : Optional[str] = None

