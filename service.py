import grpc
from concurrent import futures
import time
import logging

import service_pb2
import service_pb2_grpc
import lstm

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Predictor(service_pb2_grpc.PredictorServicer):
    def _get_frames(self, symbol, trend_length):
        # NOTE: filters configurable?
        times = lstm.get_time_series_daily(symbol, filters=["1. open"], outputsize="full")
        vectors = lstm.times_to_vectors(times)[::-1]
        return lstm.get_frames(vectors, seq_len=trend_length, with_target=True)


    def _get_trained_model(self, frames):
        train_x, train_y = lstm.seperate_xy(lstm.normalize_frames(frames))
        return lstm.setup_lstm_model(train_x, train_y)


    def _predict_frame(self, model, frame):
        return lstm.predict_sequences_multiple(model, [frame])


    def Predict(self, request, context):
        symbol = request.symbol
        trend_length = request.trend_length
        print(f"RECEIVED: symbol: {symbol}, trend length: {trend_length}")

        # TODO: cache predictions
        frames = self._get_frames(symbol, trend_length)
        model = self._get_trained_model(frames)
        last_frame = frames[-1][1:]
        prediction = self._predict_frame(model, lstm.normalize_frame(last_frame))

        prediction_val = prediction[0][0]
        prediction_val_denorm = lstm.denormalize_dim(prediction_val, last_frame[0][0])

        return service_pb2.PredictionReply(val=prediction_val, val_denorm=prediction_val_denorm)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_PredictorServicer_to_server(Predictor(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            # Keep server on until keyboard interrupt
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()