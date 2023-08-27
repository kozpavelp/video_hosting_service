from logging import getLogger
from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from api.models.models import UserCreate, ShowUser, DeletedUserResp, UpdatedUserReq, UpdatedUserResp
from database.dals import UserDAL
from database.session import get_db

logger = getLogger(__name__)

user_router = APIRouter()


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active
            )


async def _delete_user(user_id, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            deleted_user_id = await user_dal.delete_user(user_id=user_id)
        return deleted_user_id


async def _get_user_by_id(user_id, db) -> Union[ShowUser, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(user_id=user_id)
            if user is not None:
                return ShowUser(
                    user_id=user.user_id,
                    name=user.name,
                    surname=user.surname,
                    email=user.email,
                    is_active=user.is_active
                )


async def _update_user(cleaned_params: dict, user_id: UUID, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            updated_user_id = await user_dal.update_user(
                user_id,
                **cleaned_params
            )
            return updated_user_id


@user_router.post('/', response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f'Database error: {err}')


@user_router.delete('/', response_model=DeletedUserResp)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> DeletedUserResp:
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f'User with id:{user_id} not found in database.')
    return DeletedUserResp(deleted_user_id=deleted_user_id)


@user_router.get('/', response_model=ShowUser)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f'User with id:{user_id} not found in database.')
    return user


@user_router.patch('/', response_model=UpdatedUserResp)
async def update_user(user_id: UUID, body: UpdatedUserReq, db: AsyncSession = Depends(get_db)) -> UpdatedUserResp:
    cleaned_params = body.dict(exclude_none=True)
    if cleaned_params == {}:
        raise HTTPException(status_code=422, detail='Для продолжения должен быть изменен хотябы один параметр')
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f'User with id:{user_id} not found in database.')
    try:
        updated_user_id = await _update_user(cleaned_params=cleaned_params, user_id=user_id, db=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f'Database error: {err}')
    return UpdatedUserResp(updated_user_id=updated_user_id)
