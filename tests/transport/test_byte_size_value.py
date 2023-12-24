#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.transport.byte_size_unit import ByteSizeUnit
from opensearch_sdk_py.transport.byte_size_value import ByteSizeValue


class TestByteSizeValue(unittest.TestCase):
    def test_byte_size_value(self) -> None:
        bsv = ByteSizeValue(42, ByteSizeUnit.KB)
        self.assertEqual(bsv.size, 42)
        self.assertEqual(bsv.unit, ByteSizeUnit.KB)
        self.assertEqual(str(bsv), "42kb")

    def test_parse_byte_size_value(self) -> None:
        bsv = ByteSizeValue.parse("42mb")
        self.assertEqual(bsv.size, 42)
        self.assertEqual(bsv.unit, ByteSizeUnit.MB)
        bsv = ByteSizeValue.parse("42 gb")
        self.assertEqual(bsv.size, 42)
        self.assertEqual(bsv.unit, ByteSizeUnit.GB)

        self.assertRaises(ValueError, ByteSizeValue.parse, "no digits")
        self.assertRaises(ValueError, ByteSizeValue.parse, "100eb")

    def test_byte_size_value_to_bytes(self) -> None:
        bsv = ByteSizeValue(42, ByteSizeUnit.BYTES)
        self.assertEqual(bsv.to_bytes(), 42)
        bsv = ByteSizeValue(42, ByteSizeUnit.KB)
        self.assertEqual(bsv.to_bytes(), 42 * 1024)
        bsv = ByteSizeValue(42, ByteSizeUnit.MB)
        self.assertEqual(bsv.to_bytes(), 42 * 1024**2)
        bsv = ByteSizeValue(42, ByteSizeUnit.GB)
        self.assertEqual(bsv.to_bytes(), 42 * 1024**3)
        bsv = ByteSizeValue(42, ByteSizeUnit.TB)
        self.assertEqual(bsv.to_bytes(), 42 * 1024**4)
        bsv = ByteSizeValue(42, ByteSizeUnit.PB)
        self.assertEqual(bsv.to_bytes(), 42 * 1024**5)
