from fastapi.routing import APIRouter

from fastapi import Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from .service import city_service
from .model import CityResponse, CityCreate, CityUpdate
from .exception import CityNotFound
from .enum import CitySortEnum

from ....core.response import ListResponse, MessageResponse
from ....security.authentication import get_current_user
from ....security.authorization import get_current_permissions
from ....database.core import get_db
from ....core.exception import UnAuthorizedException, ForbidenException

router = APIRouter(prefix="/cities", tags=["Cities"])

@router.get("/", response_model=ListResponse[CityResponse])
def get_cities(
    db: Session = Depends(get_db),
    query_str: Optional[str] = Query(None, description="Search by city name"),
    sort_by : Optional[CitySortEnum] = Query(None),
    page : Optional[int] = None,
    limit : Optional[int] = None,
):
    """
    Get a list of cities with filtering, pagination and optional search.
    """
    return city_service.get_cities(db=db, query_str=query_str, sort_by=sort_by, page = page, limit=limit)

@router.get("/{city_id}", response_model=CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)):
    """
    Get a specific city by its ID.
    """
    city = city_service.get_city(city_id=city_id, db=db)
    if city is None:
        raise CityNotFound(city_id=city_id)
    return city

@router.post("/", response_model=CityResponse)
def create_city(city: CityCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    """
    Create a new city.
    """
    permissions = get_current_permissions(role_id = user.role_id)
    if  "create_city" not in permissions:
        raise ForbidenException()
    return city_service.create_city(city=city, db=db)


@router.put("/{city_id}", response_model=CityResponse)
def update_city(city_id: int, city: CityUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    """
    Update an existing city by its ID.
    """
    permissions = get_current_permissions(role_id = user.role_id)
    if  "edit_city" not in permissions:
        raise ForbidenException()
    db_city = city_service.get_city(city_id=city_id, db = db)
    if db_city is None:
        raise CityNotFound()
    return city_service.update_city(db_city,city=city, db=db)


@router.delete("/{city_id}", response_model=MessageResponse)
def delete_city(city_id : int, db:Session = Depends(get_db), user = Depends(get_current_user)):
    permissions = get_current_permissions(role_id = user.role_id)
    if  "delete_city" not in permissions: 
        raise ForbidenException()
    db_city = city_service.get_city(city_id=city_id, db = db)
    if db_city is None:
        raise CityNotFound()
    city_service.delete_city(city_id=city_id, db = db)
    return MessageResponse(detail=f"City with id = {city_id} deleted successfully")
