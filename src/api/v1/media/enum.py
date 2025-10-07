from enum import Enum

class MediaFileSortEnum(str, Enum):
    created_at_asc = "created_at_asc"
    created_at_desc = "created_at_desc"
    created_by_asc = "created_by_asc"
    created_by_desc = "created_by_desc"
    size_asc = "size_asc"
    size_desc = "size_desc"

class MediaTypeEnum(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"