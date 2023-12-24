#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.transport.time_unit import TimeUnit
from opensearch_sdk_py.transport.time_value import TimeValue


class TestTimeValue(unittest.TestCase):
    def test_time_value(self) -> None:
        tv = TimeValue(42, TimeUnit.SECONDS)
        self.assertEqual(tv.duration, 42)
        self.assertEqual(tv.time_unit, TimeUnit.SECONDS)
        self.assertEqual(str(tv), "42s")

    def test_parse_time_value(self) -> None:
        tv = TimeValue.parse("42s")
        self.assertEqual(tv.duration, 42)
        self.assertEqual(tv.time_unit, TimeUnit.SECONDS)
        tv = TimeValue.parse("24 h")
        self.assertEqual(tv.duration, 24)
        self.assertEqual(tv.time_unit, TimeUnit.HOURS)

        self.assertRaises(ValueError, TimeValue.parse, "no digits")
        self.assertRaises(ValueError, TimeValue.parse, "9 weeks")

    def test_time_value_to_nanos(self) -> None:
        tv = TimeValue(42, TimeUnit.NANOSECONDS)
        self.assertEqual(tv.to_nanos(), 42)
        tv = TimeValue(42, TimeUnit.MICROSECONDS)
        self.assertEqual(tv.to_nanos(), 42_000)
        tv = TimeValue(42, TimeUnit.MILLISECONDS)
        self.assertEqual(tv.to_nanos(), 42_000_000)
        tv = TimeValue(42, TimeUnit.SECONDS)
        self.assertEqual(tv.to_nanos(), 42_000_000_000)
        tv = TimeValue(42, TimeUnit.MINUTES)
        self.assertEqual(tv.to_nanos(), 42_000_000_000 * 60)
        tv = TimeValue(42, TimeUnit.HOURS)
        self.assertEqual(tv.to_nanos(), 42_000_000_000 * 3600)
        tv = TimeValue(42, TimeUnit.DAYS)
        self.assertEqual(tv.to_nanos(), 42_000_000_000 * 86400)
