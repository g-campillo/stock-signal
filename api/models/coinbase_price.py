from typing import List, Dict


class CoinbasePrice:
    ticker: str
    buy: float
    sell: float
    time: str

    def __init__(self, product_id: str, bids: List[Dict], asks: List[Dict], time: str):
        self.ticker: str = product_id
        self.buy: float = float(bids[0].get("price"))
        self.sell: float = float(asks[0].get("price"))
        self.time: str = time

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ticker={self.ticker} buy={self.buy} sell={self.sell} time={self.time}>"