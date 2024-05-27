# Built-in Modules (python)
import logging

# Custom Modules
from api.routes import TradingViewBlueprint

# Installed Modules (pip)
from flask import (
    request,
    Flask,
)


log = logging.getLogger(__name__)
app = Flask(__name__)
app.register_blueprint(TradingViewBlueprint, url_prefix="/tradingview")

if __name__ == "__main__":
    app.run()