# Built-in Modules (python)
from dataclasses import dataclass

@dataclass
class TradingViewOrder:
    ticker: str
    action: str
    contracts: float
    position_size: float
    interval: int
    close: str
    time: str

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ticker={self.ticker} action={self.action} contracts={self.contracts} position_size={self.position_size} interval={self.interval} close={self.close} time={self.time}>"