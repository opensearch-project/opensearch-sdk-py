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


class BooleanSetting(Setting):
    def __init__(self, key: str, default_value: bool, *properties: Setting.Property) -> None:
        parser: BooleanSetting.Parser = BooleanSetting.Parser()
        super().__init__(Setting.Type.BOOLEAN, key, lambda s: str(default_value), None, parser, None, properties)

    class Parser(SettingParser):
        def parse(self, s: str) -> bool:
            # match Java behavior: True (ignoring case) is true, otherwise false
            return s.lower() == "true"
