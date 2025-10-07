from fastapi import HTTPException, status

class UserSpotNotFound(HTTPException):
    def __init__(self, spot_id : int, user_id : int, type : str):
        super().__init__(detail=f"User spot with spot_id = {spot_id}, user_id = {user_id}. type={type} not found",
                         status_code=status.HTTP_404_NOT_FOUND)


class UserSpotExist(HTTPException):
    def __init__(self, spot_id : int, user_id : int, type : str):
        super().__init__(detail=f"User spot with spot_id = {spot_id}, user_id = {user_id}. type={type} already exists",
                         status_code=status.HTTP_409_CONFLICT)