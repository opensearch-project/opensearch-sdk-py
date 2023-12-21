#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.settings.setting import Setting
from opensearch_sdk_py.settings.settings import Settings
from opensearch_sdk_py.settings.time_value_setting import TimeValueSetting
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.time_unit import TimeUnit
from opensearch_sdk_py.transport.time_value import TimeValue


class TestTimeValueSetting(unittest.TestCase):
    def test_time_value_setting(self) -> None:
        s = TimeValueSetting("time.to.sleep", TimeValue(8, TimeUnit.HOURS))
        settings = Settings()
        self.assertEqual(s.get(settings).duration, 8)
        self.assertEqual(s.get(settings).time_unit, TimeUnit.HOURS)
        settings = Settings({"time.to.sleep": "30m"})
        self.assertEqual(s.get(settings).duration, 30)
        self.assertEqual(s.get(settings).time_unit, TimeUnit.MINUTES)

        self.assertRaises(ValueError, TimeValueSetting, "key", TimeValue(1, TimeUnit.HOURS), TimeValueSetting.ZERO, TimeValue(30, TimeUnit.MINUTES))
        self.assertRaises(ValueError, TimeValueSetting, "key", TimeValue(10, TimeUnit.MINUTES), TimeValue(15, TimeUnit.MINUTES), TimeValue(30, TimeUnit.MINUTES))
        self.assertRaises(ValueError, TimeValueSetting, "key", TimeValue(-2, TimeUnit.MICROSECONDS), TimeValueSetting.ZERO)
        self.assertRaises(ValueError, TimeValueSetting, "key", TimeValueSetting.ZERO, TimeValue(-2, TimeUnit.MICROSECONDS), TimeValueSetting.ZERO)
        self.assertRaises(ValueError, TimeValueSetting, "key", TimeValueSetting.ZERO, TimeValueSetting.ZERO, TimeValue(-2, TimeUnit.MICROSECONDS))

    def test_parser_read_write(self) -> None:
        parser = TimeValueSetting.Parser(TimeValueSetting.ZERO, TimeValue(5, TimeUnit.MINUTES), "foo", Setting.Property.FILTERED)
        self.assertEqual(parser.min_value.duration, 0)
        self.assertEqual(parser.max_value.duration, 5)
        self.assertEqual(parser.max_value.time_unit, TimeUnit.MINUTES)
        self.assertEqual(parser.key, "foo")
        self.assertTrue(parser.is_filtered)

        output = StreamOutput()
        parser.write_to(output)
        input = StreamInput(output.getvalue())
        parser = TimeValueSetting.Parser(TimeValueSetting.ZERO, TimeValueSetting.ZERO, "").read_from(input)

        self.assertEqual(parser.min_value.duration, 0)
        self.assertEqual(parser.max_value.duration, 5)
        self.assertEqual(parser.max_value.time_unit, TimeUnit.MINUTES)
        self.assertEqual(parser.key, "foo")
        self.assertTrue(parser.is_filtered)

    def test_parser_read_write_no_max(self) -> None:
        parser = TimeValueSetting.Parser(TimeValueSetting.ZERO, TimeValueSetting.MINUS_ONE, "foo", Setting.Property.DYNAMIC, Setting.Property.NODE_SCOPE)
        self.assertEqual(parser.min_value.duration, 0)
        self.assertEqual(parser.max_value.duration, -1)
        self.assertEqual(parser.key, "foo")
        self.assertFalse(parser.is_filtered)

        output = StreamOutput()
        parser.write_to(output)
        input = StreamInput(output.getvalue())
        parser = TimeValueSetting.Parser(TimeValueSetting.ZERO, TimeValueSetting.ZERO, "").read_from(input)

        self.assertEqual(parser.min_value.duration, 0)
        self.assertEqual(parser.max_value.duration, -1)
        self.assertEqual(parser.key, "foo")
        self.assertFalse(parser.is_filtered)

    def test_parsing(self) -> None:
        parser = TimeValueSetting.Parser(TimeValue(5, TimeUnit.MINUTES), TimeValue(10, TimeUnit.MINUTES), "foo")
        eight_minutes = parser("8m")
        self.assertEqual(eight_minutes.duration, 8)
        self.assertEqual(eight_minutes.time_unit, TimeUnit.MINUTES)
        self.assertEqual(str(eight_minutes), "8m")
        self.assertRaises(ValueError, parser, "not a time value")
        self.assertRaises(ValueError, parser, "-2m")
        self.assertRaises(ValueError, parser, "2m")
        self.assertRaises(ValueError, parser, "12m")
