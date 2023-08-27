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

            # TODO: Refactor TcpHeader reading into NetworkMessage class
            header = TcpHeader()
            header.read_from(input)
            print(f"\t{header}")

            # TODO: Refactor headers into a ThreadContext class
            # TODO: Refactor Thread Context reading into OutboundMessage(NetworkMessage) class
            # Thread Context written for both request and response
            request_headers = input.read_string_to_string_dict()
            if len(request_headers):
                print(f"\trequest headers: {request_headers}")

            response_headers = input.read_string_to_string_array_dict()
            if len(response_headers):
                print(f"\tresponse headers: {response_headers}")

            # Features and actions only written for requests
            if header.is_request():
                # TODO: Refactor reading features and action name into Request(OutboundMessage) class
                # TODO: Also create a Response(OutboundMessage) class that doesn't read these
                features = input.read_string_array()
                if len(features):
                    print(f"\tfeatures: {features}")

                action = input.read_string()
                print(f"\taction: {action}")

                # TODO: We switch here from NetworkMessage subclasses to TransportMessage subclasses
                # Bytes read in NetworkMessage are added to both message and variable header length
                # Bytes read in TransportMessage are only added to message length

                # TODO: Create TransportMessage class
                # TODO: Refactor reading TaskId into TransportRequest(TransportMessage) class
                # TODO: Also have a TransportResponse(TransportMessage) class that doesn't read anything
                task_id = TaskId()
                task_id.read_from(input)

                # TODO: Need a better way of mathing these action names to reading their classes
                # The additional bytes read inside this conditional are Writeables based on the specific request
                if action == 'internal:tcp/handshake':
                    # TODO: refactor into HandshakeRequest class. Note OpenSearch has two HandshakeRequest classes.
                    # This one is o.o.transport.TransportHandshaker.HandshakeRequest. 
                    # It reads/writes vint vesrsion wrapped in BytesReference
                    # Other one is o.o.transport.HandshakeRequest used for internal:transport/handshake. 

                    # TODO, consider BytesReference reading in streaminput.  First read the size
                    # Note version as a writeable uses a vint, while version in TCP header is bigendian int
                    data = input.read_bytes(input.read_array_size())
                    # Internally this is a vint 0xa38eb741 -> 3000099 ^ MASK                    
                    os_version_int = StreamInput(data).read_v_int() ^ Version.MASK
                    os_version = Version(os_version_int)

                    # TODO: Here we end the reading of the request writeables (TransportMessage subclass)
                    # and begin creating a response (NetworkMessage subclass followed by TransportMessage subclass)

                    # Standard response header and variable header are part of NetworkMessage and subclasses
                    # TODO: This TcpHeader should probably be part of NetworkMessage class per earlier comment
                    # TODO: this length should probably be a default size in the TcpHeader constructor or a constant or both
                    message_length = TcpHeader.HEADER_SIZE - TcpHeader.MARKER_BYTES_SIZE - TcpHeader.MESSAGE_LENGTH_SIZE
                    response_header = TcpHeader(request_id=header.request_id, status=header.status, size=message_length, version=header.version)
                    response_header.set_response()
                    
                    # TODO: Variable header writing should be part of OutboundMessage class per earlier comment
                    variable_header = StreamOutput()
                    # These bytes are the context maps
                    # TODO: Refactor this by implementing writing the thread context 
                    variable_header.write_v_int(len(request_headers))
                    for key in request_headers:
                        variable_header.write_string(key)
                        variable_header.write_string(request_headers[key])
                    variable_header.write_v_int(len(response_headers))
                    for key in response_headers:
                        variable_header.write_string(key)
                        variable_header.write_string_array(response_headers[key])

                    # TODO: Here we switch from NetworkMessage subclass to TransportMessage subclass
                    # Bytes here don't count against variable header length but are added to total message length
                    writeable_data = StreamOutput()
                    # TODO: refactor into HandshakeResponse class. Note OpenSearch has two HandshakeResponse classes.
                    # This one is o.o.transport.TransportHandshaker.HandshakeResponse
                    # Unlike the request which wraps version in a BytesReference we just directly write vint
                    # Version.CURRENT
                    writeable_data.write_v_int(current_version_id)
                    
                    # Done with the NetworkMessage and TransportMessage

                    # TODO: Doing math here to set values in TCP header but this math should be refactored to be accounted for
                    # in the NetworkMessage (response & variable header) and TransportMessage (writeable bytes) classes
                    # Note we need to know the header lengths for the initial response header class before writing it to
                    # the overall stream. 
                    variable_bytes = variable_header.getvalue()
                    response_header.variable_header_size = len(variable_bytes)
                    response_header.size += response_header.variable_header_size

                    writeable_bytes = writeable_data.getvalue()
                    response_header.size += len(writeable_bytes)

                    # In OpenSearch these values are written by skipping the header in the stream and then going back
                    # to start of stream to write it. Here we just assemble the parts and write together at the end.
                    output = StreamOutput()
                    response_header.write_to(output)
                    output.write(variable_bytes)
                    output.write(writeable_bytes)
                                        
                    raw_out = output.getvalue()
                    print(f"\tparsed TCP handshake, OpenSearch {os_version}, returning a response")
                    print(f"\nsent handshake response, {len(raw_out)} byte(s):\n\t#{raw_out}\n\t{response_header}")
                    
                    await loop.sock_sendall(conn, output.getvalue())
                elif action == 'internal:transport/handshake':
                    # TODO: refactor into HandshakeRequest class. Note OpenSearch has two HandshakeRequest classes.
                    # This one is o.o.transport.HandshakeRequest. Doesn't read anything in.

                    # TODO: Here we end the reading of the request writeables (TransportMessage subclass)
                    # and begin creating a response (NetworkMessage subclass followed by TransportMessage subclass)

                    # Standard response header and variable header are part of NetworkMessage and subclasses
                    # Copied from above (obvious refactor candidate!)
                    message_length = TcpHeader.HEADER_SIZE - TcpHeader.MARKER_BYTES_SIZE - TcpHeader.MESSAGE_LENGTH_SIZE
                    response_header = TcpHeader(request_id=header.request_id, status=header.status, size=message_length, version=header.version)
                    response_header.set_response()
                    
                    variable_header = StreamOutput()
                    # These bytes are the context maps
                    # TODO: Refactor this by implementing writing the thread context 
                    variable_header.write_v_int(len(request_headers))
                    for key in request_headers:
                        variable_header.write_string(key)
                        variable_header.write_string(request_headers[key])
                    variable_header.write_v_int(len(response_headers))
                    for key in response_headers:
                        variable_header.write_string(key)
                        variable_header.write_string_array(response_headers[key])

                    # TODO: Here we switch from NetworkMessage subclass to TransportMessage subclass
                    # Bytes here don't count against variable header length but are added to total message length
                    writeable_data = StreamOutput()

                    # TODO: refactor into HandshakeResponse class. Note OpenSearch has two HandshakeResponse classes.
                    # This one is o.o.transport.HandshakeResponse
                    # It writes am (Optional) DiscoveryNode, ClusterName (wraps a string), and Version

                    # OptionalWriteable(DiscoveryNode)
                    writeable_data.write_boolean(True) # optional is present
                    # TODO: Refactor to a DiscoveryNode object. 
                    # The discovery_extension_node implies one was written but not committed
                    # Begin DiscoveryNode object
                    writeable_data.write_string("hello-world");
                    writeable_data.write_string("nodeId");
                    writeable_data.write_string("ephemeralId");
                    writeable_data.write_string("127.0.0.1"); # hostName
                    writeable_data.write_string("127.0.0.1"); # hostAddress
                    # TODO: Refactor to TransportAddress object. transport_address.py exists but needs the below code.
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

                    # Done with the NetworkMessage and TransportMessage

                    # Back to same math as before to assemble the pieces
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
                elif action == 'internal:discovery/extensions':
                    # TODO: implement InitializeExtensionRequest. Totally skipping reading the request 
                    # until we have the DiscoveryNode and DiscoveryExtensionNode classes
                    # we would also then send multiple requests to OpenSearch to implement extension points
                    # before sending a response.
                    # sometime between tcp and transport handshakes the uniqueId gets added to the thread context
                    # so adding that here so it will get added to response headers
                    request_headers['extension_unique_id'] = 'hello-world'

                    # for now other than that thread context, we will just send the response to make OpenSearch 
                    # happy that we initialized

                    # TODO: Here we end the reading of the request writeables (TransportMessage subclass)
                    # and begin creating a response (NetworkMessage subclass followed by TransportMessage subclass)

                    # Standard response header and variable header are part of NetworkMessage and subclasses
                    # TODO: This TcpHeader should probably be part of NetworkMessage class per earlier comment
                    # TODO: this length should probably be a default size in the TcpHeader constructor or a constant or both
                    message_length = TcpHeader.HEADER_SIZE - TcpHeader.MARKER_BYTES_SIZE - TcpHeader.MESSAGE_LENGTH_SIZE
                    response_header = TcpHeader(request_id=header.request_id, status=header.status, size=message_length, version=header.version)
                    response_header.set_response()

                    # TODO: Variable header writing should be part of OutboundMessage class per earlier comment
                    variable_header = StreamOutput()
                    # These bytes are the context maps
                    # TODO: Refactor this by implementing writing the thread context 
                    variable_header.write_v_int(len(request_headers))
                    for key in request_headers:
                        variable_header.write_string(key)
                        variable_header.write_string(request_headers[key])
                    variable_header.write_v_int(len(response_headers))
                    for key in response_headers:
                        variable_header.write_string(key)
                        variable_header.write_string_array(response_headers[key])

                    # TODO: Here we switch from NetworkMessage subclass to TransportMessage subclass
                    # Bytes here don't count against variable header length but are added to total message length
                    writeable_data = StreamOutput()
                    # TODO: refactor into InitializeExtensionResponse.
                    # Write a string extension name, and then string array of implemented interfaces
                    # Extension name comes from ExtensionSettings
                    writeable_data.write_string('hello-world')
                    # Implemented interfaces are collection of java class names
                    # TODO: Implement write string array in Stream Output
                    writeable_data.write_v_int(2)
                    writeable_data.write_string('Extension')
                    writeable_data.write_string('ActionExtension')
                    
                    # Done with the NetworkMessage and TransportMessage

                    # TODO: Doing math here to set values in TCP header but this math should be refactored to be accounted for
                    # in the NetworkMessage (response & variable header) and TransportMessage (writeable bytes) classes
                    # Note we need to know the header lengths for the initial response header class before writing it to
                    # the overall stream. 
                    variable_bytes = variable_header.getvalue()
                    response_header.variable_header_size = len(variable_bytes)
                    response_header.size += response_header.variable_header_size

                    writeable_bytes = writeable_data.getvalue()
                    response_header.size += len(writeable_bytes)

                    # In OpenSearch these values are written by skipping the header in the stream and then going back
                    # to start of stream to write it. Here we just assemble the parts and write together at the end.
                    output = StreamOutput()
                    response_header.write_to(output)
                    output.write(variable_bytes)
                    output.write(writeable_bytes)
                                        
                    raw_out = output.getvalue()
                    print(f"\tparsed Extension initialization request, returning a response")
                    print(f"\nsent init response, {len(raw_out)} byte(s):\n\t#{raw_out}\n\t{response_header}")

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
