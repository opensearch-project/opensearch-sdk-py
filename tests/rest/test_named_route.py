#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.rest.named_route import NamedRoute
from opensearch_sdk_py.rest.rest_method import RestMethod


class TestNamedRoute(unittest.TestCase):
    def test_named_route(self) -> None:
        nr = NamedRoute(method=RestMethod.GET, path="/test", unique_name="testing")
        self.assertEqual(nr.method, RestMethod.GET)
        self.assertEqual(nr.path, "/test")
        self.assertEqual(nr.unique_name, "testing")
        self.assertEqual(str(nr), "GET /test testing")
