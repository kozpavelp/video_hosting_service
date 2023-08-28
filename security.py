from datetime import datetime
from datetime import timedelta
from typing import Optional

from jose import jwt

import config


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    encode.update({"exp": expire})
    encoded_jwt = jwt.encode(encode, config.SECRET_KEY, algorithm=config.ALG)
    return encoded_jwt
