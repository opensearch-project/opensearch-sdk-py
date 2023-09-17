#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.protobuf import ExtensionIdentityProto_pb2


class TestExtensionIdentityProto_pb2(unittest.TestCase):
    def test_identity(self) -> None:
        identity = ExtensionIdentityProto_pb2.ExtensionIdentity()
        identity.uniqueId = "test"
        serialized_str = identity.SerializeToString()

        parsed_identity = ExtensionIdentityProto_pb2.ExtensionIdentity()
        parsed_identity.ParseFromString(serialized_str)
        self.assertEqual(parsed_identity.uniqueId, identity.uniqueId)
