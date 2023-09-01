import unittest

from opensearch_sdk_py.transport.extension_dependency import ExtensionDependency
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.version import Version


class TestExtensionDependency(unittest.TestCase):
    def test_extension_dependency(self):
        ed = ExtensionDependency()
        self.assertEqual(ed.unique_id, "")
        self.assertEqual(str(ed.version), "0.0.0.0")

        ed = ExtensionDependency("foo", Version(1000099))
        self.assertEqual(ed.unique_id, "foo")
        self.assertEqual(str(ed.version), "1.0.0.99")

        out = StreamOutput()
        ed.write_to(out)

        input = StreamInput(out.getvalue())
        ed = ExtensionDependency().read_from(input)
        self.assertEqual(ed.unique_id, "foo")
        self.assertEqual(str(ed.version), "1.0.0.99")
