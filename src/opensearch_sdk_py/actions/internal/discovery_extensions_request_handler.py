#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import logging

from opensearch_sdk_py.actions.internal.register_rest_actions_response_handler import RegisterRestActionsResponseHandler
from opensearch_sdk_py.actions.request_handler import RequestHandler
from opensearch_sdk_py.actions.response_handlers import ResponseHandlers
from opensearch_sdk_py.api.action_extension import ActionExtension
from opensearch_sdk_py.transport.initialize_extension_request import InitializeExtensionRequest
from opensearch_sdk_py.transport.initialize_extension_response import InitializeExtensionResponse
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.register_rest_actions_request import RegisterRestActionsRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class DiscoveryExtensionsRequestHandler(RequestHandler):
    def __init__(self, extension: ActionExtension, response_handlers: ResponseHandlers) -> None:
        super().__init__("internal:discovery/extensions", extension)
        self.response_handlers = response_handlers

    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        initialize_extension_request = InitializeExtensionRequest().read_from(input)
        logging.debug(f"< {initialize_extension_request}")

        # Create the response message preserving the request id, but don't send it yet.
        # This will be sent when response handler calls send()
        self.response = OutboundMessageResponse(
            request.thread_context_struct,
            request.features,
            InitializeExtensionResponse(self.extension.name, self.extension.implemented_interfaces),
            request.version,
            request.request_id,
            request.is_handshake,
            request.is_compress,
        )

        # Sometime between tcp and transport handshakes and the eventual response,
        # the uniqueId gets added to the thread context.
        # request.thread_context_struct.request_headers["extension_unique_id"] = self.extension.name

        # Now send our own initialization requests.

        # Create the request, this gets us an auto-increment request id
        register_request = OutboundMessageRequest(
            thread_context=request.thread_context_struct,
            features=request.features,
            message=RegisterRestActionsRequest(self.extension.name, self.extension.named_routes),
            version=request.version,
            action="internal:discovery/registerrestactions",
            is_handshake=False,
            is_compress=False,
        )
        # Register response handler to handle this request ID invoking this class's send()
        register_response_handler = RegisterRestActionsResponseHandler(self)
        self.response_handlers.register(register_request.request_id, register_response_handler)
        # Now send the request
        return register_response_handler.send(register_request)
