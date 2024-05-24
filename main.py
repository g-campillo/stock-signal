from flask import (
    Flask,
    request
)

app = Flask(__name__)

@app.route("/tradingview/webhook", methods=["POST"])
def tradingview_hook():
    data = request.get_json()
    print(data)
    return {}, 200


if __name__ == "__main__":
    app.run()