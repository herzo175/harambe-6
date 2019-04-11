# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import service_pb2 as service__pb2


class PredictorStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Predict = channel.unary_unary(
        '/endpoints.harambe_6.Predictor/Predict',
        request_serializer=service__pb2.PredictionRequest.SerializeToString,
        response_deserializer=service__pb2.PredictionReply.FromString,
        )


class PredictorServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Predict(self, request, context):
    """Sends a greeting
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_PredictorServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Predict': grpc.unary_unary_rpc_method_handler(
          servicer.Predict,
          request_deserializer=service__pb2.PredictionRequest.FromString,
          response_serializer=service__pb2.PredictionReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'endpoints.harambe_6.Predictor', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
