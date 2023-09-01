# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/OutboundMessage.java#L168

from opensearch_sdk_py.transport.outbound_message import OutboundMessage
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.thread_context_struct import ThreadContextStruct
from opensearch_sdk_py.transport.transport_message import TransportMessage
from opensearch_sdk_py.transport.version import Version

class OutboundMessageResponse(OutboundMessage):
    def __init__(self, thread_context: ThreadContextStruct=None,
                 features: list[str]=[],
                 message: TransportMessage=None,
                 version: Version=None,
                 request_id: int=1,
                 is_handshake: bool=False,
                 is_compress: bool=False):
        super().__init__(thread_context, version, 1, request_id, message)
        self.features = features
        if is_handshake:
            self.tcp_header.set_handshake()
        if is_compress:
            self.tcp_header.set_compress()

    def read_from(self, input: StreamInput):
        super().read_from(input)
        self.features = input.read_string_array()

    def write_to(self, output: StreamOutput):
        variable_bytes = StreamOutput()
        variable_bytes.write_string_array(self.features)
        super().write_to(output, variable_bytes)
