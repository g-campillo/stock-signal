# Built-in Modules (python)
from api.models.trading_view_order import TradingViewOrder

# Installed Modules (pip)
from flask import (
    request,
    Blueprint,
)

TradingViewBlueprint = Blueprint("example_blueprint", __name__)

@TradingViewBlueprint.route("/alert", methods=["POST"])
def alert():
    print(request.get_json())
    order: TradingViewOrder = TradingViewOrder(**request.get_json())
    print(order)
    return {}, 200