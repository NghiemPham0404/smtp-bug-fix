from typing import List, Optional, Tuple
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
from fastapi import HTTPException, status

from .enum import SpotAttributeSortEnum
from .model import *

from ....core.response import ListResponse
from ....entities.spot import SpotAttribute, SpotAttributeMediaFile
from ....entities.media import MediaFile
from ....core.aws_s3_helper import generate_presigned_url


class SpotAttributeService:


    def get_spot_attributes(
    self,
    db: Session,
    spot_id: int,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: SpotAttributeSortEnum = SpotAttributeSortEnum.sort_order_asc,
) -> ListResponse:
        query = (
            db.query(
                SpotAttribute,
                func.coalesce(func.array_agg(MediaFile.url).filter(MediaFile.id.isnot(None)), []).label("media_file_urls")
            )
            .outerjoin(
                SpotAttributeMediaFile,
                SpotAttributeMediaFile.spot_attribute_id == SpotAttribute.id,
            )
            .outerjoin(MediaFile, MediaFile.id == SpotAttributeMediaFile.media_file_id)
            .filter(SpotAttribute.spot_id == spot_id)
            .group_by(SpotAttribute.id)
        )

        if search:
            query = query.filter(SpotAttribute.name.ilike(f"%{search}%"))

        # Sorting (same as before)
        if sort_by == SpotAttributeSortEnum.sort_order_asc:
            query = query.order_by(asc(SpotAttribute.sort_order))
        elif sort_by == SpotAttributeSortEnum.sort_order_desc:
            query = query.order_by(desc(SpotAttribute.sort_order))
        elif sort_by == SpotAttributeSortEnum.name_asc:
            query = query.order_by(asc(SpotAttribute.name))
        elif sort_by == SpotAttributeSortEnum.name_desc:
            query = query.order_by(desc(SpotAttribute.name))
        elif sort_by == SpotAttributeSortEnum.created_time_asc:
            query = query.order_by(asc(SpotAttribute.created_at))
        elif sort_by == SpotAttributeSortEnum.created_time_desc:
            query = query.order_by(desc(SpotAttribute.created_at))

        total_results = query.count()
        total_pages = (total_results + limit - 1) // limit

        rows = query.offset((page - 1) * limit).limit(limit).all()

        # Build SpotAttribute objects with media_file_urls attached
        results = []
        for attr, urls in rows:
            if urls is not None:
                urls = [generate_presigned_url(url) for url in urls]
                attr.media_file_urls = urls
            results.append(attr)

        return ListResponse(
            results=results,
            page=page,
            total_results=total_results,
            total_pages=total_pages,
        )


    def create_spot_attribute(
        self,
        db: Session,
        spot_id: int,
        data: SpotAttributeCreate,
        user_id: int,
    ):
        new_attr = SpotAttribute(
            spot_id=spot_id,
            name=data.name,
            description=data.description,
            sort_order=data.sort_order,
            created_at=datetime.now(timezone.utc),
            created_by=user_id,
        )
        db.add(new_attr)
        db.commit()
        db.refresh(new_attr)

        if data.media_file_ids:
            for media_id in data.media_file_ids:
                link = SpotAttributeMediaFile(
                    spot_attribute_id=new_attr.id,
                    media_file_id=media_id,
                )
                db.add(link)
            db.commit()

        return self.get_spot_attribute(db, new_attr.id)
    

    def get_spot_attribute_by_name(self,db : Session, spot_id, name):
        return ( db.query(SpotAttribute)
            .filter(
                SpotAttribute.spot_id == spot_id,
                SpotAttribute.name == name,
            )
            .first())
    

    def get_spot_attribute(self, db : Session, spot_attribute_id):

        query = (
            db.query(
                SpotAttribute,
                func.coalesce(func.array_agg(MediaFile.url), []).label("media_file_urls"),
            )
            .outerjoin(
                SpotAttributeMediaFile,
                SpotAttributeMediaFile.spot_attribute_id == SpotAttribute.id,
            )
            .outerjoin(MediaFile, MediaFile.id == SpotAttributeMediaFile.media_file_id)
            .filter(SpotAttribute.id == spot_attribute_id)
            .group_by(SpotAttribute.id)
        )

        result, media_file_urls = query.first()

        if result is None:
            return None

        result.media_file_urls = [generate_presigned_url(url) for url in media_file_urls] or []
        return result
    



    def update_spot_attribute(
        self,
        db: Session,
        attr: SpotAttribute,
        data: SpotAttributeUpdate,
    ):
        
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(attr, key, value)
        attr.updated_at = datetime.now(timezone.utc)
        db.commit()

        # Update media files
        if data.media_file_ids is not None:
            db.query(SpotAttributeMediaFile).filter(
                SpotAttributeMediaFile.spot_attribute_id == attr.id
            ).delete()

            for media_id in data.media_file_ids:
                link = SpotAttributeMediaFile(
                    spot_attribute_id=attr.id,
                    media_file_id=media_id,
                )
                db.add(link)

            db.commit()

        db.refresh(attr)
        return self.get_spot_attribute(db, attr.id)
    

    def delete_spot_attribute(
        self,
        db: Session,
        attr : SpotAttribute,
    ):

        db.delete(attr)
        db.commit()
