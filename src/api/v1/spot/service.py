from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, case, distinct, or_

from .enum import SpotSortEnum

from .model import SpotCreate, SpotUpdate

from ....core.response import ListResponse
from ....entities.spot import ScenicSpot, UserSpot, SpotAttribute
from ....entities.tag import SpotTag
from ....entities.feedback import Feedback
from ....api.v1.spot.model import SpotResponse

class ScenicSpotService:

    def get_scenic_spots(
        self,
        db: Session,
        query_str: Optional[str] = None,
        tags: Optional[List[int]] = None,
        created_by: Optional[int] = None,
        assignee_id: Optional[int] = None,
        spot_type: Optional[int] = None,
        city_id: Optional[int] = None,
        status: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        page : int = 1,
        limit : int = 20,
    ):
        
        """ 
        Get a list of scenic spots with filters and pagination. 
        
        Parameters Params: 
            - db (Session): The database session. 
            - pagination (PaginationParams): Pagination parameters including page, limit, sort, and order. 
            - tags (Optional[List[int]]): A list of tag IDs to filter by. 
            - created_by (Optional[int]): The ID of the user who created the spot. 
            - assignee_id (Optional[int]): The ID of the user assigned to the spot. 
            - spot_type (Optional[int]): The type of the spot. 
            - city_id (Optional[int]): The ID of the city the spot belongs to. 
            - status (Optional[List[str]]): A list of statuses to filter by.
        
        Output:    
            ListResponse[SpotResponse]
        """

        # Base query with aggregations
        viewed_count = func.count(distinct(case((UserSpot.type == "VIEWED", UserSpot.spot_id)))).label("viewed_count")
        visited_count = func.count(distinct(case((UserSpot.type == "VISITED", UserSpot.spot_id)))).label("visited_count")
        favorite_count = func.count(distinct(case((UserSpot.type == "FAVORITE", UserSpot.spot_id)))).label("favorite_count")
        saved_count = func.count(distinct(case((UserSpot.type == "SAVED", UserSpot.spot_id)))).label("saved_count")
        average_rating = func.coalesce(func.avg(Feedback.rating), 0).label("average_rating")
        feedbacks_count = func.count(distinct(Feedback.id)).label("feedback_count")

        query = (
            db.query(
                ScenicSpot,
                viewed_count,
                visited_count,
                favorite_count,
                saved_count,
                average_rating,
                feedbacks_count,
                func.coalesce(
                func.array_agg(distinct(SpotTag.tag_id)).filter(SpotTag.tag_id.isnot(None)), []
                ).label("spot_tag_ids"),
                func.coalesce(
                    func.array_agg(distinct(SpotAttribute.id)).filter(SpotAttribute.id.isnot(None)), []
                ).label("spot_attributes_ids"),

            )
            .outerjoin(UserSpot, ScenicSpot.id == UserSpot.spot_id)
            .outerjoin(SpotTag, ScenicSpot.id == SpotTag.spot_id)
            .outerjoin(SpotAttribute, ScenicSpot.id == SpotAttribute.spot_id)
            .outerjoin(Feedback, ScenicSpot.id == Feedback.spot_id)
        )

        # Filtering
        if tags:
            query = query.filter(SpotTag.tag_id.in_(tags))
        if created_by:
            query = query.filter(ScenicSpot.created_by == created_by)
        if assignee_id:
            query = query.filter(ScenicSpot.assignee_id == assignee_id)
        if spot_type:
            query = query.filter(ScenicSpot.type == spot_type)
        if city_id:
            query = query.filter(ScenicSpot.city_id == city_id)
        if status:
            query = query.filter(ScenicSpot.status.in_(status))
        if query_str:
            query = query.filter(
                or_(
                func.unaccent(func.lower(ScenicSpot.name)).ilike(f"%{query_str.lower()}%"),
                ScenicSpot.name.ilike(f"%{query_str}%"),)
                
            )

        query = query.group_by(ScenicSpot.id)

        # Sorting
        sort_map = {
            SpotSortEnum.name_asc: ScenicSpot.name.asc(),
            SpotSortEnum.name_desc: ScenicSpot.name.desc(),
            SpotSortEnum.visited_count_asc: visited_count.asc(),
            SpotSortEnum.visited_count_desc: visited_count.desc(),
            SpotSortEnum.favorite_count_asc: favorite_count.asc(),
            SpotSortEnum.favorite_count_desc: favorite_count.desc(),
            SpotSortEnum.create_time_asc: ScenicSpot.created_at.asc(),
            SpotSortEnum.create_time_desc: ScenicSpot.created_at.desc(),
            SpotSortEnum.update_time_asc: ScenicSpot.updated_at.asc(),
            SpotSortEnum.update_time_desc: ScenicSpot.updated_at.desc(),
        }

        if sort_by in sort_map:
            query = query.order_by(sort_map[sort_by])

        # Total count using subquery (safer with GROUP BY)
        subquery = query.with_entities(ScenicSpot.id).subquery()
        total_results = db.query(func.count()).select_from(subquery).scalar()
        total_pages = (total_results + limit - 1) // limit

        # Apply pagination
        offset = (page - 1) * limit
        results = query.offset(offset).limit(limit).all()

        # Build response
        spots: List[SpotResponse] = []
        for spot, viewed_count, visited_count, favorite_count, saved_count, average_rating, feedbacks_count, spot_tag_ids, spot_attributes_ids in results:
            spot.viewed_count = viewed_count or 0
            spot.visited_count = visited_count or 0
            spot.favorite_count = favorite_count or 0
            spot.saved_count = saved_count or 0
            spot.average_rating = round(float(average_rating or 0), 1)
            spot.feedbacks_count = feedbacks_count or 0
            spot.spot_tag_ids = spot_tag_ids or []
            spot.spot_attributes_ids = spot_attributes_ids or []
            spots.append(spot)

        return ListResponse[SpotResponse](
            results=spots,
            page=page,
            total_results=total_results,
            total_pages=total_pages,
        )



    def get_scenic_spot(self, spot_id: int, db: Session):
        # Base query with aggregations
        viewed_count = func.count(distinct(case((UserSpot.type == "VIEWED", UserSpot.spot_id)))).label("viewed_count")
        visited_count = func.count(distinct(case((UserSpot.type == "VISITED", UserSpot.spot_id)))).label("visited_count")
        favorite_count = func.count(distinct(case((UserSpot.type == "FAVORITE", UserSpot.spot_id)))).label("favorite_count")
        saved_count = func.count(distinct(case((UserSpot.type == "SAVED", UserSpot.spot_id)))).label("saved_count")

        average_rating = func.coalesce(func.avg(Feedback.rating), 0).label("average_rating")
        feedbacks_count = func.count(distinct(Feedback.id)).label("feedback_count")

        query = (
            db.query(
                ScenicSpot,
                viewed_count,
                visited_count,
                favorite_count,
                saved_count,
                average_rating,
                feedbacks_count,
                func.coalesce(
                    func.array_agg(distinct(SpotTag.tag_id)).filter(SpotTag.tag_id.isnot(None)), []
                ).label("spot_tag_ids"),
                func.coalesce(
                    func.array_agg(distinct(SpotAttribute.id)).filter(SpotAttribute.id.isnot(None)), []
                ).label("spot_attributes_ids"),
            )
            .outerjoin(UserSpot, ScenicSpot.id == UserSpot.spot_id)
            .outerjoin(SpotTag, ScenicSpot.id == SpotTag.spot_id)
            .outerjoin(SpotAttribute, ScenicSpot.id == SpotAttribute.spot_id)
            .outerjoin(Feedback, ScenicSpot.id == Feedback.spot_id)
            .filter(ScenicSpot.id == spot_id)
            .group_by(ScenicSpot.id)
        )

        result = query.first()
        if not result:
            return None

        spot, viewed_count, visited_count, favorite_count, saved_count, average_rating, feedbacks_count,spot_tag_ids, spot_attributes_ids = result
        spot.viewed_count = viewed_count
        spot.visited_count = visited_count
        spot.favorite_count = favorite_count
        spot.saved_count = saved_count
        spot.average_rating = round(float(average_rating or 0), 1)
        spot.feedbacks_count = feedbacks_count or 0
        spot.spot_tag_ids = spot_tag_ids
        spot.spot_attributes_ids = spot_attributes_ids        
        return spot


    def create_spot(self, db: Session, spot_data: SpotCreate, user_id: int):
        # Create the base spot record
        spot = ScenicSpot(
            city_id=spot_data.city_id,
            name=spot_data.name,
            address=spot_data.address,
            description=spot_data.description,
            longitude=spot_data.longitude,
            latitude=spot_data.latitude,
            radius=spot_data.radius,
            status=spot_data.status,
            thumb_img=spot_data.thumb_img,
            type=spot_data.type,
            assignee_id=spot_data.assignee_id,
            created_at=spot_data.created_at,
            created_by=user_id,
        )
        db.add(spot)
        db.commit()
        db.refresh(spot)

        # Handle relations (tags + attributes)
        if spot_data.spot_tag_ids:
            spot_tags = [SpotTag(spot_id=spot.id, tag_id=tid) for tid in spot_data.spot_tag_ids]
            db.bulk_save_objects(spot_tags)
        db.commit()

        spot.spot_tag_ids = spot_data.spot_tag_ids

        return spot


    def update_spot(self, db: Session, db_spot: ScenicSpot, spot_data: SpotUpdate, user_id : int):
        # Update fields
        for field, value in spot_data.model_dump(exclude_unset=True).items():
            setattr(db_spot, field, value)
        db_spot.updated_by = user_id
        db.commit()
        db.refresh(db_spot)

        # Update relations if provided
        if spot_data.spot_tag_ids is not None:
            db.query(SpotTag).filter(SpotTag.spot_id == db_spot.id).delete()
            if spot_data.spot_tag_ids:
                db.bulk_save_objects([SpotTag(spot_id=db_spot.id, tag_id=tid) for tid in spot_data.spot_tag_ids])
        db.commit()

        return self.get_scenic_spot(db_spot.id, db)


    def delete_spot(self, db: Session, db_spot: ScenicSpot):
        db.delete(db_spot)
        db.commit()


spot_service = ScenicSpotService()