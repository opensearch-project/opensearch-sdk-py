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
    # TODO, probably should be a constant elsewhere
    current_version_id = Version(3000099).id
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

                    # Standard response header and variable header, need to refactor from here to the interesting part
                    # TODO: this should probably be a default size in the TcpHeader constructor or a constant or both
                    message_length = TcpHeader.HEADER_SIZE - TcpHeader.MARKER_BYTES_SIZE - TcpHeader.MESSAGE_LENGTH_SIZE
                    response_header = TcpHeader(request_id=header.request_id, status=header.status, size=message_length, version=header.version)
                    response_header.set_response()
                    
                    variable_header = StreamOutput()
                    # These bytes are the context maps
                    variable_header.write_byte(0)
                    variable_header.write_byte(0)
                    # No features on a response

                    # Here's the interesting part of this response.
                    writeable_data = StreamOutput()
                    # Version.CURRENT
                    writeable_data.write_v_int(current_version_id)
                    
                    # Interesting part complete, back to math to assemble the pieces
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
                    print(f"\tparsed TCP handshake, OpenSearch {os_version}, returning a response")
                    print(f"\nsent handshake response, {len(raw_out)} byte(s):\n\t#{raw_out}\n\t{response_header}")
                    
                    await loop.sock_sendall(conn, output.getvalue())
                elif action == 'internal:transport/handshake':
                    # No writeable data for this request action, we just send a response

                    # Standard response header and variable header, need to refactor from here to the interesting part
                    # TODO: this should probably be a default size in the TcpHeader constructor or a constant or both
                    message_length = TcpHeader.HEADER_SIZE - TcpHeader.MARKER_BYTES_SIZE - TcpHeader.MESSAGE_LENGTH_SIZE
                    response_header = TcpHeader(request_id=header.request_id, status=header.status, size=message_length, version=header.version)
                    response_header.set_response()
                    
                    variable_header = StreamOutput()
                    # These bytes are the context maps
                    variable_header.write_byte(0)
                    variable_header.write_byte(0)
                    # No features on a response

                    # Here's the interesting part of this response.
                    writeable_data = StreamOutput()
                    # OptionalWriteable(DiscoveryNode)
                    writeable_data.write_boolean(True) # optional is present
                    # TODO: Refactor to an object
                    # Begin DiscoveryNode object
                    writeable_data.write_string("hello-world");
                    writeable_data.write_string("nodeId");
                    writeable_data.write_string("ephemeralId");
                    writeable_data.write_string("127.0.0.1"); # hostName
                    writeable_data.write_string("127.0.0.1"); # hostAddress
                    # TODO: Refactor to an object
                    # Begin TransportAddress object
                    writeable_data.write_byte(4) # IP address has 4 bytes
                    writeable_data.write_byte(127) # The address
                    writeable_data.write_byte(0)
                    writeable_data.write_byte(0)
                    writeable_data.write_byte(1)
                    writeable_data.write_string("127.0.0.1"); # address.getHostString
                    writeable_data.write_int(1234) # The port
                    # End TransportAddress object
                    # Write attributes map: VInt size and key value string pairs
                    writeable_data.write_v_int(0) # Empty attributes map
                    # for att in range(): write_string(key), write_string(value)
                    # Write roles. Vint size and triplets with name, abbr, canContainData
                    writeable_data.write_v_int(4) 
                    writeable_data.write_string("cluster_manager")
                    writeable_data.write_string("m")
                    writeable_data.write_boolean(False)
                    writeable_data.write_string("data")
                    writeable_data.write_string("d")
                    writeable_data.write_boolean(True)
                    writeable_data.write_string("ingest")
                    writeable_data.write_string("i")
                    writeable_data.write_boolean(False)
                    writeable_data.write_string("remote_cluster_client")
                    writeable_data.write_string("r")
                    writeable_data.write_boolean(False)
                    # Version
                    writeable_data.write_v_int(current_version_id)
                    # End DiscoveryNode Object

                    # ClusterName
                    writeable_data.write_string("opensearch")

                    # Version.CURRENT
                    writeable_data.write_v_int(current_version_id)

                    # Interesting part complete, back to same math as before to assemble the pieces
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
                    print(f"\tparsed Transport handshake, returning a response")
                    print(f"\nsent handshake response, {len(raw_out)} byte(s):\n\t#{raw_out}\n\t{response_header}")
                    
                    await loop.sock_sendall(conn, output.getvalue())
                else:
                    print(f"\tparsed action {header}, haven't yet written what to do with it")
            else:
                print(f"\tparsed {header}, this is a response to something I sent, haven't yet written what to do with it")

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
