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
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.time_unit import TimeUnit
from opensearch_sdk_py.transport.time_value import TimeValue


class TimeValueSetting(Setting):
    ZERO = TimeValue(0, TimeUnit.NANOSECONDS)
    MINUS_ONE = TimeValue(-1, TimeUnit.MILLISECONDS)

    def __init__(self, key: str, default_value: TimeValue, min_value: int = MINUS_ONE, max_value: int = MINUS_ONE, *properties: Setting.Property) -> None:
        parser: TimeValueSetting.Parser = TimeValueSetting.Parser(min_value, max_value, key, properties)
        parser.bounds_check(default_value)
        super().__init__(Setting.Type.TIME_VALUE, key, lambda s: str(default_value), None, parser, None, properties)

    class Parser(SettingParser):
        def __init__(self, min_value: TimeValue, max_value: TimeValue, key: str, *properties: Setting.Property) -> None:
            if min_value.duration < -1:
                raise ValueError("min_value must be positive or -1 if undefined")
            if max_value.duration < -1:
                raise ValueError("max_value must be positive or -1 if undefined")
            self.min_value = min_value
            self.max_value = max_value
            self.key = key
            self.is_filtered: bool = Setting.Property.FILTERED in properties

        def parse(self, s: str) -> TimeValue:
            return self.bounds_check(TimeValue.parse(s))

        def bounds_check(self, value: TimeValue) -> TimeValue:
            if self.min_value.duration >= 0 and self.min_value.to_nanos() > value.to_nanos():
                raise ValueError("Value for setting [" + self.key + "], must be above " + str(self.min_value))
            if self.max_value.duration >= 0 and self.max_value.to_nanos() < value.to_nanos():
                raise ValueError("Value for setting [" + self.key + "], must be below " + str(self.max_value))
            return value

        def read_from(self, input: StreamInput) -> "TimeValueSetting.Parser":
            has_max = input.read_boolean()
            self.key = input.read_string()
            self.min_value = input.read_time_value()
            self.max_value = input.read_time_value() if has_max else TimeValueSetting.MINUS_ONE
            self.is_filtered = input.read_boolean()
            return self

        def write_to(self, output: StreamOutput) -> "TimeValueSetting.Parser":
            has_max = self.max_value.duration >= 0
            output.write_boolean(has_max)
            output.write_string(self.key)
            output.write_time_value(self.min_value)
            if has_max:
                output.write_time_value(self.max_value)
            output.write_boolean(self.is_filtered)
            return self
