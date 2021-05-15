import logging
import os
import signal
import sys
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from app.protos import hello_pb2, hello_pb2_grpc

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)
root_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class HelloService(hello_pb2_grpc.HelloService):
    def hello(
        self, request: hello_pb2.HelloRequest, context
    ) -> hello_pb2.HelloResponse:
        name = request.name
        return hello_pb2.HelloResponse(message=f"[gRPC] Welcome to {name}!")


def main():
    with open(os.path.join(root_directory, "mygrpc/keys/key.pem"), "rb") as f:
        private_key = f.read()
    with open(os.path.join(root_directory, "mygrpc/keys/cert.pem"), "rb") as f:
        certificate_chain = f.read()

    INSECURE_PORT = os.getenv("INSECURE_PORT", "0.0.0.0:8085")
    SECURE_PORT = os.getenv("INSECURE_PORT", "0.0.0.0:8085")
    server_credentials = grpc.ssl_server_credentials(
        ((private_key, certificate_chain),)
    )

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    SERVICE_NAMES = [h.service_name() for h in server._state.generic_handlers]
    SERVICE_NAMES.append(reflection.SERVICE_NAME)
    logger.debug(f"SERVICE_NAMES: {SERVICE_NAMES}")
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    # 不需要加密访问
    server.add_insecure_port(INSECURE_PORT)

    # 需要 cert.pem 才能访问
    server.add_secure_port(SECURE_PORT, server_credentials)

    server.start()

    def signal_term_handler(signal, frame):
        logger.warning("got SIGTERM begin")
        server.stop(60)
        logger.warning("got SIGTERM end")
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_term_handler)
    signal.signal(signal.SIGINT, signal_term_handler)

    logger.info("My Pid is %d", os.getpid())
    server.wait_for_termination()


if __name__ == "__main__":
    main()
