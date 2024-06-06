from enum import Enum, auto

from .base import BaseEnum


class PortfolioType(BaseEnum, Enum):
    DEFAULT = auto()