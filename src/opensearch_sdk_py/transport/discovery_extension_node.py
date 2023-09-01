from opensearch_sdk_py.transport.extension_dependency import ExtensionDependency
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.transport_address import TransportAddress
from opensearch_sdk_py.transport.version import Version

class DiscoveryExtensionNode(DiscoveryNode):
    def __init__(self,
                 node_name: str='',
                 node_id: str='',
                 address: TransportAddress=None,
                 attributes: dict[str, str]=dict(),
                 version: Version=Version(),
                 minimum_compatible_version: Version=Version(),
                 dependencies: list[ExtensionDependency]=[]):
        super().__init__(node_name=node_name,
                         node_id=node_id,
                         address=address,
                         attributes=attributes,
                         version=version)
        self.minimum_compatible_version = minimum_compatible_version
        self.dependencies = dependencies

    def read_from(self, input: StreamInput):
        super().read_from(input)
        self.minimum_compatible_version = input.read_version()
        self.dependencies = []
        num_dependencies = input.read_v_int()
        for d in range(num_dependencies):
            self.dependencies.append(ExtensionDependency().read_from(input))
        return self

    def write_to(self, output: StreamOutput):
        super().write_to(output)
        output.write_version(self.minimum_compatible_version)
        output.write_v_int(len(self.dependencies))
        for d in self.dependencies:
            d.write_to(output)
