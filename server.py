import os
import sys

from flask import Flask, request, jsonify, Response

import app
import lstm


server = Flask(__name__)


@server.route("/predict", methods=["POST"])
def predict():
    body = request.get_json()

    print(f"body: {body}")

    symbol = body["symbol"]
    trend_length = body.get("trend_length")
    trend_start_date = body.get("trend_start_date")
    trend_end_date = body.get("trend_end_date")

    print(
        f"RECEIVED: symbol: {symbol}, trend length: {trend_length},"
        f"start: {trend_start_date}, end: {trend_end_date}"
    )

    try:
        prediction_val, prediction_val_denorm = app.predict(symbol, trend_length, trend_start_date, trend_end_date)
        return jsonify({
            "prediction_val": prediction_val,
            "prediction_val_denorm": prediction_val_denorm
        })
    except ValueError as e:
        return str(e), 400


if __name__ == "__main__":
    server.run(host="0.0.0.0",port=int(os.environ.get("PORT", sys.argv[1])))