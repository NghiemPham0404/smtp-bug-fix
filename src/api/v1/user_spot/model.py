from typing import List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel
from enum import Enum


class UserSpot_User(BaseModel):
    id : int
    name : str
    avatar : Optional[str] = None
    created_at : datetime


class UserSpot_Spot(BaseModel):
    id : int
    name : str
    thumb_img : Optional[str] = None
    created_at : datetime


class UserSpotType(Enum):
    VISITED = "VISITED"
    SAVED = "SAVED"
    FAVORITE = "FAVORITE"
    VIEWED = "VIEWED"


class UserSpotBase(BaseModel):
    type : UserSpotType