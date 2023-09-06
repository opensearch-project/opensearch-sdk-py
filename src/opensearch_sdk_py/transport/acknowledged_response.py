# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/extensions/AcknowledgedResponse.java

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_response import TransportResponse


class AcknowledgedResponse(TransportResponse):
    def __init__(self, status: bool = False):
        super().__init__()
        self.status = status

    def read_from(self, input: StreamInput) -> "AcknowledgedResponse":
        super().read_from(input)
        self.status = input.read_boolean()
        return self

    def write_to(self, output: StreamOutput) -> "AcknowledgedResponse":
        super().write_to(output)
        output.write_boolean(self.status)
        return self
