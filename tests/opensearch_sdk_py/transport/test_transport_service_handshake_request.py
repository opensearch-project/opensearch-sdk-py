import unittest

from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_service_handshake_request import (
    TransportServiceHandshakeRequest,
)
from tests.opensearch_sdk_py.transport.data.netty_trace_data import NettyTraceData


class TestTransportServiceHandshakeRequest(unittest.TestCase):
    def test_transport_request(self):
        tshr = TransportServiceHandshakeRequest()

        out = StreamOutput()
        tshr.write_to(out)
        self.assertEqual(out.getvalue(), b"\x00")

        tshr = TransportServiceHandshakeRequest()
        tshr.read_from(input=StreamInput(out.getvalue()))

    def test_read_write_transport_handshake_request(self):
        data = NettyTraceData.load(
            "tests/opensearch_sdk_py/transport/data/transport_service_handshake_request.txt"
        ).data

        input = StreamInput(data)
        request = OutboundMessageRequest()
        request.read_from(input)
        thhr = TransportServiceHandshakeRequest()
        thhr.read_from(input)

        out = StreamOutput()
        request.write_to(out)
        thhr.write_to(out)
        self.assertEqual(out.getvalue(), data)
