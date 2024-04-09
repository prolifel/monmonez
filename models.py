from pydantic import BaseModel
from typing import Any, Union

STATEMENT_TYPES = [
    "cimb",
]


class Response(BaseModel):
    message: str
    data: Any


class TokenData(BaseModel):
    username: Union[str, None] = None


class Env(BaseModel):
    ACCESS_TOKEN_EXPIRE_MINUTES: Union[int, None] = None
    SECRET_KEY: Union[str, None] = None
    ALGORITHM: Union[str, None] = None
    APP_USER: Union[str, None] = None
