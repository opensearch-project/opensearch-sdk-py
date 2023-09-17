#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.actions.internal.tcp_handshake_request_handler import TcpHandshakeRequestHandler
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_handshaker_handshake_request import TransportHandshakerHandshakeRequest
from opensearch_sdk_py.transport.transport_handshaker_handshake_response import TransportHandshakerHandshakeResponse
from opensearch_sdk_py.transport.version import Version


class TestTcpHandshakeRequestHandler(unittest.TestCase):
    def test_tcp_handhsake_request_handler(self) -> None:
        test_output = StreamOutput()
        OutboundMessageRequest(
            message=TransportHandshakerHandshakeRequest(Version(Version.CURRENT)),
            version=Version(Version.CURRENT),
        ).write_to(test_output)
        test_input = StreamInput(test_output.getvalue())

        omr = OutboundMessageRequest()
        omr.read_from(test_input)
        thrh = TcpHandshakeRequestHandler()
        output = thrh.handle(omr, test_input)

        input = StreamInput(output.getvalue())
        response = OutboundMessageResponse()
        response.read_from(input)
        message = TransportHandshakerHandshakeResponse()
        message.read_from(input)
        self.assertEqual(message.version.id, Version.CURRENT_ID)
