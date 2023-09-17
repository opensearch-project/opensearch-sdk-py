#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.actions.internal.request_error_handler import RequestErrorHandler
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.http_version import HttpVersion
from opensearch_sdk_py.rest.rest_execute_on_extension_response import RestExecuteOnExtensionResponse
from opensearch_sdk_py.rest.rest_method import RestMethod
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.version import Version


class TestRequestErrorHandler(unittest.TestCase):
    def test_request_error_handler(self) -> None:
        reh = RequestErrorHandler(status=RestStatus.NOT_FOUND, content_type=ExtensionRestResponse.JSON_CONTENT_TYPE, content=bytes('{{"error": "test"}}', "utf-8"))
        self.assertEqual(RestStatus.NOT_FOUND, reh.status)
        self.assertEqual(ExtensionRestResponse.JSON_CONTENT_TYPE, reh.content_type)
        self.assertEqual('{{"error": "test"}}', str(reh.content, "utf-8"))

        omr = OutboundMessageRequest(
            message=ExtensionRestRequest(
                method=RestMethod.GET,
                path="/test",
                http_version=HttpVersion.HTTP_1_1,
            ),
            version=Version(Version.CURRENT),
        )
        output = reh.handle(omr, None)

        input = StreamInput(output.getvalue())
        response = OutboundMessageResponse()
        response.read_from(input)
        message = RestExecuteOnExtensionResponse()
        message.read_from(input)
        self.assertEqual(RestStatus.NOT_FOUND, message.status)
        self.assertEqual(ExtensionRestResponse.JSON_CONTENT_TYPE, message.content_type)
        self.assertIn("test", str(message.content, "utf-8"))
