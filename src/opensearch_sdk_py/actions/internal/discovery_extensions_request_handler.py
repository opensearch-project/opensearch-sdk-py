#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import logging

from opensearch_sdk_py.actions.internal.environment_settings_response_handler import EnvironmentSettingsResponseHandler
from opensearch_sdk_py.actions.internal.register_rest_actions_response_handler import RegisterRestActionsResponseHandler
from opensearch_sdk_py.actions.request_handler import RequestHandler
from opensearch_sdk_py.actions.response_handlers import ResponseHandlers
from opensearch_sdk_py.api.action_extension import ActionExtension
from opensearch_sdk_py.transport.extension_transport_request import ExtensionTransportRequest
from opensearch_sdk_py.transport.initialize_extension_request import InitializeExtensionRequest
from opensearch_sdk_py.transport.initialize_extension_response import InitializeExtensionResponse
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.register_rest_actions_request import RegisterRestActionsRequest
from opensearch_sdk_py.transport.request_type import RequestType
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class DiscoveryExtensionsRequestHandler(RequestHandler):
    def __init__(self, extension: ActionExtension, response_handlers: ResponseHandlers) -> None:
        super().__init__("internal:discovery/extensions", extension)
        self.response_handlers = response_handlers

    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        initialize_extension_request = InitializeExtensionRequest().read_from(input)
        logging.debug(f"< {initialize_extension_request}")

        # We will stack requests/responses, generating them in the reverse order that we send them
        # Order of sending:  resgister rest actions, then environment settings request, then init response
        # Order of generating: init response, environment settings request, register rest actions

        # Final Init Response to this init request, preserving the request ID
        self.response = OutboundMessageResponse(
            request.thread_context_struct,
            request.features,
            InitializeExtensionResponse(self.extension.name, self.extension.implemented_interfaces),
            request.version,
            request.request_id,
            request.is_handshake,
            request.is_compress,
        )

        # Stack the Environment Settings request/response, chained to the above init response
        settings_request = OutboundMessageRequest(
            thread_context=request.thread_context_struct,
            features=request.features,
            message=ExtensionTransportRequest(RequestType.REQUEST_EXTENSION_ENVIRONMENT_SETTINGS),
            version=request.version,
            action="internal:discovery/enviornmentsettings",
        )
        settings_response_handler = EnvironmentSettingsResponseHandler(self)
        self.response_handlers.register(settings_request.request_id, settings_response_handler)

        # Stack the Register Rest request/response, chained to the above env settings request
        register_request = OutboundMessageRequest(
            thread_context=request.thread_context_struct,
            features=request.features,
            message=RegisterRestActionsRequest(self.extension.name, self.extension.named_routes),
            version=request.version,
            action="internal:discovery/registerrestactions",
        )
        register_response_handler = RegisterRestActionsResponseHandler(settings_response_handler, settings_request)
        self.response_handlers.register(register_request.request_id, register_response_handler)

        # Now send the request at top of stack
        return register_response_handler.send(register_request)
