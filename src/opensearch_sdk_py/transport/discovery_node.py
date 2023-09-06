#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import base64
import uuid
from typing import Optional

from sortedcollections import OrderedSet

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_address import TransportAddress
from opensearch_sdk_py.transport.version import Version


class DiscoveryNode:
    def __init__(
        self,
        node_name: str = "",
        node_id: Optional[str] = None,
        ephemeral_id: Optional[str] = None,
        host_name: Optional[str] = None,
        host_address: Optional[str] = None,
        address: Optional[TransportAddress] = None,
        attributes: dict[str, str] = dict(),
        roles: set[tuple] = set(),  # DiscoveryNodeRole
        version: Optional[Version] = None,
    ) -> None:
        # node_id and address are required unless we are just initializing for read_from
        if node_id and address:
            self.node_id = node_id
            self.node_name = node_name
            # OpenSearch uses Encoder.RFC4648_URLSAFE and strips the last 2 bytes of padding
            self.ephemeral_id = ephemeral_id if ephemeral_id else base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2].decode()
            self.host_name = host_name if host_name else address.host_name
            self.host_address = host_address if host_address else str(address.address)
            self.address = address
            self.attributes = attributes
            self.roles = roles
            self.version = version if version else Version(Version.CURRENT)

    def read_from(self, input: StreamInput) -> "DiscoveryNode":
        self.node_name = input.read_string()
        self.node_id = input.read_string()
        self.ephemeral_id = input.read_string()
        self.host_name = input.read_string()
        self.host_address = input.read_string()
        self.address = TransportAddress().read_from(input)
        self.attributes = input.read_string_to_string_dict()
        self.roles = OrderedSet()
        roles_size = input.read_v_int()
        for i in range(roles_size):
            self.roles.add((input.read_string(), input.read_string(), input.read_boolean()))
        self.version = input.read_version()
        return self

    def write_to(self, output: StreamOutput) -> "DiscoveryNode":
        output.write_string(self.node_name)
        output.write_string(self.node_id)
        output.write_string(self.ephemeral_id)
        output.write_string(self.host_name)
        output.write_string(self.host_address)
        self.address.write_to(output)
        output.write_string_to_string_dict(self.attributes)
        output.write_v_int(len(self.roles))
        for role in self.roles:
            output.write_string(role[0])
            output.write_string(role[1])
            output.write_boolean(role[2])
        output.write_version(self.version)
        return self
