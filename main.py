
# Custom Modules
from log import setup_logging
setup_logging()

from api.routes import TradingViewBlueprint

# Installed Modules (pip)
from flask import (
    Flask,
)

import logging

logger = logging.getLogger(__name__)


app = Flask(__name__)
app.register_blueprint(TradingViewBlueprint, url_prefix="/tradingview")

if __name__ == "__main__":
    app.run(threaded=True)