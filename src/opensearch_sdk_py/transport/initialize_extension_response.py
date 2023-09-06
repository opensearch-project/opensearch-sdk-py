# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/discovery/InitializeExtensionResponse.java

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_response import TransportResponse


class InitializeExtensionResponse(TransportResponse):
    def __init__(self, name: str = "", implemented_interfaces: list[str] = []):
        super().__init__()
        self.name = name
        self.implemented_interfaces = implemented_interfaces

    def read_from(self, input: StreamInput) -> "InitializeExtensionResponse":
        super().read_from(input)
        self.name = input.read_string()
        self.implemented_interfaces = input.read_string_array()
        return self

    def write_to(self, output: StreamOutput) -> "InitializeExtensionResponse":
        super().write_to(output)
        output.write_string(self.name)
        output.write_string_array(self.implemented_interfaces)
        return self
