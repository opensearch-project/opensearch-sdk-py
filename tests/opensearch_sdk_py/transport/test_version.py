import unittest

from opensearch_sdk_py.transport.version import Version

class TestVersion(unittest.TestCase):
    def test_2_10_0_99(self):
        v = Version(136317827)
        self.assertEqual(v.id, 2100099)
        self.assertEqual(v.major, 2)
        self.assertEqual(v.minor, 10)
        self.assertEqual(v.revision, 0)
        self.assertEqual(v.build, 99)
        self.assertEqual(v.data, 136317827)
        self.assertEqual(str(v), '2.10.0.99')
        self.assertEqual(bytes(v), b'\x08 \x0b\x83')
