import logging
from os import getenv
from typing import Optional

from dotenv import load_dotenv
import alpaca_trade_api as old_alpaca_api
from alpaca.common.exceptions import APIError
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetAssetsRequest
from alpaca.trading.enums import OrderSide, TimeInForce, AssetStatus as AlpacaAssetStatus, AssetClass as AlpacaAssetClass
from alpaca.trading.models import TradeAccount as AlpacaAccount, Asset as AlpacaAsset, Position as AlpacaPosition

from api.external import AlpacaDataAPI
from api.models import TradingViewOrder, AlpacaQuote
from api.enums import TradingViewAction
from api.tickers import get_tradingview_ticker
from api.exceptions import BuyingPowerException, AssetNotTradeable, NoOpenPositions


log = logging.getLogger(__name__)
load_dotenv(override=True)

class AlpacaService:
    def __init__(self) -> None:
        self._api_key: str = getenv("ALPACA_API_KEY")
        self._api_secret: str = getenv("ALPACA_API_SECRET")
        self._purchase_amount: float = float(getenv("BUY_AMOUNT"))
        self._data_api_url: str = getenv("ALPACA_DATA_API_URL")
        self._client: TradingClient = TradingClient(api_key=self._api_key, secret_key=self._api_secret)
        self._data_api: AlpacaDataAPI = AlpacaDataAPI(url=self._data_api_url, version="v1beta3", api_key=self._api_key, api_secret=self._api_secret)

        self.account: AlpacaAccount = self.get_account_info()
    
    def execute_trade(self, tv_order: TradingViewOrder) -> None:
        try:
            position: AlpacaPosition = self.get_position(ticker=tv_order.ticker)
            quote: AlpacaQuote = self._data_api.get_price(equity=tv_order.equity.to_str(), tickers=[tv_order.alpaca_price_ticker]).get(tv_order.alpaca_price_ticker)
            asset: AlpacaAsset = self.get_asset(ticker=tv_order.ticker)
            qty = self._calculate_qty(order=tv_order, asset=asset, position=position, quote=quote)
            order: MarketOrderRequest = self.create_market_order(ticker=tv_order.ticker, qty=qty, side=self._get_order_side(tv_order.action), time_in_force=TimeInForce.GTC)
            self._client.submit_order(order_data=order)
            print(f"Executed {tv_order.action} on {tv_order.ticker} (qty={qty})")
        except Exception as e:
            log.error(f"error placing {tv_order.action} order on {tv_order.ticker}: {e}")
    
    def create_market_order(self, ticker: str, qty: float, side: OrderSide, time_in_force: TimeInForce) -> MarketOrderRequest:
        return MarketOrderRequest(
            symbol=ticker,
            qty=qty,
            side=side,
            time_in_force=time_in_force
        )

    def get_account_info(self) -> Optional[AlpacaAccount]:
        try:
            return self._client.get_account()
        except APIError as e:
            log.error(f"alpaca api error getting account info: {e}")
            return None
        except Exception as e:
            log.error(f"unexpected error getting account info: {e}")
    
    def get_asset(self, ticker: str) -> Optional[AlpacaAsset]:
        try:
            return self._client.get_asset(symbol_or_asset_id=ticker)
        except APIError as e:
            log.error(f"alpaca api error getting asset {ticker}: {e}")
            return None
        except Exception as e:
            log.error(f"unexpected error getting position for {ticker} :{e}")
    
    def get_position(self, ticker: str) -> Optional[AlpacaPosition]:
        try:
            return self._client.get_open_position(symbol_or_asset_id=ticker)
        except APIError as e:
            log.error(f"alpaca api error getting {ticker} position: {e}")
            return None
        except Exception as e:
            log.error(f"unexpected error getting position for {ticker}: {e}")

    def _calculate_qty(self, order: TradingViewOrder, asset: AlpacaAsset, position: AlpacaPosition, quote: AlpacaQuote) -> float:
        if not asset.tradable or asset.status != AlpacaAssetStatus.ACTIVE:
            raise AssetNotTradeable(f"{order.ticker} is not a tradeable or is not active asset (tradeable={asset.tradable} status={asset.status})")

        if order.action == TradingViewAction.SELL and position is None:
            raise NoOpenPositions(f"Cannot sell {order.ticker} as there are no open positions")

        if order.action == TradingViewAction.SELL:
            return min(order.buy_sell_amount/quote.bid_price, float(position.qty))
        
        if order.action == TradingViewAction.BUY:
            return order.buy_sell_amount / quote.asking_price
    
    def _get_order_side(self, action: TradingViewAction) -> Optional[OrderSide]:
        actions = {
            TradingViewAction.BUY: OrderSide.BUY,
            TradingViewAction.SELL: OrderSide.SELL
        }
        return actions.get(action, None)

