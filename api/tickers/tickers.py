import logging

from api.enums import TradingViewAction
from api.exceptions import TickerException


log = logging.getLogger(__name__)

# Trasnlating the tradingview ticker to an Alpaca ticker 
TICKERS: dict[str, dict[TradingViewAction, str]] = {
    "BTCUSD": {
        TradingViewAction.BUY: "BTC/USD",
        TradingViewAction.SELL: "BTCUSD"
    }
}

def get_tradingview_ticker(ticker: str, action: TradingViewAction) -> str:
    try:
        return TICKERS[ticker][action]
    except KeyError:
        raise TickerException(f"Could not get TradingView ticker for {ticker} with action {action}")