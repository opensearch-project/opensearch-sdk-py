#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from enum import Enum
from typing import Any, Callable, Optional

from opensearch_sdk_py.settings.parser import Parser
from opensearch_sdk_py.settings.settings import Settings
from opensearch_sdk_py.settings.validator import Validator


class Setting:
    def __init__(self, type: "Setting.Type", key: str, default_value: Callable[[Settings], str], fallback: Optional["Setting"], parser: Parser, validator: Optional[Validator], *properties: "Setting.Property") -> None:
        self.type = type
        self.key = key
        self.default_value = default_value
        self.fallback = fallback
        self.parser = parser
        self.validator = validator
        self.properties = properties

    def get(self, settings: Settings) -> Any:
        value = settings.get(self.key)
        if value and self.validator:
            self.validator.validate(value)
        return self.parser.parse(value) if value else self.parser.parse(self.default_value(settings))

    Property = Enum("Property", ["FILTERED", "DYNAMIC", "FINAL", "DEPRECATED", "NODE_SCOPE", "CONSISTENT", "INDEX_SCOPE", "NOT_COPYABLE_ON_RESIZE", "INTERNAL_INDEX", "PRIVATE_INDEX", "EXTENSION_SCOPE"], start=0)

    Type = Enum("Type", ["BOOLEAN", "INTEGER", "LONG", "FLOAT", "DOUBLE", "STRING", "TIME_VALUE", "BYTE_SIZE_VALUE", "VERSION"], start=0)
