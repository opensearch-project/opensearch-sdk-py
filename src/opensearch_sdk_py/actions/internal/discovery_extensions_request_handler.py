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
from opensearch_sdk_py.rest.extension_rest_handlers import ExtensionRestHandlers
from opensearch_sdk_py.transport.initialize_extension_request import InitializeExtensionRequest
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.register_rest_actions_request import RegisterRestActionsRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class DiscoveryExtensionsRequestHandler(RequestHandler):
    # TODO: make this private to this class
    init_response_request_id = None

    def __init__(self) -> None:
        super().__init__("internal:discovery/extensions")

    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        initialize_extension_request = InitializeExtensionRequest().read_from(input)
        logging.debug(f"< {initialize_extension_request}")

        # Sometime between tcp and transport handshakes and the eventual response,
        # the uniqueId gets added to the thread context.
        request.thread_context_struct.request_headers["extension_unique_id"] = "hello-world"

        # TODO: Other initialization, ideally async
        DiscoveryExtensionsRequestHandler.init_response_request_id = request.request_id

        return self.send(
            OutboundMessageRequest(
                thread_context=request.thread_context_struct,
                features=request.features,
                message=RegisterRestActionsRequest("hello-world", ExtensionRestHandlers().named_routes()),
                version=request.version,
                action="internal:discovery/registerrestactions",
                is_handshake=False,
                is_compress=False,
            )
        )
