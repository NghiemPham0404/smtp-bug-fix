from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from datetime import datetime, timezone

from .model import SpotTypeResponse, SpotTypeCreate, SpotTypeUpdate
from .enum import SpotTypeSortEnum

from ....core.response import ListResponse
from ....entities.spot import SpotType, ScenicSpot

class SpotTypeService:

    def get_spot_types(
        self,
        db: Session,
        query_str: Optional[str],
        sort_by: Optional[SpotTypeSortEnum],
        page: int,
        limit: int,
    ) -> ListResponse[SpotTypeResponse]:

        # Base query with spot count
        spots_count = func.count(distinct(ScenicSpot.id)).label("spots_count")

        query = (
            db.query(
                SpotType,
                spots_count,
            )
            .outerjoin(ScenicSpot, (ScenicSpot.type == SpotType.id) and ScenicSpot.type != "DRAFT")
            .group_by(SpotType.id)
        )

        # Filtering
        if query_str:
            query = query.filter(SpotType.name.ilike(f"%{query_str}%"))

        # Sorting
        sort_map = {
            SpotTypeSortEnum.name_asc: SpotType.name.asc(),
            SpotTypeSortEnum.name_desc: SpotType.name.desc(),
            SpotTypeSortEnum.create_time_asc: SpotType.created_at.asc(),
            SpotTypeSortEnum.create_time_desc: SpotType.created_at.desc(),
            SpotTypeSortEnum.update_time_asc: SpotType.updated_at.asc(),
            SpotTypeSortEnum.update_time_desc: SpotType.updated_at.desc(),
            SpotTypeSortEnum.spot_count_asc: spots_count.asc(),
            SpotTypeSortEnum.spot_count_desc: spots_count.desc(),
        }
        if sort_by in sort_map:
            query = query.order_by(sort_map[sort_by])

        # Total count
        subquery = query.with_entities(SpotType.id).subquery()
        total_results = db.query(func.count()).select_from(subquery).scalar()

        # Pagination
        if (page is not None and limit is not None):
            offset = (page - 1) * limit
            query = query.offset(offset).limit(limit)
            total_pages = (total_results + limit - 1) // limit
        else:
            page = 1
            total_pages = 1

        results = query.all()

        # Build response list
        types: List[SpotTypeResponse] = []
        for spot_type, spots_count in results:
            spot_type.spots_count = spots_count or 0
            types.append(spot_type)

        return ListResponse[SpotTypeResponse](
            results=types,
            page=page,
            total_results=total_results,
            total_pages=total_pages,
        )


    def get_spot_type(self,type_id: int, db: Session):
        spots_count = func.count(distinct(ScenicSpot.id)).label("spots_count")

        query = (
            db.query(
                SpotType,
                spots_count,
            )
            .outerjoin(ScenicSpot, (ScenicSpot.type == SpotType.id) and ScenicSpot.status != "DRAFT")
            .filter(SpotType.id == type_id)
            .group_by(SpotType.id)
        )

        result = query.first()

        if not result:
            return None
        
        spot_type, spots_count = query.first()
        spot_type.spots_count = spots_count
        return spot_type


    def create_spot_type(self, spot_type_data: SpotTypeCreate, db: Session):
        spot_type = SpotType(
            name=spot_type_data.name,
            icon_url=spot_type_data.icon_url,
            image_url=spot_type_data.image_url,
            created_at = datetime.now(timezone.utc)
        )
        db.add(spot_type)
        db.commit()
        db.refresh(spot_type)

        return spot_type


    def update_spot_type(self, db_spot_type: SpotType, spot_type_data: SpotTypeUpdate, db: Session):
        
        if spot_type_data.name is not None:
            db_spot_type.name = spot_type_data.name
        if spot_type_data.icon_url is not None:
            db_spot_type.icon_url = spot_type_data.icon_url
        if spot_type_data.image_url is not None:
            db_spot_type.image_url = spot_type_data.image_url

        db_spot_type.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_spot_type)

        # Count related spots
        spots_count = (
            db.query(func.count(distinct(ScenicSpot.id)))
            .filter(ScenicSpot.type == db_spot_type.id, ScenicSpot.status != "DRAFT")
            .scalar()
        )

        db_spot_type.spots_count = spots_count
        return db_spot_type


    def delete_spot_type(self, db_spot_type:SpotType, db: Session):
        db.delete(db_spot_type)
        db.commit()
    

spot_type_service = SpotTypeService()