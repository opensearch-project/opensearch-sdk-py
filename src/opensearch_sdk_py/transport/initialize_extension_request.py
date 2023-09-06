# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/discovery/InitializeExtensionRequest.java

from opensearch_sdk_py.transport.discovery_extension_node import DiscoveryExtensionNode
from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_request import TransportRequest


class InitializeExtensionRequest(TransportRequest):
    def __init__(
        self,
        source_node: DiscoveryNode = None,
        extension: DiscoveryExtensionNode = None,
    ) -> None:
        super().__init__()
        self.source_node = source_node
        self.extension = extension

    def read_from(self, input: StreamInput) -> "InitializeExtensionRequest":
        super().read_from(input)
        self.source_node = DiscoveryNode().read_from(input)
        self.extension = DiscoveryExtensionNode().read_from(input)
        return self

    def write_to(self, output: StreamOutput) -> "InitializeExtensionRequest":
        super().write_to(output)
        self.source_node.write_to(output)
        self.extension.write_to(output)
        return self
