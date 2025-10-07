from fastapi import HTTPException, status


class TagNotFound(HTTPException):
    def __init__(self, tag_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with id {tag_id} not found",
        )
