from typing import Optional
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session

from .service import tag_service
from .model import TagResponse, TagCreate, TagUpdate
from .enum import TagSortEnum
from .exception import TagNotFound

from ....core.response import ListResponse, MessageResponse
from ....core.exception import ForbidenException
from ....database.core import get_db
from ....security.authorization import get_current_permissions
from ....security.authentication import get_current_user

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("/", response_model=ListResponse[TagResponse])
def read_tags(
    db: Session = Depends(get_db),
    query_str: Optional[str] = Query(None, description="Search tags by name"),
    created_by: Optional[int] = Query(None, description="Filter by creator ID"),
    sort_by: Optional[TagSortEnum] = Query(None),
    page: Optional[int]= Query(None),
    limit: Optional[int]= Query(None),
):
    """
    Get tags with optional filters, sorting, and pagination.
    """
    return tag_service.get_tags(
        db,
        query_str=query_str,
        created_by=created_by,
        sort_by=sort_by,
        page=page,
        limit=limit,
    )


@router.get("/{tag_id}", response_model=TagResponse)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    """
    Get a specific tag by its ID.
    """
    tag = tag_service.get_tag(tag_id=tag_id, db=db)
    if tag is None:
        raise TagNotFound(tag_id=tag_id)
    return tag

@router.post("/", response_model=TagResponse, status_code=201)
def create_tag_endpoint(tag_data: TagCreate = Body(...), 
                        db: Session = Depends(get_db), 
                        user = Depends(get_current_user)):
    """
    Create a new tag with optional linked scenic spots.
    """
    permissions = get_current_permissions(user.role_id)
    if "create_tag" not in permissions:
        raise ForbidenException()
    return tag_service.create_tag(tag_data=tag_data, user_id=user.id, db=db)


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag_endpoint(tag_id: int, tag_data: TagUpdate = Body(...), 
                        db: Session = Depends(get_db), 
                        user = Depends(get_current_user)):
    """
    Update an existing tag and its related scenic spots.
    """
    permissions = get_current_permissions(user.role_id)
    if "edit_tag" not in permissions:
        raise ForbidenException()
    db_tag = tag_service.get_tag(tag_id, db)
    if db_tag is None:
        raise TagNotFound(tag_id)
    return tag_service.update_tag(db_tag=db_tag, tag_data=tag_data, db=db)


@router.delete("/{tag_id}", response_model=MessageResponse)
def delete_tag_endpoint(tag_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    """
    Delete a tag by ID.
    """
    permissions = get_current_permissions(user.role_id)
    if "edit_tag" not in permissions:
        raise ForbidenException()
    db_tag = tag_service.get_tag(tag_id, db)
    if db_tag is None:
        raise TagNotFound(tag_id)
    tag_service.delete_tag(db_tag=db_tag, db=db)
    return MessageResponse(detail=f"Tag with id = {tag_id} deleted successfully")
