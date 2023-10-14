from typing import Union
from uuid import UUID

from fastapi import HTTPException

from api.schemas.schemas import ShowUser
from api.schemas.schemas import UserCreate
from database.dals import UserDAL
from database.models import RoleList
from database.models import User
from hashing import Hasher


def check_permissions(target_user: User, current_user: User) -> bool:
    # check if superadmin deactivating self
    if RoleList.PORTAL_SUPERADMIN in target_user.roles:
        raise HTTPException(status_code=406, detail="Superadmin can not be deleted")

    if target_user.user_id != current_user.user_id:
        # admin check
        if not {RoleList.PORTAL_ADMIN, RoleList.PORTAL_SUPERADMIN}.intersection(
            current_user.roles
        ):
            return False
        # check if admin deactivating superadmin
        if (
            RoleList.PORTAL_ADMIN in current_user.roles
            and RoleList.PORTAL_SUPERADMIN in target_user.roles
        ):
            return False
        # check if admin deactivating admin
        if (
            RoleList.PORTAL_ADMIN in current_user.roles
            and RoleList.PORTAL_ADMIN in target_user.roles
        ):
            return False

    return True


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_pwd=Hasher.get_pwd_hash(body.password),
            roles=[RoleList.PORTAL_USER],
        )
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


async def _delete_user(user_id, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(user_id=user_id)
    return deleted_user_id


async def _get_user_by_id(user_id, session) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(user_id=user_id)
        if user is not None:
            return user


async def _update_user(
    cleaned_params: dict, user_id: UUID, session
) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(user_id, **cleaned_params)
        return updated_user_id
