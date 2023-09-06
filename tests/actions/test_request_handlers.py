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
from opensearch_sdk_py.actions.request_handlers import RequestHandlers
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from tests.transport.data.netty_trace_data import NettyTraceData


class TestRequestHandlers(unittest.TestCase):
    def test_registers_handler(self) -> None:
        self.assertEqual(len(RequestHandlers()), 4)
        self.assertIsInstance(RequestHandlers()["internal:tcp/handshake"], TcpHandshakeRequestHandler)

    def test_handle(self) -> None:
        data = NettyTraceData.load("tests/transport/data/tcp_handshake.txt").data
        input = StreamInput(data)
        request = OutboundMessageRequest().read_from(input)
        output = RequestHandlers().handle(request, input)
        self.assertIsInstance(output, StreamOutput)
