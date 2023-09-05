
from handlers.transport_handler import TransportHandler

from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.discovery_node_role import DiscoveryNodeRole
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import (
    OutboundMessageResponse,
)
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_address import TransportAddress
from opensearch_sdk_py.transport.transport_handshaker_handshake_request import (
    TransportHandshakerHandshakeRequest,
)
from opensearch_sdk_py.transport.transport_handshaker_handshake_response import (
    TransportHandshakerHandshakeResponse,
)
from opensearch_sdk_py.transport.transport_service_handshake_request import (
    TransportServiceHandshakeRequest,
)
from opensearch_sdk_py.transport.transport_service_handshake_response import (
    TransportServiceHandshakeResponse,
)


class HandshakeHandler():

    @staticmethod
    def handle_tcp_handshake(request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        tcp_handshake = TransportHandshakerHandshakeRequest().read_from(
            input
        )
        print(f"\topensearch_version: {tcp_handshake.version}")
        print("\tparsed TCP handshake, returning a response")

        return TransportHandler.send_response(OutboundMessageResponse(
            request.thread_context_struct,
            request.features,
            TransportHandshakerHandshakeResponse(request.get_version()),
            request.get_version(),
            request.get_request_id(),
            request.is_handshake(),
            request.is_compress(),
        ))

    @staticmethod
    def handle_transport_handshake(request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        transport_handshake = TransportServiceHandshakeRequest().read_from(
            input
        )
        print(f"\ttask_id: {transport_handshake.parent_task_id}")
        print("\tparsed Transport handshake, returning a response")

        return TransportHandler.send_response(OutboundMessageResponse(
            request.thread_context_struct,
            request.features,
            TransportServiceHandshakeResponse(
                DiscoveryNode(
                    node_name="hello-world",
                    node_id="hello-world",
                    address=TransportAddress("127.0.0.1", 1234),
                    roles={
                        DiscoveryNodeRole.CLUSTER_MANAGER_ROLE,
                        DiscoveryNodeRole.DATA_ROLE,
                        DiscoveryNodeRole.INGEST_ROLE,
                        DiscoveryNodeRole.REMOTE_CLUSTER_CLIENT_ROLE,
                    },
                )
            ),
            request.get_version(),
            request.get_request_id(),
            request.is_handshake(),
            request.is_compress(),
        ))
