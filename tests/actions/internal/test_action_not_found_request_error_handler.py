#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.actions.internal.action_not_found_request_error_handler import ActionNotFoundRequestErrorHandler
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.version import Version


class TestActionNotFoundRequestHandler(unittest.TestCase):
    class MyExtension(Extension):
        def __init__(self) -> None:
            super().__init__("hello-world")

    def setUp(self) -> None:
        self.extension = TestActionNotFoundRequestHandler.MyExtension()
        self.request = OutboundMessageRequest(version=Version(2100099), request_id=42, action="internal:invalid")
        self.handler = ActionNotFoundRequestErrorHandler(self.extension, self.request)

    def test_init(self) -> None:
        self.assertEqual(self.handler.action, "internal:error")
        self.assertEqual(self.handler.status, RestStatus.NOT_FOUND)
        self.assertEqual(self.handler.content_type, ExtensionRestResponse.JSON_CONTENT_TYPE)
        self.assertEqual(self.handler.content, b'{"error": "No handler found for internal:invalid"}')
        self.assertEqual(self.handler.extension, self.extension)

    def test_handle(self) -> None:
        response = self.handler.handle(self.request, None)
        message = OutboundMessageResponse().read_from(StreamInput(response.getvalue()))
        self.assertEqual(message.request_id, self.request.request_id)
        self.assertEqual(message.message_bytes, None)
