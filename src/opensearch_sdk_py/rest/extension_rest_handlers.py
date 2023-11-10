#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import fnmatch
import logging
import re
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
            # The route path (part of route.key) may contain a named wildcard such as /foo/{bar}
            # which will assign a user value to the param bar. In this class we'll save thie wildcard
            key = re.sub(r"\{(.+?)\}", "*", route.key)
            if key in self:
                raise Exception(f"Can not register {route.key}, {key} is already registered.")

            # for matching the handler on the extension side only method and wildcard path matter
            self[key] = klass
            # but we have to send the full named route to OpenSearch
            self.named_routes.append(str(route))

    def handle(self, route: str, request: ExtensionRestRequest) -> ExtensionRestResponse:
        # first attempt exact match without substitution
        if route in self:
            return self[route].handle_request(request)
        # if no match try wildcard match
        for key in self.keys():
            if fnmatch.fnmatch(route, key):
                return self[key].handle_request(request)
        # no match, we shouldn't get here if registration worked
        raise Exception(f"Can not find a matching route for {route}.")
