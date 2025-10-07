from fastapi import HTTPException, status


class SpotTypeNotFound(HTTPException):
    def __init__(self, type_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spot type with id {type_id} not found",
        )
