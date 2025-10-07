
from enum import Enum

from enum import Enum

class SpotSortEnum(str, Enum):
    name_asc = "name_asc"
    name_desc = "name_desc"
    visited_count_asc = "visited_count_asc"
    visited_count_desc = "visited_count_desc"
    favorite_count_asc = "favorite_count_asc"
    favorite_count_desc = "favorite_count_desc"
    create_time_asc = "create_time_asc"
    create_time_desc = "create_time_desc"
    update_time_asc = "update_time_asc"
    update_time_desc = "update_time_desc"


class SpotStatusEnum(str, Enum):
    draft = "DRAFT"
    pending = "APPROVED-PENDING"
    active = "ACTIVE"
    closed = "CLOSED"