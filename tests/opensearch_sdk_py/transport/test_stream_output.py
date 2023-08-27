import unittest

from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.version import Version

class TestStreamOutput(unittest.TestCase):
    def test_write_byte(self):
        out = StreamOutput()
        out.write_byte(42)
        self.assertEqual(out.getvalue(), b'\x2a')
        self.assertRaises(OverflowError, out.write_byte, 256)

    def test_write_int(self):
        out = StreamOutput()
        out.write_int(42)
        self.assertEqual(out.getvalue(), b'\x00\x00\x00\x2a')

    def test_write_v_int(self):
        out = StreamOutput()
        out.write_v_int(42)
        self.assertEqual(out.getvalue(), b'\x2a')
        # 7 bit max
        out.seek(0,0)
        out.write_v_int(127)
        self.assertEqual(out.getvalue(), b'\x7f')
        out.seek(0,0)
        out.write_v_int(128)
        self.assertEqual(out.getvalue(), b'\x80\x01')
        # 14 bit max
        out.seek(0,0)
        out.write_v_int(16383)
        self.assertEqual(out.getvalue(), b'\xff\x7f')
        out.seek(0,0)
        out.write_v_int(16384)
        self.assertEqual(out.getvalue(), b'\x80\x80\x01')
        # 21 bit max
        out.seek(0,0)
        out.write_v_int(2097151)
        self.assertEqual(out.getvalue(), b'\xff\xff\x7f')
        out.seek(0,0)
        out.write_v_int(2097152)
        self.assertEqual(out.getvalue(), b'\x80\x80\x80\x01')
        # 28 bit max
        out.seek(0,0)
        out.write_v_int(268435455)
        self.assertEqual(out.getvalue(), b'\xff\xff\xff\x7f')
        out.seek(0,0)
        out.write_v_int(268435456)
        self.assertEqual(out.getvalue(), b'\x80\x80\x80\x80\x01')

    def test_write_version(self):
        out = StreamOutput()
        v = Version(2100099)
        out.write_version(v)
        self.assertEqual(out.getvalue(), b'\x08\x20\x0b\x83')

    def test_write_long(self):
        out = StreamOutput()
        out.write_long(5409454583320448)
        self.assertEqual(out.getvalue(), b'\x00\x13\x37\xde\xca\xde\x0f\x80')

    def test_write_string(self):
        out = StreamOutput()
        out.write_string("test")
        self.assertEqual(out.getvalue(), b'\x04test')

    def test_write_long(self):
        out = StreamOutput()
        out.write_boolean(True)
        out.write_boolean(False)
        self.assertEqual(out.getvalue(), b'\x01\x00')
