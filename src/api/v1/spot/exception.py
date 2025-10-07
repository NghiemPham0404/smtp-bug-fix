from fastapi import HTTPException, status


class SpotNotFound(HTTPException):
    def __init__(self, spot_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenic spot with ID {spot_id} not found",
        )