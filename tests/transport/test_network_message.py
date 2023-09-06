#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.transport.network_message import NetworkMessage
from opensearch_sdk_py.transport.version import Version


class TestNetworkMessage(unittest.TestCase):
    def test_network_message(self) -> None:
        nm = NetworkMessage(version=Version(2100099), request_id=42)
        self.assertEqual(len(nm.thread_context_struct.request_headers), 0)
        self.assertEqual(len(nm.thread_context_struct.response_headers), 0)
        self.assertEqual(nm.request_id, 42)
        self.assertEqual(nm.version.id, 136317827)
        self.assertFalse(nm.is_request)
        self.assertTrue(nm.is_response)
        self.assertFalse(nm.is_error)
        self.assertFalse(nm.is_compress)
        self.assertFalse(nm.is_handshake)
