#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import logging

from opensearch_sdk_py.actions.request_handler import RequestHandler
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.rest_execute_on_extension_response import RestExecuteOnExtensionResponse
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class ExtensionRestRequestHandler(RequestHandler):
    def __init__(self) -> None:
        super().__init__("internal:extensions/restexecuteonextensiontaction")

    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        extension_rest_request = ExtensionRestRequest().read_from(input)
        logging.info(f"\tmethod: {extension_rest_request.method}, path: {extension_rest_request.path}")
        logging.info("\tparsed REST Request, returning REST response")

        response_bytes = bytes("Hello from Python!", "utf-8")
        response_bytes += b"\x20\xf0\x9f\x91\x8b"

        return self.send(
            OutboundMessageResponse(
                request.thread_context_struct,
                request.features,
                RestExecuteOnExtensionResponse(RestStatus.OK, "text/html; charset=utf-8", response_bytes),
                request.get_version(),
                request.get_request_id(),
                request.is_handshake(),
                request.is_compress(),
            )
        )
