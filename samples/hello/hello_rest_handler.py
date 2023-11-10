#!/usr/bin/env python
#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import logging

from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.named_route import NamedRoute
from opensearch_sdk_py.rest.rest_method import RestMethod
from opensearch_sdk_py.rest.rest_status import RestStatus


class HelloRestHandler(ExtensionRestHandler):
    def handle_request(self, rest_request: ExtensionRestRequest) -> ExtensionRestResponse:
        logging.debug(f"handling {rest_request}")
        consumed_params = list[str]()
        if "name" in rest_request.params:
            name = rest_request.params["name"]
            consumed_params.append("name")
            response_bytes = bytes(f"Hello {name}! 👋\n", "utf-8")
        else:
            response_bytes = bytes("Hello from Python! 👋\n", "utf-8")
        return ExtensionRestResponse(RestStatus.OK, response_bytes, ExtensionRestResponse.TEXT_CONTENT_TYPE, consumed_params=consumed_params)

    @property
    def routes(self) -> list[NamedRoute]:
        return [NamedRoute(method=RestMethod.GET, path="/hello", unique_name="greeting"), NamedRoute(method=RestMethod.GET, path="/hello/{name}", unique_name="personal_greeting")]
