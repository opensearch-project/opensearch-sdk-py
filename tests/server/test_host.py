#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.server.host import Host


class TestHost(unittest.TestCase):
    class MyHost(Host):
        def run(self) -> None:
            pass

    def test_init(self) -> None:
        host = TestHost.MyHost()
        self.assertEqual(host.address, "localhost")
        self.assertIsNone(host.port)
