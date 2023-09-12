#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.api.action_extension import ActionExtension
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.named_route import NamedRoute
from opensearch_sdk_py.rest.rest_method import RestMethod


class TestActionExtension(unittest.TestCase):
    class MyHelloRestHandler(ExtensionRestHandler):
        def handle_request(self, rest_request: ExtensionRestRequest) -> ExtensionRestResponse:
            pass

        @property
        def routes(self) -> list[NamedRoute]:
            return [NamedRoute(method=RestMethod.GET, path="/route", unique_name="unique")]

    class MyActionExtension(Extension, ActionExtension):
        @property
        def rest_handlers(self) -> list[ExtensionRestHandler]:
            return [TestActionExtension.MyHelloRestHandler()]

    def setUp(self) -> None:
        self._extension = TestActionExtension.MyActionExtension()
        return super().setUp()

    def test_implemented_interfaces(self) -> None:
        self.assertListEqual(self._extension.implemented_interfaces, ["Extension", "ActionExtension"])
