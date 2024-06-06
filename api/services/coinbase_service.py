import json
import logging
from os import getenv
from uuid import uuid4
from typing import Union

from dotenv import load_dotenv
from coinbase import jwt_generator
from requests import get, post, Response

from api.enums import HTTPMethods
from api.exceptions import APIError, BuyingPowerException, NoOpenPositions
from api.enums import TradingViewAction
from api.models import CoinbasePrice, CoinbaseAccount, TradingViewOrder, CoinbasePortfolioBreakdown, CoinbasePosition


log = logging.getLogger(__name__)
load_dotenv(override=True)

class CoinbaseService:
    def __init__(self):
        self._api_key: str = getenv("COINBASE_API_KEY")
        self._api_secret: str = getenv("COINBASE_API_SECRET")
        self._account_uuid: str = getenv("COINBASE_TRANSACTION_ACCOUNT_UUID")
        self._portfolio_uuid: str = getenv("COINBASE_PORTFOLIO_UUID")
        self.url: str = getenv("COINBASE_API_URL")
        self.base_path: str = getenv("COINBASE_API_BASE_PATH")
        self.min_dollar_amount: float = float(getenv("COINBASE_MIN_DOLLAR_AMOUNT"))
    
    def submit_order(self, order: TradingViewOrder) -> None:
        log.info(f"Creating {order.action} for {order.asset}")
        account: CoinbaseAccount = self.get_account()
        body: dict = self._build_order_data(order=order, account=account)
        res: Response = self._post_request(sub_path="brokerage/orders", body=json.dumps(body))

        data: dict = res.json()
        log.debug("Order response", extra=data)
        if not HTTPMethods.is_success(code=res.status_code) or not data.get("success"):
            raise APIError(f"Error submitting order: {res.status_code} -> {data}")
        
        log.info("Sucessfully submitted the order")
    
    def get_account_breakdown(self) -> CoinbasePortfolioBreakdown:
        log.info("Getting coinbase account breakdown")
        res: Response = self._get_request(sub_path=f"brokerage/portfolios/{self._portfolio_uuid}")

        data: dict = res.json()
        log.debug("Account breakdown response", extra=data)
        if not HTTPMethods.is_success(code=res.status_code):
            raise APIError(f"Error getting portfolio listing: {res.status_code} -> {data}")
        
        log.info("Successfully got the account breakdown")
        return CoinbasePortfolioBreakdown(**data)

    def list_accounts(self) -> dict:
        log.info("Getting account listing")
        res: Response = self._get_request(sub_path="brokerage/accounts")

        log.debug("Got account listing", extra=res.json())
        if not HTTPMethods.is_success(code=res.status_code):
            raise APIError(f"Error getting account listing: {res.status_code} -> {res.json()}")
        
        return res.json()
    
    def list_portfolios(self) -> dict:
        log.info("Getting portfolio listing")
        res: Response = self._get_request(sub_path="brokerage/portfolios")

        log.debug("Got portfolio listing", extra=res.json())
        if not HTTPMethods.is_success(code=res.status_code):
            raise APIError(f"Error getting portfolio listing: {res.status_code} -> {res.json()}")
        
        return res.json()

    def get_account(self) -> CoinbaseAccount:
        log.info(f"Getting account {self._account_uuid}")
        res: Response = self._get_request(sub_path=f"brokerage/accounts/{self._account_uuid}")

        log.debug("Got account info", extra=res.json())
        if not HTTPMethods.is_success(code=res.status_code):
            raise APIError(f"Got unsucessful status code: {res.status_code}")
        
        return CoinbaseAccount(**res.json().get("account"))

    def get_bid_ask(self, ticker: str) -> CoinbasePrice:
        log.info(f"Getting bid/asking price for {ticker}")
        res: Response = self._get_request(sub_path="brokerage/best_bid_ask", params={"product_ids": ticker})

        log.debug(f"Bid/Asking price data for {ticker}", extra=res.json())
        if not HTTPMethods.is_success(code=res.status_code):
            raise APIError(f"Got unsuccessful status code: {res.status_code}")

        return CoinbasePrice(**res.json().get("pricebooks")[0])

    def get_holding(self, portofolio: CoinbasePortfolioBreakdown, asset: str) -> Union[CoinbasePosition, None]:
        log.info(f"Getting holding for {asset}")
        for position in portofolio.breakdown.spot_positions:
            if position.asset == asset:
                log.info(f"Found {asset} holding")
                log.debug(position)
                return position
        
        log.info(f"No {asset} holdings found")
        return None

    def _calc_qty(self, order: TradingViewOrder, account: CoinbaseAccount) -> float:
        log.debug(f"Calculating qty to {order.action.name} of {order.asset}")

        cb_price: CoinbasePrice = self.get_bid_ask(ticker=order.ticker)
        log.debug(f"{order.asset} buy={cb_price.buy} sell={cb_price.sell}")

        if order.action == TradingViewAction.BUY:
            if account.available_balance.value < self.min_dollar_amount or order.buy_sell_amount > account.available_balance.value:
                log.error(f"Insuffcient funds for buying {order.asset}", extra={"available_balance": account.available_balance.value, "min_dollar_amount": self.min_dollar_amount, "buy_sell_amount": order.buy_sell_amount})
                raise BuyingPowerException(f"Insufficient funds to buy {order.asset}. Balance: {account.available_balance.value}")

            log.debug(f"Quantity to buy: {order.buy_sell_amount / cb_price.buy}")
            return order.buy_sell_amount / cb_price.buy
        
        if order.action == TradingViewAction.SELL:
            portofolio: CoinbasePortfolioBreakdown = self.get_account_breakdown()
            holding: CoinbasePosition = self.get_holding(portofolio=portofolio, asset=order.asset)
            if holding is None:
                log.error(f"Cannot sell {order.asset} as there are no holdings")
                raise NoOpenPositions(f"Cannot sell {order.asset} as there are now open positions or the asset {order.asset} could not be found")
            
            log.debug(f"Selling {holding.total_balance_crypto:.8f} of {order.asset}")
            return holding.total_balance_crypto

    def _build_order_data(self, order: TradingViewOrder, account: CoinbaseAccount) -> dict:
        data: dict =  {
            "client_order_id": str(uuid4()),
            "product_id": order.ticker,
            "side": order.action.to_str().upper(),
            "order_configuration": {
                "market_market_ioc": {
                    "base_size": f"{self._calc_qty(order=order, account=account):.8f}"
                }
            },
            "retail_portfolio_id": account.retail_portfolio_id
        }

        log.debug("Created order data", extra=data)

        return data

    def _get_request(self, sub_path: str,  params: dict = {}) -> Response:
        path: str = f"{self.base_path}/{sub_path}"
        headers = self._get_headers(method=HTTPMethods.GET.to_str(), path=f"/{path}")
        log.debug(f"Getting {self.url}/{path}", extra={**params})
        return get(url=f"{self.url}/{path}", headers=headers, params=params)
    
    def _post_request(self, sub_path: str, body: str) -> Response:
        path: str = f"{self.base_path}/{sub_path}"
        headers = self._get_headers(method=HTTPMethods.POST.to_str(), path=f"/{path}")
        log.debug(f"Post {self.url}/{path}", extra={**headers, **json.loads(body)})
        return post(url=f"{self.url}/{path}", headers=headers, data=body)

    def _get_headers(self, method: str, path: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._get_jwt(method=method, path=path)}",
            "Content-Type": "application/json"
        }

    def _get_jwt(self, method: str, path: str) -> str:
        log.debug("Creating JWT token...")
        uri: str = jwt_generator.format_jwt_uri(method=method, path=path)
        return jwt_generator.build_rest_jwt(uri=uri, key_var=self._api_key, secret_var=self._api_secret)

