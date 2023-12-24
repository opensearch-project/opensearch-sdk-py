#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest
from enum import Enum

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.time_unit import TimeUnit


class TestStreamInput(unittest.TestCase):
    def test_read_byte(self) -> None:
        input = StreamInput(b"\x2a\xff")
        self.assertEqual(input.read_byte(), 42)
        self.assertEqual(input.read_byte(), -1)

    def test_read_bytes(self) -> None:
        input = StreamInput(b"\x27\x10\x42")
        self.assertEqual(input.read_bytes(3), b"\x27\x10\x42")

    def test_read_int(self) -> None:
        input = StreamInput(b"\x00\x00\x00\x2a\xff\xff\xff\xff")
        self.assertEqual(input.read_int(), 42)
        self.assertEqual(input.read_int(), -1)

    def test_read_short(self) -> None:
        input = StreamInput(b"\x12\x34\xff\xff")
        self.assertEqual(input.read_short(), 4660)
        self.assertEqual(input.read_short(), -1)

    def test_read_float(self) -> None:
        input = StreamInput(b"\x40\x49\x0f\xdb\x7f\x80\x00\x00")
        self.assertAlmostEqual(input.read_float(), 3.1415927410125732)
        self.assertAlmostEqual(input.read_float(), float("inf"))

    def test_read_double(self) -> None:
        input = StreamInput(b"\x40\x05\xBF\x0A\x8B\x14\x57\x69")
        self.assertAlmostEqual(input.read_double(), 2.718281828459045)

    def test_read_boolean(self) -> None:
        input = StreamInput(b"\x00\x01\x02")
        self.assertEqual(input.read_boolean(), False)
        self.assertEqual(input.read_boolean(), True)
        self.assertRaises(Exception, input.read_boolean)

    def test_read_optional_boolean(self) -> None:
        input = StreamInput(b"\x00\x01\x02\x03")
        self.assertEqual(input.read_optional_boolean(), False)
        self.assertEqual(input.read_optional_boolean(), True)
        self.assertEqual(input.read_optional_boolean(), None)
        self.assertRaises(Exception, input.read_optional_boolean)

    def test_read_v_int(self) -> None:
        input = StreamInput(b"\x2a")
        self.assertEqual(input.read_v_int(), 42)
        input = StreamInput(b"\x80\x01")
        self.assertEqual(input.read_v_int(), 128)
        input = StreamInput(b"\x80\x80\x01")
        self.assertEqual(input.read_v_int(), 128**2)
        input = StreamInput(b"\x80\x80\x80\x01")
        self.assertEqual(input.read_v_int(), 128**3)
        input = StreamInput(b"\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_v_int(), 128**4)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x01")
        self.assertRaises(Exception, input.read_v_int)

    def test_read_version(self) -> None:
        input = StreamInput(b"\x83\x97\x80\x41")
        v = input.read_version()
        self.assertEqual(v.id, 136317827)
        self.assertEqual(str(v), "2.10.0.99")

    def test_read_optional_int(self) -> None:
        input = StreamInput(b"\x01\x00\x00\x00\x2a\x01\xff\xff\xff\xff\x00")
        self.assertEqual(input.read_optional_int(), 42)
        self.assertEqual(input.read_optional_int(), -1)
        self.assertEqual(input.read_optional_int(), None)

    def test_read_long(self) -> None:
        input = StreamInput(b"\x00\x00\x00\x01\x02\x03\x04\x05\xff\xff\xff\xff\xff\xff\xff\xff")
        self.assertEqual(input.read_long(), 4328719365)
        self.assertEqual(input.read_long(), -1)

    def test_read_v_long(self) -> None:
        input = StreamInput(b"\x2a")
        self.assertEqual(input.read_v_long(), 42)
        input = StreamInput(b"\x80\x01")
        self.assertEqual(input.read_v_long(), 128)
        input = StreamInput(b"\x80\x80\x01")
        self.assertEqual(input.read_v_long(), 128**2)
        input = StreamInput(b"\x80\x80\x80\x01")
        self.assertEqual(input.read_v_long(), 128**3)
        input = StreamInput(b"\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_v_long(), 128**4)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_v_long(), 128**5)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_v_long(), 128**6)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_v_long(), 128**7)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_v_long(), 128**8)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_v_long(), 128**9)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertRaises(Exception, input.read_v_long)

    def test_read_optional_v_long(self) -> None:
        input = StreamInput(b"\x01\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_optional_v_long(), 128**9)
        input = StreamInput(b"\x00\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_optional_v_long(), None)
        input = StreamInput(b"\x01\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertRaises(Exception, input.read_optional_v_long)

    def test_read_optional_long(self) -> None:
        input = StreamInput(b"\x01\x00\x00\x00\x00\x00\x00\x00\x2a\x01\xff\xff\xff\xff\xff\xff\xff\xff\x00")
        self.assertEqual(input.read_optional_long(), 42)
        self.assertEqual(input.read_optional_long(), -1)
        self.assertEqual(input.read_optional_long(), None)

    def test_read_z_long(self) -> None:
        input = StreamInput(b"\x2a")
        self.assertEqual(input.read_z_long(), 21)
        input = StreamInput(b"\x2b")
        self.assertEqual(input.read_z_long(), -21)
        input = StreamInput(b"\x80\x01")
        self.assertEqual(input.read_z_long(), 64)
        input = StreamInput(b"\x81\x01")
        self.assertEqual(input.read_z_long(), -64)
        input = StreamInput(b"\x80\x80\x01")
        self.assertEqual(input.read_z_long(), 64 * 128)
        input = StreamInput(b"\x81\x80\x01")
        self.assertEqual(input.read_z_long(), -64 * 128)
        input = StreamInput(b"\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), 64 * 128**2)
        input = StreamInput(b"\x81\x80\x80\x01")
        self.assertEqual(input.read_z_long(), -64 * 128**2)
        input = StreamInput(b"\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), 64 * 128**3)
        input = StreamInput(b"\x81\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), -64 * 128**3)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), 64 * 128**4)
        input = StreamInput(b"\x81\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), -64 * 128**4)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), 64 * 128**5)
        input = StreamInput(b"\x81\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), -64 * 128**5)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), 64 * 128**6)
        input = StreamInput(b"\x81\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), -64 * 128**6)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), 64 * 128**7)
        input = StreamInput(b"\x81\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), -64 * 128**7)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), 64 * 128**8)
        input = StreamInput(b"\x81\x80\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertEqual(input.read_z_long(), -64 * 128**8)
        input = StreamInput(b"\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01")
        self.assertRaises(Exception, input.read_z_long)

    def test_read_optional_string(self) -> None:
        input = StreamInput(b"\x01\x04test")
        self.assertEqual(input.read_optional_string(), "test")
        input = StreamInput(b"\x00\x04test")
        self.assertEqual(input.read_optional_string(), None)

    def test_read_array_size(self) -> None:
        input = StreamInput(b"\x2a")
        self.assertEqual(input.read_array_size(), 42)
        input = StreamInput(b"\x81\x80\x80\x80\x08")  # 2**32+1
        self.assertRaises(Exception, input.read_array_size)
        # impossible to test rase on -1 as it can't ever happen

    def test_read_string(self) -> None:
        input = StreamInput(b"\x04test")
        self.assertEqual(input.read_string(), "test")

    def test_read_string_array(self) -> None:
        input = StreamInput(b"\x02\x03foo\x03bar")
        self.assertEqual(input.read_string_array(), ["foo", "bar"])

    def test_read_optional_string_array(self) -> None:
        input = StreamInput(b"\x01\x02\x03foo\x03bar")
        self.assertEqual(input.read_optional_string_array(), ["foo", "bar"])
        input = StreamInput(b"\x00\x02\x03foo\x03bar")
        self.assertEqual(input.read_optional_string_array(), None)

    def test_read_string_to_string_dict(self) -> None:
        input = StreamInput(b"\x02\x03foo\x03bar\x03baz\x03qux")
        dict = input.read_string_to_string_dict()
        self.assertDictEqual(dict, {"foo": "bar", "baz": "qux"})
        input = StreamInput(b"\x00")
        dict = input.read_string_to_string_dict()
        self.assertDictEqual(dict, {})

    def test_read_string_to_string_array_dict(self) -> None:
        input = StreamInput(b"\x02\x03foo\x02\x03bar\x03baz\x03qux\x00")
        dict = input.read_string_to_string_array_dict()
        self.assertDictEqual(dict, {"foo": ["bar", "baz"], "qux": []})
        input = StreamInput(b"\x00")
        dict = input.read_string_to_string_array_dict()
        self.assertDictEqual(dict, {})

    def test_read_string_to_string_set_dict(self) -> None:
        input = StreamInput(b"\x02\x03foo\x03\x03bar\x03baz\x03bar\x03qux\x00")
        dict = input.read_string_to_string_set_dict()
        self.assertEqual(len(dict), 2)
        self.assertSetEqual(dict["foo"], {"bar", "baz"})
        self.assertSetEqual(dict["qux"], set())

    def test_read_generic_value(self) -> None:
        # -1
        input = StreamInput(b"\xff")
        self.assertIsNone(input.read_generic_value())
        # 0
        input = StreamInput(b"\x00\x04test")
        self.assertEqual(input.read_generic_value(), "test")
        # 1
        input = StreamInput(b"\x01\x00\x00\x00\x2a")
        self.assertEqual(input.read_generic_value(), 42)
        # 2
        input = StreamInput(b"\x02\x00\x00\x00\x01\x02\x03\x04\x05")
        self.assertEqual(input.read_generic_value(), 4328719365)
        # 5
        input = StreamInput(b"\x05\x01")
        self.assertEqual(input.read_generic_value(), True)
        # 6
        input = StreamInput(b"\x06\x00")
        self.assertEqual(input.read_generic_value(), b"")
        input = StreamInput(b"\x06\x03\x27\x10\x42")
        self.assertEqual(input.read_generic_value(), b"\x27\x10\x42")
        # 7
        input = StreamInput(b"\x07\x00")
        self.assertEqual(input.read_generic_value(), [])
        input = StreamInput(b"\x07\x02\x00\x03foo\x00\x03bar")
        self.assertEqual(input.read_generic_value(), ["foo", "bar"])
        # 11
        input = StreamInput(b"\x0b\x2a")
        self.assertEqual(input.read_generic_value(), 42)
        # 16
        input = StreamInput(b"\x10\x00\x2a")
        self.assertEqual(input.read_generic_value(), 42)
        # not implemented
        input = StreamInput(b"\xfe")
        self.assertRaises(Exception, input.read_generic_value)

    def test_read_enum(self) -> None:
        TestEnum = Enum("TestEnum", ["FOO", "BAR", "BAZ"], start=0)
        input = StreamInput(b"\x01")
        self.assertEqual(input.read_enum(TestEnum), TestEnum.BAR)

    def test_read_time_value(self) -> None:
        input = StreamInput(b"\x0a\x04")
        tv = input.read_time_value()
        self.assertEqual(tv.duration, 5)
        self.assertEqual(tv.time_unit, TimeUnit.MINUTES)
        input = StreamInput(b"\x03\x02")
        tv = input.read_time_value()
        self.assertEqual(tv.duration, -1)
        input = StreamInput(b"\x00\x00")
        tv = input.read_time_value()
        self.assertEqual(tv.duration, 0)
