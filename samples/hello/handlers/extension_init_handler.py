
from handlers.transport_handler import TransportHandler

from opensearch_sdk_py.transport.acknowledged_response import AcknowledgedResponse
from opensearch_sdk_py.transport.initialize_extension_request import (
    InitializeExtensionRequest,
)
from opensearch_sdk_py.transport.initialize_extension_response import (
    InitializeExtensionResponse,
)
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import (
    OutboundMessageResponse,
)
from opensearch_sdk_py.transport.register_rest_actions_request import (
    RegisterRestActionsRequest,
)
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class ExtensionInitHandler():

    # TODO: replace this constant with auto-incremented value
    REGISTER_REST_REQUEST_ID = 101
    # TODO: make this private to this class
    init_response_request_id = -1

    @staticmethod
    def handle_init_request(request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        initialize_extension_request = (
            InitializeExtensionRequest().read_from(input)
        )
        print(
            f"\tsource node: {initialize_extension_request.source_node.address.host_name}"
            + f":{initialize_extension_request.source_node.address.port}"
            + f", extension {initialize_extension_request.extension.address.host_name}"
            + f":{initialize_extension_request.extension.address.port}"
        )
        print("\tparsed Init Request, returning REST registration request")

        # Sometime between tcp and transport handshakes and the eventual response,
        # the uniqueId gets added to the thread context.
        request.thread_context_struct.request_headers[
            "extension_unique_id"
        ] = "hello-world"

        # TODO: Other initialization, ideally async

        ExtensionInitHandler.init_response_request_id = request.get_request_id()

        return TransportHandler.send_request(OutboundMessageRequest(
            request.thread_context_struct,
            request.features,
            RegisterRestActionsRequest(
                "hello-world", ["GET /hello hw_greeting"]
            ),
            request.get_version(),
            "internal:discovery/registerrestactions",
            ExtensionInitHandler.REGISTER_REST_REQUEST_ID,
            False,
            False,
        ))

    @staticmethod
    def handle_register_rest_response(response: OutboundMessageResponse, input: StreamInput) -> StreamOutput:
        ack_response = AcknowledgedResponse().read_from(input)
        print(f"\trequest {response.get_request_id()} acknowledged: {ack_response.status}")
        print("\tparsed Acknowledged response for REST registration, returning init response")

        return TransportHandler.send_response(OutboundMessageResponse(
            response.thread_context_struct,
            response.features,
            InitializeExtensionResponse(
                "hello-world", ["Extension", "ActionExtension"]
            ),
            response.get_version(),
            ExtensionInitHandler.init_response_request_id,
            response.is_handshake(),
            response.is_compress(),
        ))
