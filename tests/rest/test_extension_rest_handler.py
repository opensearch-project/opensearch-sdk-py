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
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.rest_status import RestStatus


class TestExtensionRestHandler(unittest.TestCase):
    def test_default_handler(self) -> None:
        handler = DefaultRestHandler()
        self.assertEqual(len(handler.routes), 0)


class DefaultRestHandler(ExtensionRestHandler):
    def handle_request(self, rest_request: ExtensionRestRequest) -> ExtensionRestResponse:
        return ExtensionRestResponse(status=RestStatus.NOT_IMPLEMENTED)
