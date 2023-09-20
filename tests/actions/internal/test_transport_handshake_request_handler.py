#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.actions.internal.transport_handshake_request_handler import TransportHandshakeRequestHandler
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_service_handshake_request import TransportServiceHandshakeRequest
from opensearch_sdk_py.transport.transport_service_handshake_response import TransportServiceHandshakeResponse
from opensearch_sdk_py.transport.version import Version


class TestTransportHandshakeRequestHandler(unittest.TestCase):
    class MyExtension(Extension):
        def __init__(self) -> None:
            super().__init__("test-extension")

    def setUp(self) -> None:
        self.extension = TestTransportHandshakeRequestHandler.MyExtension()

    def test_transport_handhsake_request_handler(self) -> None:
        test_output = StreamOutput()
        OutboundMessageRequest(
            message=TransportServiceHandshakeRequest(),
            version=Version(Version.CURRENT),
        ).write_to(test_output)
        test_input = StreamInput(test_output.getvalue())

        omr = OutboundMessageRequest()
        omr.read_from(test_input)
        thrh = TransportHandshakeRequestHandler(self.extension)
        output = thrh.handle(omr, test_input)

        input = StreamInput(output.getvalue())
        response = OutboundMessageResponse()
        response.read_from(input)
        message = TransportServiceHandshakeResponse()
        message.read_from(input)
        self.assertIsInstance(message.discovery_node, DiscoveryNode)
        self.assertEqual(message.cluster_name, "")
        self.assertEqual(message.version.id, Version.CURRENT_ID)
