import unittest

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.thread_context_struct import ThreadContextStruct


class TestThreadContextStruct(unittest.TestCase):
    def test_thread_context_struct_write(self) -> None:
        tcs = ThreadContextStruct()
        tcs.request_headers["foo"] = "bar"
        tcs.response_headers["baz"] = {"qux", "quux"}

        output = StreamOutput()
        tcs.write_to(output)
        # set may be in any order
        self.assertIn(
            output.getvalue(),
            [
                b"\x01\x03foo\x03bar\x01\x03baz\x02\x03qux\x04quux",
                b"\x01\x03foo\x03bar\x01\x03baz\x02\x04quux\x03qux",
            ],
        )

    def test_thread_context_struct_read(self) -> None:
        tcs = ThreadContextStruct()
        tcs.read_from(StreamInput(b"\x01\x03foo\x03bar\x01\x03baz\x02\x03qux\x04quux"))
        self.assertEqual(tcs.request_headers["foo"], "bar")
        self.assertSetEqual(tcs.response_headers["baz"], {"quux", "qux"})

    def test_empty_thread_context_struct(self) -> None:
        tcs = ThreadContextStruct()
        self.assertEqual(len(tcs.request_headers), 0)
        self.assertEqual(len(tcs.response_headers), 0)

        output = StreamOutput()
        tcs.write_to(output)
        self.assertEqual(output.getvalue(), b"\x00\x00")

        tcs.read_from(StreamInput(b"\x00\x00"))
        self.assertEqual(len(tcs.request_headers), 0)
        self.assertEqual(len(tcs.response_headers), 0)
