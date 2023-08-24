#!/usr/bin/env python
import logging
import asyncio, socket

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.tcp_header import TcpHeader
from opensearch_sdk_py.transport.version import Version
from opensearch_sdk_py.transport.handshake_request import HandshakeRequest
from opensearch_sdk_py.transport.handshake_response import HandshakeResponse

async def handle_connection(conn, loop):
    try:
        conn.setblocking(False)
        # out = StreamOutput(loop, conn)
        while raw := await loop.sock_recv(conn, 1024 * 10):
            # output = StreamOutput(loop, conn)
            input = StreamInput(raw)
            print(f"\nreceived {input}, {len(raw)} byte(s)\n\t#{str(raw)}")
            header = TcpHeader()
            header.read_from(input)
            print(f"\t{header}")

            # TODO: This is probably not correct, this is included in all request/response
            # with the only difference being the action, but it broke the "response handshake"
            if header.is_request():
                request_headers = input.read_string_to_string_dict()
                print(f"\trequest headers: {request_headers}")
                if len(request_headers):
                    print(f"\trequest headers: {request_headers}")

                response_headers = input.read_string_to_string_array_dict()
                print(f"\tresponse headers: {response_headers}")
                if len(response_headers):
                    print(f"\tresponse headers: {response_headers}")

            features = input.read_string_array()
            if len(features):
                print(f"\tfeatures: {features}")

            if header.is_request():
                action = input.read_string()
                print(f"\taction: {action}")
                # TODO: action is always followed by a null byte. 
                # Is read_string broken (are strings null terminated?)
                input.read_byte()

                # TODO: need a better system of handling all these actions
                # The additional bytes read inside this conditional are Writeables based on the specific request
                if action == 'internal:tcp/handshake':
                    # Writeable data for this action is a BytesReference of length 4 which parses to vint version
                    data_size = input.read_v_int()
                    data = input.read_bytes(data_size)
                    # 0xa38eb741 -> 3000099
                    # TODO: not sure I'm doing this right but it works, fix it or delete this comment :-)
                    os_version_input = StreamInput(data)
                    os_version_int = os_version_input.read_v_int()
                    os_version = Version(os_version_int)
                    print(f"\tparsed TCP handshake, OpenSearch {os_version}, should return a response with this version")
                    # output = StreamOutput()
                    # TODO: use setResponse on the status
                    # TODO: append headers and features (or 3 0-bytes for temp)
                    # TODO: add os_version_int to end
                    # TODO: correct the size and variable size values for the above changes
                    # response_header = TcpHeader(request_id=header.request_id, status=header.status, size=48, version=header.version)
                    # response_header.write_to(output)
                    # for i in range(8):
                    #     handshake_response = HandshakeResponse(version=header.version)
                    #     handshake_response.write_to(output)
                    # await loop.sock_sendall(conn, output.getvalue())
                    await loop.sock_sendall(conn, raw)
                else:
                    print(f"\tparsed action {header}, not sure what to do with it")
            elif header.is_handshake():
                await loop.sock_sendall(conn, raw)
            else:
                # just send back the same message
                # await loop.sock_sendall(conn, raw)
                print(f"\tparsed {header}, not sure what to do with it")

            # read the rest of the message
            # input.read_bytes(header.variable_header_size)

    except Exception as ex:
        logging.exception(ex)
    finally:
        conn.close()

async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1234))
    server.setblocking(False)
    server.listen()

    loop = asyncio.get_event_loop()

    print(f"listening, {server}")
    while True:
        conn, _ = await loop.sock_accept(server)
        print(f"got a connection, {conn}")
        loop.create_task(handle_connection(conn, loop))

asyncio.run(run_server())
