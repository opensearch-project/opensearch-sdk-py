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
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_handshaker_handshake_request import TransportHandshakerHandshakeRequest
from opensearch_sdk_py.transport.transport_handshaker_handshake_response import TransportHandshakerHandshakeResponse
from opensearch_sdk_py.transport.version import Version


class TcpHandshakeRequestHandler(RequestHandler):
    def __init__(self, extension: Extension) -> None:
        super().__init__("internal:tcp/handshake", extension)

    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        tcp_handshake = TransportHandshakerHandshakeRequest().read_from(input)
        logging.debug(f"< {tcp_handshake}")
        self.response = OutboundMessageResponse(
            request.thread_context_struct,
            request.features,
            TransportHandshakerHandshakeResponse(Version(Version.CURRENT)),
            Version(Version.MIN_COMPAT),
            request.request_id,
            request.is_handshake,
            request.is_compress,
        )
        return self.send()
