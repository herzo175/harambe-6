# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='service.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\rservice.proto\"9\n\x11PredictionRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x14\n\x0ctrend_length\x18\x02 \x01(\x05\"2\n\x0fPredictionReply\x12\x0b\n\x03val\x18\x01 \x01(\x01\x12\x12\n\nval_denorm\x18\x02 \x01(\x01\x32>\n\tPredictor\x12\x31\n\x07Predict\x12\x12.PredictionRequest\x1a\x10.PredictionReply\"\x00\x62\x06proto3')
)




_PREDICTIONREQUEST = _descriptor.Descriptor(
  name='PredictionRequest',
  full_name='PredictionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='symbol', full_name='PredictionRequest.symbol', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trend_length', full_name='PredictionRequest.trend_length', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=74,
)


_PREDICTIONREPLY = _descriptor.Descriptor(
  name='PredictionReply',
  full_name='PredictionReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='val', full_name='PredictionReply.val', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='val_denorm', full_name='PredictionReply.val_denorm', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=76,
  serialized_end=126,
)

DESCRIPTOR.message_types_by_name['PredictionRequest'] = _PREDICTIONREQUEST
DESCRIPTOR.message_types_by_name['PredictionReply'] = _PREDICTIONREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PredictionRequest = _reflection.GeneratedProtocolMessageType('PredictionRequest', (_message.Message,), dict(
  DESCRIPTOR = _PREDICTIONREQUEST,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:PredictionRequest)
  ))
_sym_db.RegisterMessage(PredictionRequest)

PredictionReply = _reflection.GeneratedProtocolMessageType('PredictionReply', (_message.Message,), dict(
  DESCRIPTOR = _PREDICTIONREPLY,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:PredictionReply)
  ))
_sym_db.RegisterMessage(PredictionReply)



_PREDICTOR = _descriptor.ServiceDescriptor(
  name='Predictor',
  full_name='Predictor',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=128,
  serialized_end=190,
  methods=[
  _descriptor.MethodDescriptor(
    name='Predict',
    full_name='Predictor.Predict',
    index=0,
    containing_service=None,
    input_type=_PREDICTIONREQUEST,
    output_type=_PREDICTIONREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PREDICTOR)

DESCRIPTOR.services_by_name['Predictor'] = _PREDICTOR

# @@protoc_insertion_point(module_scope)
