# Built-in Modules (python)
from api.services import AlpacaService
from api.models import TradingViewOrder

# Installed Modules (pip)
from flask import (
    request,
    Blueprint,
)
from alpaca.trading.enums import OrderSide, TimeInForce

TradingViewBlueprint = Blueprint("example_blueprint", __name__)

@TradingViewBlueprint.route("/alert", methods=["POST"])
def alert():
    order: TradingViewOrder = TradingViewOrder(**request.get_json())
    print(f"Got signal: {order}")
    alpaca: AlpacaService = AlpacaService()
    alpaca.execute_trade(
        ticker=order.ticker,
        qty=order.position_size,
        side=order.action,
        time_in_force=TimeInForce.GTC
    )
    return {}, 200