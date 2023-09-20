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
from opensearch_sdk_py.api.action_extension import ActionExtension
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.rest_execute_on_extension_response import RestExecuteOnExtensionResponse
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class ExtensionRestRequestHandler(RequestHandler):
    def __init__(self, extension: ActionExtension) -> None:
        super().__init__("internal:extensions/restexecuteonextensiontaction", extension)

    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        extension_rest_request = ExtensionRestRequest().read_from(input)
        logging.debug(f"< {extension_rest_request}")

        route = f"{extension_rest_request.method.name} {extension_rest_request.path}"
        response = self.extension.handle(route, extension_rest_request)

        return self.send(
            OutboundMessageResponse(
                request.thread_context_struct,
                request.features,
                RestExecuteOnExtensionResponse(
                    status=response.status,
                    content_type=response.content_type,
                    content=response.content,
                    headers=response.headers,
                    consumed_params=response.consumed_params,
                    content_consumed=response.content_consumed,
                ),
                request.version,
                request.request_id,
                request.is_handshake,
                request.is_compress,
            )
        )
