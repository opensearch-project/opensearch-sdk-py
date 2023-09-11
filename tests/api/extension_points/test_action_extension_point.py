#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.api.extension_points.action_extension_point import ActionExtensionPoint
from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.named_route import NamedRoute
from opensearch_sdk_py.rest.rest_method import RestMethod


class TestActionExtensionPoint(unittest.TestCase):
    class MyHelloRestHandler(ExtensionRestHandler):
        def handle_request(self, rest_request: ExtensionRestRequest) -> ExtensionRestResponse:
            pass

        @property
        def routes(self) -> list[NamedRoute]:
            return [NamedRoute(method=RestMethod.GET, path="/route", unique_name="unique")]

    class MyActionExtensionPoint(ActionExtensionPoint):
        def __init__(self) -> None:
            super().__init__([TestActionExtensionPoint.MyHelloRestHandler()])

    # TODO: get rid of the singleton in ExtensionRestHandlers()

    # def setUp(self) -> None:
    #     self._extension_point = TestActionExtensionPoint.MyActionExtensionPoint()
    #     return super().setUp()

    # def test_implemented_interfaces(self):
    #     self.assertListEqual(self._extension_point.implemented_interfaces, ["ActionExtension"])
