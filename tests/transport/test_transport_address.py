#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest
from ipaddress import AddressValueError

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_address import TransportAddress


class TestTransportAddress(unittest.TestCase):
    def test_address_no_host(self) -> None:
        ta = TransportAddress("1.2.3.4", 1234)
        self.assertEqual(str(ta.address), "1.2.3.4")
        self.assertEqual(int(ta.address), 16909060)
        self.assertEqual(ta.host_name, "1.2.3.4")
        self.assertEqual(ta.port, 1234)
        out = StreamOutput()
        ta.write_to(out)
        self.assertEqual(out.getvalue(), b"\x04\x01\x02\x03\x04\x071.2.3.4\x00\x00\x04\xd2")

    def test_address_with_host(self) -> None:
        ta = TransportAddress("1.2.3.4", 1234, "host.name")
        self.assertEqual(str(ta.address), "1.2.3.4")
        self.assertEqual(int(ta.address), 16909060)
        self.assertEqual(ta.host_name, "host.name")
        self.assertEqual(ta.port, 1234)
        out = StreamOutput()
        ta.write_to(out)
        self.assertEqual(out.getvalue(), b"\x04\x01\x02\x03\x04\x09host.name\x00\x00\x04\xd2")

        ta2 = TransportAddress()
        ta2.read_from(input=StreamInput(out.getvalue()))
        self.assertEqual(str(ta2.address), "1.2.3.4")
        self.assertEqual(int(ta2.address), 16909060)
        self.assertEqual(ta2.host_name, "host.name")
        self.assertEqual(ta2.port, 1234)

    def test_address_invalid(self) -> None:
        self.assertRaises(AddressValueError, TransportAddress, "1.2.3.4.5", 1234)
        ta = TransportAddress()
        self.assertRaises(Exception, ta.read_from, input=StreamInput(b"\x05\x01\x02\x03\x04\x05\x09host.name\x00\x00\x04\xd2"))
