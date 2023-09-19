#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import logging
from typing import Dict

from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse


class ExtensionRestHandlers(Dict[str, ExtensionRestHandler]):
    named_routes: list[str]

    def __init__(self) -> None:
        self.named_routes = []
        super().__init__()

    def register(self, klass: ExtensionRestHandler) -> None:
        logging.info(f"Registering {klass}")
        for route in klass.routes:
            # for matching the handler on the extension side only method and path matter
            self[route.key] = klass
            # but we have to send the full named route to OpenSearch
            self.named_routes.append(str(route))

    def handle(self, route: str, request: ExtensionRestRequest) -> ExtensionRestResponse:
        return self[route].handle_request(request)
