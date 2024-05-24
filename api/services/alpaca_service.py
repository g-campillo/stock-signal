import logging
from os import getenv
from typing import Optional

from dotenv import load_dotenv
from alpaca.common.exceptions import APIError
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, AssetStatus as AlpacaAssetStatus
from alpaca.trading.models import TradeAccount as AlpacaAccount, Asset as AlpacaAsset, Position as AlpacaPosition

from api.enums import TradingViewAction
from api.tickers import get_tradingview_ticker
from api.exceptions import BuyingPowerException, AssetNotTradeable


log = logging.getLogger(__name__)
load_dotenv()

class AlpacaService:
    def __init__(self) -> None:
        self._api_key: str = getenv("ALPACA_API_KEY")
        self._api_secret: str = getenv("ALPACA_API_SECRET")
        self._purchase_amount: float = float(getenv("BUY_AMOUNT"))
        self._client: TradingClient = TradingClient(api_key=self._api_key, secret_key=self._api_secret)

        self.account: AlpacaAccount = self.get_account_info()
    
    def execute_trade(self, ticker: str, qty: float, side: TradingViewAction, time_in_force: TimeInForce) -> None:
        try:
            asset: AlpacaAsset = self.get_asset(ticker=ticker)
            qty = self._calculate_qty(ticker=ticker, qty=qty, action=side, asset=asset)
            order: MarketOrderRequest = MarketOrderRequest(
                symbol=get_tradingview_ticker(ticker=ticker, action=side),
                qty=qty,
                side=self._get_order_side(action=side),
                time_in_force=time_in_force
            )
            self._client.submit_order(order_data=order)
            print(f"Executed {side} on {ticker} (qty={qty})")
        except Exception as e:
            log.error(f"error placing {side} order on {ticker}: {e}")
    
    def get_account_info(self) -> AlpacaAccount:
        try:
            return self._client.get_account()
        except APIError as e:
            log.error(f"alpaca api error getting account info: {e}")
        except Exception as e:
            log.error(f"unexpected error getting account info: {e}")
    
    def get_asset(self, ticker: str) -> AlpacaAsset:
        try:
            return self._client.get_asset(symbol_or_asset_id=ticker)
        except APIError as e:
            log.error(f"alpaca api error getting asset {ticker}: {e}")
        except Exception as e:
            log.error(f"unexpected error getting position for {ticker} :{e}")
    
    def get_position(self, ticker: str) -> Optional[AlpacaPosition]:
        try:
            return self._client.get_open_position(symbol_or_asset_id=ticker)
        except APIError as e:
            log.error(f"alpaca api error getting {ticker} position: {e}")
        except Exception as e:
            log.error(f"unexpected error getting position for {ticker}: {e}")

    def _calculate_qty(self, ticker: str, qty: float, action: TradingViewAction, asset: AlpacaAsset) -> float:
        if not asset.tradable or asset.status != AlpacaAssetStatus.ACTIVE:
            raise AssetNotTradeable(f"{ticker} is not a tradeable or is not active asset (tradeable={asset.tradable} status={asset.status})")

        if action == TradingViewAction.SELL:
            postion: AlpacaPosition = self.get_position(ticker=ticker)
            return min(float(postion.qty), qty)

        return qty
    
    def _get_order_side(self, action: TradingViewAction) -> Optional[OrderSide]:
        actions = {
            TradingViewAction.BUY: OrderSide.BUY,
            TradingViewAction.SELL: OrderSide.SELL
        }
        return actions.get(action, None)

