from fastapi import APIRouter, Depends, UploadFile, Query
from sqlalchemy.orm import Session
from typing import List

from .model import MediaFileResponse
from .service import media_service
from .enum import *
from .exception import MediaFileNotFound

from ....database.core import get_db
from ....security.authentication import get_current_user
from ....security.authorization import get_current_permissions
from ....core.response import ListResponse, MessageResponse
from ....core.exception import UnAuthorizedException


router = APIRouter(prefix="/media-files", tags=["Media Files"])


@router.get("/", response_model=ListResponse[MediaFileResponse])
def get_files(
    page: int = 1,
    page_size: int = 20,
    sort_by: MediaFileSortEnum = MediaFileSortEnum.created_at_desc,
    type_filter: MediaTypeEnum | None = None,
    user_id : int | None = None,
    db: Session = Depends(get_db),
):
    return media_service.list_media_files(
        db, page, page_size, sort_by, type_filter, user_id
    )


@router.get("/{media_id}", response_model=MediaFileResponse)
def get_file(media_id: int, db: Session = Depends(get_db)):
    media = media_service.get_media_file(db, media_id)
    if media is None:
        raise MediaFileNotFound(media_id=media_id)
    return media


@router.post("/", response_model=MediaFileResponse)
def upload_file(
    file: UploadFile,
    is_public: bool = False,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    permissions = get_current_permissions(role_id=user.role_id)
    if "upload_media" not in permissions:
        raise UnAuthorizedException()
    return media_service.upload_media_file(db, file, user.id, is_public=is_public)


@router.delete("/{media_id}")
def remove_file(
    media_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    permissions = get_current_permissions(role_id=user.role_id)
    if "delete_media" not in permissions:
        raise UnAuthorizedException()
    
    media_file = media_service.get_media_file(db=db, media_id=media_id)

    if media_file is None:
        raise MediaFileNotFound()

    if user.id != media_file.created_by:
        raise UnAuthorizedException()

    media_service.delete_media_file(db, media_file)
    return MessageResponse(detail=f"media file with id = {media_id} deleted successfully")


spot_media_file_router = APIRouter(prefix="", tags=["Spot Media Files"])


@spot_media_file_router.get("/scenic_spots/{spot_id}/media_files", response_model=ListResponse[MediaFileResponse])
def list_spot_media_files(
    spot_id: int,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return media_service.get_spot_media_files(db, spot_id, page, limit)


@spot_media_file_router.post("/scenic_spots/{spot_id}/media_files", response_model=MediaFileResponse)
def add_spot_media_file(
    spot_id: int,
    file: UploadFile,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    permissions = get_current_permissions(role_id=user.role_id)
    if "edit_spot" not in permissions:
        raise UnAuthorizedException()
    
    return media_service.upload_spot_media_file(db, spot_id, file, user.id)


@spot_media_file_router.delete("/scenic_spots/{spot_id}/media_files/{media_file_id}", response_model=MessageResponse)
def remove_spot_media_files(
    spot_id: int,
    media_file_id : int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    permissions = get_current_permissions(role_id=user.role_id)
    if "edit_spot" not in permissions:
        raise UnAuthorizedException()
    
    spot_media_file = media_service.get_spot_media_file(db, spot_id, media_file_id)

    if spot_media_file is None:
        raise MediaFileNotFound()
    
    media_file = media_service.get_media_file(db=db, media_id=media_file_id)

    if media_file is None:
        raise MediaFileNotFound()

    media_service.delete_media_file(db, media_file)
    return MessageResponse(detail=f"spot media file with id = {media_file_id} and spot id = {spot_id} deleted successfully")
