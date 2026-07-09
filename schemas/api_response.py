from typing import Generic
from typing import Optional
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):

    success: bool

    message: str

    data: Optional[T] = None