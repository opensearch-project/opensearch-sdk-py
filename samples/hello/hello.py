#!/usr/bin/env python
import logging
import asyncio, socket

from opensearch_sdk_py.transport.outbound_message import OutboundMessage
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.task_id import TaskId
from opensearch_sdk_py.transport.tcp_header import TcpHeader
from opensearch_sdk_py.transport.transport_handshaker_handshake_request import TransportHandshakerHandshakeRequest
from opensearch_sdk_py.transport.transport_service_handshake_request import TransportServiceHandshakeRequest
from opensearch_sdk_py.transport.transport_status import TransportStatus
from opensearch_sdk_py.transport.version import Version
from opensearch_sdk_py.transport.handshake_request import HandshakeRequest
from opensearch_sdk_py.transport.handshake_response import HandshakeResponse
from opensearch_sdk_py.transport.transport_address import TransportAddress

async def handle_connection(conn, loop):
    try:
        conn.setblocking(False)
        # out = StreamOutput(loop, conn)
        while raw := await loop.sock_recv(conn, 1024 * 10):
            input = StreamInput(raw)
            print(f"\nreceived {input}, {len(raw)} byte(s)\n\t#{str(raw)}")

            # Quick check on request vs. response
            is_request = raw[TcpHeader.VERSION_POSITION - 1] & TransportStatus.STATUS_REQRES == 0

            if is_request:
                request = OutboundMessageRequest()
                request.read_from(input)
                print(f"\t{request.tcp_header}")
                if request.thread_context_struct.request_headers or request.thread_context_struct.response_headers:
                    print(f"\t{request.thread_context_struct}")
                if request.features:
                    print(f"\tfeatures: {request.features}")
                if request.action:
                    print(f"\taction: {request.action}")

                # TODO: Need a better way of matching these action names to reading their classes
                if request.action == 'internal:tcp/handshake':
                    tcp_handshake = TransportHandshakerHandshakeRequest()
                    tcp_handshake.read_from(input)
                    print(f"\topensearch_version: {tcp_handshake.version}")

                    # TODO: Here we end the reading of the request writeables (TransportMessage subclass)
                    # and begin creating a response (NetworkMessage subclass followed by TransportMessage subclass)

                    # Standard response header and variable header are part of NetworkMessage and subclasses
                    # TODO: This will be part of a Response subclass of NetworkMessage
                    response_header = TcpHeader(request_id=request.get_request_id(), status=0, version=request.get_version())
                    response_header.set_response()
                    if request.is_handshake():
                        response_header.set_handshake()
                    
                    # TODO: Variable header writing should be part of OutboundMessage class per earlier comment
                    variable_header = StreamOutput()

                    # TODO: Refactor this by implementing writing the thread context 
                    variable_header.write_string_to_string_dict(request.thread_context_struct.request_headers)
                    variable_header.write_string_to_string_array_dict(request.thread_context_struct.response_headers)

                    # TODO: Here we switch from NetworkMessage subclass to TransportMessage subclass
                    # Bytes here don't count against variable header length but are added to total message length
                    writeable_data = StreamOutput()
                    # TODO: refactor into HandshakeResponse class. Note OpenSearch has two HandshakeResponse classes.
                    # This one is o.o.transport.TransportHandshaker.HandshakeResponse
                    # Unlike the request which wraps version in a BytesReference we just directly write vint
                    writeable_data.write_v_int(Version.CURRENT)
                    
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
                    print(f"\tparsed TCP handshake, returning a response")
                    print(f"\nsent handshake response, {len(raw_out)} byte(s):\n\t#{raw_out}\n\t{response_header}")
                    
                    await loop.sock_sendall(conn, output.getvalue())
                elif request.action == 'internal:transport/handshake':
                    transport_handshake = TransportServiceHandshakeRequest()
                    transport_handshake.read_from(input)

                    # Standard response header and variable header are part of NetworkMessage and subclasses
                    # TODO: This will be part of a Response subclass of NetworkMessage
                    response_header = TcpHeader(request_id=request.get_request_id(), status=0, version=request.get_version())
                    response_header.set_response()
                    if request.is_handshake():
                        response_header.set_handshake()
                    
                    variable_header = StreamOutput()

                    # TODO: Refactor this by implementing writing the thread context 
                    variable_header.write_string_to_string_dict(request.thread_context_struct.request_headers)
                    variable_header.write_string_to_string_array_dict(request.thread_context_struct.response_headers)

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
                    TransportAddress('127.0.0.1', 1234).write_to(writeable_data) # address
                    # Write attributes map
                    attributes = dict()
                    writeable_data.write_string_to_string_dict(attributes)
                    # Write roles. Vint size and triplets with name, abbr, canContainData
                    roles = [['cluster_manager', 'm', False],
                             ['data', 'd', True],
                             ['ingest', 'i', False],
                             ['remote_cluster_client', 'r', False]]
                    writeable_data.write_v_int(len(roles))
                    for r in roles:
                        writeable_data.write_string(r[0])
                        writeable_data.write_string(r[1])
                        writeable_data.write_boolean(r[2])
                    # Version
                    writeable_data.write_v_int(Version.CURRENT)
                    # End DiscoveryNode Object

                    # ClusterName
                    writeable_data.write_string("opensearch")

                    # Version.CURRENT
                    writeable_data.write_v_int(Version.CURRENT)

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
                elif request.action == 'internal:discovery/extensions':
                    # TODO: These will be part of the TransportMessage subclass implemented here
                    task_id = TaskId()
                    task_id.read_from(input)

                    # TODO: implement InitializeExtensionRequest. Totally skipping reading the request 
                    # until we have the DiscoveryNode and DiscoveryExtensionNode classes
                    # we would also then send multiple requests to OpenSearch to implement extension points
                    # before sending a response.
                    # sometime between tcp and transport handshakes the uniqueId gets added to the thread context
                    # so adding that here so it will get added to response headers
                    request.thread_context_struct.request_headers['extension_unique_id'] = 'hello-world'

                    # for now other than that thread context, we will just send the response to make OpenSearch 
                    # happy that we initialized

                    # TODO: Here we end the reading of the request writeables (TransportMessage subclass)
                    # and begin creating a response (NetworkMessage subclass followed by TransportMessage subclass)

                    # Standard response header and variable header are part of NetworkMessage and subclasses
                    # TODO: This will be part of a Response subclass of NetworkMessage
                    response_header = TcpHeader(request_id=request.get_request_id(), status=0, version=request.get_version())
                    response_header.set_response()
                    if request.is_handshake():
                        response_header.set_handshake()

                    # TODO: Variable header writing should be part of OutboundMessage class per earlier comment
                    variable_header = StreamOutput()

                    # TODO: Refactor this by implementing writing the thread context 
                    variable_header.write_string_to_string_dict(request.thread_context_struct.request_headers)
                    variable_header.write_string_to_string_array_dict(request.thread_context_struct.response_headers)

                    # TODO: Here we switch from NetworkMessage subclass to TransportMessage subclass
                    # Bytes here don't count against variable header length but are added to total message length
                    writeable_data = StreamOutput()
                    # TODO: refactor into InitializeExtensionResponse.
                    # Write a string extension name, and then string array of implemented interfaces
                    # Extension name comes from ExtensionSettings
                    writeable_data.write_string('hello-world')
                    # Implemented interfaces are collection of java class names
                    writeable_data.write_string_array(['Extension', 'ActionExtension'])
                    
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
                    print(f"\tparsed action {request.tcp_header}, haven't yet written what to do with it")
            else:
                print(f"\tparsed {request.tcp_header}, this is a response to something I sent, haven't yet written what to do with it")

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
