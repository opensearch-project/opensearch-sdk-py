#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.settings.parser.integer_parser import IntegerParser
from opensearch_sdk_py.settings.setting_property import SettingProperty
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestIntegerParser(unittest.TestCase):
    def test_parser(self) -> None:
        parser = IntegerParser(0, 100, "foo", SettingProperty.FILTERED)
        self.assertEqual(parser.min_value, 0)
        self.assertEqual(parser.max_value, 100)
        self.assertEqual(parser.key, "foo")
        self.assertTrue(parser.is_filtered)

    def test_parser_read_write(self) -> None:
        parser = IntegerParser(0, 100, "foo", SettingProperty.DYNAMIC, SettingProperty.NODE_SCOPE)
        self.assertEqual(parser.min_value, 0)
        self.assertEqual(parser.max_value, 100)
        self.assertEqual(parser.key, "foo")
        self.assertFalse(parser.is_filtered)

        output = StreamOutput()
        parser.write_to(output)
        input = StreamInput(output.getvalue())
        parser = IntegerParser().read_from(input)

        self.assertEqual(parser.min_value, 0)
        self.assertEqual(parser.max_value, 100)
        self.assertEqual(parser.key, "foo")
        self.assertFalse(parser.is_filtered)

    def test_parsing(self) -> None:
        parser = IntegerParser(0, 100, "foo")
        self.assertEqual(parser("42"), 42)
        self.assertRaises(ValueError, parser, "not an integer")
        self.assertRaises(ValueError, parser, -1)
        self.assertRaises(ValueError, parser, 101)
