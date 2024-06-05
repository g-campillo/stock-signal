from enum import Enum, auto

from .base import BaseEnum

class HTTPMethods(BaseEnum, Enum):
    GET = auto()
    POST = auto

    @classmethod
    def is_success(cls, code: int):
        return 200 <= code <= 299