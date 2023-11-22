#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.transport.extension_transport_request import ExtensionTransportRequest
from opensearch_sdk_py.transport.request_type import RequestType
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestExtensionTransportRequest(unittest.TestCase):
    def test_extension_transport_request(self) -> None:
        etr = ExtensionTransportRequest(RequestType.REQUEST_EXTENSION_ENVIRONMENT_SETTINGS, "test")
        self.assertEqual(etr.er.requestType, RequestType.REQUEST_EXTENSION_ENVIRONMENT_SETTINGS.value)
        self.assertEqual(etr.er.identity.uniqueId, "test")

        out = StreamOutput()
        etr.write_to(out)
        etr = ExtensionTransportRequest(RequestType.GET_SETTINGS)
        self.assertEqual(etr.er.requestType, RequestType.GET_SETTINGS.value)
        self.assertEqual(etr.er.identity.uniqueId, "")
        etr.read_from(input=StreamInput(out.getvalue()))
        self.assertEqual(etr.er.requestType, RequestType.REQUEST_EXTENSION_ENVIRONMENT_SETTINGS.value)
        self.assertEqual(etr.er.identity.uniqueId, "test")

    def test_extension_transport_request_no_id(self) -> None:
        etr = ExtensionTransportRequest(RequestType.REQUEST_EXTENSION_ENVIRONMENT_SETTINGS)
        self.assertEqual(etr.er.requestType, RequestType.REQUEST_EXTENSION_ENVIRONMENT_SETTINGS.value)
        self.assertEqual(etr.er.identity.uniqueId, "")

        out = StreamOutput()
        etr.write_to(out)
        etr = ExtensionTransportRequest(RequestType.GET_SETTINGS)
        self.assertEqual(etr.er.requestType, RequestType.GET_SETTINGS.value)
        self.assertEqual(etr.er.identity.uniqueId, "")
        etr.read_from(input=StreamInput(out.getvalue()))
        self.assertEqual(etr.er.requestType, RequestType.REQUEST_EXTENSION_ENVIRONMENT_SETTINGS.value)
        self.assertEqual(etr.er.identity.uniqueId, "")
