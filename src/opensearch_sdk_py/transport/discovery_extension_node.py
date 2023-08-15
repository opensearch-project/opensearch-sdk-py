from stream_input import StreamInput
from stream_output import StreamOutput
from discovery_node import DiscoveryNode

class DiscoveryExtensionNode(DiscoveryNode):
    def __init__(self):
        super().__init__(self)

    def read_from(self, input: StreamInput):
        # minimumCompatibleVersion = in.readVersion();
        # int size = in.readVInt();
        # dependencies = new ArrayList<>(size);
        # for (int i = 0; i < size; i++) {
        #     dependencies.add(new ExtensionDependency(in));
        # }
        pass

    def write_to(self, output: StreamOutput):
        pass
