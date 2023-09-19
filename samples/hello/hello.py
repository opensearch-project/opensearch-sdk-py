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

from hello_extension import HelloExtension

from opensearch_sdk_py.actions.internal.discovery_extensions_request_handler import DiscoveryExtensionsRequestHandler
from opensearch_sdk_py.actions.internal.request_error_handler import RequestErrorHandler
from opensearch_sdk_py.actions.request_handlers import RequestHandlers
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.server.async_host import AsyncHost
from opensearch_sdk_py.transport.acknowledged_response import AcknowledgedResponse
from opensearch_sdk_py.transport.initialize_extension_response import InitializeExtensionResponse
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.tcp_header import TcpHeader


class HelloExtensionHost(AsyncHost):
    def on_input(self, input: StreamInput) -> StreamOutput:
        request_handlers = RequestHandlers()
        header = TcpHeader().read_from(input)
        logging.debug(f"< {header}")

        if header.is_request:
            request: OutboundMessageRequest = OutboundMessageRequest().read_from(input, header)
            logging.info(f"< {request}")
            if request.action in request_handlers:
                output = request_handlers.handle(request, input)
            else:
                output = RequestErrorHandler(status=RestStatus.NOT_FOUND, content_type=ExtensionRestResponse.JSON_CONTENT_TYPE, content=bytes(f'{{"error": "No handler found for {request.method.name} {request.path}"}}', "utf-8")).handle(
                    request, input
                )
        else:
            response = OutboundMessageResponse().read_from(input, header)
            # TODO: Error handling
            if response.is_error:
                output = None
                logging.warn(f"< error {header}")
            else:
                ack_response = AcknowledgedResponse().read_from(input)
                logging.debug(f"< response {response}, {ack_response}")
                output = StreamOutput()
                response = OutboundMessageResponse(
                    response.thread_context_struct,
                    response.features,
                    InitializeExtensionResponse("hello-world", ["Extension", "ActionExtension"]),
                    response.version,
                    DiscoveryExtensionsRequestHandler.init_response_request_id,
                    response.is_handshake,
                    response.is_compress,
                )
                response.write_to(output)
                logging.info(f"> {response}")
        return output


logging.basicConfig(encoding="utf-8", level=logging.INFO)

# TODO We should pass this instance to the SDK and SDK should execute the code below
extension = HelloExtension()
logging.info(f"Starting {extension} that implements {extension.implemented_interfaces}.")

host = HelloExtensionHost()
host.run()
