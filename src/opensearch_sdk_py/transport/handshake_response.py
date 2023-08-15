from stream_input import StreamInput
from stream_output import StreamOutput
from transport_response import TransportResponse
from discovery_node import DiscoveryNode
from cluster_name import ClusterName

from version import Version

class HandshakeResponse(TransportResponse):
    def __init__(self, discovery_node: DiscoveryNode = None, cluster_name: ClusterName = None, version: Version = None):
        self.discovery_node = discovery_node
        self.cluster_name = cluster_name
        self.version = version
    
    def read_from(self, input: StreamInput):
        pass

    def write_to(self, output: StreamOutput):
        pass