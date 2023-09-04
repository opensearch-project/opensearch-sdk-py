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
        self._variable_bytes = None
        if message:
            self._message = bytes(message)
            self.tcp_header.size += len(self._message)
        else:
            self._message = None
        self.tcp_header.variable_header_size = self.thread_context_struct.size

    # subclasses call super().read_from first then read their own attributes
    def read_from(self, input: StreamInput):
        self.tcp_header.read_from(input)
        self.thread_context_struct.read_from(input)
        return self

    @property
    def variable_bytes(self):
        return self._variable_bytes

    @variable_bytes.setter
    def variable_bytes(self, variable_bytes: bytes):
        if self._variable_bytes:
            self.tcp_header.size -= len(self._variable_bytes)
            self.tcp_header.variable_header_size -= len(self._variable_bytes)
        self.tcp_header.size += len(variable_bytes)
        self.tcp_header.variable_header_size += len(variable_bytes)
        self._variable_bytes = variable_bytes

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message: bytes):
        if self._message:
            self.tcp_header.size -= len(self._message)
        self.tcp_header.size += len(message)
        self._message = message

    # subclasses create stream of variable attributes and pass here
    def write_to(self, output: StreamOutput):
        self.tcp_header.write_to(output)
        self.thread_context_struct.write_to(output)
        if self._variable_bytes:
            output.write(self._variable_bytes)
        if self._message:
            output.write(self._message)
