#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.settings.byte_size_value_setting import ByteSizeValueSetting
from opensearch_sdk_py.settings.settings import Settings
from opensearch_sdk_py.transport.byte_size_unit import ByteSizeUnit
from opensearch_sdk_py.transport.byte_size_value import ByteSizeValue
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestByteSizeValueSetting(unittest.TestCase):
    def test_byte_size_value_setting(self) -> None:
        s = ByteSizeValueSetting("unix.v1.lines", ByteSizeValue(4501, ByteSizeUnit.BYTES))
        settings = Settings()
        self.assertEqual(s.get(settings).size, 4501)
        self.assertEqual(s.get(settings).unit, ByteSizeUnit.BYTES)
        settings = Settings({"unix.v1.lines": "4kb"})
        self.assertEqual(s.get(settings).size, 4)
        self.assertEqual(s.get(settings).unit, ByteSizeUnit.KB)

        self.assertRaises(ValueError, ByteSizeValueSetting, "key", ByteSizeValue(1, ByteSizeUnit.KB), ByteSizeValueSetting.ZERO, ByteSizeValue(512, ByteSizeUnit.BYTES))
        self.assertRaises(ValueError, ByteSizeValueSetting, "key", ByteSizeValue(10, ByteSizeUnit.MB), ByteSizeValue(15, ByteSizeUnit.MB), ByteSizeValue(1, ByteSizeUnit.GB))
        self.assertRaises(ValueError, ByteSizeValueSetting, "key", ByteSizeValue(-2, ByteSizeUnit.KB), ByteSizeValueSetting.ZERO)
        self.assertRaises(ValueError, ByteSizeValueSetting, "key", ByteSizeValueSetting.ZERO, ByteSizeValue(-2, ByteSizeUnit.KB), ByteSizeValueSetting.ZERO)
        self.assertRaises(ValueError, ByteSizeValueSetting, "key", ByteSizeValueSetting.ZERO, ByteSizeValueSetting.ZERO, ByteSizeValue(-2, ByteSizeUnit.KB))

    def test_parser_read_write(self) -> None:
        parser = ByteSizeValueSetting.Parser(ByteSizeValue(100, ByteSizeUnit.KB), ByteSizeValue(5, ByteSizeUnit.MB), "foo")
        self.assertEqual(parser.min_value.size, 100)
        self.assertEqual(parser.min_value.unit, ByteSizeUnit.KB)
        self.assertEqual(parser.max_value.size, 5)
        self.assertEqual(parser.max_value.unit, ByteSizeUnit.MB)
        self.assertEqual(parser.key, "foo")

        output = StreamOutput()
        parser.write_to(output)
        input = StreamInput(output.getvalue())
        parser = ByteSizeValueSetting.Parser(ByteSizeValueSetting.ZERO, ByteSizeValueSetting.ZERO, "").read_from(input)

        self.assertEqual(parser.min_value.size, 100)
        self.assertEqual(parser.min_value.unit, ByteSizeUnit.KB)
        self.assertEqual(parser.max_value.size, 5)
        self.assertEqual(parser.max_value.unit, ByteSizeUnit.MB)
        self.assertEqual(parser.key, "foo")

    def test_parsing(self) -> None:
        parser = ByteSizeValueSetting.Parser(ByteSizeValue(5, ByteSizeUnit.KB), ByteSizeValue(10, ByteSizeUnit.KB), "foo")
        eight_kb = parser.parse("8k")
        self.assertEqual(eight_kb.size, 8)
        self.assertEqual(eight_kb.unit, ByteSizeUnit.KB)
        self.assertEqual(str(eight_kb), "8kb")
        self.assertRaises(ValueError, parser.parse, "not a byte size value")
        self.assertRaises(ValueError, parser.parse, "-2kb")
        self.assertRaises(ValueError, parser.parse, "2k")
        self.assertRaises(ValueError, parser.parse, "12k")
