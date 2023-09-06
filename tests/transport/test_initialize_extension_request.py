import unittest

from opensearch_sdk_py.transport.discovery_extension_node import DiscoveryExtensionNode
from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.initialize_extension_request import InitializeExtensionRequest
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_address import TransportAddress
from tests.transport.data.netty_trace_data import NettyTraceData


class TestInitializeExtensionRequest(unittest.TestCase):
    def test_initialize_extension_request(self) -> None:
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

    def test_read_write(self) -> None:
        data = NettyTraceData.load(
            "tests/transport/data/initialize_extension_request.txt"
        ).data

        input = StreamInput(data)
        request = OutboundMessageRequest()
        request.read_from(input)
        thhr = InitializeExtensionRequest()
        thhr.read_from(input)
        self.assertEqual(thhr.source_node.node_id, "1GpM1ZNmTxOttjQhkVwA6g")
        self.assertEqual(thhr.extension.node_id, "hello-world")

        out = StreamOutput()
        request.write_to(out)
        thhr.write_to(out)
        self.assertEqual(out.getvalue(), data)
