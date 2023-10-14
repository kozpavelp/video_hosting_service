import uuid
from enum import Enum

from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RoleList(str, Enum):
    PORTAL_USER = "PORTAL_USER"
    PORTAL_ADMIN = "PORTAL_ADMIN"
    PORTAL_SUPERADMIN = "PORTAL_SUPERADMIN"


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    hashed_pwd = Column(String, nullable=False)
    roles = Column(ARRAY(String), nullable=False)

    @property
    def is_superadmin(self) -> bool:
        return RoleList.PORTAL_SUPERADMIN in self.roles

    @property
    def is_admin(self) -> bool:
        return RoleList.PORTAL_ADMIN in self.roles

    def add_admin_role(self):
        if not self.is_admin:
            return {*self.roles, RoleList.PORTAL_ADMIN}

    def remove_admin_role(self):
        if self.is_admin:
            return {role for role in self.roles if role != RoleList.PORTAL_ADMIN}


class Video(Base):
    __tablename__ = 'video'

    video_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
