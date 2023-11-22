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
from typing import Any

from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.version import Version


class TestStreamOutput(unittest.TestCase):
    def test_write_byte(self) -> None:
        out = StreamOutput()
        out.write_byte(42)
        self.assertEqual(out.getvalue(), b"\x2a")
        self.assertRaises(OverflowError, out.write_byte, 256)

    def test_write_int(self) -> None:
        out = StreamOutput()
        out.write_int(42)
        self.assertEqual(out.getvalue(), b"\x00\x00\x00\x2a")
        self.assertRaises(OverflowError, out.write_int, 4294967296)

    def test_write_v_int(self) -> None:
        out = StreamOutput()
        out.write_v_int(42)
        self.assertEqual(out.getvalue(), b"\x2a")
        # 7 bit max
        out.seek(0, 0)
        out.write_v_int(127)
        self.assertEqual(out.getvalue(), b"\x7f")
        self.assertEqual(StreamOutput.v_int_size(127), 1)
        out.seek(0, 0)
        out.write_v_int(128)
        self.assertEqual(out.getvalue(), b"\x80\x01")
        self.assertEqual(StreamOutput.v_int_size(128), 2)
        # 14 bit max
        out.seek(0, 0)
        out.write_v_int(16383)
        self.assertEqual(out.getvalue(), b"\xff\x7f")
        self.assertEqual(StreamOutput.v_int_size(16383), 2)
        out.seek(0, 0)
        out.write_v_int(16384)
        self.assertEqual(out.getvalue(), b"\x80\x80\x01")
        self.assertEqual(StreamOutput.v_int_size(16384), 3)
        # 21 bit max
        out.seek(0, 0)
        out.write_v_int(2097151)
        self.assertEqual(out.getvalue(), b"\xff\xff\x7f")
        self.assertEqual(StreamOutput.v_int_size(2097151), 3)
        out.seek(0, 0)
        out.write_v_int(2097152)
        self.assertEqual(out.getvalue(), b"\x80\x80\x80\x01")
        self.assertEqual(StreamOutput.v_int_size(2097152), 4)
        # 28 bit max
        out.seek(0, 0)
        out.write_v_int(268435455)
        self.assertEqual(out.getvalue(), b"\xff\xff\xff\x7f")
        self.assertEqual(StreamOutput.v_int_size(268435455), 4)
        out.seek(0, 0)
        out.write_v_int(268435456)
        self.assertEqual(out.getvalue(), b"\x80\x80\x80\x80\x01")
        self.assertEqual(StreamOutput.v_int_size(268435456), 5)

    def test_write_version(self) -> None:
        out = StreamOutput()
        v = Version(2100099)
        out.write_version(v)
        self.assertEqual(out.getvalue(), b"\x83\x97\x80\x41")

    def test_version_size(self) -> None:
        out = StreamOutput()
        v = Version(2100099)
        out.write_version(v)
        self.assertEqual(StreamOutput.version_size(v), len(out.getvalue()))

    def test_write_version_zero(self) -> None:
        out = StreamOutput()
        v = Version()
        v.id = 0
        out.write_version(v)
        self.assertEqual(out.getvalue(), b"\x00")

    def test_version_zero_size(self) -> None:
        out = StreamOutput()
        v = Version()
        v.id = 0
        out.write_version(v)
        self.assertEqual(StreamOutput.version_size(v), len(out.getvalue()))

    def test_write_long(self) -> None:
        out = StreamOutput()
        out.write_long(5409454583320448)
        self.assertEqual(out.getvalue(), b"\x00\x13\x37\xde\xca\xde\x0f\x80")

    def test_write_byte_array(self) -> None:
        out = StreamOutput()
        out.write_byte_array(b"test")
        self.assertEqual(out.getvalue(), b"\x04test")

    def test_write_string(self) -> None:
        out = StreamOutput()
        out.write_string("test")
        self.assertEqual(out.getvalue(), b"\x04test")

    def test_write_boolean(self) -> None:
        out = StreamOutput()
        out.write_boolean(True)
        out.write_boolean(False)
        self.assertEqual(out.getvalue(), b"\x01\x00")

    def test_write_string_array(self) -> None:
        out = StreamOutput()
        out.write_string_array(["foo", "bar"])
        self.assertEqual(out.getvalue(), b"\x02\x03foo\x03bar")

    def test_write_string_to_string_dict(self) -> None:
        d = dict()
        d["foo"] = "bar"
        d["baz"] = "qux"
        out = StreamOutput()
        out.write_string_to_string_dict(d)
        self.assertEqual(out.getvalue(), b"\x02\x03foo\x03bar\x03baz\x03qux")
        self.assertEqual(StreamOutput.string_to_string_dict_size(d), len(out.getvalue()))

    def test_write_string_to_string_array_dict(self) -> None:
        d = dict()
        d["foo"] = ["bar", "baz"]
        d["qux"] = []
        out = StreamOutput()
        out.write_string_to_string_array_dict(d)
        self.assertEqual(out.getvalue(), b"\x02\x03foo\x02\x03bar\x03baz\x03qux\x00")
        self.assertEqual(StreamOutput.string_to_string_collection_dict_size(d), len(out.getvalue()))

    def test_write_string_to_string_set_dict(self) -> None:
        d: dict[str, Any] = dict()
        d["foo"] = {"bar", "baz"}
        d["qux"] = {}
        out = StreamOutput()
        out.write_string_to_string_set_dict(d)
        self.assertIn(
            out.getvalue(),
            [
                b"\x02\x03foo\x02\x03bar\x03baz\x03qux\x00",
                b"\x02\x03foo\x02\x03baz\x03bar\x03qux\x00",
            ],
        )
        self.assertEqual(StreamOutput.string_to_string_collection_dict_size(d), len(out.getvalue()))

    def test_write_array_list(self) -> None:
        out = StreamOutput()
        out.write_array_list(["foo", "bar"])
        self.assertEqual(out.getvalue(), b"\x02\x00\x03foo\x00\x03bar")

    def test_write_generic_value(self) -> None:
        out = StreamOutput()
        out.write_generic_value(None)
        out.write_generic_value("test")
        out.write_generic_value(42)
        out.write_generic_value(True)
        self.assertEqual(out.getvalue(), b"\xff\x00\x04test\x02\x00\x00\x00\x00\x00\x00\x00\x2a\05\01")
        out = StreamOutput()
        out.write_generic_value(b"test")
        out.write_generic_value(["foo", "bar"])
        self.assertEqual(out.getvalue(), b"\x06\x04test\x07\x02\x00\x03foo\x00\x03bar")

    def test_write_enum(self) -> None:
        TestEnum = Enum("TestEnum", ["FOO", "BAR", "BAZ"], start=0)
        out = StreamOutput()
        out.write_enum(TestEnum.BAZ)
        self.assertEqual(out.getvalue(), b"\x02")
