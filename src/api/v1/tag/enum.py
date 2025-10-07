from enum import Enum


class TagSortEnum(str, Enum):
    name_asc = "name_asc"
    name_desc = "name_desc"
    create_time_asc = "create_time_asc"
    create_time_desc = "create_time_desc"
    update_time_asc = "update_time_asc"
    update_time_desc = "update_time_desc"
