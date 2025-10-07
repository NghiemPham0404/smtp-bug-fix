from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from .service import feedback_service
from .model import FeedbackCreate, FeedbackUpdate, FeedbackResponse
from .enum import FeedbackSortEnum
from .exception import FeedbackNotFound, AlreadyLikeFeedbackException
from ....core.response import ListResponse, MessageResponse
from ....database.core import get_db
from ....security.authentication import get_current_user  # adjust if your project uses a different dependency
from ....security.authorization import get_current_permissions
from ....core.exception import UnAuthorizedException, ForbidenException

router = APIRouter(prefix="/feedbacks", tags=["Feedbacks"])


@router.get("/", response_model=ListResponse[FeedbackResponse])
def list_feedbacks(
    db: Session = Depends(get_db),
    spot_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    sort_by: Optional[FeedbackSortEnum] = Query(None),
    page: int = Query(default=1, gt=0),
    limit: int = Query(default=20, gt=0, lt=100),
):
    return feedback_service.get_feedbacks(db=db, spot_id=spot_id, user_id=user_id, sort_by=sort_by, page=page, limit=limit)


@router.get("/{feedback_id}", response_model=FeedbackResponse)
def read_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = feedback_service.get_feedback(feedback_id=feedback_id, db=db)
    if feedback is None:
        raise FeedbackNotFound(feedback_id=feedback_id)
    return feedback


@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_new_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    permissions = get_current_permissions(current_user.role_id)
    if "submit_feedback" in permissions:
        return feedback_service.create_feedback(db=db, user_id=current_user.id, data=data)
    else:
        raise ForbidenException()


@router.put("/{feedback_id}", response_model=FeedbackResponse)
def update_existing_feedback(
    feedback_id: int,
    data: FeedbackUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    
    permissions = get_current_permissions(current_user.role_id)
    if "edit_feedback" not in permissions:
        raise ForbidenException()
    
    db_feedback = feedback_service.get_feedback(db=db, feedback_id=feedback_id)
    if db_feedback is None:
        raise FeedbackNotFound(feedback_id=feedback_id)
    if db_feedback.user_id != current_user.id:
        raise UnAuthorizedException()
    
    updated = feedback_service.update_feedback(db=db, db_feedback=db_feedback, data=data)
    return updated


@router.delete("/{feedback_id}", response_model=MessageResponse)
def delete_existing_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    permissions = get_current_permissions(current_user.role_id)
    if "delete_feedback" not in permissions:
        raise ForbidenException()
    
    db_feedback = feedback_service.get_feedback(db=db, feedback_id=feedback_id)
    if db_feedback is None:
        raise FeedbackNotFound(feedback_id=feedback_id)
    if db_feedback.user_id != current_user.id:
        raise UnAuthorizedException()

    feedback_service.delete_feedback(db=db, db_feedback=db_feedback)
    return MessageResponse(f"Feedback with id = {feedback_id} deleted successfully")


@router.post("/{feedback_id}/like", response_model=MessageResponse)
def like_feedback(feedback_id:int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    permissions = get_current_permissions(current_user.role_id)
    if "like_feedback" not in permissions:
        raise ForbidenException()
    db_feedback = feedback_service.get_feedback(db=db, feedback_id=feedback_id)
    if db_feedback is None:
        raise FeedbackNotFound(feedback_id=feedback_id)
    existing = feedback_service.get_feecback_like(db=db, feedback_id=feedback_id, user_id=current_user.id)
    if existing:
        raise AlreadyLikeFeedbackException(feedback_id=feedback_id)
    feedback_service.like_feedback(db=db, feedback_id=feedback_id, user_id=current_user.id)
    return MessageResponse(detail=f"Feedback with id = {feedback_id} liked successfully")


@router.delete("/{feedback_id}/like", response_model=MessageResponse)
def unlike_feedback(feedback_id:int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    permissions = get_current_permissions(current_user.role_id)
    if "like_feedback" not in permissions:
        raise ForbidenException()
    db_feedback = feedback_service.get_feedback(db=db, feedback_id=feedback_id)
    if db_feedback is None:
        raise FeedbackNotFound(feedback_id=feedback_id)
    existing = feedback_service.get_feecback_like(db=db, feedback_id=feedback_id, user_id=current_user.id)
    if existing:
        feedback_service.unlike_feedback(db=db, feedback_like=existing)
        return MessageResponse(detail=f"Feedback with id = {feedback_id} unliked successfully")