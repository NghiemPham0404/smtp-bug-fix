from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from .service import SpotAttributeService, SpotAttributeSortEnum
from .model import (
    SpotAttributeCreate,
    SpotAttributeUpdate,
    SpotAttributeResponse,
)
from .exception import SpotAttributeNotFound, SpotAttributeExist

from ....database.core import get_db
from ....core.response import MessageResponse, ListResponse
from ....security.authentication import get_current_user
from ....security.authorization import get_current_permissions
from ....core.exception import ForbidenException

router = APIRouter(prefix="/scenic_spots/{spot_id}/spot_attributes", tags=["Spot Attributes"])

service = SpotAttributeService()


@router.get("/", response_model=ListResponse[SpotAttributeResponse])
def get_spot_attributes(
    spot_id: int,
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    sort_by: SpotAttributeSortEnum = SpotAttributeSortEnum.sort_order_asc,
    db: Session = Depends(get_db),
):

    return service.get_spot_attributes(db, spot_id, search, page, limit, sort_by)


@router.post("/", response_model=SpotAttributeResponse, status_code=status.HTTP_201_CREATED)
def create_spot_attribute(
    spot_id: int,
    spot_attr_create: SpotAttributeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    permissions = get_current_permissions(current_user.role_id)
    if "edit_spot" not in permissions:
        raise ForbidenException()
    
    attr = service.get_spot_attribute_by_name(db, spot_id, spot_attr_create.name)
    if attr is not None:
        raise SpotAttributeExist(spot_id, spot_attr_create.name)
    

    return service.create_spot_attribute(db, spot_id, spot_attr_create, current_user.id)


@router.put("/{spot_attribute_id}", response_model=SpotAttributeResponse)
def update_spot_attribute(
    spot_id: int,
    spot_attribute_id: int,
    body: SpotAttributeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    permissions = get_current_permissions(current_user.role_id)
    if "edit_spot" not in permissions:
        raise ForbidenException()

    attr = service.get_spot_attribute(db, spot_attribute_id)
    if attr is None:
        raise SpotAttributeNotFound(spot_attribute_id)
    
    duplicate_name_attr = service.get_spot_attribute_by_name(db, spot_id, body.name)
    if attr.id != duplicate_name_attr.id:
        raise SpotAttributeExist(spot_id, body.name)

    return service.update_spot_attribute(db, attr, body)


@router.delete("/{spot_attribute_id}", response_model=MessageResponse)
def delete_spot_attribute(
    spot_attribute_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    permissions = get_current_permissions(current_user.role_id)
    if "edit_spot" not in permissions:
        raise ForbidenException()
    
    attr = service.get_spot_attribute(db, spot_attribute_id)
    if attr is None:
        raise SpotAttributeNotFound(spot_attribute_id)

    service.delete_spot_attribute(db, attr)
    return MessageResponse(detail=f"Spot attribute with id = {spot_attribute_id} deleted successfully")

