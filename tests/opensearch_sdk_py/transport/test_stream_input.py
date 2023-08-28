import unittest

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.version import Version

class TestStreamInput(unittest.TestCase):
    def test_read_byte(self):
        input = StreamInput(b'\x2a')
        self.assertEqual(input.read_byte(), 42)

    def test_read_bytes(self):
        input = StreamInput(b'\x27\x10\x42')
        self.assertEqual(input.read_bytes(3), b'\x27\x10\x42')

    def test_read_int(self):
        input = StreamInput(b'\x00\x00\x00\x2a\x00\x00\x00\x2a\x00')
        self.assertEqual(input.read_int(), 42)
        self.assertEqual(input.read_int(), 42)
        self.assertRaises(IndexError, input.read_int)

    def test_read_short(self):
        input = StreamInput(b'\x12\x34\x56\x78\x90')
        self.assertEqual(input.read_short(), 4660)
        self.assertEqual(input.read_short(), 22136)
        self.assertRaises(IndexError, input.read_short)

    def test_read_boolean(self):
        input = StreamInput(b'\x00\x01\x02')
        self.assertEqual(input.read_boolean(), False)
        self.assertEqual(input.read_boolean(), True)
        self.assertRaises(Exception, input.read_boolean)

    def test_read_optional_boolean(self):
        input = StreamInput(b'\x00\x01\x02\x03')
        self.assertEqual(input.read_optional_boolean(), False)
        self.assertEqual(input.read_optional_boolean(), True)
        self.assertEqual(input.read_optional_boolean(), None)
        self.assertRaises(Exception, input.read_optional_boolean)

    def test_read_v_int(self):
        input = StreamInput(b'\x2a')
        self.assertEqual(input.read_v_int(), 42)
        input = StreamInput(b'\x80\x01')
        self.assertEqual(input.read_v_int(), 128)
        input = StreamInput(b'\x80\x80\x01')
        self.assertEqual(input.read_v_int(), 128**2)
        input = StreamInput(b'\x80\x80\x80\x01')
        self.assertEqual(input.read_v_int(), 128**3)
        input = StreamInput(b'\x80\x80\x80\x80\x01')
        self.assertEqual(input.read_v_int(), 128**4)
        input = StreamInput(b'\x80\x80\x80\x80\x80\x01')
        self.assertRaises(Exception, input.read_v_int)

    def test_read_version(self):
        input = StreamInput(b'\x83\x97\x80\x41')        
        self.assertEqual(str(input.read_version()), '2.10.0.99')

    def test_read_optional_int(self):
        input = StreamInput(b'\x01\x00\x00\x00\x2a\x00\x01')
        self.assertEqual(input.read_optional_int(), 42)
        self.assertEqual(input.read_optional_int(), None)
        self.assertRaises(IndexError, input.read_optional_int)

    def test_read_long(self):
        input = StreamInput(b'\x00\x00\x00\x01\x02\x03\x04\x05\x00\x00\x00\x01\x02\x03\x04\x05\x00')
        self.assertEqual(input.read_long(), 4328719365)
        self.assertEqual(input.read_long(), 4328719365)
        self.assertRaises(IndexError, input.read_long)

    def test_read_v_long(self):
        input = StreamInput(b'\x2a')
        self.assertEqual(input.read_v_long(), 42)
        input = StreamInput(b'\x80\x01')
        self.assertEqual(input.read_v_long(), 128)
        input = StreamInput(b'\x80\x80\x01')
        self.assertEqual(input.read_v_long(), 128**2)
        input = StreamInput(b'\x80\x80\x80\x01')
        self.assertEqual(input.read_v_long(), 128**3)
        input = StreamInput(b'\x80\x80\x80\x80\x01')
        self.assertEqual(input.read_v_long(), 128**4)
        input = StreamInput(b'\x80\x80\x80\x80\x80\x01')
        self.assertEqual(input.read_v_long(), 128**5)
        input = StreamInput(b'\x80\x80\x80\x80\x80\x80\x01')
        self.assertEqual(input.read_v_long(), 128**6)
        input = StreamInput(b'\x80\x80\x80\x80\x80\x80\x80\x01')
        self.assertEqual(input.read_v_long(), 128**7)
        input = StreamInput(b'\x80\x80\x80\x80\x80\x80\x80\x80\x01')
        self.assertEqual(input.read_v_long(), 128**8)
        input = StreamInput(b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01')
        self.assertEqual(input.read_v_long(), 128**9)
        input = StreamInput(b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01')
        self.assertRaises(Exception, input.read_v_long)

    def test_read_optional_v_long(self):
        input = StreamInput(b'\x01\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01')
        self.assertEqual(input.read_optional_v_long(), 128**9)
        input = StreamInput(b'\x00\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01')
        self.assertEqual(input.read_optional_v_long(), None)
        input = StreamInput(b'\x01\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01')
        self.assertRaises(Exception, input.read_optional_v_long)

    def test_read_optional_long(self):
        input = StreamInput(b'\x01\x00\x00\x00\x00\x00\x00\x00\x2a\x00\x01')
        self.assertEqual(input.read_optional_long(), 42)
        self.assertEqual(input.read_optional_long(), None)
        self.assertRaises(IndexError, input.read_optional_long)

    def test_read_optional_string(self):
        input = StreamInput(b'\x01\x04test')        
        self.assertEqual(input.read_optional_string(), 'test')
        input = StreamInput(b'\x00\x04test')        
        self.assertEqual(input.read_optional_string(), None)

    def test_read_array_size(self):
        input = StreamInput(b'\x2a')
        self.assertEqual(input.read_array_size(), 42)
        input = StreamInput(b'\x81\x80\x80\x80\x08') # 2**32+1
        self.assertRaises(Exception, input.read_array_size)
        # impossible to test rase on -1 as it can't ever happen

    def test_read_string(self):
        input = StreamInput(b'\x04test')        
        self.assertEqual(input.read_string(), 'test')

    def test_read_string_array(self):
        input = StreamInput(b'\x02\x03foo\x03bar')        
        self.assertEqual(input.read_string_array(), ['foo', 'bar'])

    def test_read_optional_string_array(self):
        input = StreamInput(b'\x01\x02\x03foo\x03bar')        
        self.assertEqual(input.read_optional_string_array(), ['foo', 'bar'])
        input = StreamInput(b'\x00\x02\x03foo\x03bar')        
        self.assertEqual(input.read_optional_string_array(), None)

    def test_read_string_to_string_dict(self):
        input = StreamInput(b'\x02\x03foo\x03bar\x03baz\x03qux')
        dict = input.read_string_to_string_dict()
        self.assertEqual(len(dict), 2)
        self.assertEqual(dict['foo'], 'bar')
        self.assertEqual(dict['baz'], 'qux')

    def test_read_string_to_string_array_dict(self):
        input = StreamInput(b'\x02\x03foo\x02\x03bar\x03baz\x03qux\x00')
        dict = input.read_string_to_string_array_dict()
        self.assertEqual(len(dict), 2)
        self.assertEqual(dict['foo'], ['bar', 'baz'])
        self.assertEqual(dict['qux'], [])
