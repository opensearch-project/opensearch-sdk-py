#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest
from typing import Optional

from opensearch_sdk_py.actions.internal.register_rest_actions_response_handler import RegisterRestActionsResponseHandler
from opensearch_sdk_py.actions.response_handler import ResponseHandler
from opensearch_sdk_py.transport.acknowledged_response import AcknowledgedResponse
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.version import Version


class TestRegisterRestActionsResponseHandler(unittest.TestCase):
    def test_register_rest_actions_response_handler(self) -> None:
        input = StreamInput(bytes(OutboundMessageRequest(version=Version(2100099), message=AcknowledgedResponse(status=True))))
        omr = OutboundMessageRequest().read_from(input)
        request = OutboundMessageRequest()
        next_handler = FakeResponseHandler()
        output = RegisterRestActionsResponseHandler(next_handler, request).handle(omr, input)
        self.assertEqual(output, b"test")

        input = StreamInput(bytes(OutboundMessageRequest(version=Version(2100099), message=AcknowledgedResponse(status=False))))
        omr = OutboundMessageRequest().read_from(input)
        output = RegisterRestActionsResponseHandler(next_handler, request).handle(omr, input)
        self.assertIsNone(output)


class FakeResponseHandler(ResponseHandler):
    def handle(self, request: OutboundMessageRequest, input: StreamInput = None) -> Optional[bytes]:
        pass

    def send(self, request: OutboundMessageRequest) -> StreamOutput:
        return b"test"
