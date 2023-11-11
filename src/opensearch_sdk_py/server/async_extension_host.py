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

from opensearch_sdk_py.actions.internal.action_not_found_request_error_handler import ActionNotFoundRequestErrorHandler
from opensearch_sdk_py.actions.internal.discovery_extensions_request_handler import DiscoveryExtensionsRequestHandler
from opensearch_sdk_py.actions.internal.extension_rest_request_handler import ExtensionRestRequestHandler
from opensearch_sdk_py.actions.internal.tcp_handshake_request_handler import TcpHandshakeRequestHandler
from opensearch_sdk_py.actions.internal.transport_handshake_request_handler import TransportHandshakeRequestHandler
from opensearch_sdk_py.actions.request_handlers import RequestHandlers
from opensearch_sdk_py.actions.response_handlers import ResponseHandlers
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.server.async_host import AsyncHost
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.tcp_header import TcpHeader


class AsyncExtensionHost(AsyncHost):
    response_handlers: ResponseHandlers
    request_handlers: RequestHandlers

    def __init_response_handlers(self) -> None:
        self.response_handlers = ResponseHandlers(self.extension)

    def __init_request_handlers(self) -> None:
        self.request_handlers = RequestHandlers(self.extension)
        self.request_handlers.register(DiscoveryExtensionsRequestHandler(self.extension, self.response_handlers))
        self.request_handlers.register(ExtensionRestRequestHandler(self.extension))
        self.request_handlers.register(TcpHandshakeRequestHandler(self.extension))
        self.request_handlers.register(TransportHandshakeRequestHandler(self.extension))

    def serve(self, extension: Extension) -> None:
        self.extension = extension
        self.__init_response_handlers()
        self.__init_request_handlers()

    def on_input(self, input: StreamInput) -> StreamOutput:
        header = TcpHeader().read_from(input)
        logging.debug(f"< {header}")

        if header.is_request:
            request: OutboundMessageRequest = OutboundMessageRequest().read_from(input, header)
            logging.info(f"< {request}")
            output = self.request_handlers.handle(request, input)
            if output is None:
                output = ActionNotFoundRequestErrorHandler(self.extension, request).handle(request, input)
        else:
            response: OutboundMessageResponse = OutboundMessageResponse().read_from(input, header)
            if response.is_error:
                # TODO: Error handling
                output = None
                logging.warning(f"< error {header}")
            else:
                logging.info(f"< response {response}")
                output = self.response_handlers.handle(response, input)
                if output is None:  # pragma: no cover
                    # TODO: Error handling
                    logging.warning(f"< response id {response.request_id} not registered")
        return output
