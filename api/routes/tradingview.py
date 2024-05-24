# Built-in Modules (python)
import json

# Installed Modules (pip)
from flask import (
    request,
    Blueprint,
)

TradingViewBlueprint = Blueprint("example_blueprint", __name__)

@TradingViewBlueprint.route("/alert", methods=["POST"])
def alert():
    data: dict = json.loads(request.data.decode("utf-8"))
    print(data)
    return {}, 200