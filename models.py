from pydantic import BaseModel
from typing import Any
from typing import Union

STATEMENT_TYPES = [
    "cimb",
]


class Response(BaseModel):
    message: str
    data: Any


class TokenData(BaseModel):
    username: Union[str, None] = None
