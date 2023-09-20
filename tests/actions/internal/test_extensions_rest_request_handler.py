#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest
from unittest.mock import patch

from mock import MagicMock

from opensearch_sdk_py.actions.internal.extension_rest_request_handler import ExtensionRestRequestHandler
from opensearch_sdk_py.api.action_extension import ActionExtension
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.http_version import HttpVersion
from opensearch_sdk_py.rest.rest_execute_on_extension_response import RestExecuteOnExtensionResponse
from opensearch_sdk_py.rest.rest_method import RestMethod
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.version import Version


class TestExtensionsRestRequestHandler(unittest.TestCase):
    class MyExtension(Extension, ActionExtension):
        def __init__(self) -> None:
            Extension.__init__(self, "hello-world")
            ActionExtension.__init__(self)

    def setUp(self) -> None:
        self.extension = TestExtensionsRestRequestHandler.MyExtension()

    @patch("opensearch_sdk_py.rest.extension_rest_handlers.ExtensionRestHandlers.handle")
    def test_extension_rest_request_handler(self, mock_handle: MagicMock) -> None:
        mock_handle.return_value = ExtensionRestResponse(
            status=RestStatus.OK,
            content=b"test",
            content_type=ExtensionRestResponse.TEXT_CONTENT_TYPE,
        )

        test_output = StreamOutput()
        OutboundMessageRequest(
            message=ExtensionRestRequest(
                method=RestMethod.GET,
                path="/test",
                http_version=HttpVersion.HTTP_1_1,
            ),
            version=Version(Version.CURRENT),
        ).write_to(test_output)
        test_input = StreamInput(test_output.getvalue())

        omr = OutboundMessageRequest()
        omr.read_from(test_input)
        errh = ExtensionRestRequestHandler(self.extension)
        output = errh.handle(omr, test_input)

        input = StreamInput(output.getvalue())
        response = OutboundMessageResponse()
        response.read_from(input)
        message = RestExecuteOnExtensionResponse()
        message.read_from(input)
        self.assertEqual(RestStatus.OK, message.status)
        self.assertEqual(ExtensionRestResponse.TEXT_CONTENT_TYPE, message.content_type)
        self.assertIn("test", str(message.content, "utf-8"))
