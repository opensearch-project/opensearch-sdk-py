import unittest

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_service_handshake_request import TransportServiceHandshakeRequest

class TestTransportServiceHandshakeRequest(unittest.TestCase):
    def test_transport_request(self):
        tshr = TransportServiceHandshakeRequest()

        out = StreamOutput()
        tshr.write_to(out)
        self.assertEqual(out.getvalue(), b'\x00')

        tshr = TransportServiceHandshakeRequest()
        tshr.read_from(input=StreamInput(out.getvalue()))