
from handlers.transport_handler import TransportHandler

from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.rest_execute_on_extension_response import (
    RestExecuteOnExtensionResponse,
)
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import (
    OutboundMessageResponse,
)
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class ExtensionRestRequestHandler():

    @staticmethod
    def handle_rest_request(request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        extension_rest_request = (
            ExtensionRestRequest().read_from(input)
        )
        print(
            f"\tmethod: {extension_rest_request.method}, path: {extension_rest_request.path}"
        )
        print("\tparsed REST Request, returning REST response")

        response_bytes = bytes("Hello from Python!", "utf-8")
        response_bytes += b"\x20\xf0\x9f\x91\x8b"

        return TransportHandler.send_response(OutboundMessageResponse(
            request.thread_context_struct,
            request.features,
            RestExecuteOnExtensionResponse(
                RestStatus.OK,
                "text/html; charset=utf-8",
                response_bytes
            ),
            request.get_version(),
            request.get_request_id(),
            request.is_handshake(),
            request.is_compress(),
        ))
