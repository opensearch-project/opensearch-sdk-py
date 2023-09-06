#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.transport.discovery_node import DiscoveryNode
from opensearch_sdk_py.transport.outbound_message import OutboundMessage
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_address import TransportAddress
from opensearch_sdk_py.transport.transport_service_handshake_response import TransportServiceHandshakeResponse
from opensearch_sdk_py.transport.version import Version
from tests.transport.data.netty_trace_data import NettyTraceData


class TestTransportServiceHandshakeResponse(unittest.TestCase):
    def test_transport_service_handshake_response(self) -> None:
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

    def test_read_write_transport_handshake_response(self) -> None:
        data = NettyTraceData.load("tests/transport/data/transport_service_handshake_response.txt").data

        input = StreamInput(data)
        request = OutboundMessage()
        request.read_from(input)
        thhr = TransportServiceHandshakeResponse()
        thhr.read_from(input)
        self.assertEqual(thhr.discovery_node.node_id, "lFaxidDtTzSv1yYnOe7NRA")
        self.assertEqual(thhr.cluster_name, "opensearch")
        self.assertEqual(str(thhr.version), "3.0.0.99")

        out = StreamOutput()
        request.write_to(out)
        thhr.write_to(out)
        self.assertEqual(out.getvalue(), data)
