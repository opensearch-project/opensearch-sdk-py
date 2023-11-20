#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.protobuf import ExtensionRequestProto_pb2
from opensearch_sdk_py.transport.request_type import RequestType


class TestExtensionRequestProto_pb2(unittest.TestCase):
    def test_extension_request(self) -> None:
        request = ExtensionRequestProto_pb2.ExtensionRequest()
        request.requestType = RequestType.GET_SETTINGS.value
        request.identity.uniqueId = "test"
        serialized_str = request.SerializeToString()

        parsed_request = ExtensionRequestProto_pb2.ExtensionRequest()
        parsed_request.ParseFromString(serialized_str)
        self.assertEqual(parsed_request.requestType, RequestType.GET_SETTINGS.value)
        self.assertEqual(parsed_request.identity.uniqueId, "test")

    def test_extension_request_no_id(self) -> None:
        request = ExtensionRequestProto_pb2.ExtensionRequest()
        request.requestType = RequestType.GET_SETTINGS.value
        serialized_str = request.SerializeToString()

        parsed_request = ExtensionRequestProto_pb2.ExtensionRequest()
        parsed_request.ParseFromString(serialized_str)
        self.assertEqual(parsed_request.requestType, RequestType.GET_SETTINGS.value)
        self.assertEqual(parsed_request.identity.uniqueId, "")
