import json
from os import getenv
from uuid import uuid4

from dotenv import load_dotenv
from coinbase import jwt_generator
from requests import get, post, Response

from api.enums import HTTPMethods
from api.exceptions import APIError
from api.enums import TradingViewAction
from api.models import CoinbasePrice, CoinbaseAccount

load_dotenv(override=True)

class CoinbaseService:
    def __init__(self):
        self._api_key: str = getenv("COINBASE_API_KEY")
        self._api_secret: str = getenv("COINBASE_API_SECRET")
        self._account_uuid: str = getenv("COINBASE_TRANSACTION_ACCOUNT_UUID")
        self.url: str = getenv("COINBASE_API_URL")
        self.base_path: str = getenv("COINBASE_API_BASE_PATH")
    
    def submit_order(self, ticker: str, side: TradingViewAction):
        body: dict = self._build_order_data(ticker=ticker, side=side, qty=None)
        res: Response = self._post_request(sub_path="brokerage/orders", body=json.dumps(body))

        if not HTTPMethods.is_success(code=res.status_code):
            raise APIError(f"Error submitting order: {res.status_code} -> {res.json()}")
    
    def get_account(self):
        res: Response = self._get_request(sub_path=f"brokerage/accounts/{self._account_uuid}")

        if not HTTPMethods.is_success(code=res.status_code):
            raise APIError(f"Got unsucessful status code: {res.status_code}")
        
        return CoinbaseAccount(**res.json().get("account"))

    def get_bid_ask(self, ticker: str) -> CoinbasePrice:
        res: Response = self._get_request(sub_path="brokerage/best_bid_ask", params={"product_ids": ticker})

        if not HTTPMethods.is_success(code=res.status_code):
            raise APIError(f"Got unsuccessful status code: {res.status_code}")

        return CoinbasePrice(**res.json().get("pricebooks")[0])

    def _build_order_data(self, ticker: str, side: TradingViewAction, qty: float) -> dict:
        return {
            "client_order_id": str(uuid4()),
            "product_id": ticker,
            "side": side.to_str(),
            "order_configuration": {
                "market_market_ioc": {
                    "base_size": str(qty)
                }
            }
        }

    def _get_request(self, sub_path: str,  params: dict = {}) -> Response:
        path: str = f"{self.base_path}/{sub_path}"
        headers = self._get_headers(method=HTTPMethods.GET.to_str(), path=f"/{path}")
        return get(url=f"{self.url}/{path}", headers=headers, params=params)
    
    def _post_request(self, sub_path: str, body: str) -> Response:
        path: str = f"{self.base_path}/{sub_path}"
        headers = self._get_headers(method=HTTPMethods.POST.to_str(), path=f"/{path}")
        return post(url=f"{self.url}/{path}", headers=headers, data=body)

    def _get_headers(self, method: str, path: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._get_jwt(method=method, path=path)}",
            "Content-Type": "application/json"
        }

    def _get_jwt(self, method: str, path: str):
        uri: str = jwt_generator.format_jwt_uri(method=method, path=path)
        return jwt_generator.build_rest_jwt(uri=uri, key_var=self._api_key, secret_var=self._api_secret)

