from math import ceil
from typing import Generic, List, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class MessageResponse(BaseModel):
    detail : str
    model_config = ConfigDict(from_attributes=True)

class ListResponse(BaseModel, Generic[T]):
    results : List[T]
    page  : int
    total_results : int
    total_pages : int
    model_config = ConfigDict(from_attributes=True)