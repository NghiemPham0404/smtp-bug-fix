from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional
from datetime import datetime
from .enum import MediaTypeEnum


class MediaFileBase(BaseModel):
    url: str
    format: Optional[str] = None
    type: MediaTypeEnum
    size: Optional[int] = None


class MediaFileCreate(BaseModel):
    type: MediaTypeEnum
    file: bytes  # uploaded file content
    filename: str


class MediaFileResponse(MediaFileBase):
    id: int
    url: str
    format: Optional[str] = None
    type: MediaTypeEnum
    size: Optional[int] = None
    created_by: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    model_config : ConfigDict = ConfigDict(from_attributes=True)

