from fastapi import HTTPException, status

class CityNotFound(HTTPException):
    def __init__(self, city_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with ID {city_id} not found",
        )