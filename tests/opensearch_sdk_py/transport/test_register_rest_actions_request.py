import unittest

from opensearch_sdk_py.transport.register_rest_actions_request import (
    RegisterRestActionsRequest,
)
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestRegisterRestActionsRequest(unittest.TestCase):
    def test_register_rest_actions_request(self):
        rrar = RegisterRestActionsRequest()
        self.assertEqual(rrar.rra.identity.uniqueId, "")
        self.assertSequenceEqual(rrar.rra.restActions, [])
        self.assertSequenceEqual(rrar.rra.deprecatedRestActions, [])

        rrar = RegisterRestActionsRequest("test", ["foo", "bar"], ["baz", "qux"])
        self.assertEqual(rrar.rra.identity.uniqueId, "test")
        self.assertSequenceEqual(rrar.rra.restActions, ["foo", "bar"])
        self.assertSequenceEqual(rrar.rra.deprecatedRestActions, ["baz", "qux"])

        out = StreamOutput()
        rrar.write_to(out)

        input = StreamInput(out.getvalue())
        rrar = RegisterRestActionsRequest().read_from(input)
        self.assertEqual(rrar.rra.identity.uniqueId, "test")
        self.assertSequenceEqual(rrar.rra.restActions, ["foo", "bar"])
        self.assertSequenceEqual(rrar.rra.deprecatedRestActions, ["baz", "qux"])
