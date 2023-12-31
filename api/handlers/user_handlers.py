from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.handlers.actions.auth import get_current_user_from_token
from api.handlers.actions.user import _create_new_user
from api.handlers.actions.user import _delete_user
from api.handlers.actions.user import _get_user_by_id
from api.handlers.actions.user import _update_user
from api.handlers.actions.user import check_permissions
from api.schemas.schemas import DeletedUserResp
from api.schemas.schemas import ShowUser
from api.schemas.schemas import UpdatedUserReq
from api.schemas.schemas import UpdatedUserResp
from api.schemas.schemas import UserCreate
from database.models import User
from database.session import get_db

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.delete("/", response_model=DeletedUserResp)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> DeletedUserResp:
    # Check permissions
    user_to_delete = await _get_user_by_id(user_id, db)
    if user_to_delete is None:
        raise HTTPException(
            status_code=404, detail=f"User with id:{user_id} not found in database."
        )

    if not check_permissions(target_user=user_to_delete, current_user=current_user):
        raise HTTPException(status_code=403, detail="Forbidden.")

    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id:{user_id} not found in database."
        )
    return DeletedUserResp(deleted_user_id=deleted_user_id)


@user_router.get("/")  # response_model = ShowUser ???
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id:{user_id} not found in database."
        )
    return user


@user_router.patch("/", response_model=UpdatedUserResp)
async def update_user(
    user_id: UUID,
    body: UpdatedUserReq,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResp:
    user = await _get_user_by_id(user_id, db)
    cleaned_params = body.dict(exclude_none=True)
    if cleaned_params == {}:
        raise HTTPException(
            status_code=422,
            detail="Для продолжения должен быть изменен хотябы один параметр",
        )
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id:{user_id} not found in database."
        )
    # Check permissions
    user_to_update = await _get_user_by_id(user_id, db)
    if user_to_update.user_id != current_user.user_id:
        if not check_permissions(target_user=user_to_update, current_user=current_user):
            raise HTTPException(status_code=403, detail="Forbidden.")

    try:
        updated_user_id = await _update_user(
            cleaned_params=cleaned_params, user_id=user_id, session=db
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

    return UpdatedUserResp(updated_user_id=updated_user_id)


@user_router.patch("/admin_role", response_model=UpdatedUserResp)
async def grant_admin_role(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    if current_user.user_id == user_id:
        raise HTTPException(status_code=400, detail="Can not promote yourself")

    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden.")

    target_user = await _get_user_by_id(user_id, db)

    if target_user.is_admin or target_user.is_superadmin:
        raise HTTPException(
            status_code=409, detail=f"User with id:{user_id} is already promoted"
        )

    if target_user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id:{user_id} not found in db"
        )

    data_to_update = {"roles": target_user.add_admin_role()}

    try:
        updated_user_id = await _update_user(
            cleaned_params=data_to_update, user_id=user_id, session=db
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error:{err}")
    return UpdatedUserResp(updated_user_id=updated_user_id)


@user_router.delete("/admin_role", response_model=UpdatedUserResp)
async def revoke_admin_role(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    if current_user.user_id == user_id:
        raise HTTPException(status_code=400, detail="Can not change self roles")

    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden.")

    target_user = await _get_user_by_id(user_id, db)

    if not target_user.is_admin:
        raise HTTPException(
            status_code=409, detail=f"User with id: {user_id} is not admin"
        )

    if target_user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id: {user_id} not found in db"
        )

    data_to_update = {"roles": target_user.remove_admin_role()}

    try:
        updated_user_id = await _update_user(
            cleaned_params=data_to_update, user_id=user_id, session=db
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error:{err}")
    return UpdatedUserResp(updated_user_id=updated_user_id)
