from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional

class CityBase(BaseModel):
    name : str
    longitude : float
    latitude : float
    radius : float

class CityCreate(CityBase):
    thumb_image : Optional[str] = None
    created_at : datetime = datetime.now(timezone.utc)

class CityUpdate(CityBase):
    thumb_image : Optional[str] = None
    updated_at : datetime = datetime.now(timezone.utc)


class CityResponse(BaseModel):
    id : int
    name : str
    thumb_image : Optional[str] = None
    longitude : float
    latitude : float
    radius : float
    created_at : datetime
    updated_at :  Optional[datetime] = None

    spots_count : Optional[int] = 0

