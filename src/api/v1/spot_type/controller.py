from typing import Optional
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session

from .service import spot_type_service
from .model import SpotTypeResponse, SpotTypeCreate, SpotTypeUpdate
from .enum import SpotTypeSortEnum
from .exception import SpotTypeNotFound

from ....core.response import ListResponse, MessageResponse
from ....database.core import get_db
from ....security.authentication import get_current_user
from ....security.authorization import get_current_permissions
from ....core.exception import ForbidenException

router = APIRouter(prefix="/spot_types", tags=["Spot types"])


@router.get("/", response_model=ListResponse[SpotTypeResponse])
def read_spot_types(
    db: Session = Depends(get_db),
    query_str: Optional[str] = Query(None, description="Search spot types by name"),
    sort_by: Optional[SpotTypeSortEnum] = Query(None),
    page: Optional[int] = None,
    limit: Optional[int] = None,
):
    """
    Get spot types with optional filters, sorting, and pagination.
    """
    return spot_type_service.get_spot_types(
        db,
        query_str=query_str,
        sort_by=sort_by,
        page=page,
        limit=limit,
    )


@router.get("/{type_id}", response_model=SpotTypeResponse)
def read_spot_type(type_id: int, db: Session = Depends(get_db)):
    """
    Get a specific spot type by its ID.
    """
    spot_type = spot_type_service.get_spot_type(type_id=type_id, db=db)
    if spot_type is None:
        raise SpotTypeNotFound(type_id=type_id)
    return spot_type


@router.post("/", response_model=SpotTypeResponse, status_code=201)
def create_spot_type_endpoint(spot_type_data: SpotTypeCreate = Body(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Create a new spot type.
    """
    permissions = get_current_permissions(user.role_id)
    if "create_spot_type" not in permissions:
        return ForbidenException()
    return spot_type_service.create_spot_type(spot_type_data=spot_type_data, db=db)


@router.put("/{type_id}", response_model=SpotTypeResponse)
def update_spot_type_endpoint(type_id: int, 
                              spot_type_data: SpotTypeUpdate = Body(...), 
                              db: Session = Depends(get_db),
                              user=Depends(get_current_user)):
    """
    Update an existing spot type.
    """
    permissions = get_current_permissions(user.role_id)
    if "edit_spot_type" not in permissions:
        return ForbidenException()
    db_spot_type = spot_type_service.get_spot_type(type_id, db)
    if db_spot_type is None:
        raise SpotTypeNotFound()
    return spot_type_service.update_spot_type(db_spot_type = db_spot_type, spot_type_data=spot_type_data, db=db)


@router.delete("/{type_id}", response_model=MessageResponse)
def delete_spot_type_endpoint(type_id: int, 
                              db: Session = Depends(get_db),
                              user=Depends(get_current_user)):
    """
    Delete a spot type by ID.
    """
    permissions = get_current_permissions(user.role_id)
    if "delete_spot_type" not in permissions:
        return ForbidenException()
    db_spot_type = spot_type_service.get_spot_type(type_id, db)
    if db_spot_type is None:
        raise SpotTypeNotFound(type_id=type_id)
    spot_type_service.delete_spot_type(db_spot_type=db_spot_type, db=db)
    return MessageResponse(detail=f"spot type with id = {type_id} deleted successfully")