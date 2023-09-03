# https://github.com/opensearch-project/OpenSearch/blob/cc007e4511dfb7faec70eff656c02e53a1c410f7/server/src/main/java/org/opensearch/transport/TransportHandshaker.java#L192

# this is the request for the internal:tcp/handshake action

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_request import TransportRequest
from opensearch_sdk_py.transport.version import Version


class TransportHandshakerHandshakeRequest(TransportRequest):
    def __init__(self, version: Version = None):
        super().__init__()
        self.version = version

    def read_from(self, input: StreamInput):
        super().read_from(input)
        input.read_v_int()
        self.version = input.read_version()

    def write_to(self, output: StreamOutput):
        super().write_to(output)
        version_bytes = StreamOutput()
        if self.version:
            # TODO: can we know the future size of version without writing it to a stream?
            version_bytes = StreamOutput()
            version_bytes.write_version(self.version)
            output.write_v_int(len(version_bytes.getvalue()))
            output.write(version_bytes.getvalue())
