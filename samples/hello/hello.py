#!/usr/bin/env python
import asyncio
import logging
import socket

from handlers.extension_init_handler import ExtensionInitHandler
from handlers.handshake_handler import HandshakeHandler
from handlers.transport_handler import TransportHandler

from opensearch_sdk_py.transport.outbound_message import OutboundMessage
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import (
    OutboundMessageResponse,
)
from opensearch_sdk_py.transport.stream_input import StreamInput


async def handle_connection(conn, loop):
    try:
        conn.setblocking(False)
        # out = StreamOutput(loop, conn)
        while raw := await loop.sock_recv(conn, 1024 * 10):
            input = StreamInput(raw)
            print(f"\nreceived {input}, {len(raw)} byte(s)\n\t#{str(raw)}")

            header = OutboundMessage().read_from(input)
            print(f"\t{header.tcp_header}")
            if (
                header.thread_context_struct.request_headers
                or header.thread_context_struct.response_headers
            ):
                print(f"\t{header.thread_context_struct}")

            if header.is_request():
                request = OutboundMessageRequest().read_from(input, header)
                if request.features:
                    print(f"\tfeatures: {request.features}")
                if request.action:
                    print(f"\taction: {request.action}")

                # TODO: Need a better way of matching these action names to their handlers
                if request.action == "internal:tcp/handshake":
                    output = HandshakeHandler.handle_tcp_handshake(request, input)
                    await loop.sock_sendall(conn, output.getvalue())
                elif request.action == "internal:transport/handshake":
                    output = HandshakeHandler.handle_transport_handshake(request, input)
                    await loop.sock_sendall(conn, output.getvalue())
                elif request.action == "internal:discovery/extensions":
                    output = ExtensionInitHandler.handle_init_request(request, input)
                    await loop.sock_sendall(conn, output.getvalue())
                else:
                    print(
                        f"\tparsed action {header.tcp_header}, haven't yet written what to do with it"
                    )
            else:
                response = OutboundMessageResponse().read_from(input, header)
                # TODO: Need to track pending request id's and their handlers
                if header.get_request_id() == TransportHandler.register_rest_request_id:
                    output = ExtensionInitHandler.handle_register_rest_response(response, input)
                    await loop.sock_sendall(conn, output.getvalue())
                else:
                    print(
                        f"\tparsed {header.tcp_header}, this is a response to something I haven't sent"
                    )

    except Exception as ex:
        logging.exception(ex)
    finally:
        conn.close()


async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 1234))
    server.setblocking(False)
    server.listen()

    loop = asyncio.get_event_loop()

    print(f"listening, {server}")
    while True:
        conn, _ = await loop.sock_accept(server)
        print(f"got a connection, {conn}")
        loop.create_task(handle_connection(conn, loop))


asyncio.run(run_server())
