from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_request import TransportRequest

class HandshakeRequest(TransportRequest):
    def read_from(self, input: StreamInput):
        super().read_from(input)
        self.version = input.read_version()

    def write_to(self, output: StreamOutput):
        super().write_to(output)
        output.write_version(self.version)

    def __str__(self):
        return f"version={self.version}"
