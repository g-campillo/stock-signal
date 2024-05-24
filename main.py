from flask import Flask

app = Flask(__name__)

@app.route("/tradingview/webhook")
def tradingview_hook():
    return {}, 200


if __name__ == "__main__":
    app.run()