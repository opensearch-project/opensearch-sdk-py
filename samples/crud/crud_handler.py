#!/usr/bin/env python
#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import json
import logging

from opensearchpy import OpenSearch

from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.named_route import NamedRoute
from opensearch_sdk_py.rest.rest_method import RestMethod
from opensearch_sdk_py.rest.rest_status import RestStatus

logging.basicConfig(encoding="utf-8", level=logging.INFO)


class CRUDRestHandler(ExtensionRestHandler):
    def __init__(self) -> None:
        self.client = OpenSearch(hosts=[{"host": "localhost", "port": 9200}], http_auth=("admin", "admin"), use_ssl=False, verify_certs=False, ssl_show_warn=False)  # For testing only. Don't store credentials in code.

    def handle_request(self, request: ExtensionRestRequest) -> ExtensionRestResponse:
        logging.info(f"handling {request}")
        logging.info(f"request method: {request.method}")

        if request.method == RestMethod.POST:
            # Create a document
            index_name = "test-index"
            document = request.content()
            response = self.client.index(index=index_name, body=document, refresh=True)
            response_bytes = bytes(json.dumps(response).encode("utf-8"))
            return ExtensionRestResponse(request, RestStatus.OK, response_bytes, ExtensionRestResponse.JSON_CONTENT_TYPE)

        elif request.method == RestMethod.GET:
            # Search for documents
            index_name = "test-index"
            q = request.param("q")

            query = {"size": 5, "query": {"multi_match": {"query": q, "fields": ["title^2", "director"]}}}
            response = self.client.search(body=query, index=index_name)
            response_bytes = bytes(json.dumps(response).encode("utf-8"))
            return ExtensionRestResponse(request, RestStatus.OK, response_bytes, ExtensionRestResponse.JSON_CONTENT_TYPE)

        elif request.method == RestMethod.PUT:
            # Update a document
            index_name = "test-index"
            id = request.param("id")
            document = request.content()
            response = self.client.index(index=index_name, body=document, id=id, refresh=True)
            response_bytes = bytes(json.dumps(response), "utf-8")
            return ExtensionRestResponse(request, RestStatus.OK, response_bytes, ExtensionRestResponse.JSON_CONTENT_TYPE)

        elif request.method == RestMethod.DELETE:
            # Delete a document
            index_name = "test-index"
            id = request.param("id")
            response = self.client.delete(index=index_name, id=id)
            response_bytes = bytes(json.dumps(response), "utf-8")
            logging.info(f"response: {response}")
            return ExtensionRestResponse(request, RestStatus.OK, response_bytes, ExtensionRestResponse.JSON_CONTENT_TYPE)

        else:
            return ExtensionRestResponse(RestStatus.NOT_FOUND, bytes("Not found", "utf-8"), ExtensionRestResponse.TEXT_CONTENT_TYPE)

    @property
    def routes(self) -> list[NamedRoute]:
        return [
            NamedRoute(method=RestMethod.POST, path="/crud", unique_name="crud_post"),
            NamedRoute(method=RestMethod.GET, path="/crud", unique_name="crud_get"),
            NamedRoute(method=RestMethod.PUT, path="/crud", unique_name="crud_put"),
            NamedRoute(method=RestMethod.DELETE, path="/crud", unique_name="crud_delete"),
        ]
