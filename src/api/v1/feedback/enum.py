from enum import Enum


class FeedbackSortEnum(str, Enum):
    CREATED_TIME_ASC = "created_time_asc"
    CREATE_TIME_DESC = "created_time_desc"
    UPDATE_TIME_ASC = "updated_time_asc"
    UPDATE_TIME_DESC = "updated_time_desc"
    RATING_ASC = "rating_asc"
    RATING_DESC = "rating_desc"
    LIKES_COUNT_ASC = "likes_count_asc"
    LIKES_COUNT_DESC = "likes_count_des"
