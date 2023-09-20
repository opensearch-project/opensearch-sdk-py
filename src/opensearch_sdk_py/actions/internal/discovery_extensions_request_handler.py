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
from opensearch_sdk_py.transport.initialize_extension_request import InitializeExtensionRequest
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.register_rest_actions_request import RegisterRestActionsRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class DiscoveryExtensionsRequestHandler(RequestHandler):
    def __init__(self, extension: ActionExtension) -> None:
        super().__init__("internal:discovery/extensions", extension)

    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        initialize_extension_request = InitializeExtensionRequest().read_from(input)
        logging.debug(f"< {initialize_extension_request}")

        # Sometime between tcp and transport handshakes and the eventual response,
        # the uniqueId gets added to the thread context.
        # request.thread_context_struct.request_headers["extension_unique_id"] = self.extension.name
        self.extension.init_response_request_id = request.request_id

        return self.send(
            OutboundMessageRequest(
                thread_context=request.thread_context_struct,
                features=request.features,
                message=RegisterRestActionsRequest(self.extension.name, self.extension.named_routes),
                version=request.version,
                action="internal:discovery/registerrestactions",
                is_handshake=False,
                is_compress=False,
            )
        )
