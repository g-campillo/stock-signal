from api.enums import TradingViewAction, Equity

# Built-in Modules (python)
from dataclasses import dataclass

@dataclass
class TradingViewOrder:
    ticker: str
    asset: str
    action: TradingViewAction
    time: str
    buy_sell_amount: float

    def __init__(self, ticker: str, asset: str, action: str, time: str, buy_sell_amount: float):
        self.ticker = ticker
        self.asset = asset
        self.action = TradingViewAction.from_str(action)
        self.time = time
        self.buy_sell_amount = buy_sell_amount

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ticker={self.ticker} asset={self.asset} action={self.action} time={self.time}>"