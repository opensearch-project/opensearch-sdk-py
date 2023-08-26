#!/usr/bin/env python
import logging
import asyncio, socket

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.task_id import TaskId
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

            # Thread Context written for both request and response
            request_headers = input.read_string_to_string_dict()
            if len(request_headers):
                print(f"\trequest headers: {request_headers}")

            response_headers = input.read_string_to_string_array_dict()
            if len(response_headers):
                print(f"\tresponse headers: {response_headers}")

            # Features and actions only written for requests
            if header.is_request():
                features = input.read_string_array()
                if len(features):
                    print(f"\tfeatures: {features}")

                action = input.read_string()
                print(f"\taction: {action}")

                task_id = TaskId()
                task_id.read_from(input)

                # TODO: need a better system of handling all these actions
                # The additional bytes read inside this conditional are Writeables based on the specific request
                if action == 'internal:tcp/handshake':
                    # Writeable data for this action is a BytesReference of length 4
                    data = input.read_bytes(input.read_array_size())
                    # Internally this is a vint 0xa38eb741 -> 3000099 ^ MASK                    
                    os_version_int = StreamInput(data).read_v_int() ^ Version.MASK
                    os_version = Version(os_version_int)

                    message_length = TcpHeader.HEADER_SIZE - TcpHeader.MARKER_BYTES_SIZE - TcpHeader.MESSAGE_LENGTH_SIZE
                    response_header = TcpHeader(request_id=header.request_id, status=header.status, size=message_length, version=header.version)
                    response_header.set_response()
                    
                    variable_header = StreamOutput()
                    # These bytes are the context maps
                    variable_header.write_byte(0)
                    variable_header.write_byte(0)
                    # No features on a response

                    writeable_data = StreamOutput()
                    # This is written last without any length bit
                    writeable_data.write_v_int(Version(os_version_int).id)
                    
                    variable_bytes = variable_header.getvalue()
                    response_header.variable_header_size = len(variable_bytes)
                    response_header.size += response_header.variable_header_size

                    writeable_bytes = writeable_data.getvalue()
                    response_header.size += len(writeable_bytes)

                    output = StreamOutput()
                    response_header.write_to(output)
                    output.write(variable_bytes)
                    output.write(writeable_bytes)
                                        
                    raw_out = output.getvalue()
                    print(f"\tparsed TCP handshake, OpenSearch {os_version}, returning a response, {len(raw_out)} byte(s):\n\t#{raw_out}\n\t{response_header}")
                    
                    await loop.sock_sendall(conn, output.getvalue())
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
