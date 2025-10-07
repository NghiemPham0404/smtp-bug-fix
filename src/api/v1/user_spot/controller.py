from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .service import user_spots_service
from .model import UserSpotType, UserSpot_Spot, UserSpot_User, UserSpotBase
from .enum import UserSpotSortEnum
from .exception import UserSpotNotFound, UserSpotExist

from ....database.core import get_db
from ....core.response import ListResponse, MessageResponse
from ....security.authentication import get_current_user
from ....security.authorization import get_current_permissions
from ....core.exception import ForbidenException, UnAuthorizedException

router = APIRouter(prefix="", tags=["UserSpots"])


@router.post("/scenic_spots/{spot_id}/users/{user_id}", status_code=201)
def add_user_spot(
    spot_id: int,
    user_id: int,
    user_spot_base : UserSpotBase,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Add a user_spot entry (VISITED, SAVED, FAVORITE, VIEWED).
    """
    
    permissions = get_current_permissions(user.role_id)
    if "add_user_spot" not in permissions:
        raise ForbidenException()
    
    if user_id != user.id:
        raise UnAuthorizedException()
    
    user_spot = user_spots_service.get_user_spot(db, spot_id, user_id, type=user_spot_base.type)
    if user_spot is not None:
        raise UserSpotExist()
    
    user_spots_service.add_user_spot(db=db, spot_id=spot_id, user_id=user_id, type=user_spot_base.type)
    return MessageResponse(detail=f"user_spot with user id = {user_id}, spot_id = {spot_id} type = {user_spot_base.type.name} created successfully")


@router.delete("/scenic_spots/{spot_id}/users/{user_id}", response_model=MessageResponse)
def delete_user_spot(
    spot_id: int,
    user_id: int,
    user_spot_base : UserSpotBase,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Delete a user_spot entry.
    """
    permissions = get_current_permissions(user.role_id)
    if "remove_user_spot" not in permissions:
        raise ForbidenException()
    
    if user_id != user.id:
        raise UnAuthorizedException()
    
    user_spot = user_spots_service.get_user_spot(db, spot_id, user_id, type=user_spot_base.type)
    if user_spot is None:
        raise UserSpotNotFound(user_id=user_id, spot_id=spot_id, type=user_spot_base.type)
    
    user_spots_service.delete_user_spot(db, user_spot)
    
    return MessageResponse(
        detail=f"user_spot with user id = {user_id}, spot_id = {spot_id} type = {user_spot_base.type.name} deleted successfully"
        )


@router.get("/users/{user_id}/scenic_spots", response_model=ListResponse[UserSpot_Spot])
def get_user_spots(
    user_id: int,
    type: UserSpotType,
    db: Session = Depends(get_db),
    search: str = Query(None),
    order_by: UserSpotSortEnum = Query(None),
    page: int = Query(1, gt=0),
    limit: int = Query(20, gt=0, lt=100),
    user = Depends(get_current_user)
):
    """
    Get all spots of a user by type.
    """
    permissions = get_current_permissions(user.role_id)
    if "view_user_spots" not in permissions:
        raise ForbidenException()
    return user_spots_service.get_user_spots(
        db=db, user_id=user_id, type=type, page=page, limit=limit, search=search, order_by=order_by
    )


@router.get("/scenic_spots/{spot_id}/users", response_model=ListResponse[UserSpot_User])
def get_spot_users_endpoint(
    spot_id: int,
    type: UserSpotType,
    db: Session = Depends(get_db),
    page: int = Query(1, gt=0),
    limit: int = Query(20, gt=0, lt=100),
    user = Depends(get_current_user)
):
    """
    Get all users of a spot by type.
    """
    permissions = get_current_permissions(user.role_id)
    if "view_user_spots" not in permissions:
        raise ForbidenException()
    return user_spots_service.get_spot_users(db=db, spot_id=spot_id, type=type, page=page, limit=limit)
