import unittest

from opensearch_sdk_py.transport.version import Version

class TestVersion(unittest.TestCase):
    def test_2_10_0_99(self):
        v = Version(2100099)
        self.assertEqual(v.id, 136317827)
        self.assertEqual(v.major, 2)
        self.assertEqual(v.minor, 10)
        self.assertEqual(v.revision, 0)
        self.assertEqual(v.build, 99)
        self.assertEqual(str(v), '2.10.0.99')
        self.assertEqual(bytes(v), b'\x08 \x0b\x83')

    def test_2_10_0_99_data(self):
        v = Version()
        v.from_bytes(b'\x08 \x0b\x83')
        self.assertEqual(v.id, 136317827)
        self.assertEqual(v.major, 2)
        self.assertEqual(v.minor, 10)
        self.assertEqual(v.revision, 0)
        self.assertEqual(v.build, 99)
        self.assertEqual(str(v), '2.10.0.99')
        self.assertEqual(bytes(v), b'\x08 \x0b\x83')

    def test_empty(self):
        v = Version()
        self.assertEqual(v.id, Version.MASK)
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.revision, 0)
        self.assertEqual(v.build, 0)
        self.assertEqual(str(v), '0.0.0.0')
        self.assertEqual(bytes(v), b'\x08\x00\x00\x00')
