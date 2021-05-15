import collections

import grpc


class _ClientCallDetails(
    collections.namedtuple(
        "_ClientCallDetails", ("method", "timeout", "metadata", "credentials")
    ),
    grpc.ClientCallDetails,
):
    pass


class GrpcClientInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):
    def new_client_call_details(self, client_call_details):
        return _ClientCallDetails(
            client_call_details.method,
            5.0 if client_call_details.timeout is None else client_call_details.timeout,
            ()
            if client_call_details.metadata is None
            else client_call_details.metadata,
            client_call_details.credentials,
        )

    def intercept_unary_unary(self, continuation, client_call_details, request):
        return continuation(self.new_client_call_details(client_call_details), request)

    def intercept_unary_stream(self, continuation, client_call_details, request):
        return continuation(self.new_client_call_details(client_call_details), request)

    def intercept_stream_unary(
        self, continuation, client_call_details, request_iterator
    ):
        return continuation(
            self.new_client_call_details(client_call_details), request_iterator
        )

    def intercept_stream_stream(
        self, continuation, client_call_details, request_iterator
    ):
        return continuation(
            self.new_client_call_details(client_call_details), request_iterator
        )
