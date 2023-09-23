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
from opensearch_sdk_py.actions.response_handlers import ResponseHandlers
from opensearch_sdk_py.api.action_extension import ActionExtension
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from tests.transport.data.netty_trace_data import NettyTraceData


class TestDiscoveryExtensionsRequestHandler(unittest.TestCase):
    class MyExtension(Extension, ActionExtension):
        def __init__(self) -> None:
            Extension.__init__(self, "hello-world")
            ActionExtension.__init__(self)

        @property
        def rest_handlers(self) -> list[ExtensionRestHandler]:
            return []

    def setUp(self) -> None:
        self.extension = TestDiscoveryExtensionsRequestHandler.MyExtension()
        self.response_handlers = ResponseHandlers(self.extension)
        self.handler = DiscoveryExtensionsRequestHandler(self.extension, self.response_handlers)

    def test_init(self) -> None:
        self.assertEqual(self.handler.action, "internal:discovery/extensions")
        self.assertEqual(self.handler.extension, self.extension)

    def test_handle(self) -> None:
        data = NettyTraceData.load("tests/transport/data/initialize_extension_request.txt").data
        input = StreamInput(data)
        request = OutboundMessageRequest().read_from(input)
        output = self.handler.handle(request, input)
        self.assertIsInstance(output, StreamOutput)
        self.assertEqual(self.handler.response.request_id, 10)
