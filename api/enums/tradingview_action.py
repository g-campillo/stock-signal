from api.enums import BaseEnum

from enum import Enum, auto


class TradingViewAction(BaseEnum, Enum):
    BUY = auto()
    SELL = auto()