# Built-in Modules (python)

# Custom Modules
from api.routes import TradingViewBlueprint

# Installed Modules (pip)
from flask import (
    request,
    Flask,
)

app = Flask(__name__)
app.register_blueprint(TradingViewBlueprint, url_prefix="/tradingview")


if __name__ == "__main__":
    app.run()