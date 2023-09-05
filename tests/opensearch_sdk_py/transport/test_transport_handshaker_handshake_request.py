import unittest

from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_handshaker_handshake_request import TransportHandshakerHandshakeRequest
from opensearch_sdk_py.transport.version import Version
from tests.opensearch_sdk_py.transport.data.netty_trace_data import NettyTraceData


class TestTransportHandshakerHandshakeRequest(unittest.TestCase):
    def test_transport_request(self):
        thhr = TransportHandshakerHandshakeRequest(Version(2100099))
        self.assertEqual(thhr.version.id, 136317827)

        out = StreamOutput()
        thhr.write_to(out)
        self.assertEqual(out.getvalue(), b"\x00\x04\x83\x97\x80\x41")

        thhr = TransportHandshakerHandshakeRequest()
        thhr.read_from(input=StreamInput(out.getvalue()))
        self.assertEqual(thhr.version.id, 136317827)
        self.assertEqual(str(thhr.version), "2.10.0.99")

    def test_read_write(self):
        data = NettyTraceData.load(
            "tests/opensearch_sdk_py/transport/data/tcp_handshake.txt"
        ).data

        input = StreamInput(data)
        request = OutboundMessageRequest()
        request.read_from(input)
        thhr = TransportHandshakerHandshakeRequest()
        thhr.read_from(input)
        self.assertEqual(str(thhr.version), "3.0.0.99")

        out = StreamOutput()
        request.write_to(out)
        thhr.write_to(out)
        self.assertEqual(out.getvalue(), data)
