import unittest

from opensearch_sdk_py.transport.outbound_message import OutboundMessage
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.tcp_header import TcpHeader
from opensearch_sdk_py.transport.transport_status import TransportStatus
from opensearch_sdk_py.transport.version import Version


class TestOutboundMessage(unittest.TestCase):
    def test_outbound_message(self):
        om = OutboundMessage(version=Version(2100099))
        self.assertEqual(len(om.thread_context_struct.request_headers), 0)
        self.assertEqual(len(om.thread_context_struct.response_headers), 0)
        self.assertEqual(om.get_request_id(), 1)
        self.assertEqual(om.get_version().id, 136317827)
        self.assertTrue(om.is_request())
        self.assertFalse(om.is_error())
        self.assertFalse(om.is_compress())
        self.assertFalse(om.is_handshake())

    def test_outbound_message_stream(self):
        om = OutboundMessage(
            request_id=2,
            version=Version(3000099),
            status=TransportStatus.STATUS_HANDSHAKE,
        )
        out = StreamOutput()
        subclass_out = StreamOutput(b"\x01\x02\x03")
        om.write_to(out, subclass_out)
        self.assertEqual(
            len(out.getvalue()),
            om.tcp_header.size + TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE,
        )

        om = OutboundMessage()
        om.read_from(input=StreamInput(out.getvalue()))
        self.assertEqual(om.get_request_id(), 2)
        self.assertTrue(om.is_handshake())
        self.assertEqual(
            om.tcp_header.size,
            len(out.getvalue()) - TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE,
        )
        self.assertEqual(
            om.tcp_header.variable_header_size, 5
        )  # 2 for context, 3 for subclass
        self.assertEqual(
            om.tcp_header.variable_header_size,
            om.tcp_header.size
            + TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE
            - TcpHeader.HEADER_SIZE,
        )
