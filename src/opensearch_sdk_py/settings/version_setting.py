#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from opensearch_sdk_py.settings.parser import Parser as SettingParser
from opensearch_sdk_py.settings.setting import Setting
from opensearch_sdk_py.transport.version import Version


class VersionSetting(Setting):
    def __init__(self, key: str, default_value: Version, *properties: Setting.Property) -> None:
        parser: VersionSetting.Parser = VersionSetting.Parser()
        super().__init__(Setting.Type.VERSION, key, lambda s: str(default_value.id), None, parser, None, properties)

    class Parser(SettingParser):
        def parse(self, s: str) -> Version:
            return Version(int(s) ^ Version.MASK)
