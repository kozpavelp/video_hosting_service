"""Модуль валидации"""
import re
import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import constr
from pydantic import EmailStr
from pydantic import validator


LETTER_MATCH = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """Convert everything to json"""

        from_attributes = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH.match(value):
            HTTPException(status_code=422, detail="Имя должно состоять из букв")
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH.match(value):
            HTTPException(status_code=422, detail="Фамилия должна состоять из букв")
        return value


class VideoCreate(BaseModel):
    name: str
    file_path: str

class ShowVideo(BaseModel):
    video_id: uuid.UUID
    name: str
    file_path: str

class DeletedUserResp(BaseModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResp(BaseModel):
    updated_user_id: uuid.UUID


class UpdatedUserReq(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH.match(value):
            raise HTTPException(status_code=422, detail="Имя должно состоять из букв")
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH.match(value):
            raise HTTPException(
                status_code=422, detail="Фамилия должна состоять из букв"
            )
        return value


class Token(BaseModel):
    access_token: str
    type_token: str
