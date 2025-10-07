from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from datetime import timezone, datetime

from .model import *

from ....entities import User
from ....core.response import ListResponse
from ....core.aws_s3_helper import generate_presigned_url


def get_avatar_by_name(name : str):
    return f'https://api.dicebear.com/9.x/initials/png?backgroundType=gradientLinear&seed={name}'

def get_user_avatar(user):
    if user.avatar:
        if user.avatar.startswith("http"):
            return user.avatar
        return generate_presigned_url(user.avatar)
    else:
        return get_avatar_by_name(user.name)


class UserService:

    def list_users(
        self,
        db: Session,
        page: int = 1,
        limit: int = 20,
        sort_by: UserSortBy = UserSortBy.joined_date_desc,
        is_active: bool | None = None,
        role_id: int | None = None,
    ) -> ListResponse[UserResponse]:
        query = db.query(User)

        # Filtering
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        if role_id is not None:
            query = query.filter(User.role_id == role_id)

        # Sorting
        if sort_by == UserSortBy.joined_date_asc:
            query = query.order_by(asc(User.joined_date))
        elif sort_by == UserSortBy.joined_date_desc:
            query = query.order_by(desc(User.joined_date))
        elif sort_by == UserSortBy.last_login_asc:
            query = query.order_by(asc(User.last_login))
        elif sort_by == UserSortBy.last_login_desc:
            query = query.order_by(desc(User.last_login))
        elif sort_by == UserSortBy.name_asc:
            query = query.order_by(asc(User.name))
        elif sort_by == UserSortBy.name_desc:
            query = query.order_by(desc(User.name))
        elif sort_by == UserSortBy.email_asc:
            query = query.order_by(asc(User.email))
        elif sort_by == UserSortBy.email_desc:
            query = query.order_by(desc(User.email))

        # Count + Pagination
        total_results = query.count()
        total_pages = (total_results + limit - 1) // limit
        offset = (page - 1) * limit
        users = query.offset(offset).limit(limit).all()

        results = []
        for user in users:
            user.avatar = get_user_avatar(user)
            results.append(UserResponse(**user.__dict__))

        return ListResponse[UserResponse](
            results=results,
            page=page,
            total_results=total_results,
            total_pages=total_pages,
        )


    def get_user(self, db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        return user
    

    def create_user(self, db: Session, user_create: UserCreate):
        user = User(**user_create.model_dump())
        user.joined_date = datetime.now(timezone.utc)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    

    def update_user(self, db: Session, db_user : UserUpdate, user_update: UserUpdate):
        for key, value in user_update.model_dump(exclude_none=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    

    def delete_user(self, db: Session, db_user : User):
        db.delete(db_user)
        db.commit()
    

user_service = UserService()