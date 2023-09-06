import unittest

from opensearch_sdk_py.transport.initialize_extension_response import InitializeExtensionResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestInitializeExtensionResponse(unittest.TestCase):
    def test_initialize_extension_response(self) -> None:
        ier = InitializeExtensionResponse()
        self.assertEqual(ier.name, "")
        self.assertListEqual(ier.implemented_interfaces, [])

        ier = InitializeExtensionResponse("test", ["Extension", "ActionExtension"])
        self.assertEqual(ier.name, "test")
        self.assertListEqual(
            ier.implemented_interfaces, ["Extension", "ActionExtension"]
        )

        out = StreamOutput()
        ier.write_to(out)

        input = StreamInput(out.getvalue())
        ier = InitializeExtensionResponse().read_from(input)
        self.assertEqual(ier.name, "test")
        self.assertListEqual(
            ier.implemented_interfaces, ["Extension", "ActionExtension"]
        )
