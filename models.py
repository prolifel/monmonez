from pydantic import BaseModel
from typing import Any

STATEMENT_TYPES = [
    "cimb",
]


class Response(BaseModel):
    message: str
    data: Any
