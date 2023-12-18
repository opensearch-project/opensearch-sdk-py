#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from typing import Any, Callable, Optional

from opensearch_sdk_py.settings.integer_parser import IntegerParser
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

    @classmethod
    def int_setting(cls, key: str, default_value: int, min_value: int = IntegerParser.MIN_VALUE, max_value: int = IntegerParser.MAX_VALUE, *properties: SettingProperty) -> "Setting":
        if not (IntegerParser.MIN_VALUE <= min_value <= IntegerParser.MAX_VALUE):
            raise ValueError("min_value must be within signed 32-bit integer range")
        if not (IntegerParser.MIN_VALUE <= max_value <= IntegerParser.MAX_VALUE):
            raise ValueError("max_value must be within signed 32-bit integer range")
        if not (min_value <= default_value <= max_value):
            raise ValueError("default_value must be within signed 32-bit integer range and between min_value and max_value")
        return Setting(SettingType.INTEGER, key, lambda s: str(default_value), fallback=None, parser=IntegerParser(min_value, max_value, key, properties), validator=None, properties=properties)
