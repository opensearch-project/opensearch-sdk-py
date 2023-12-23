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
from opensearch_sdk_py.settings.version_setting import VersionSetting
from opensearch_sdk_py.transport.version import Version


class TestVersionSetting(unittest.TestCase):
    def test_version_setting(self) -> None:
        s = VersionSetting("version", Version(3000099))
        settings = Settings()
        self.assertEqual(str(s.get(settings)), "3.0.0.99")
        settings = Settings({"version": "2110099"})
        self.assertEqual(str(s.get(settings)), "2.11.0.99")

    def test_parsing(self) -> None:
        parser = VersionSetting.Parser()
        self.assertEqual(str(parser.parse("2090102")), "2.9.1.2")
