"""Data Access Layer"""
from typing import Union
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import RoleList
from database.models import User, Video


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        name: str,
        surname: str,
        email: str,
        hashed_pwd: str,
        roles: list[RoleList],
    ) -> User:
        new_user = User(
            name=name, surname=surname, email=email, hashed_pwd=hashed_pwd, roles=roles
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.user_id)
        )
        result = await self.db_session.execute(query)
        deleted_user_row = result.fetchone()
        if deleted_user_row is not None:
            return deleted_user_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        result = await self.db_session.execute(query)
        user_row = result.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.is_active == True, User.user_id == user_id))
            .values(kwargs)
            .returning(User.user_id)
        )
        result = await self.db_session.execute(query)
        user_row = result.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        result = await self.db_session.execute(query)
        user_row = result.fetchone()
        if user_row is not None:
            return user_row[0]


class VideoDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def upload_video(self, name: str, file_path: str) -> Video:
        new_video = Video(
            name=name,
            file_path=file_path
        )
        self.db_session.add(new_video)
        await self.db_session.flush()
        return new_video
