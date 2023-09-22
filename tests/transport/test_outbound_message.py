#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.transport.outbound_message import OutboundMessage
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.tcp_header import TcpHeader
from opensearch_sdk_py.transport.transport_request import TransportRequest
from opensearch_sdk_py.transport.transport_status import TransportStatus
from opensearch_sdk_py.transport.version import Version


class TestOutboundMessage(unittest.TestCase):
    def test_outbound_message(self) -> None:
        om = OutboundMessage(version=Version(2100099), request_id=42)
        self.assertEqual(len(om.thread_context_struct.request_headers), 0)
        self.assertEqual(len(om.thread_context_struct.response_headers), 0)
        self.assertEqual(om.request_id, 42)
        self.assertEqual(om.version.id, 136317827)
        self.assertFalse(om.is_request)
        self.assertTrue(om.is_response)
        self.assertFalse(om.is_error)
        self.assertFalse(om.is_compress)
        self.assertFalse(om.is_handshake)

    def test_outbound_message_stream(self) -> None:
        om_out = OutboundMessage(request_id=2, version=Version(3000099), status=TransportStatus.STATUS_HANDSHAKE, message=TransportRequest())
        out = StreamOutput()
        om_out.variable_bytes = b"\x01\x02\x03"
        om_out.message_bytes = b"\x04\x05\x06\x07"
        om_out.write_to(out)

        self.assertEqual(
            len(out.getvalue()),
            om_out.tcp_header.size + TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE,
        )

        om = OutboundMessage()
        om.read_from(input=StreamInput(out.getvalue()))
        self.assertEqual(om.request_id, 2)
        self.assertTrue(om.is_handshake)
        self.assertEqual(om.variable_bytes, om_out.variable_bytes)
        # self.assertEqual(om.message_bytes, om_out.message_bytes)
        self.assertEqual(
            om.tcp_header.size,
            len(out.getvalue()) - TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE,
        )
        self.assertEqual(om.tcp_header.variable_header_size, 5)  # 2 for context, 3 for subclass
        self.assertEqual(om.tcp_header.size + TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE - TcpHeader.HEADER_SIZE, om.tcp_header.variable_header_size + len(om_out.message_bytes))

    def test_outbound_message_variable_bytes(self) -> None:
        om = OutboundMessage()
        self.assertEqual(om.tcp_header.size, TcpHeader.VARIABLE_HEADER_SIZE_POSITION)
        self.assertEqual(om.tcp_header.variable_header_size, om.thread_context_struct.size)
        om.variable_bytes = b"\x01\x02\x03"
        self.assertEqual(om.variable_bytes, b"\x01\x02\x03")
        self.assertEqual(om.tcp_header.size, TcpHeader.VARIABLE_HEADER_SIZE_POSITION + 3)
        self.assertEqual(om.tcp_header.variable_header_size, om.thread_context_struct.size + 3)
        om.variable_bytes = b"\x01\x02\x03\x04"
        self.assertEqual(om.tcp_header.size, TcpHeader.VARIABLE_HEADER_SIZE_POSITION + 4)
        self.assertEqual(om.variable_bytes, b"\x01\x02\x03\x04")
        self.assertEqual(om.tcp_header.variable_header_size, om.thread_context_struct.size + 4)

    def test_outbound_message_message_bytes(self) -> None:
        om = OutboundMessage()
        self.assertEqual(om.tcp_header.size, TcpHeader.VARIABLE_HEADER_SIZE_POSITION)
        om.message_bytes = b"\x01\x02\x03"
        self.assertEqual(om.tcp_header.size, TcpHeader.VARIABLE_HEADER_SIZE_POSITION + 3)
        self.assertEqual(om.message_bytes, b"\x01\x02\x03")
        om.message_bytes = b"\x01\x02\x03\x04"
        self.assertEqual(om.tcp_header.size, TcpHeader.VARIABLE_HEADER_SIZE_POSITION + 4)
        self.assertEqual(om.message_bytes, b"\x01\x02\x03\x04")
