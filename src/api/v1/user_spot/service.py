
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from .model import UserSpotType, UserSpot_User, UserSpot_Spot
from .enum import UserSpotSortEnum

from ....entities.spot import UserSpot
from ....entities.spot import ScenicSpot
from ....entities.user import User
from ....core.response import ListResponse


class UserSpotService:


    def add_user_spot(self, db: Session, spot_id: int, user_id: int, type: UserSpotType):
        user_spot = UserSpot(
            spot_id=spot_id,
            created_by=user_id,
            type=type.value,
            created_at=func.now(),
        )
        db.add(user_spot)
        db.commit()
    

    def get_user_spot(self, db : Session, spot_id: int, user_id: int, type: UserSpotType):
        return (
            db.query(UserSpot)
            .filter(
                UserSpot.spot_id == spot_id,
                UserSpot.created_by == user_id,
                UserSpot.type == type.value,
            )
            .first()
        )


    def delete_user_spot(self, db: Session, db_user_spot : UserSpot):
        db.delete(db_user_spot)
        db.commit()
        return True


    def get_user_spots(
        self,
        db: Session,
        user_id: int,
        type: UserSpotType,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        order_by: Optional[UserSpotSortEnum] = None,
    ) -> ListResponse[UserSpot_Spot]:
        query = (
            db.query(
                ScenicSpot.id,
                ScenicSpot.name,
                ScenicSpot.thumb_img,
                UserSpot.created_at,
            )
            .join(UserSpot, ScenicSpot.id == UserSpot.spot_id)
            .filter(UserSpot.created_by == user_id, UserSpot.type == type.value)
        )

        if search:
            query = query.filter(ScenicSpot.name.ilike(f"%{search}%"))

        # Sorting
        if order_by:
            sort_map = {
                UserSpotSortEnum.create_time_asc : UserSpot.created_at.asc(),
                UserSpotSortEnum.create_time_desc : UserSpot.created_at.desc(),
                UserSpotSortEnum.name_asc : ScenicSpot.name.asc(),
                UserSpotSortEnum.name_desc : ScenicSpot.name.desc()
            }
            if order_by in sort_map:
                order_by_value = sort_map[order_by]
            else:
                order_by_value = UserSpot.created_at.desc()
            query = query.order_by(order_by_value)

        total_results = query.count()
        total_pages = (total_results + limit - 1) // limit
        offset = (page - 1) * limit
        results = query.offset(offset).limit(limit).all()

        spots = [UserSpot_Spot(id=s[0], name=s[1], thumb_img=s[2], created_at=s[3]) for s in results]

        return ListResponse[UserSpot_Spot](
            results=spots, page=page, total_results=total_results, total_pages=total_pages
        )


    def get_spot_users(
        self,
        db: Session,
        spot_id: int,
        type: UserSpotType,
        page: int = 1,
        limit: int = 20,
    ) -> ListResponse[UserSpot_User]:
        query = (
            db.query(
                User.id,
                User.name,
                User.avatar,
                UserSpot.created_at,
            )
            .join(UserSpot, User.id == UserSpot.created_by)
            .filter(UserSpot.spot_id == spot_id, UserSpot.type == type.value)
            .order_by(UserSpot.created_at.desc())
        )

        total_results = query.count()
        total_pages = (total_results + limit - 1) // limit
        offset = (page - 1) * limit
        results = query.offset(offset).limit(limit).all()

        users = [UserSpot_User(id=u[0], name=u[1], avatar=u[2], created_at=u[3]) for u in results]

        return ListResponse[UserSpot_User](
            results=users, page=page, total_results=total_results, total_pages=total_pages
        )


user_spots_service = UserSpotService()
