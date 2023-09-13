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

from opensearch_sdk_py.actions.request_handler import RequestHandler
from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.rest_execute_on_extension_response import RestExecuteOnExtensionResponse
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


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
        if route in self:
            return getattr(self[route], "handle_request")(request)
        return ErrorHandler(status=RestStatus.NOT_FOUND, content_type=ExtensionRestResponse.JSON_CONTENT_TYPE, content=bytes(f'{{"error": "No handler found for {request.method.name} {request.path}"}}', "utf-8"))


class ErrorHandler(RequestHandler):
    def __init__(
        self,
        status: RestStatus,
        content: bytes,
        content_type: str,
    ):
        self.status = status
        self.content = content
        self.content_type = content_type

    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        self.send(
            OutboundMessageResponse(
                request.thread_context_struct,
                request.features,
                RestExecuteOnExtensionResponse(
                    status=self.status,
                    content_type=self.content_type,
                    content=self.content,
                ),
                request.version,
                request.request_id,
                request.is_handshake,
                request.is_compress,
            )
        )
