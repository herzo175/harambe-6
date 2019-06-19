import logging
import sys

import grpc
import requests

import service_pb2
import service_pb2_grpc

# HOST='localhost:50051'
HOST='35.224.74.56:80'
PROTOCOL='http'

def run_grpc():
    with grpc.insecure_channel(HOST) as channel:
        # with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.PredictorStub(channel)
        response = stub.Predict(service_pb2.PredictionRequest(symbol="MSFT", trend_start_date="2019-03-10", trend_end_date="2019-03-15"))
        print(f"Client received: {response.val_denorm}")


def run_server():
    url = f"{PROTOCOL}://{HOST}/predict"
    # response = requests.post(url, json={"symbol": "MSFT", "trend_start_date": "2019-03-10", "trend_end_date": "2019-03-15"})
    response = requests.post(url, json={"symbol": "MSFT", "trend_length": 15})
    print(response.json())


if __name__ == '__main__':
    logging.basicConfig()

    mode = sys.argv[1] if len(sys.argv) > 1 else "server"

    if mode == "grpc":
        run_grpc()
    else:
        run_server()