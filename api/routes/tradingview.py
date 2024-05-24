# Built-in Modules (python)


# Installed Modules (pip)
from flask import (
    request,
    Blueprint,
)

TradingViewBlueprint = Blueprint("example_blueprint", __name__)

@TradingViewBlueprint.route("/alert", methods=["POST"])
def alert():
    print(request.get_json())
    return {}, 200