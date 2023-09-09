#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler
from opensearch_sdk_py.rest.extension_rest_handlers import ExtensionRestHandlers
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.named_route import NamedRoute
from opensearch_sdk_py.rest.rest_method import RestMethod


class TestExtensionRestHandlers(unittest.TestCase):
    def test_registers_handler(self) -> None:
        handlers = ExtensionRestHandlers()
        handlers.register(FakeRestHandler())
        self.assertEqual(len(ExtensionRestHandlers()), 2)
        self.assertIsInstance(ExtensionRestHandlers()["GET /foo"], FakeRestHandler)
        self.assertIsInstance(ExtensionRestHandlers()["GET /bar"], FakeRestHandler)
        self.assertListEqual(ExtensionRestHandlers().named_routes(), ["GET /foo get_foo", "GET /bar get_bar"])


class FakeRestHandler(ExtensionRestHandler):
    def __init__(self) -> None:
        super().__init__()

    def handle_request(self, rest_request: ExtensionRestRequest) -> ExtensionRestResponse:
        pass

    def routes(self) -> list[NamedRoute]:
        return [NamedRoute(RestMethod.GET, "/foo", "get_foo"), NamedRoute(RestMethod.GET, "/bar", "get_bar")]
