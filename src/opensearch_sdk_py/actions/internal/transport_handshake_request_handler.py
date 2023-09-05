import logging

from opensearch_sdk_py.actions.request_handler import RequestHandler
from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.discovery_node_role import DiscoveryNodeRole
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.transport_address import TransportAddress
from opensearch_sdk_py.transport.transport_service_handshake_request import TransportServiceHandshakeRequest
from opensearch_sdk_py.transport.transport_service_handshake_response import TransportServiceHandshakeResponse


class TransportHandshakeRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__("internal:transport/handshake")

    def handle(self, request: OutboundMessageRequest, input: StreamInput):
        transport_handshake = TransportServiceHandshakeRequest().read_from(input)
        logging.info(f"\ttask_id: {transport_handshake.parent_task_id}")
        logging.info("\tparsed Transport handshake, returning a response")

        return self.send(OutboundMessageResponse(
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
