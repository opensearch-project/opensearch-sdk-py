#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.protobuf import RegisterRestActionsProto_pb2


class TestRegisterRestActionsProto_pb2(unittest.TestCase):
    def test_register_rest_actions(self) -> None:
        actions = RegisterRestActionsProto_pb2.RegisterRestActions()
        actions.identity.uniqueId = "test"
        actions.restActions[:] = ["foo", "bar"]
        actions.deprecatedRestActions[:] = ["baz", "qux"]
        serialized_str = actions.SerializeToString()

        parsed_actions = RegisterRestActionsProto_pb2.RegisterRestActions()
        parsed_actions.ParseFromString(serialized_str)
        self.assertEqual(parsed_actions.identity.uniqueId, actions.identity.uniqueId)
        self.assertEqual(parsed_actions.restActions, actions.restActions)
        self.assertEqual(parsed_actions.deprecatedRestActions, actions.deprecatedRestActions)
