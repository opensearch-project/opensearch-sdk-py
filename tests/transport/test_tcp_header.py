#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.tcp_header import TcpHeader
from opensearch_sdk_py.transport.transport_status import TransportStatus
from opensearch_sdk_py.transport.version import Version
from tests.transport.data.netty_trace_data import NettyTraceData


class TestTcpHeader(unittest.TestCase):
    def test_tcp_header(self) -> None:
        header = TcpHeader(version=Version(3000099))
        self.assertEqual(header.prefix, b"ES")
        self.assertEqual(header.request_id, 1)
        self.assertTrue(header.is_request())
        self.assertFalse(header.is_error())
        self.assertFalse(header.is_compress())
        self.assertFalse(header.is_handshake())
        self.assertEqual(header.size, TcpHeader.MESSAGE_SIZE)
        self.assertEqual(header.variable_header_size, 0)
        self.assertEqual(
            str(header),
            "['request'] b'ES', message=17 byte(s), request_id=1, status=0, version=3.0.0.99",
        )

        header.set_response()
        self.assertFalse(header.is_request())
        header.set_request()
        self.assertTrue(header.is_request())
        header.set_error()
        self.assertTrue(header.is_error())
        header.set_compress()
        self.assertTrue(header.is_compress())
        header.set_handshake()
        self.assertTrue(header.is_handshake())

    def test_tcp_header_stream(self) -> None:
        out = StreamOutput()
        TcpHeader(
            request_id=2,
            version=Version(3000099),
            status=TransportStatus.STATUS_HANDSHAKE,
        ).write_to(out)
        self.assertEqual(len(out.getvalue()), TcpHeader.HEADER_SIZE)

        header = TcpHeader()
        header.read_from(input=StreamInput(out.getvalue()))
        self.assertEqual(header.prefix, b"ES")
        self.assertEqual(header.request_id, 2)
        self.assertTrue(header.is_handshake())
        self.assertEqual(header.size, TcpHeader.MESSAGE_SIZE)
        self.assertEqual(header.variable_header_size, 0)

    def test_read_write(self) -> None:
        data = NettyTraceData.load("tests/transport/data/tcp_header.txt").data
        header = TcpHeader()
        header.read_from(StreamInput(data))
        self.assertEqual(header.prefix, b"ES")
        self.assertEqual(header.request_id, 8)
        self.assertTrue(header.is_handshake())
        self.assertEqual(header.version.id, 136317827)
        self.assertEqual(header.size, 49)
        self.assertEqual(header.variable_header_size, 26)
        out = StreamOutput()
        header.write_to(out)
        self.assertEqual(out.getvalue(), data)
