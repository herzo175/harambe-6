import logging

import grpc

import service_pb2
import service_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.PredictorStub(channel)
        response = stub.Predict(service_pb2.PredictionRequest(symbol="MSFT", trend_length=15))
        print(f"Greeter client received: {response.val_denorm}")


if __name__ == '__main__':
    logging.basicConfig()
    run()