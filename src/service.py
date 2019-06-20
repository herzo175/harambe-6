import grpc
from concurrent import futures
from datetime import datetime
import time
import logging
import sys
import os

import app
from predictor import lstm
from api import service_pb2
from api import service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Predictor(service_pb2_grpc.PredictorServicer):
    def Predict(self, request, context):
        symbol = request.symbol
        trend_length = request.trend_length
        trend_start_date = request.trend_start_date
        trend_end_date = request.trend_end_date

        print(
            f"RECEIVED: symbol: {symbol}, trend length: {trend_length},"
            f"start: {trend_start_date}, end: {trend_end_date}"
        )

        try:
            prediction_val, prediction_val_denorm = app.predict(symbol, trend_length, trend_start_date, trend_end_date)
            return service_pb2.PredictionReply(val=prediction_val, val_denorm=prediction_val_denorm)
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return service_pb2.PredictionReply()


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_PredictorServicer_to_server(Predictor(), server)
    print(f"starting on port {port}")
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    try:
        while True:
            # Keep server on until keyboard interrupt
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    port = os.getenv("PORT", sys.argv[1])
    logging.basicConfig()
    serve(port)