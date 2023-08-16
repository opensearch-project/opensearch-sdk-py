from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_request import TransportRequest
from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.discovery_extension_node import DiscoveryExtensionNode

class InitializeExtensionRequest(TransportRequest):
    def __init__(self):
        super().__init__(self)

    def read_from(self, input: StreamInput):
        super().read_from(self, input)
        self.source_node = DiscoveryNode(input)
        self.extension = DiscoveryExtensionNode(input)

    def write_to(self, output: StreamOutput):
        super().write_to(output)
        # source_node.write_to(output)
        # extension.write_to(output)
