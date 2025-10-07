from fastapi import HTTPException, status


class FeedbackNotFound(HTTPException):
    def __init__(self, feedback_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feedback with id {feedback_id} not found",
        )


class AlreadyLikeFeedbackException(HTTPException):
    def __init__(self, feedback_id:int):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Feedback with id {feedback_id} not found",
        )
