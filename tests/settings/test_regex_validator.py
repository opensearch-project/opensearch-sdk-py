#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.settings.regex_validator import RegexValidator
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestRegexValidator(unittest.TestCase):
    def test_regex_validator(self) -> None:
        v = RegexValidator(r"\d+")
        v.validate("3")  # does not raise
        self.assertRaises(ValueError, v.validate, "three")
        v = RegexValidator(r"\d+", False)
        self.assertRaises(ValueError, v.validate, "3")
        v.validate("three")  # does not raise

    def test_regex_read_write(self) -> None:
        v = RegexValidator(r"\d+")
        self.assertEqual(v.regex, r"\d+")
        self.assertTrue(v.is_matching)

        output = StreamOutput()
        v.write_to(output)
        input = StreamInput(output.getvalue())
        v = RegexValidator().read_from(input)

        self.assertEqual(v.regex, r"\d+")
        self.assertTrue(v.is_matching)
