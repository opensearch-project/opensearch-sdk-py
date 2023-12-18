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


class TestSetting(unittest.TestCase):
    def test_settings(self) -> None:
        settings = Settings()
        s = Setting.int_setting("answer.to.life", 24)
        self.assertEqual(s.get(settings), 24)
        settings = Settings({"answer.to.life": "42"})
        self.assertEqual(s.get(settings), 42)
