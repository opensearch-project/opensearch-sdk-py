import unittest

from opensearch_sdk_py.transport.acknowledged_response import AcknowledgedResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestAcknowledgedResponse(unittest.TestCase):
    def test_initialize_extension_response(self):
        ar = AcknowledgedResponse()
        self.assertFalse(ar.status)

        ar = AcknowledgedResponse(True)
        self.assertTrue(ar.status)

        out = StreamOutput()
        ar.write_to(out)

        input = StreamInput(out.getvalue())
        ar = AcknowledgedResponse().read_from(input)
        self.assertTrue(ar.status)
