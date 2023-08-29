from typing import Union

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import config
from database.dals import UserDAL
from database.models import User
from database.session import get_db
from hashing import Hasher

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _get_user_by_email(email: str, session):
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


async def get_current_user_from_token(
    token: str = Depends(oauth_scheme), db: AsyncSession = Depends(get_db)
):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=config.ALG)
        email: str = payload.get("sub")
        print("email extracted:", email)
        if email is None:
            raise exception
    except JWTError:
        raise exception
    user = await _get_user_by_email(email, db)
    if user is None:
        raise exception
    return user
