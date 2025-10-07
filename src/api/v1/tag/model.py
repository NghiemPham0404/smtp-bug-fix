from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TagResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    created_by: Optional[int]
    updated_at: Optional[datetime]

    spots_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)

class TagBase(BaseModel):
    name: str

    spots_ids : Optional[List[int]] = None

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass