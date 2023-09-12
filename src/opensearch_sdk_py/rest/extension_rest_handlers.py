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
    _singleton = None
    _named_routes: list[str] = []

    def __new__(cls):  # type:ignore
        if cls._singleton is None:
            cls._singleton = super(ExtensionRestHandlers, cls).__new__(cls)
        return cls._singleton

    @classmethod
    def __reset__(self) -> None:
        self._singleton = None
        self._named_routes = []

    def register(self, klass: ExtensionRestHandler) -> None:
        logging.info(f"Registering {klass}")
        for route in klass.routes:
            # for matching the handler on the extension side only method and path matter
            self[route.key] = klass
            # but we have to send the full named route to OpenSearch
            self._named_routes.append(str(route))

    @property
    def named_routes(self) -> list[str]:
        return self._named_routes

    def handle(self, route: str, request: ExtensionRestRequest) -> ExtensionRestResponse:
        handler = self[route]
        # TODO error response if no handler found (handler is None)
        return getattr(handler, "handle_request")(request)
