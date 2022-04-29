# -*- coding: utf-8 -*-
import grpc
from hello_pb2_grpc import HelloServiceServicer, add_HelloServiceServicer_to_server
from hello_pb2 import HelloResponse
import concurrent.futures as futures
import hello_pb2
# from grpc_reflection.v1alpha import reflection
import logging


class Service(HelloServiceServicer):
    def hello(self, request, context):
        print("received messsage header:", context.invocation_metadata())
        first_name = request.firstName
        last_name = request.lastName
        return HelloResponse(greeting="hi, {} {}!".format(first_name, last_name))


class MyUnaryServerInterceptor1(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        print("Interceptor：Start----1")
        respn = continuation(handler_call_details)
        print("Interceptor：End----2", respn)
        return respn


if __name__ == '__main__':
    import os
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=6565, help="server port")
    os.environ["GRPC_VERBOSITY"] = "debug"
    args = parser.parse_args()
    port = args.port
    with open("./key_file/certificate.pem", "rb") as f:
        cert = f.read()
    with open("./key_file/cert.key", "rb") as f:
        key = f.read()

    server_credential = grpc.ssl_server_credentials(((key, cert),))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1), interceptors=[MyUnaryServerInterceptor1()])
    add_HelloServiceServicer_to_server(Service(), server)

    server.add_secure_port("[::]:{}".format(port), server_credential)
    server.start()
    print("server start @ {}".format(port))
    logging.basicConfig()
    server.wait_for_termination()
