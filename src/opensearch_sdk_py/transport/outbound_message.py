# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/OutboundMessage.java

from opensearch_sdk_py.transport.network_message import NetworkMessage
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.thread_context_struct import ThreadContextStruct
from opensearch_sdk_py.transport.transport_message import TransportMessage
from opensearch_sdk_py.transport.version import Version


class OutboundMessage(NetworkMessage):
    def __init__(
        self,
        thread_context: ThreadContextStruct = None,
        version: Version = None,
        status: int = 0,
        request_id: int = 1,
        message: TransportMessage = None,
    ):
        super().__init__(thread_context, version, status, request_id)
        self.message = message

    # subclasses call super().read_from first then read their own attributes
    def read_from(self, input: StreamInput):
        self.tcp_header.read_from(input)
        self.thread_context_struct.read_from(input)
        return self

    # subclasses create stream of variable attributes and pass here
    def write_to(self, output: StreamOutput, variable_bytes: StreamOutput):
        variable_header = StreamOutput()
        self.thread_context_struct.write_to(variable_header)
        variable_header.write(variable_bytes.getvalue())
        variable_len = len(variable_header.getvalue())
        self.tcp_header.size += variable_len
        self.tcp_header.variable_header_size += variable_len

        message_out = StreamOutput()
        if self.message:
            self.message.write_to(message_out)
        message_len = len(message_out.getvalue())
        self.tcp_header.size += message_len

        self.tcp_header.write_to(output)
        output.write(variable_header.getvalue())
        output.write(message_out.getvalue())
