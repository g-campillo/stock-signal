from dataclasses import dataclass


@dataclass
class AlpacaQuote:
    ticker: str
    asking_price: float
    asking_size: float
    bid_price: float
    bid_size: float
    time: str

    def __init__(self, ticker: str, ap: float, bp: float, bs: float, t: str, **kwargs):
        self.ticker: str = ticker
        self.asking_price: float = ap 
        self.asking_size: float = kwargs.get("as")
        self.bid_price: float = bp
        self.bid_size: float = bs
        self.time: str = t
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ticker={self.ticker} asking_price={self.asking_price}> bid_price={self.bid_price} time={self.time}"