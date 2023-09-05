import unittest

from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.discovery_node_role import DiscoveryNodeRole
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_address import TransportAddress
from opensearch_sdk_py.transport.version import Version


class TestDiscoveryNode(unittest.TestCase):
    def test_discovery_node(self):
        dn = DiscoveryNode(node_id="id", address=TransportAddress("127.0.0.1"))
        self.assertEqual(dn.node_name, "")
        self.assertEqual(dn.node_id, "id")
        self.assertEqual(len(dn.ephemeral_id), 22)
        self.assertEqual(dn.host_name, "127.0.0.1")
        self.assertEqual(dn.host_address, "127.0.0.1")
        self.assertEqual(str(dn.address.address), "127.0.0.1")
        self.assertEqual(dn.address.port, 0)
        self.assertDictEqual(dn.attributes, {})
        self.assertSetEqual(dn.roles, set())
        self.assertEqual(dn.version.id, Version.CURRENT_ID)

    def test_discovery_node_read_write(self):
        dn = DiscoveryNode(
            node_name="name",
            node_id="id",
            address=TransportAddress("1.2.3.4", 1234, "foo.bar"),
            attributes={"foo": "bar", "baz": "qux"},
            roles={DiscoveryNodeRole.DATA_ROLE, DiscoveryNodeRole.INGEST_ROLE},
        )
        self.assertEqual(dn.node_name, "name")
        self.assertEqual(dn.node_id, "id")
        self.assertEqual(len(dn.ephemeral_id), 22)
        self.assertEqual(dn.host_name, "foo.bar")
        self.assertEqual(dn.host_address, "1.2.3.4")
        self.assertEqual(str(dn.address.address), "1.2.3.4")
        self.assertEqual(dn.address.port, 1234)
        self.assertDictEqual(dn.attributes, {"foo": "bar", "baz": "qux"})
        self.assertSetEqual(
            dn.roles, {DiscoveryNodeRole.DATA_ROLE, DiscoveryNodeRole.INGEST_ROLE}
        )
        self.assertEqual(dn.version.id, Version.CURRENT_ID)
        ephemeral_id = dn.ephemeral_id

        output = StreamOutput()
        dn.write_to(output)
        input = StreamInput(output.getvalue())
        dn = DiscoveryNode().read_from(input)
        self.assertEqual(dn.node_name, "name")
        self.assertEqual(dn.node_id, "id")
        self.assertEqual(dn.ephemeral_id, ephemeral_id)
        self.assertEqual(dn.host_name, "foo.bar")
        self.assertEqual(dn.host_address, "1.2.3.4")
        self.assertEqual(str(dn.address.address), "1.2.3.4")
        self.assertEqual(dn.address.port, 1234)
        self.assertDictEqual(dn.attributes, {"foo": "bar", "baz": "qux"})
        self.assertSetEqual(
            set(dn.roles), {DiscoveryNodeRole.DATA_ROLE, DiscoveryNodeRole.INGEST_ROLE}
        )
        self.assertEqual(dn.version.id, Version.CURRENT_ID)
