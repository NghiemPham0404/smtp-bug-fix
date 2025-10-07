from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class FeedbackBase(BaseModel):
    rating: int
    text: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    spot_id: int

    media_file_ids : Optional[List[int]] = []


class FeedbackUpdate(BaseModel):
    rating: Optional[int] = None
    text: Optional[str] = None

    media_file_ids : Optional[List[int]] = []


class FeedbackUserBase(BaseModel):
    id: int
    name: str
    avatar: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class FeedbackResponse(FeedbackBase):
    id: int
    rating: int
    text: Optional[str] = None
    spot_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


    user: Optional[FeedbackUserBase] = None
    media_file_urls: Optional[List[str]] = []
    likes_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)
