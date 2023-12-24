#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.settings.boolean_setting import BooleanSetting
from opensearch_sdk_py.settings.settings import Settings


class TestBooleanSetting(unittest.TestCase):
    def test_boolean_setting(self) -> None:
        s = BooleanSetting("glass.half.full", False)
        settings = Settings()
        self.assertFalse(s.get(settings))
        settings = Settings({"glass.half.full": True})
        self.assertTrue(s.get(settings))
