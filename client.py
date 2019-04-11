import logging

import grpc
import requests

import service_pb2
import service_pb2_grpc


def run_grpc():
    with grpc.insecure_channel('harambe-6-i4ox34kasa-uc.a.run.app') as channel:
        # with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.PredictorStub(channel)
        response = stub.Predict(service_pb2.PredictionRequest(symbol="MSFT", trend_start_date="2019-03-10", trend_end_date="2019-03-15"))
        print(f"Greeter client received: {response.val_denorm}")


def run_server():
    # url = "http://localhost:50051/predict"
    url = "https://harambe-6-i4ox34kasa-uc.a.run.app/predict"
    # response = requests.post(url, json={"symbol": "MSFT", "trend_start_date": "2019-03-10", "trend_end_date": "2019-03-15"})
    response = requests.post(url, json={"symbol": "MSFT", "trend_length": 15})
    print(response.json())


if __name__ == '__main__':
    logging.basicConfig()
    # run_grpc()
    run_server()