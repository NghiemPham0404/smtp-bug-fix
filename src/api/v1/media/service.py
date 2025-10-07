import boto3
import mimetypes
import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .model import MediaTypeEnum, MediaFileResponse
from .enum import *

from ....entities.media import MediaFile
from ....entities.spot import SpotMediaFile, ScenicSpot
from ....core.response import ListResponse
from ....core.config.aws_s3_config import settings
from ....core.aws_s3_helper import (generate_presigned_url, get_s3_client)


def validate_media_type(content_type: str) -> MediaTypeEnum:
    if content_type.startswith("image/"):
        return MediaTypeEnum.IMAGE
    elif content_type.startswith("video/"):
        return MediaTypeEnum.VIDEO
    elif content_type.startswith("audio/"):
        return MediaTypeEnum.AUDIO
    else:
        raise HTTPException(status_code=400, detail="Invalid media type")

class MediaFileService:
    
    def upload_media_file(
    self,
    db: Session,
    file: UploadFile,
    user_id: int,
    is_public: bool = False,  # new parameter
):
        content_type = file.content_type
        media_type = validate_media_type(content_type)

        ext = mimetypes.guess_extension(content_type) or ""
        folder = "public" if is_public else "private"
        key = f"{folder}/{user_id}/{uuid.uuid4()}{ext}"

        s3_client = get_s3_client()
        s3_client.upload_fileobj(
            file.file,
            settings.AWS_S3_BUCKET,
            key,
            ExtraArgs={"ContentType": content_type},
        )

        media_file = MediaFile(
            url=key,  # store only the key, not the public URL
            format=content_type,
            type=media_type.value,
            size=file.size,
            created_by=user_id,
            created_at=datetime.now(timezone.utc),
        )

        db.add(media_file)
        db.commit()
        db.refresh(media_file)

        # If public, we can use a public URL, otherwise presigned
        response = MediaFileResponse(**media_file.__dict__)
        if is_public:
            response.url = f"https://{settings.AWS_S3_BUCKET}.s3.amazonaws.com/{key}"
        else:
            response.url = generate_presigned_url(key)

        return response


    def list_media_files(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        sort_by: MediaFileSortEnum = MediaFileSortEnum.created_at_desc,
        type_filter: MediaTypeEnum | None = None,
        user_id: int | None = None,
    ):
        query = db.query(MediaFile)

        # Filtering
        if type_filter:
            query = query.filter(MediaFile.type == type_filter.value)
        if user_id:
            query = query.filter(MediaFile.created_by == user_id)

        total_results = query.count()
        total_pages = (total_results + page_size - 1) // page_size

        # Sorting
        if sort_by == MediaFileSortEnum.created_at_asc:
            query = query.order_by(MediaFile.created_at.asc())
        elif sort_by == MediaFileSortEnum.created_at_desc:
            query = query.order_by(MediaFile.created_at.desc())
        elif sort_by == MediaFileSortEnum.created_by_asc:
            query = query.order_by(MediaFile.created_by.asc())
        elif sort_by == MediaFileSortEnum.created_by_desc:
            query = query.order_by(MediaFile.created_by.desc())
        elif sort_by == MediaFileSortEnum.size_asc:
            query = query.order_by(MediaFile.size.asc())
        elif sort_by == MediaFileSortEnum.size_desc:
            query = query.order_by(MediaFile.size.desc())

        # Pagination
        media_list = (
            query.offset((page - 1) * page_size).limit(page_size).all()
        )

        # Replace key with presigned URL
        for media in media_list:
            media.url = generate_presigned_url(media.url)

        return ListResponse[MediaFileResponse](
            total_results=total_results,
            page=page,
            total_pages=total_pages,
            results=[MediaFileResponse(**m.__dict__) for m in media_list],
        )



    def get_media_file(self, db: Session, media_id: int):
        media = db.query(MediaFile).filter(MediaFile.id == media_id).first()
        if media is not None:
            media.url = generate_presigned_url(media.url, expires_in=3600)
        return media


    def delete_media_file(self, db: Session, media: MediaFile):

        # Delete from S3
        s3_client = get_s3_client()
        s3_client.delete_object(Bucket=settings.AWS_S3_BUCKET, Key=media.url)

        db.delete(media)
        db.commit()


    def get_spot_media_files(self, db: Session, spot_id: int, page: int, limit: int) -> ListResponse[MediaFileResponse]:
        query = (
            db.query(MediaFile)
            .join(SpotMediaFile, MediaFile.id == SpotMediaFile.media_file_id)
            .filter(SpotMediaFile.spot_id == spot_id)
            .order_by(MediaFile.created_at.desc())  # reverse chronological
        )

        total_results = query.count()
        total_pages = (total_results + limit - 1) // limit

        results = query.offset((page - 1) * limit).limit(limit).all()

        for m in results:
            m.url = generate_presigned_url(m.url)

        results = [
            MediaFileResponse(**m.__dict__)
            for m in results
        ]

        return ListResponse[MediaFileResponse](
            results=results,
            page=page,
            total_results=total_results,
            total_pages=total_pages,
        )
    
    def get_spot_media_file(self, db: Session, spot_id: int, media_file_id: int):
        query = (
            db.query(SpotMediaFile).filter(SpotMediaFile.spot_id == spot_id, SpotMediaFile.media_file_id == media_file_id).first()
        )

        return query


    def upload_spot_media_file(self, db: Session, spot_id: int, file: UploadFile, user_id: int):
        media_file = self.upload_media_file(db, file, user_id, is_public=True)

        spot_media = SpotMediaFile(spot_id=spot_id, media_file_id=media_file.id)
        db.add(spot_media)

        db.commit()
        db.refresh(spot_media)

        return media_file
    

media_service = MediaFileService()