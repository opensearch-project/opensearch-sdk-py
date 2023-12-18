#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from symbol import varargslist
from typing import Callable

from opensearch_sdk_py.settings.integer_parser import IntegerParser
from opensearch_sdk_py.settings.setting_property import SettingProperty
from opensearch_sdk_py.settings.setting_type import SettingType
from opensearch_sdk_py.settings.settings import Settings


class Setting:
    def __init__(
        self, type: SettingType, key: str, default_value: Callable[[Settings], str], fallback: "Setting" = None, parser: Callable[[str], any()] = None, validator: Callable[[any()]] = None, *properties: varargslist(SettingProperty)
    ) -> None:
        self.type = type
        self.key = key
        self.default_value = default_value
        self.fallback = fallback
        self.parser = parser
        self.validator = validator
        self.properties = properties

    @classmethod
    def int_setting(cls, key: str, default_value: int, min_value: int = IntegerParser.MIN_VALUE, max_value: int = IntegerParser.MAX_VALUE, *properties: varargslist("SettingProperty")) -> "Setting":
        if not (IntegerParser.MIN_VALUE <= min_value <= IntegerParser.MAX_VALUE):
            raise ValueError("min_value must be within signed 32-bbit integer range")
        if not (IntegerParser.MIN_VALUE <= max_value <= IntegerParser.MAX_VALUE):
            raise ValueError("max_value must be within signed 32-bbit integer range")
        if not (min_value <= default_value <= max_value):
            raise ValueError("default_value must be within signed 32-bbit integer range and between min_value and max_value")
        return Setting(SettingType.INTEGER, key, default_value, parser=IntegerParser(min_value, max_value, key, properties), properties=properties)
