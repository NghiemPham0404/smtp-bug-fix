from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session

from .service import spot_service
from .model import (SpotResponse, SpotCreate, SpotUpdate)
from .enum import SpotSortEnum, SpotStatusEnum
from .exception import SpotNotFound

from ....core.response import ListResponse, MessageResponse
from ....database.core import get_db
from ....security.authentication import get_current_user
from ....security.authorization import get_current_permissions
from ....core.exception import ForbidenException

router = APIRouter(prefix="/scenic_spots", tags=["Scenic Spots"])
    

@router.get("/", response_model= ListResponse[SpotResponse])
def read_scenic_spots(
    db: Session = Depends(get_db),
    query_str : Optional[str] = Query(None),
    tags: Optional[List[int]] = Query(None),
    created_by: Optional[int] = Query(None),
    assignee_id: Optional[int] = Query(None),
    spot_type: Optional[int] = Query(None),
    city_id: Optional[int] = Query(None),
    status: Optional[List[str]] = Query(
        None,
        description="Filter by status",
        examples=[
            SpotStatusEnum.draft,
            SpotStatusEnum.pending,
            SpotStatusEnum.active,
            SpotStatusEnum.closed  
        ]
    ),
    sort_by: Optional[SpotSortEnum] = Query(None,examples=[
        SpotSortEnum.name_asc,
        SpotSortEnum.name_desc,
        SpotSortEnum.visited_count_asc,
        SpotSortEnum.visited_count_desc,
        SpotSortEnum.favorite_count_asc,
        SpotSortEnum.favorite_count_desc,
        SpotSortEnum.create_time_asc,
        SpotSortEnum.create_time_desc,
        SpotSortEnum.update_time_asc,
        SpotSortEnum.update_time_desc,
    ]),
    page : int= Query(default=1, gt=0),
    limit : int= Query(default=20, gt=0, lt=100),
):
    """
    Get scenic spots with optional filters, sorting, and pagination.
    """
    return spot_service.get_scenic_spots(
        db,
        query_str=query_str,
        tags=tags,
        created_by=created_by,
        assignee_id=assignee_id,
        spot_type=spot_type,
        city_id=city_id,
        status=status,
        sort_by = sort_by,
        page = page,
        limit = limit
    )


@router.get("/{spot_id}", response_model=SpotResponse)
def read_scenic_spot(spot_id: int, db: Session = Depends(get_db)):
    """
    Get a specific scenic spot by its ID.
    """
    scenic_spot = spot_service.get_scenic_spot(spot_id=spot_id, db=db)
    
    if scenic_spot is None:
        raise SpotNotFound(spot_id=spot_id)
    
    return scenic_spot


@router.post("/", response_model=SpotResponse, status_code=201)
def create_spot_endpoint(spot_data: SpotCreate = Body(...), 
                         db: Session = Depends(get_db), 
                         user = Depends(get_current_user)):
    """
    Create a new scenic spot with optional tags and attributes.
    """
    permissions = get_current_permissions(user.role_id)
    
    if "create_spot" not in permissions:
        raise ForbidenException()
    
    return spot_service.create_spot(db=db, spot_data=spot_data, user_id=user.id)


@router.put("/{spot_id}", response_model=SpotResponse)
def update_spot_endpoint(spot_id: int, 
                         spot_data: SpotUpdate = Body(...), 
                         db: Session = Depends(get_db), 
                         user = Depends(get_current_user)):
    """
    Update an existing scenic spot, including tags and attributes.
    """
    permissions = get_current_permissions(user.role_id)
    
    if "edit_spot" not in permissions:
        raise ForbidenException()
    
    if "approve_spot" not in permissions and spot_data.status == SpotStatusEnum.active:
        raise ForbidenException()
    
    db_spot = spot_service.get_scenic_spot(spot_id, db)
    
    if db_spot.created_by != user.id and db_spot.assignee_id != user.id:
        raise ForbidenException()
    
    if db_spot is None:
        raise SpotNotFound()
    
    return spot_service.update_spot(db=db, db_spot = db_spot, spot_data=spot_data, user_id=user.id)


@router.delete("/{spot_id}", response_model=MessageResponse)
def delete_spot_endpoint(spot_id: int, 
                         db: Session = Depends(get_db), 
                         user = Depends(get_current_user)                  
                         ):
    """
    Delete a scenic spot by ID.
    """
    permissions = get_current_permissions(user.role_id)
    
    if "delete_spot" not in permissions:
        raise ForbidenException()
    
    db_spot = spot_service.get_scenic_spot(spot_id, db)
    
    if db_spot is None:
        raise SpotNotFound()
    
    spot_service.delete_spot(db=db, db_spot=db_spot)
    
    return MessageResponse(detail=f"spot with id = {spot_id} deleted successfully")