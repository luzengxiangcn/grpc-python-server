# -*- coding: utf-8 -*-
import os

import grpc
from hello_pb2_grpc import HelloServiceStub
from hello_pb2 import HelloRequest
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=6565, help="server port")
os.environ["GRPC_VERBOSITY"] = "debug"
args = parser.parse_args()
port = args.port

with open("./key_file/certificate.pem", "rb") as f:
    cert = f.read()
credentials = grpc.ssl_channel_credentials(root_certificates=cert)
channel = grpc.secure_channel("[::]:{}".format(port), credentials,
                              options=(('grpc.ssl_target_name_override', "UNKNOWN",),
                                       ))
stub = HelloServiceStub(channel)

greeting = HelloRequest(firstName="Albertoimpl", lastName="Alberto C. Ríos")

response, call = stub.hello.with_call(
            greeting,
    metadata=(
        ('initial-metadata-1', 'The value should be str'),
        ('binary-metadata-bin',
         b'With -bin surffix, the value can be bytes'),
        ('accesstoken', 'gRPC Python is great')
    ))

print(response.greeting)
