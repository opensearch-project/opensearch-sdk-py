#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.settings.long_setting import LongSetting
from opensearch_sdk_py.settings.setting import Setting
from opensearch_sdk_py.settings.settings import Settings
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestLongSetting(unittest.TestCase):
    def test_long_setting(self) -> None:
        s = LongSetting("answer.to.life", 2**42)
        settings = Settings()
        self.assertEqual(s.get(settings), 2**42)
        settings = Settings({"answer.to.life": "42"})
        self.assertEqual(s.get(settings), 42)

        self.assertRaises(ValueError, LongSetting, "key", 10, 0, 5)
        self.assertRaises(ValueError, LongSetting, "key", 0, LongSetting.MIN_VALUE - 1)
        self.assertRaises(ValueError, LongSetting, "key", 0, 0, LongSetting.MAX_VALUE + 1)

    def test_parser(self) -> None:
        parser = LongSetting.Parser(0, 100, "foo", Setting.Property.FILTERED)
        self.assertEqual(parser.min_value, 0)
        self.assertEqual(parser.max_value, 100)
        self.assertEqual(parser.key, "foo")
        self.assertTrue(parser.is_filtered)

    def test_parser_read_write(self) -> None:
        parser = LongSetting.Parser(-100, 100, "foo", Setting.Property.DYNAMIC, Setting.Property.NODE_SCOPE)
        self.assertEqual(parser.min_value, -100)
        self.assertEqual(parser.max_value, 100)
        self.assertEqual(parser.key, "foo")
        self.assertFalse(parser.is_filtered)

        output = StreamOutput()
        parser.write_to(output)
        input = StreamInput(output.getvalue())
        parser = LongSetting.Parser(0, 0, "").read_from(input)

        self.assertEqual(parser.min_value, -100)
        self.assertEqual(parser.max_value, 100)
        self.assertEqual(parser.key, "foo")
        self.assertFalse(parser.is_filtered)

    def test_parsing(self) -> None:
        parser = LongSetting.Parser(0, 100, "foo")
        self.assertEqual(parser("42"), 42)
        self.assertRaises(ValueError, parser, "not a long")
        self.assertRaises(ValueError, parser, -1)
        self.assertRaises(ValueError, parser, 101)
