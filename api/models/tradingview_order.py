from api.enums import TradingViewAction, Equity

# Built-in Modules (python)
from dataclasses import dataclass

@dataclass
class TradingViewOrder:
    ticker: str
    alpaca_price_ticker: str
    action: TradingViewAction
    contracts: float
    position_size: float
    interval: int
    close: float
    time: str
    equity: Equity
    buy_sell_amount: float

    def __init__(self, ticker: str, action: str, contracts: float, position_size: float, interval: int, close: float, time: str, alpaca_price_ticker: str, equity: str, buy_sell_amount: float):
        self.ticker = ticker
        self.alpaca_price_ticker = alpaca_price_ticker
        self.action = TradingViewAction.from_str(action)
        self.contracts = contracts
        self.position_size = position_size
        self.interval = interval
        self.close = close
        self.time = time
        self.equity = Equity.from_str(equity)
        self.buy_sell_amount = buy_sell_amount

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ticker={self.ticker} action={self.action} contracts={self.contracts} position_size={self.position_size} interval={self.interval} close={self.close} time={self.time}>"