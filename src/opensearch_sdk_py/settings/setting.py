#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from typing import Any, Callable, Optional

from opensearch_sdk_py.settings.setting_property import SettingProperty
from opensearch_sdk_py.settings.setting_type import SettingType
from opensearch_sdk_py.settings.settings import Settings


class Setting:
    def __init__(self, type: SettingType, key: str, default_value: Callable[[Settings], str], fallback: Optional["Setting"], parser: Callable[[str], Any], validator: Optional[Callable], *properties: SettingProperty) -> None:
        self.type = type
        self.key = key
        self.default_value = default_value
        self.fallback = fallback
        self.parser = parser
        self.validator = validator
        self.properties = properties

    def get(self, settings: Settings) -> Any:
        # TODO Add validation
        value = settings.get(self.key)
        return self.parser(value) if value else self.parser(self.default_value(settings))
