#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from symbol import varargslist

from opensearch_sdk_py.settings.setting_property import SettingProperty
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class IntegerParser:
    MIN_VALUE: int = -(2**31)
    MAX_VALUE: int = 2**31 - 1

    def __call__(self, s: str) -> int:
        value: int = int(s)
        if not (IntegerParser.MIN_VALUE <= value <= IntegerParser.MAX_VALUE):
            filtered_s: str = " [" + s + "]" if self.is_filtered else ""
            raise ValueError("Failed to parse value" + filtered_s + " for setting [" + self.key + "], must be between " + IntegerParser.MIN_VALUE + " and " + IntegerParser.MAX_VALUE)
        return value

    def __init__(self, min_value: int, max_value: int, key: str, *properties: varargslist(SettingProperty)) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.key = key
        self.is_filtered: bool = SettingProperty.FILTERED in properties

    def read_from(self, input: StreamInput) -> "IntegerParser":
        self.min_value = input.read_int()
        self.max_value = input.read_int()
        self.key = input.read_string()
        self.is_filtered = input.read_boolean
        return self

    def write_to(self, output: StreamOutput) -> "IntegerParser":
        output.write_int(self.min_value)
        output.write_int(self.max_value)
        output.write_string(self.key)
        output.write_boolean(self.is_filtered)
        return self
