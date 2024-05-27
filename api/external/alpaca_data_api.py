import logging
from typing import List, Optional

from requests import get, Response

from api.models import AlpacaQuote
from api.exceptions import AlpacaQuoteException


log = logging.getLogger(__name__)


class AlpacaDataAPI:
    def __init__(self, url: str, version: str, api_key: str, api_secret: str) -> None:
        self._url: str = f"{url}/{version}"
        self._api_key: str = api_key
        self._api_secret: str = api_secret
    
    def get_price(self, equity: str, tickers: List[str], loc: str = "us") -> Optional[dict[str, AlpacaQuote]]:
        try:
            res: Response = get(url=f"{self._url}/{equity}/{loc}/latest/quotes", headers=self._get_headers(), params={"symbols": self._get_tickers_list(tickers=tickers)})
            if 200 <= res.status_code <= 299:
                return self._to_alpaca_quote_dict(res.json().get("quotes"))
            
            raise AlpacaQuoteException(f"error getting quotes for {self._get_tickers_list(tickers=tickers)}")
        except Exception as e:
            log.error(f"there was an error getting quotes from alpaca data api: {e}")

    def _to_alpaca_quote_dict(self, quotes: dict[str, dict]) -> dict[str, AlpacaQuote]:
        return {key: AlpacaQuote(ticker=key, **values) for key, values in quotes.items()}

    def _get_tickers_list(self, tickers: List[str]) -> str:
        return ",".join(tickers)

    def _get_headers(self) -> dict:
        return {
            "APCA-API-KEY-ID": self._api_key,
            "APCA-API-SECRET-KEY": self._api_secret,
            "User-Agent": "APCA-TRADE-SDK-PY/3.2.0"
        }