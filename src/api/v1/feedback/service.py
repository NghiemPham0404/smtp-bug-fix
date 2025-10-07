from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct, text
from datetime import datetime, timezone

from .model import FeedbackResponse, FeedbackCreate, FeedbackUpdate
from .enum import FeedbackSortEnum

# adjust the following imports to match your project paths
from ....core.aws_s3_helper import generate_presigned_url
from ....core.response import ListResponse
from ....entities.spot import ScenicSpot
from ....entities.feedback import Feedback
from ....entities.media import MediaFile  # if your MediaFile entity lives elsewhere adjust
from ....entities.feedback import FeedbackMediaFile  # adjust if named differently
from ....entities.feedback import FeedbackLike  # adjust if named differently
from ..spot.enum import SpotStatusEnum  # adjust import path if needed


class FeedbackService:
    def get_feedbacks(
        self,
        db: Session,
        spot_id: Optional[int] = None,
        user_id: Optional[int] = None,
        sort_by: Optional[FeedbackSortEnum] = None,
        page: int = 1,
        limit: int = 20,
    ) -> ListResponse[FeedbackResponse]:
        """
        List feedbacks with optional filters and include media_file_ids per feedback.
        Excludes feedbacks for spots with status == DRAFT.
        """

        media_urls_agg = func.coalesce(func.array_agg(MediaFile.url).filter(MediaFile.id.isnot(None)), []).label("media_file_urls")
        feedback_likes_count_agg = func.coalesce(func.count(distinct(FeedbackLike.created_by)), 0).label("likes_count")

        # base query: aggregate media ids per feedback, join to ScenicSpot to apply status filter
        query = (
            db.query(
                Feedback,
                media_urls_agg,
                feedback_likes_count_agg,
            )
            .outerjoin(FeedbackMediaFile, Feedback.id == FeedbackMediaFile.feedback_id)
            .outerjoin(MediaFile, MediaFile.id == FeedbackMediaFile.media_id)
            .outerjoin(FeedbackLike, Feedback.id == FeedbackLike.feedback_id)
            .join(ScenicSpot, Feedback.spot_id == ScenicSpot.id)
            .filter(ScenicSpot.status != SpotStatusEnum.draft)
            .group_by(Feedback.id)
        )

        if spot_id:
            query = query.filter(Feedback.spot_id == spot_id)
        if user_id:
            query = query.filter(Feedback.user_id == user_id)

        sort_map = {
            FeedbackSortEnum.CREATED_TIME_ASC: Feedback.created_at.asc(),
            FeedbackSortEnum.CREATE_TIME_DESC: Feedback.created_at.desc(),
            FeedbackSortEnum.UPDATE_TIME_ASC: Feedback.updated_at.asc(),
            FeedbackSortEnum.UPDATE_TIME_DESC: Feedback.updated_at.desc(),
            FeedbackSortEnum.RATING_ASC: Feedback.rating.asc(),
            FeedbackSortEnum.RATING_DESC: Feedback.rating.desc(),
        }
        if sort_by in sort_map:
            query = query.order_by(sort_map[sort_by])
        else:
            # default ordering
            query = query.order_by(Feedback.created_at.desc())

        # total results (safe with GROUP BY)
        subquery = query.with_entities(Feedback.id).subquery()
        total_results = db.query(func.count()).select_from(subquery).scalar() or 0
        total_pages = (total_results + limit - 1) // limit

        offset = (page - 1) * limit
        results: List[Tuple[Feedback, List[int], int]] = query.offset(offset).limit(limit).all()

        feedbacks: List[Feedback] = []
        for feedback, media_file_urls, feedback_likes_count in results:
            feedback.media_file_urls = [
                generate_presigned_url(url) for url in media_file_urls or []
            ]
            feedback.likes_count = feedback_likes_count or 0
            feedbacks.append(feedback)

        return ListResponse[FeedbackResponse](
            results=feedbacks,
            page=page,
            total_results=total_results,
            total_pages=total_pages,
        )


    def get_feedback(self,feedback_id: int, db: Session):
        """
        Return single feedback with aggregated media_file_urls.
        Returns None when not found or when the feedback's spot is DRAFT.
        """
        media_urls_agg = func.coalesce(func.array_agg(MediaFile.url).filter(MediaFile.id.isnot(None)), []).label("media_file_urls")
        feedback_likes_count_agg = func.coalesce(func.count(distinct(FeedbackLike.created_by)), 0).label("likes_count")

        query = (
            db.query(
                Feedback,
                media_urls_agg,
                feedback_likes_count_agg,
            )
            .outerjoin(FeedbackMediaFile, Feedback.id == FeedbackMediaFile.feedback_id)
            .outerjoin(MediaFile, MediaFile.id == FeedbackMediaFile.media_id)
            .outerjoin(FeedbackLike, Feedback.id == FeedbackLike.feedback_id)
            .join(ScenicSpot, Feedback.spot_id == ScenicSpot.id)
            .filter(Feedback.id == feedback_id, ScenicSpot.status != SpotStatusEnum.draft)
            .group_by(Feedback.id)
        )

        row = query.first()
        if not row:
            return None
        feedback, media_file_urls, feedback_likes_count = row
        feedback.media_file_urls = [
                generate_presigned_url(url) for url in media_file_urls or []
            ]
        feedback.likes_count = feedback_likes_count or 0
        return feedback


    def create_feedback(self,db: Session, user_id: int, data: FeedbackCreate):
        """
        Create a feedback record and optionally attach media files.
        Returns the full feedback object (with media_file_ids aggregated).
        """
        try:
            feedback = Feedback(
                spot_id=data.spot_id,
                user_id=user_id,
                rating=data.rating,
                text=data.text,
                created_at=datetime.now(timezone.utc)
            )
            db.add(feedback)
            db.commit()
            db.refresh(feedback)

            # attach media ids if provided
            if data.media_file_ids:
                for media_file_id in data.media_file_ids:
                    db.add(FeedbackMediaFile(feedback_id = feedback.id, media_id = media_file_id))
                    
                db.commit()

            # load aggregated feedback (with media ids)
            return self.get_feedback(feedback.id, db)
        except Exception:
            db.rollback()


    def update_feedback(
        self,
        db: Session,
        db_feedback : Feedback,
        data: FeedbackUpdate,
    ) -> Optional[Feedback]:
        # update fields
        try:
            if data.rating is not None:
                db_feedback.rating = data.rating
            if data.text is not None:
                db_feedback.text = data.text
            db_feedback.updated_at = datetime.now(timezone.utc)

            db.commit()

            # ✅ replace media mappings using ORM
            if data.media_file_ids is not None:
                # remove old relations
                db.query(FeedbackMediaFile).filter(
                    FeedbackMediaFile.feedback_id == db_feedback.id
                ).delete(synchronize_session=False)

                # add new ones
                new_links = [
                    FeedbackMediaFile(feedback_id=db_feedback.id, media_id=mid)
                    for mid in data.media_file_ids
                ]
                db.add_all(new_links)
                db.commit()

            return self.get_feedback(db_feedback.id, db)
        except Exception:
            db.rollback()


    def delete_feedback(
        self,
        db: Session,
        db_feedback : Feedback,
    ):
        db.delete(db_feedback)
        db.commit()

    
    def get_feecback_like(self, db:Session, feedback_id : int, user_id : int):
        existing = (
            db.query(FeedbackLike)
            .filter(FeedbackLike.feedback_id == feedback_id, FeedbackLike.created_by == user_id)
            .first()
        )
        return existing

    def like_feedback(self, db: Session, feedback_id: int, user_id: int):
        """
        Add a like from the given user to the feedback.
        Does nothing if feedback not found or already liked.
        """
        like = FeedbackLike(feedback_id=feedback_id, created_by=user_id, created_at = datetime.now(timezone.utc))
        db.add(like)
        db.commit()
        db.refresh(like)
        return self.get_feedback(feedback_id, db)
    

    def unlike_feedback(self, db: Session, feedback_like: FeedbackLike):
        """
        remove the like from the given user to the feedback.
        """
        db.delete(feedback_like)
        db.commit()



feedback_service = FeedbackService()

