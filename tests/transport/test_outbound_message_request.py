#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.tcp_header import TcpHeader
from opensearch_sdk_py.transport.transport_request import TransportRequest
from opensearch_sdk_py.transport.version import Version


class TestOutboundMessageRequest(unittest.TestCase):
    def test_outbound_message_request(self) -> None:
        omr = OutboundMessageRequest(version=Version(2100099), request_id=42)
        self.assertEqual(len(omr.thread_context_struct.request_headers), 0)
        self.assertEqual(len(omr.thread_context_struct.response_headers), 0)
        self.assertListEqual(omr.features, [])
        self.assertEqual(omr.action, "")
        self.assertEqual(omr.request_id, 42)
        self.assertEqual(omr.version.id, 136317827)
        self.assertTrue(omr.is_request)
        self.assertFalse(omr.is_response)
        self.assertFalse(omr.is_error)
        self.assertFalse(omr.is_compress)
        self.assertFalse(omr.is_handshake)

    def test_custom_outbound_message_request(self) -> None:
        omr = OutboundMessageRequest(
            features=["foo", "bar"],
            action="internal:test",
            is_compress=True,
            is_handshake=True,
        )
        self.assertListEqual(omr.features, ["foo", "bar"])
        self.assertEqual(omr.action, "internal:test")
        self.assertTrue(omr.is_compress)
        self.assertTrue(omr.is_handshake)

    def test_outbound_message_request_stream(self) -> None:
        omr = OutboundMessageRequest(
            features=["foo", "bar"],
            message=FakeTransportRequest(),
            action="internal:test/handshake",
            request_id=2,
            version=Version(3000099),
            is_handshake=True,
        )
        out = StreamOutput()
        omr.write_to(out)

        self.assertEqual(
            out.getvalue(),
            b"ES\x00\x00\x00\x3a\x00\x00\x00\x00\x00\x00\x00\x02\x08\x08\x2d\xc7\x23\x00\x00\x00\x23"  # tcp header
            + b"\x00\x00"  # context
            + b"\x02\x03foo\x03bar"  # features
            + b"\x17internal:test/handshake"  # action
            + b"\x00"  # task id
            + b"\x04test",
        )  # transport message
        self.assertEqual(
            len(out.getvalue()),
            omr.tcp_header.size + TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE,
        )
        self.assertIn("internal:test/handshake", str(omr))

        omr = OutboundMessageRequest()
        omr.read_from(StreamInput(out.getvalue()))
        self.assertEqual(omr.request_id, 2)
        self.assertTrue(omr.is_handshake)
        self.assertEqual(
            omr.tcp_header.size,
            len(out.getvalue()) - TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE,
        )
        self.assertEqual(omr.tcp_header.variable_header_size, 2 + 9 + 24)  # context + features string array + action
        self.assertEqual(
            omr.tcp_header.variable_header_size,
            +omr.tcp_header.size - 6 + TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE - TcpHeader.HEADER_SIZE,  # transport message (task id + strlen + str) included in header size
        )  # base header size

        # test two-part reading with optional argument
        input = StreamInput(out.getvalue())
        header = TcpHeader()
        header.read_from(input)

        omr = OutboundMessageRequest()
        omr.read_from(input, header)
        self.assertEqual(omr.request_id, 2)
        self.assertTrue(omr.is_handshake)
        self.assertListEqual(omr.features, ["foo", "bar"])
        self.assertEqual(omr.action, "internal:test/handshake")
        self.assertEqual(
            omr.tcp_header.size,
            len(out.getvalue()) - TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE,
        )
        self.assertEqual(omr.tcp_header.variable_header_size, 2 + 9 + 24)  # context + features string array + action
        self.assertEqual(
            omr.tcp_header.variable_header_size,
            +omr.tcp_header.size - 6 + TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE - TcpHeader.HEADER_SIZE,  # transport message (task id + strlen + str) included in header size
        )  # base header size


class FakeTransportRequest(TransportRequest):
    def write_to(self, output: StreamOutput) -> None:
        super().write_to(output)
        output.write_string("test")
