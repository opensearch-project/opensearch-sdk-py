#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.settings.double_setting import DoubleSetting
from opensearch_sdk_py.settings.setting import Setting
from opensearch_sdk_py.settings.settings import Settings
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestDoubleSetting(unittest.TestCase):
    def test_float_setting(self) -> None:
        s = DoubleSetting("answer.to.life", 24.0)
        settings = Settings()
        self.assertAlmostEqual(s.get(settings), 24.0)
        settings = Settings({"answer.to.life": "42.0"})
        self.assertAlmostEqual(s.get(settings), 42.0)

        self.assertRaises(ValueError, DoubleSetting, "key", 10.0, 0.0, 5.0)

    def test_parser(self) -> None:
        parser = DoubleSetting.Parser(0.0, 100.0, "foo", Setting.Property.FILTERED)
        self.assertAlmostEqual(parser.min_value, 0.0)
        self.assertAlmostEqual(parser.max_value, 100.0)
        self.assertEqual(parser.key, "foo")
        self.assertTrue(parser.is_filtered)

    def test_parser_read_write(self) -> None:
        parser = DoubleSetting.Parser(-100.0, 100.0, "foo", Setting.Property.DYNAMIC, Setting.Property.NODE_SCOPE)
        self.assertAlmostEqual(parser.min_value, -100.0)
        self.assertAlmostEqual(parser.max_value, 100.0)
        self.assertEqual(parser.key, "foo")
        self.assertFalse(parser.is_filtered)

        output = StreamOutput()
        parser.write_to(output)
        input = StreamInput(output.getvalue())
        parser = DoubleSetting.Parser(0.0, 0.0, "").read_from(input)

        self.assertAlmostEqual(parser.min_value, -100.0)
        self.assertAlmostEqual(parser.max_value, 100.0)
        self.assertEqual(parser.key, "foo")
        self.assertFalse(parser.is_filtered)

    def test_parsing(self) -> None:
        parser = DoubleSetting.Parser(0.0, 100.0, "foo")
        self.assertAlmostEqual(parser("42.0"), 42.0)
        self.assertRaises(ValueError, parser, "not a double")
        self.assertRaises(ValueError, parser, -1.0)
        self.assertRaises(ValueError, parser, 101.0)
