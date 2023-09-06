#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.tcp_header import TcpHeader
from opensearch_sdk_py.transport.transport_response import TransportResponse
from opensearch_sdk_py.transport.version import Version


class TestOutboundMessageResponse(unittest.TestCase):
    def test_outbound_message_response(self) -> None:
        omr = OutboundMessageResponse(version=Version(2100099))
        self.assertEqual(len(omr.thread_context_struct.request_headers), 0)
        self.assertEqual(len(omr.thread_context_struct.response_headers), 0)
        self.assertListEqual(omr.features, [])
        self.assertEqual(omr.get_request_id(), 1)
        self.assertEqual(omr.get_version().id, 136317827)
        self.assertTrue(omr.is_response())
        self.assertFalse(omr.is_error())
        self.assertFalse(omr.is_compress())
        self.assertFalse(omr.is_handshake())

    def test_custom_outbound_message_response(self) -> None:
        omr = OutboundMessageResponse(features=["foo", "bar"], is_compress=True, is_handshake=True)
        self.assertListEqual(omr.features, ["foo", "bar"])
        self.assertTrue(omr.is_compress())
        self.assertTrue(omr.is_handshake())

    def test_outbound_message_response_stream(self) -> None:
        omr = OutboundMessageResponse(
            features=["foo", "bar"],
            message=bytes(FakeTransportResponse()),
            request_id=2,
            version=Version(3000099),
            is_handshake=True,
        )
        out = StreamOutput()
        omr.write_to(out)
        self.assertEqual(
            out.getvalue(),
            b"ES\x00\x00\x00\x18\x00\x00\x00\x00\x00\x00\x00\x02\x09\x08\x2d\xc7\x23\x00\x00\x00\x02" + b"\x00\x00" + b"\x04test",  # tcp header  # context
        )  # transport message
        self.assertEqual(
            len(out.getvalue()),
            omr.tcp_header.size + TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE,
        )

        omr = OutboundMessageResponse()
        omr.read_from(input=StreamInput(out.getvalue()))
        self.assertEqual(omr.get_request_id(), 2)
        self.assertTrue(omr.is_handshake())
        self.assertEqual(
            omr.tcp_header.size,
            len(out.getvalue()) - TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE,
        )
        self.assertEqual(omr.tcp_header.variable_header_size, 2)  # context
        self.assertEqual(
            omr.tcp_header.variable_header_size,
            +omr.tcp_header.size - 5 + TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE - TcpHeader.HEADER_SIZE,  # transport message (strlen + str) included in header size
        )  # base header size


class FakeTransportResponse(TransportResponse):
    def __init__(self) -> None:
        super().__init__()

    def write_to(self, output: StreamOutput) -> None:
        super().write_to(output)
        output.write_string("test")
