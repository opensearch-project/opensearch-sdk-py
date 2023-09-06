#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
class DiscoveryNodeRole:
    DATA_ROLE = ("data", "d", True)
    INGEST_ROLE = ("ingest", "i", False)
    CLUSTER_MANAGER_ROLE = ("cluster_manager", "m", False)
    REMOTE_CLUSTER_CLIENT_ROLE = ("remote_cluster_client", "r", False)
    SEARCH_ROLE = ("search", "s", True)

    BUILT_IN_ROLES = [
        DATA_ROLE,
        INGEST_ROLE,
        CLUSTER_MANAGER_ROLE,
        REMOTE_CLUSTER_CLIENT_ROLE,
        SEARCH_ROLE,
    ]

    def __init__(self) -> None:
        self.role_dict = dict()
        for role in DiscoveryNodeRole.BUILT_IN_ROLES:
            self.role_dict[role[0]] = role
