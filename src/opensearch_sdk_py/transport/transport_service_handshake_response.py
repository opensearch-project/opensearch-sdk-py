# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/TransportService.java#L723

# this is the response for the internal:transport/handshake action

from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_response import TransportResponse
from opensearch_sdk_py.transport.version import Version


class TransportServiceHandshakeResponse(TransportResponse):
    def __init__(
        self,
        discovery_node: DiscoveryNode = None,
        cluster_name: str = "",
        version: Version = None,
    ):
        super().__init__()
        self.discovery_node = discovery_node
        self.cluster_name = cluster_name
        self.version = version if version else Version(Version.CURRENT)

    def read_from(self, input: StreamInput):
        super().read_from(input)
        # DiscoveryNode is an optional writeable
        if input.read_boolean():
            self.discovery_node = DiscoveryNode().read_from(input)
        self.cluster_name = input.read_string()
        self.version = input.read_version()
        return self

    def write_to(self, output: StreamOutput):
        response_bytes = StreamOutput()
        if self.discovery_node:
            response_bytes.write_boolean(True)
            self.discovery_node.write_to(response_bytes)
        else:
            response_bytes.write_boolean(False)
        response_bytes.write_string(self.cluster_name)
        response_bytes.write_version(self.version)
        super().write_to(output, response_bytes)
