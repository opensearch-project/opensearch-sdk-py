import unittest

from opensearch_sdk_py.transport.discovery_extension_node import DiscoveryExtensionNode
from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.initialize_extension_request import (
    InitializeExtensionRequest,
)
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_address import TransportAddress


class TestInitializeExtensionRequest(unittest.TestCase):
    def test_initialize_extension_request(self):
        ier = InitializeExtensionRequest(
            extension=DiscoveryExtensionNode(
                node_id="extension_node",
                address=TransportAddress("1.2.3.4", 1234, "foo.bar"),
            ),
            source_node=DiscoveryNode(
                node_id="opensearch_node",
                address=TransportAddress("5.6.7.8", 5678, "bar.baz"),
            ),
        )

        self.assertEqual(ier.source_node.node_id, "opensearch_node")
        self.assertEqual(ier.extension.node_id, "extension_node")

        output = StreamOutput()
        ier.write_to(output)

        input = StreamInput(output.getvalue())
        request = InitializeExtensionRequest()
        ier = request.read_from(input)
        self.assertEqual(ier.source_node.node_id, 'opensearch_node')
        self.assertEqual(ier.extension.node_id, 'extension_node')
