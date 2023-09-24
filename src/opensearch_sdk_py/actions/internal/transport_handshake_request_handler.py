#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import logging

from opensearch_sdk_py.actions.request_handler import RequestHandler
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.discovery_node_role import DiscoveryNodeRole
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_address import TransportAddress
from opensearch_sdk_py.transport.transport_service_handshake_request import TransportServiceHandshakeRequest
from opensearch_sdk_py.transport.transport_service_handshake_response import TransportServiceHandshakeResponse


class TransportHandshakeRequestHandler(RequestHandler):
    def __init__(self, extension: Extension) -> None:
        super().__init__("internal:transport/handshake", extension)

    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        transport_handshake = TransportServiceHandshakeRequest().read_from(input)
        logging.debug(f"< {transport_handshake}")

        self.response = OutboundMessageResponse(
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
            request.version,
            request.request_id,
            request.is_handshake,
            request.is_compress,
        )
        return self.send()
