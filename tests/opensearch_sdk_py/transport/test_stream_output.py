import unittest
from enum import Enum

from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.version import Version


class TestStreamOutput(unittest.TestCase):
    def test_write_byte(self):
        out = StreamOutput()
        out.write_byte(42)
        self.assertEqual(out.getvalue(), b"\x2a")
        self.assertRaises(OverflowError, out.write_byte, 256)

    def test_write_int(self):
        out = StreamOutput()
        out.write_int(42)
        self.assertEqual(out.getvalue(), b"\x00\x00\x00\x2a")
        self.assertRaises(OverflowError, out.write_int, 4294967296)

    def test_write_v_int(self):
        out = StreamOutput()
        out.write_v_int(42)
        self.assertEqual(out.getvalue(), b"\x2a")
        # 7 bit max
        out.seek(0, 0)
        out.write_v_int(127)
        self.assertEqual(out.getvalue(), b"\x7f")
        out.seek(0, 0)
        out.write_v_int(128)
        self.assertEqual(out.getvalue(), b"\x80\x01")
        # 14 bit max
        out.seek(0, 0)
        out.write_v_int(16383)
        self.assertEqual(out.getvalue(), b"\xff\x7f")
        out.seek(0, 0)
        out.write_v_int(16384)
        self.assertEqual(out.getvalue(), b"\x80\x80\x01")
        # 21 bit max
        out.seek(0, 0)
        out.write_v_int(2097151)
        self.assertEqual(out.getvalue(), b"\xff\xff\x7f")
        out.seek(0, 0)
        out.write_v_int(2097152)
        self.assertEqual(out.getvalue(), b"\x80\x80\x80\x01")
        # 28 bit max
        out.seek(0, 0)
        out.write_v_int(268435455)
        self.assertEqual(out.getvalue(), b"\xff\xff\xff\x7f")
        out.seek(0, 0)
        out.write_v_int(268435456)
        self.assertEqual(out.getvalue(), b"\x80\x80\x80\x80\x01")

    def test_write_version(self):
        out = StreamOutput()
        v = Version(2100099)
        out.write_version(v)
        self.assertEqual(out.getvalue(), b"\x83\x97\x80\x41")

    def test_write_long(self):
        out = StreamOutput()
        out.write_long(5409454583320448)
        self.assertEqual(out.getvalue(), b"\x00\x13\x37\xde\xca\xde\x0f\x80")

    def test_write_string(self):
        out = StreamOutput()
        out.write_string("test")
        self.assertEqual(out.getvalue(), b"\x04test")

    def test_write_boolean(self):
        out = StreamOutput()
        out.write_boolean(True)
        out.write_boolean(False)
        self.assertEqual(out.getvalue(), b"\x01\x00")

    def test_write_string_array(self):
        out = StreamOutput()
        out.write_string_array(["foo", "bar"])
        self.assertEqual(out.getvalue(), b"\x02\x03foo\x03bar")

    def test_write_string_to_string_dict(self):
        d = dict()
        d["foo"] = "bar"
        d["baz"] = "qux"
        out = StreamOutput()
        out.write_string_to_string_dict(d)
        self.assertEqual(out.getvalue(), b"\x02\x03foo\x03bar\x03baz\x03qux")

    def test_write_string_to_string_array_dict(self):
        d = dict()
        d["foo"] = ["bar", "baz"]
        d["qux"] = []
        out = StreamOutput()
        out.write_string_to_string_array_dict(d)
        self.assertEqual(out.getvalue(), b"\x02\x03foo\x02\x03bar\x03baz\x03qux\x00")

    def test_write_string_to_string_set_dict(self):
        d = dict()
        d["foo"] = {"bar", "baz"}
        d["qux"] = {}
        out = StreamOutput()
        out.write_string_to_string_set_dict(d)
        self.assertIn(
            out.getvalue(),
            [
                b"\x02\x03foo\x02\x03bar\x03baz\x03qux\x00",
                b"\x02\x03foo\x02\x03baz\x03bar\x03qux\x00",
            ],
        )

    def test_write_enum(self):
        TestEnum = Enum('TestEnum', ['FOO', 'BAR', 'BAZ'], start=0)
        out = StreamOutput()
        out.write_enum(TestEnum.BAZ)
        self.assertEqual(out.getvalue(), b"\x02")
