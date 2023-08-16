from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_response import TransportResponse

from opensearch_sdk_py.transport.version import Version

class HandshakeResponse(TransportResponse):
    def __init__(self, version: Version = None):
        self.version = version
    
    def read_from(self, input: StreamInput):
        super().read_from(input)
        self.version = input.read_version()

    def write_to(self, output: StreamOutput):
        super().write_to(output)
        output.write_version(self.version)

