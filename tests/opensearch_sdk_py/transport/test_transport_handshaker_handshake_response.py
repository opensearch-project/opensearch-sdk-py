import unittest

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_handshaker_handshake_response import TransportHandshakerHandshakeResponse
from opensearch_sdk_py.transport.version import Version


class TestTransportHandshakerHandshakeResponse(unittest.TestCase):
    def test_transport_handshaker_handshake_response(self):
        thhr = TransportHandshakerHandshakeResponse(Version(2100099))
        self.assertEqual(thhr.version.id, 136317827)

        out = StreamOutput()
        thhr.write_to(out)
        self.assertEqual(out.getvalue(), b"\x83\x97\x80\x41")

        input = StreamInput(out.getvalue())
        thhr = TransportHandshakerHandshakeResponse().read_from(input)
        self.assertEqual(thhr.version.id, 136317827)
        self.assertEqual(str(thhr.version), "2.10.0.99")
