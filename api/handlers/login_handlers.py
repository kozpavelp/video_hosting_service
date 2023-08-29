from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

import config
from api.handlers.actions.auth import _get_user_by_email
from api.handlers.actions.auth import authenticate_user
from api.models.models import Token
from database.models import User
from database.session import get_db
from security import create_access_token

login_router = APIRouter()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


@login_router.post("/token", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "other_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "type_token": "bearer"}


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


@login_router.get("/test_auth_endpoint")
async def endpoint_under_jwt(current_user: User = Depends(get_current_user_from_token)):
    return {"Success": True, "current_user": current_user}
