from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SpotAttributeBase(BaseModel):
    name : str
    description : Optional[str] = None
    sort_order : Optional[int] = 0


class SpotAttributeCreate(SpotAttributeBase):
    media_file_ids : Optional[list[int]] = None


class SpotAttributeUpdate(SpotAttributeBase):
    media_file_ids : Optional[list[int]] = None


class SpotAttributeResponse(BaseModel):
    id : int
    spot_id : int
    name : str
    description : Optional[str] = None
    sort_order : Optional[int] = 0
    created_at : datetime
    updated_at : Optional[datetime] = None
    created_by : int

    media_file_urls : Optional[list[str]] = []
    
    model_config = ConfigDict(from_attributes=True)