from logging import getLogger
from typing import Union
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.models import DeletedUserResp
from api.models.models import ShowUser
from api.models.models import UpdatedUserReq
from api.models.models import UpdatedUserResp
from api.models.models import UserCreate
from database.dals import UserDAL
from database.session import get_db
from hashing import Hasher



