import logging
import sys

import grpc
import requests

from api import service_pb2
from api import service_pb2_grpc

# NOTE: connection over http, will fail if network forces https
# HOST='localhost:50051'
HOST='harambe-6.default.cluster.vask.io:80'
SYMBOL="MSFT"

def run_grpc():
    with grpc.insecure_channel(HOST) as channel:
        # with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.PredictorStub(channel)
        response = stub.Predict(service_pb2.PredictionRequest(symbol=SYMBOL, trend_length=15))
        # response = stub.Predict(service_pb2.PredictionRequest(symbol=SYMBOL, trend_start_date="2019-03-10", trend_end_date="2019-03-15"))
        print(f"Client received: {response.val_denorm}")

        # response = stub.Backtest(service_pb2.BacktestRequest(symbol="MSFT", trend_length=15, prediction_start_date="2019-04-01", prediction_end_date="2019-05-20"))
        # response = stub.Backtest(service_pb2.BacktestRequest(symbol=SYMBOL, trend_length=15, prediction_start_date="2019-11-03", prediction_end_date="2019-12-29"))
        # print(f"backtest received: {response.percent_change}")


if __name__ == '__main__':
    logging.basicConfig()
    run_grpc()
