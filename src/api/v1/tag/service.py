from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from datetime import datetime, timezone

from ....core.response import ListResponse
from ....entities.tag import Tag, SpotTag
from ....entities.spot import ScenicSpot
from .model import TagResponse, TagCreate, TagUpdate
from .enum import TagSortEnum


class TagService:

    def get_tags(
        self,
        db: Session,
        query_str: Optional[str],
        created_by: Optional[int],
        sort_by: Optional[TagSortEnum],
        page: int,
        limit: int,
    ) -> ListResponse[TagResponse]:

        # Base query with spot count aggregation
        spots_count = func.count(distinct(ScenicSpot.id)).label("spots_count")

        query = (
            db.query(
                Tag,
                spots_count,
            )
            .outerjoin(SpotTag, Tag.id == SpotTag.tag_id)
            .outerjoin(ScenicSpot, ScenicSpot.id == SpotTag.spot_id)
            .group_by(Tag.id)
        )

        # Filtering
        if query_str:
            query = query.filter(Tag.name.ilike(f"%{query_str}%"))
        if created_by:
            query = query.filter(Tag.created_by == created_by)

        # Sorting
        sort_map = {
            TagSortEnum.name_asc: Tag.name.asc(),
            TagSortEnum.name_desc: Tag.name.desc(),
            TagSortEnum.create_time_asc: Tag.created_at.asc(),
            TagSortEnum.create_time_desc: Tag.created_at.desc(),
            TagSortEnum.update_time_asc: Tag.updated_at.asc(),
            TagSortEnum.update_time_desc: Tag.updated_at.desc(),
        }
        if sort_by in sort_map:
            query = query.order_by(sort_map[sort_by])

        # Total count using subquery (safe with GROUP BY)
        subquery = query.with_entities(Tag.id).subquery()
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
        tags: List[TagResponse] = []
        for tag, spots_count in results:
            tag.spots_count = spots_count or 0
            tags.append(tag)

        return ListResponse[TagResponse](
            results=tags,
            page=page,
            total_results=total_results,
            total_pages=total_pages,
        )


    def get_tag(self, tag_id: int, db: Session):
        spots_count = func.count(distinct(ScenicSpot.id)).label("spots_count")

        query = (
            db.query(
                Tag,
                spots_count,
            )
            .outerjoin(SpotTag, Tag.id == SpotTag.tag_id)
            .outerjoin(ScenicSpot, ScenicSpot.id == SpotTag.spot_id)
            .filter(Tag.id == tag_id)
            .group_by(Tag.id)
        )
        result = query.first()
        if not result:
            return None

        tag, spots_count = result
        tag.spots_count = spots_count
        return tag


    def create_tag(self, tag_data: TagCreate, user_id : int, db: Session) -> TagResponse:
        # Create new tag
        tag = Tag(name=tag_data.name, created_by = user_id, created_at = datetime.now(timezone.utc))
        db.add(tag)
        db.commit()
        db.refresh(tag)

        # If spot_ids are provided, link them
        if tag_data.spots_ids:
            spot_tags = [SpotTag(tag_id=tag.id, spot_id=sid) for sid in tag_data.spots_ids]
            db.bulk_save_objects(spot_tags)
            db.commit()

        tag.spots_count = len(tag_data.spots_ids or [])
        return tag


    def update_tag(self, db_tag: Tag, tag_data: TagUpdate, db: Session):

        # Update basic fields
        db_tag.name = tag_data.name
        db_tag.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_tag)

        if tag_data.spots_ids is not None:
            # Clear existing spot relations
            db.query(SpotTag).filter(SpotTag.tag_id == db_tag.id).delete()
            db.commit()

            # Insert new relations
            if tag_data.spots_ids:
                spot_tags = [SpotTag(tag_id=db_tag.id, spot_id=sid) for sid in tag_data.spots_ids]
                db.bulk_save_objects(spot_tags)
                db.commit()

        # Count spots
        spots_count = (
            db.query(func.count(distinct(ScenicSpot.id)))
            .join(SpotTag, ScenicSpot.id == SpotTag.spot_id)
            .filter(SpotTag.tag_id == db_tag.id)
            .scalar()
        )

        db_tag.spots_count = spots_count
        return db_tag


    def delete_tag(self, db_tag: Tag, db: Session):
        db.delete(db_tag)
        db.commit()


tag_service = TagService()