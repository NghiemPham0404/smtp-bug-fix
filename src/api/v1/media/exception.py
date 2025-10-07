from fastapi import HTTPException, status

class InvalidMediaType(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid media type")

class MediaFileNotFound(HTTPException):
    def __init__(self, media_id : int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"Media file with {media_id}")