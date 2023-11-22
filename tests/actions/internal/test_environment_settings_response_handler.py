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

from opensearch_sdk_py.actions.internal.environment_settings_response_handler import EnvironmentSettingsResponseHandler
from opensearch_sdk_py.actions.response_handler import ResponseHandler
from opensearch_sdk_py.settings.settings import Settings
from opensearch_sdk_py.transport.environment_settings_response import EnvironmentSettingsResponse
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.version import Version


class TestEnvironmentSettingsResponseHandler(unittest.TestCase):
    def test_environment_settings_response_handler(self) -> None:
        settings = Settings({"foo": "bar"})
        input = StreamInput(bytes(OutboundMessageRequest(version=Version(2100099), message=EnvironmentSettingsResponse(settings))))
        omr = OutboundMessageRequest().read_from(input)
        next_handler = FakeResponseHandler()
        output = EnvironmentSettingsResponseHandler(next_handler).handle(omr, input)
        self.assertEqual(output, b"test")


class FakeResponseHandler(ResponseHandler):
    def handle(self, input: StreamInput = None) -> Optional[bytes]:
        pass

    def send(self) -> StreamOutput:
        return b"test"
