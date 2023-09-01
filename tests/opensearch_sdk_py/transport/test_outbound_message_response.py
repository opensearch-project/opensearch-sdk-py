import unittest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.tcp_header import TcpHeader
from opensearch_sdk_py.transport.transport_response import TransportResponse
from opensearch_sdk_py.transport.transport_status import TransportStatus
from opensearch_sdk_py.transport.version import Version

class TestOutboundMessageResponse(unittest.TestCase):
    def test_outbound_message_response(self):
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

    def test_custom_outbound_message_response(self):
        omr = OutboundMessageResponse(features=['foo', 'bar'], is_compress=True, is_handshake=True)
        self.assertListEqual(omr.features, ['foo', 'bar'])
        self.assertTrue(omr.is_compress())
        self.assertTrue(omr.is_handshake())

    def test_outbound_message_response_stream(self):
        omr = OutboundMessageResponse(
                        features=['foo', 'bar'],
                        message=FakeTransportResponse(),
                        request_id=2,
                        version=Version(3000099),
                        is_handshake=True)
        out = StreamOutput()
        omr.write_to(out)
        print(out.getvalue())
        self.assertEqual(out.getvalue(),
                        b'ES\x00\x00\x00\x21\x00\x00\x00\x00\x00\x00\x00\x02\x09\x08\x2d\xc7\x23\x00\x00\x00\x0b' # tcp header
                        + b'\x00\x00' # context
                        + b'\x02\x03foo\x03bar' # features
                        + b'\x04test') # transport message
        self.assertEqual(len(out.getvalue()), omr.tcp_header.size + TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE)

        omr = OutboundMessageResponse()
        omr.read_from(input=StreamInput(out.getvalue()))
        self.assertEqual(omr.get_request_id(), 2)
        self.assertTrue(omr.is_handshake())
        self.assertEqual(omr.tcp_header.size, len(out.getvalue()) - TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE)
        self.assertEqual(omr.tcp_header.variable_header_size, 2 + 9) # context + features string array
        self.assertEqual(omr.tcp_header.variable_header_size,
                         + omr.tcp_header.size - 5 # transport message (strlen + str) included in header size
                         + TcpHeader.BYTES_REQUIRED_FOR_MESSAGE_SIZE - TcpHeader.HEADER_SIZE) # base header size
        
class FakeTransportResponse(TransportResponse):
    def __init__(self):
        super().__init__()

    def write_to(self, output: StreamOutput):
        fake_out = StreamOutput()
        fake_out.write_string('test')
        super().write_to(output, fake_out)
