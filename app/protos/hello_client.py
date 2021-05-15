import logging
import os

import grpc
from opencensus.ext.grpc import client_interceptor

from app.protos import hello_pb2, hello_pb2_grpc
from app.protos.utils.client_interceptor import GrpcClientInterceptor

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

root_directory = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


def get_channel(target: str, is_secure: bool = True) -> grpc.Channel:
    interceptors = [
        GrpcClientInterceptor(),
        client_interceptor.OpenCensusClientInterceptor(host_port=target),
    ]
    if is_secure:
        with open(os.path.join(root_directory, "mygrpc/keys/cert.pem"), "rb") as f:
            trusted_certs = f.read()
        credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        options = (("grpc.ssl_target_name_override", "grpc.seekplum.top"),)
        secure_channel = grpc.secure_channel(
            target=target, credentials=credentials, options=options
        )
        return grpc.intercept_channel(secure_channel, *interceptors)
    return grpc.intercept_channel(grpc.insecure_channel(target), *interceptors)


def main() -> None:
    target = os.getenv("CHANNEL_SERVER_TARGET", "0.0.0.0:8085")
    is_secure = os.getenv("CHANNEL_SERVER_SECURE", "") == "tls"
    channel = get_channel(
        target=target,
        is_secure=is_secure,
    )
    stub = hello_pb2_grpc.HelloServiceStub(channel)
    prefix = "TLS" if is_secure else ""
    response = stub.hello(hello_pb2.HelloRequest(name=f"{prefix} python-test123"))
    logger.warning(response.message)


if __name__ == "__main__":
    main()
