# ENV
- PYTHON >=3.0
- pip install grpcio protobuf
- export GRPC_VERBOSITY=DEBUG

# RUN Server
- cd ./python
- python server.py --port 6565

# Client
- cd ./python
- python client.py --port 6565

# Experiment
## Experiment 1
### Procedure
- clone https://github.com/Albertoimpl/spring-cloud-gateway-grpc.git
- run:  ./gradlew :grpc-server:bootRun
- run: ./gradlew :grpc-simple-gateway:bootRun
- run: ./gradlew :grpc-client:bootRun

### result
java GRPC Server Warning:
'''
2022-04-29 11:16:38.683  WARN 42994 --- [-worker-ELG-3-1] i.g.n.s.i.grpc.netty.NettyServerHandler  : Expected header TE: trailers, but null is received. This means some intermediate proxy may not support trailers
'''

## Experiment 2
### Procedure
- kill grpc-server in Experiment1
- cd ./python
- python server.py --port 6565
- another Terminal
- cd ./python
- python client.py --port 8090


### result
python GRPC Server Warning:
'''
D0429 11:21:42.101369000 123145548849152 server.cc:1334]               Failed call creation: {"created":"@1651202502.101315000","description":"Missing :authority or :path","file":"src/core/lib/surface/server.cc","file_line":1384,"referenced_errors":[{"created":"@1651202502.100956000","description":"Failed processing incoming headers","file":"src/core/ext/filters/http/server/http_server_filter.cc","file_line":111,"referenced_errors":[{"created":"@1651202502.100952000","description":"Missing header","file":"src/core/ext/filters/http/server/http_server_filter.cc","file_line":160,"key":"te"}]}]}
'''

### other
You may test code:
- cd ./python
- python server.py --port 6566
- another Terminal
- cd ./python
- python client.py --port 6566