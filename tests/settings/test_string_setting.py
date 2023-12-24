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
from opensearch_sdk_py.settings.setting import Setting
from opensearch_sdk_py.settings.settings import Settings
from opensearch_sdk_py.settings.string_setting import StringSetting


class TestStringSetting(unittest.TestCase):
    def test_string_setting(self) -> None:
        self.assertRaises(ValueError, StringSetting, "invalid.default", "3", RegexValidator(r"$\w*"))
        s = StringSetting("only.characters", "", RegexValidator(r"\w*"), Setting.Property.DYNAMIC)

        settings = Settings()
        self.assertEqual(s.get(settings), "")

        settings = Settings({"only.characters": "bar"})
        self.assertEqual(s.get(settings), "bar")
