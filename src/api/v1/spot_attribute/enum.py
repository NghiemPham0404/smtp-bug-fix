from enum import Enum


class SpotAttributeSortEnum(str, Enum):
    sort_order_asc = "sort_order_asc"
    sort_order_desc = "sort_order_desc"
    name_asc = "name_asc"
    name_desc = "name_desc"
    created_time_asc = "created_time_asc"
    created_time_desc = "created_time_desc"