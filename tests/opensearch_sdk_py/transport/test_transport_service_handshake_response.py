import unittest

from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_address import TransportAddress
from opensearch_sdk_py.transport.transport_service_handshake_response import (
    TransportServiceHandshakeResponse,
)
from opensearch_sdk_py.transport.version import Version


class TestTransportServiceHandshakeResponse(unittest.TestCase):
    def test_transport_service_handshake_response(self):
        dn = DiscoveryNode(node_id="id", address=TransportAddress("127.0.0.1"))
        tshr = TransportServiceHandshakeResponse(dn, "hello-world", Version(2100099))
        self.assertEqual(tshr.discovery_node.node_id, "id")
        self.assertEqual(tshr.cluster_name, "hello-world")
        self.assertEqual(tshr.version.id, 136317827)

        out = StreamOutput()
        tshr.write_to(out)

        input = StreamInput(out.getvalue())
        tshr = TransportServiceHandshakeResponse().read_from(input)
        self.assertEqual(tshr.discovery_node.node_id, "id")
        self.assertEqual(tshr.cluster_name, "hello-world")
        self.assertEqual(tshr.version.id, 136317827)
