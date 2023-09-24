#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.actions.internal.discovery_extensions_request_handler import DiscoveryExtensionsRequestHandler
from opensearch_sdk_py.actions.internal.extension_rest_request_handler import ExtensionRestRequestHandler
from opensearch_sdk_py.actions.internal.tcp_handshake_request_handler import TcpHandshakeRequestHandler
from opensearch_sdk_py.actions.internal.transport_handshake_request_handler import TransportHandshakeRequestHandler
from opensearch_sdk_py.actions.request_handlers import RequestHandlers
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from tests.transport.data.netty_trace_data import NettyTraceData


class TestRequestHandlers(unittest.TestCase):
    class MyExtension(Extension):
        def __init__(self) -> None:
            super().__init__("test-extension")

    def setUp(self) -> None:
        self.extension = TestRequestHandlers.MyExtension()
        self.request_handlers = RequestHandlers(self.extension)
        self.request_handlers.register(DiscoveryExtensionsRequestHandler(self.extension, None))
        self.request_handlers.register(ExtensionRestRequestHandler(self.extension))
        self.request_handlers.register(TcpHandshakeRequestHandler(self.extension))
        self.request_handlers.register(TransportHandshakeRequestHandler(self.extension))

    def test_register_handlers(self) -> None:
        self.assertEqual(len(self.request_handlers), 4)
        self.assertIsInstance(self.request_handlers["internal:tcp/handshake"], TcpHandshakeRequestHandler)

    def test_handle(self) -> None:
        data = NettyTraceData.load("tests/transport/data/tcp_handshake.txt").data
        input = StreamInput(data)
        request = OutboundMessageRequest().read_from(input)
        output = self.request_handlers.handle(request, input)
        self.assertIsInstance(output, StreamOutput)
