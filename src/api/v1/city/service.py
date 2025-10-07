from sqlalchemy.orm import Session
from sqlalchemy import func, literal, or_
from typing import List, Optional
from enum import Enum

from .enum import CitySortEnum
from .model import CityResponse, CityCreate, CityUpdate

from ....core.response import ListResponse
from ....entities.city import City
from ....entities.spot import ScenicSpot
import unicodedata

class CityService:
    def get_cities(self, db: Session, query_str : Optional[str], sort_by : Optional[str], page : int, limit : int):
        spots_count = func.count().label("spots_count")
        
        query = db.query(City, spots_count).outerjoin(ScenicSpot)
        
        #filterresults
        if query_str:
            query = query.filter(
                or_(City.name.ilike(f"%{query_str}%"),
                func.unaccent(func.lower(City.name)).ilike(f"%{query_str.lower()}%"))
            )
             
        query = query.group_by(City.id)

        #sorting
        if sort_by:
            sort_column ={
                CitySortEnum.name_asc : City.name.asc(),
                CitySortEnum.name_desc : City.name.desc(),
                CitySortEnum.created_at_asc : City.created_at.asc(),
                CitySortEnum.created_at_desc : City.created_at.desc(),
                CitySortEnum.updated_at_asc : City.updated_at.asc(),
                CitySortEnum.updated_at_desc : City.updated_at.desc(),
            }.get(sort_by)
            if sort_column is not None:
                query = query.order_by(sort_column)
        else:
            query = query.order_by(City.id.asc())

        #pagination
        total_results = query.count()
        
        if (page is not None and limit is not None):
            offset = (page - 1) * limit
            query = query.offset(offset).limit(limit)
            total_pages = (total_results + limit - 1) // limit
        else:
            page = 1
            total_pages = 1

        results = query.all()

        cities_res = []
        for city, spots_count in results:
            city_res = CityResponse(**city.__dict__, spots_count=spots_count)
            cities_res.append(city_res)
        
        return ListResponse(
            results=cities_res, 
            page=page, 
            total_results=total_results, 
            total_pages=total_pages
        )


    def get_city(self, city_id : int, db : Session) -> CityResponse:
        spots_count = func.count().label("spots_count")
        query = (db.query(City, spots_count)
                    .outerjoin(ScenicSpot)
                    .filter(City.id == city_id)
                    .group_by(City.id)
                    )
        result = query.first()
        if result is None:
            return None
        city, spots_count = result
        return CityResponse(**city.__dict__, spots_count=spots_count)       
    

    def create_city(self, city : CityCreate, db : Session):
        city = City(**city.model_dump())
        db.add(city)
        db.commit()
        db.refresh(city)
        return city

    
    def update_city(self, db_city : City, city : CityUpdate, db : Session):
        city = city.model_dump(exclude_unset=True)
        for key, value in city.items():
            setattr(db_city, key, value)
        db.commit()
        db.refresh(db_city)
        return db_city
        
    
    def delete_city(self, city_id : int, db : Session):
        db.query(City).filter(City.id == city_id).delete()
        db.commit()
        

city_service = CityService()