# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/OutboundMessage.java#L122


from opensearch_sdk_py.transport.outbound_message import OutboundMessage
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.thread_context_struct import ThreadContextStruct
from opensearch_sdk_py.transport.transport_message import TransportMessage
from opensearch_sdk_py.transport.version import Version


class OutboundMessageRequest(OutboundMessage):
    def __init__(
        self,
        thread_context: ThreadContextStruct = None,
        features: list[str] = [],
        message: TransportMessage = None,
        version: Version = None,
        action: str = "",
        request_id: int = 1,
        is_handshake: bool = False,
        is_compress: bool = False,
    ):
        super().__init__(thread_context, version, 0, request_id, message)
        self.features = features
        self.action = action
        if is_handshake:
            self.tcp_header.set_handshake()
        if is_compress:
            self.tcp_header.set_compress()
        self.__write_variable_bytes()

    def read_from(self, input: StreamInput):
        super().read_from(input)
        self.__read_variable_bytes()
        return self

    def continue_reading_from(self, input: StreamInput, om: OutboundMessage = None):
        self.tcp_header = om.tcp_header
        self.thread_context_struct = om.thread_context_struct
        self._variable_bytes = om.variable_bytes
        self.__read_variable_bytes()
        return self

    def write_to(self, output: StreamOutput):
        return super().write_to(output)

    def __read_variable_bytes(self):
        if self.variable_bytes:
            variable_stream = StreamInput(self.variable_bytes)
            self.features = variable_stream.read_string_array()
            self.action = variable_stream.read_string()

    def __write_variable_bytes(self):
        output = StreamOutput()
        output.write_string_array(self.features)
        output.write_string(self.action)
        self.variable_bytes = output.getvalue()
