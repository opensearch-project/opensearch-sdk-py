import unittest

from opensearch_sdk_py.transport.discovery_node_role import DiscoveryNodeRole


class TestDiscoveryNodeRole(unittest.TestCase):
    def test_role_dict(self) -> None:
        role_dict = DiscoveryNodeRole().role_dict
        self.assertTupleEqual(DiscoveryNodeRole.DATA_ROLE, role_dict["data"])
        self.assertTupleEqual(DiscoveryNodeRole.INGEST_ROLE, role_dict["ingest"])
        self.assertTupleEqual(
            DiscoveryNodeRole.CLUSTER_MANAGER_ROLE, role_dict["cluster_manager"]
        )
        self.assertTupleEqual(
            DiscoveryNodeRole.REMOTE_CLUSTER_CLIENT_ROLE,
            role_dict["remote_cluster_client"],
        )
        self.assertTupleEqual(DiscoveryNodeRole.SEARCH_ROLE, role_dict["search"])
