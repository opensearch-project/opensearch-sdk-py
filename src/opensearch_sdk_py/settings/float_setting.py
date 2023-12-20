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


class FloatSetting(Setting):
    def __init__(self, key: str, default_value: float, min_value: float = float("-inf"), max_value: float = float("inf"), *properties: Setting.Property) -> None:
        parser: FloatSetting.Parser = FloatSetting.Parser(min_value, max_value, key, properties)
        parser.bounds_check(default_value)
        super().__init__(Setting.Type.FLOAT, key, lambda s: str(default_value), None, parser, None, properties)

    class Parser:
        def __call__(self, s: str) -> float:
            return self.bounds_check(float(s))

        def __init__(self, min_value: float, max_value: float, key: str, *properties: Setting.Property) -> None:
            self.min_value = min_value
            self.max_value = max_value
            self.key = key
            self.is_filtered: bool = Setting.Property.FILTERED in properties

        def bounds_check(self, value: float) -> float:
            if not (self.min_value <= value <= self.max_value):
                raise ValueError("Value for setting [" + self.key + "], must be between " + str(self.min_value) + " and " + str(self.max_value))
            return value

        def read_from(self, input: StreamInput) -> "FloatSetting.Parser":
            self.min_value = input.read_float()
            self.max_value = input.read_float()
            self.key = input.read_string()
            self.is_filtered = input.read_boolean()
            return self

        def write_to(self, output: StreamOutput) -> "FloatSetting.Parser":
            output.write_float(self.min_value)
            output.write_float(self.max_value)
            output.write_string(self.key)
            output.write_boolean(self.is_filtered)
            return self
