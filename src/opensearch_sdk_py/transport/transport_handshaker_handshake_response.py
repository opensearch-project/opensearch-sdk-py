# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/TransportHandshaker.java#L229

# this is the response for the internal:tcp/handshake action

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_response import TransportResponse
from opensearch_sdk_py.transport.version import Version

class TransportHandshakerHandshakeResponse(TransportResponse):
    def __init__(self, version:Version = None):        
        super().__init__()
        self.version = version

    def read_from(self, input: StreamInput):
        super().read_from(input)
        self.version = input.read_version()

    def write_to(self, output: StreamOutput):
        response_bytes = StreamOutput()
        if self.version:
            response_bytes.write_version(self.version)
        super().write_to(output, response_bytes)
