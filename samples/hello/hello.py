#!/usr/bin/env python
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
            logging.info("")
            logging.info(f"received {input}, {len(raw)} byte(s)\n  #{str(raw)}")

            header = TcpHeader().read_from(input)
            logging.info(f"\t{header}")

            if header.is_request():
                request = OutboundMessageRequest().read_from(input, header)
                if request.thread_context_struct and request.thread_context_struct.request_headers:
                    logging.info(f"\t{request.thread_context_struct}")
                if request.features:
                    logging.info(f"\tfeatures: {request.features}")
                if request.action:
                    logging.info(f"\taction: {request.action}")

                output = RequestHandlers().handle(request, input)
                if output is None:
                    logging.info(
                        f"\tparsed action {header}, haven't yet written what to do with it"
                    )
            else:
                response = OutboundMessageResponse().read_from(input, header)
                # TODO: Error handling
                if response.is_error():
                    output = None
                    logging.info(
                        f"\tparsed {header}, this is an ERROR response"
                    )
                else:
                    ack_response = AcknowledgedResponse().read_from(input)
                    logging.info(f"\trequest {response.get_request_id()} acknowledged: {ack_response.status}")
                    logging.info("\tparsed Acknowledged response for REST registration, returning init response")
                    output = StreamOutput()
                    message = OutboundMessageResponse(
                        response.thread_context_struct,
                        response.features,
                        InitializeExtensionResponse(
                            "hello-world", ["Extension", "ActionExtension"]
                        ),
                        response.get_version(),
                        DiscoveryExtensionsRequestHandler.init_response_request_id,
                        response.is_handshake(),
                        response.is_compress(),
                    )
                    message.write_to(output)
                    logging.info(f"sent request id {message.get_request_id()}, {len(output.getvalue())} byte(s):\n  #{output}\n  {message.tcp_header}")

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

    logging.info(f"listening, {server}")
    while True:
        conn, _ = await loop.sock_accept(server)
        logging.info(f"got a connection, {conn}")
        loop.create_task(handle_connection(conn, loop))

logging.basicConfig(encoding='utf-8', level=logging.INFO)
asyncio.run(run_server())
