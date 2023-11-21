#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.settings.settings import Settings
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestSettings(unittest.TestCase):
    def test_settings(self) -> None:
        settings = Settings()
        self.assertIsNone(settings.get("bar"))
        self.assertEqual(settings.get("bar", "baz"), "baz")

    def test_settings_read_write(self) -> None:
        settings = Settings({"foo": "bar", "baz": 42, "qux": True, "bytes": b"test", "list": ["a", "b", "c"]})
        self.assertIsNone(settings.get("bar"))
        self.assertEqual(settings.get("bar", "baz"), "baz")
        self.assertEqual(settings.get("foo"), "bar")
        self.assertEqual(settings.get("foo", "baz"), "bar")
        self.assertEqual(settings.get("baz"), "42")
        self.assertEqual(settings.get("qux"), "True")
        self.assertEqual(settings.get("bytes"), "b'test'")
        self.assertEqual(settings.get("list"), "['a', 'b', 'c']")

        output = StreamOutput()
        settings.write_to(output)
        input = StreamInput(output.getvalue())
        settings = Settings().read_from(input)

        self.assertIsNone(settings.get("bar"))
        self.assertEqual(settings.get("bar", "baz"), "baz")
        self.assertEqual(settings.get("foo"), "bar")
        self.assertEqual(settings.get("foo", "baz"), "bar")
        self.assertEqual(settings.get("baz"), "42")
        self.assertEqual(settings.get("qux"), "True")
        self.assertEqual(settings.get("bytes"), "b'test'")
        self.assertEqual(settings.get("list"), "['a', 'b', 'c']")
