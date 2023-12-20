#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from opensearch_sdk_py.settings.setting import Setting
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class LongSetting(Setting):
    MIN_VALUE: int = -(2**63)
    MAX_VALUE: int = 2**63 - 1

    def __init__(self, key: str, default_value: int, min_value: int = MIN_VALUE, max_value: int = MAX_VALUE, *properties: Setting.Property) -> None:
        parser: LongSetting.Parser = LongSetting.Parser(min_value, max_value, key, properties)
        parser.bounds_check(default_value)
        super().__init__(Setting.Type.INTEGER, key, lambda s: str(default_value), None, parser, None, properties)

    class Parser:
        def __call__(self, s: str) -> int:
            return self.bounds_check(int(s))

        def __init__(self, min_value: int, max_value: int, key: str, *properties: Setting.Property) -> None:
            if not (LongSetting.MIN_VALUE <= min_value <= LongSetting.MAX_VALUE):
                raise ValueError("min_value must be within signed 64-bit integer range")
            if not (LongSetting.MIN_VALUE <= max_value <= LongSetting.MAX_VALUE):
                raise ValueError("max_value must be within signed 64-bit integer range")
            self.min_value = min_value
            self.max_value = max_value
            self.key = key
            self.is_filtered: bool = Setting.Property.FILTERED in properties

        def bounds_check(self, value: int) -> int:
            if not (self.min_value <= value <= self.max_value):
                raise ValueError("Value for setting [" + self.key + "], must be between " + str(self.min_value) + " and " + str(self.max_value))
            return value

        def read_from(self, input: StreamInput) -> "LongSetting.Parser":
            self.min_value = input.read_long()
            self.max_value = input.read_long()
            self.key = input.read_string()
            self.is_filtered = input.read_boolean()
            return self

        def write_to(self, output: StreamOutput) -> "LongSetting.Parser":
            output.write_long(self.min_value)
            output.write_long(self.max_value)
            output.write_string(self.key)
            output.write_boolean(self.is_filtered)
            return self
