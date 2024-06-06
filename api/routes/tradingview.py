import logging

from api.models import TradingViewOrder
from api.services import CoinbaseService

from flask import (
    request,
    Blueprint,
)


log = logging.getLogger(__name__)

TradingViewBlueprint = Blueprint("alert_blueprint", __name__)
coinbase_service: CoinbaseService = CoinbaseService()


@TradingViewBlueprint.route("/alert", methods=["POST"])
def alert():
    order: TradingViewOrder = TradingViewOrder(**request.get_json())
    log.info(f"Got signal: {order}")

    try:
        coinbase_service.submit_order(order=order)
    except Exception as e:
        log.error("Error submitting order")
        log.error(e)
        return "", 500
    
    return "", 200