import unittest

from opensearch_sdk_py.transport.discovery_extension_node import DiscoveryExtensionNode
from opensearch_sdk_py.transport.extension_dependency import ExtensionDependency
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_address import TransportAddress
from opensearch_sdk_py.transport.version import Version


class TestDiscoveryExtensionNode(unittest.TestCase):
    def test_discovery_extension_node(self):
        den = DiscoveryExtensionNode(
            node_id="id", address=TransportAddress("127.0.0.1")
        )
        self.assertEqual(den.node_name, "")
        self.assertEqual(den.node_id, "id")
        self.assertEqual(len(den.ephemeral_id), 22)
        self.assertEqual(den.host_name, "127.0.0.1")
        self.assertEqual(den.host_address, "127.0.0.1")
        self.assertEqual(str(den.address.address), "127.0.0.1")
        self.assertEqual(den.address.port, 0)
        self.assertDictEqual(den.attributes, {})
        self.assertSetEqual(den.roles, set())
        self.assertEqual(str(den.version), "0.0.0.0")
        self.assertEqual(str(den.minimum_compatible_version), "0.0.0.0")
        self.assertListEqual(den.dependencies, [])

        dependencies = [
            ExtensionDependency("foo", Version(1010100)),
            ExtensionDependency("bar", Version(1020000)),
        ]
        den = DiscoveryExtensionNode(
            node_id="id",
            address=TransportAddress("1.2.3.4", 1234, "foo.bar"),
            minimum_compatible_version=Version(1000100),
            dependencies=dependencies,
        )
        self.assertEqual(str(den.minimum_compatible_version), "1.0.1.0")
        self.assertEqual(len(den.dependencies), 2)
        for i in range(2):
            self.assertEqual(dependencies[i].unique_id, den.dependencies[i].unique_id)
            self.assertEqual(dependencies[i].version.id, den.dependencies[i].version.id)

        output = StreamOutput()
        den.write_to(output)
        input = StreamInput(output.getvalue())
        den = DiscoveryExtensionNode().read_from(input)

        self.assertEqual(str(den.minimum_compatible_version), "1.0.1.0")
        self.assertEqual(len(den.dependencies), 2)
        for i in range(2):
            self.assertEqual(dependencies[i].unique_id, den.dependencies[i].unique_id)
            self.assertEqual(dependencies[i].version.id, den.dependencies[i].version.id)
