#!/usr/bin/env python
#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import asyncio
import logging
import socket
from typing import Any

from opensearch_sdk_py.actions.internal.discovery_extensions_request_handler import DiscoveryExtensionsRequestHandler
from opensearch_sdk_py.actions.request_handlers import RequestHandlers
from opensearch_sdk_py.transport.acknowledged_response import AcknowledgedResponse
from opensearch_sdk_py.transport.initialize_extension_response import InitializeExtensionResponse
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.tcp_header import TcpHeader


async def handle_connection(conn: Any, loop: asyncio.AbstractEventLoop) -> None:
    try:
        conn.setblocking(False)

        while raw := await loop.sock_recv(conn, 1024 * 10):
            input = StreamInput(raw)
            logging.debug(f"< #{str(raw)}, size={len(raw)} byte(s)")

            header = TcpHeader().read_from(input)
            logging.debug(f"< {header}")

            if header.is_request():
                request = OutboundMessageRequest().read_from(input, header)
                logging.info(f"< {request}")
                output = RequestHandlers().handle(request, input)
                if output is None:
                    logging.warn(f"< unhandled {header}")
            else:
                response = OutboundMessageResponse().read_from(input, header)
                # TODO: Error handling
                if response.is_error():
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
                        response.get_version(),
                        DiscoveryExtensionsRequestHandler.init_response_request_id,
                        response.is_handshake(),
                        response.is_compress(),
                    )
                    response.write_to(output)
                    logging.info(f"> {response}")

            if output:
                await loop.sock_sendall(conn, output.getvalue())

    except Exception as ex:
        logging.exception(ex)
    finally:
        conn.close()


async def run_server() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 1234))
    server.setblocking(False)
    server.listen()

    loop = asyncio.get_event_loop()

    logging.info(f"< server={server}")
    while True:
        conn, _ = await loop.sock_accept(server)
        logging.debug(f"< connection={conn}")
        loop.create_task(handle_connection(conn, loop))


logging.basicConfig(encoding="utf-8", level=logging.INFO)
asyncio.run(run_server())
