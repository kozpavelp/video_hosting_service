from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from database.dals import UserDAL
from database.models import User
from hashing import Hasher


async def _get_user_by_email(email: str, db):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.get_user_by_email(email=email)


async def verify_pwd(email: str, password: str, db: AsyncSession):
    user = await _get_user_by_email(email, db=db)
    if user in None:
        return False
    if not Hasher.verify_pwd(password, user.hashed_pwd):
        return False
    return user


async def authenticate_user(
    email: str, password: str, db: AsyncSession
) -> Union[User, None]:
    user = await _get_user_by_email(email, db)
    if user is None:
        return
    if not Hasher.verify_pwd(password, user.hashed_pwd):
        return
    return user
