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
from opensearch_sdk_py.rest.rest_status import RestStatus


class TestExtensionRestHandlers(unittest.TestCase):
    class FakeRestHandler(ExtensionRestHandler):
        def handle_request(self, rest_request: ExtensionRestRequest) -> ExtensionRestResponse:
            return ExtensionRestResponse(status=RestStatus.NOT_IMPLEMENTED)

        @property
        def routes(self) -> list[NamedRoute]:
            return [NamedRoute(RestMethod.GET, "/foo", "get_foo"), NamedRoute(RestMethod.GET, "/bar/{foo}", "get_bar")]

    class DoubleFakeRestHandler(ExtensionRestHandler):
        def handle_request(self, rest_request: ExtensionRestRequest) -> ExtensionRestResponse:
            return ExtensionRestResponse(status=RestStatus.NOT_IMPLEMENTED)

        @property
        def routes(self) -> list[NamedRoute]:
            return [NamedRoute(RestMethod.GET, "/bar/{baz}", "get_baz")]

    def test_registers_handler(self) -> None:
        handlers = ExtensionRestHandlers()
        handlers.register(TestExtensionRestHandlers.FakeRestHandler())
        self.assertEqual(len(handlers), 2)
        self.assertIsInstance(handlers["GET /foo"], TestExtensionRestHandlers.FakeRestHandler)
        self.assertIsInstance(handlers["GET /bar/*"], TestExtensionRestHandlers.FakeRestHandler)
        self.assertListEqual(handlers.named_routes, ["GET /foo get_foo", "GET /bar/{foo} get_bar"])

        response = handlers.handle("GET /foo", ExtensionRestRequest())
        self.assertEqual(response.status, RestStatus.NOT_IMPLEMENTED)

        response = handlers.handle("GET /bar/anything", ExtensionRestRequest())
        self.assertEqual(response.status, RestStatus.NOT_IMPLEMENTED)

        error = r"Can not find a matching route for GET /baz."
        self.assertRaisesRegex(Exception, error, handlers.handle, "GET /baz", ExtensionRestRequest)
        error = r"Can not register GET /bar/{baz}, GET /bar/\* is already registered."
        self.assertRaisesRegex(Exception, error, handlers.register, TestExtensionRestHandlers.DoubleFakeRestHandler())
