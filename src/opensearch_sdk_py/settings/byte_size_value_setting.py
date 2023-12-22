#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from opensearch_sdk_py.settings.setting import Setting
from opensearch_sdk_py.transport.byte_size_unit import ByteSizeUnit
from opensearch_sdk_py.transport.byte_size_value import ByteSizeValue
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class ByteSizeValueSetting(Setting):
    MINUS_ONE = ByteSizeValue(-1, ByteSizeUnit.BYTES)
    ZERO = ByteSizeValue(0, ByteSizeUnit.BYTES)

    def __init__(self, key: str, default_value: ByteSizeValue, min_value: int = MINUS_ONE, max_value: int = MINUS_ONE, *properties: Setting.Property) -> None:
        parser: ByteSizeValueSetting.Parser = ByteSizeValueSetting.Parser(min_value, max_value, key)
        parser.bounds_check(default_value)
        super().__init__(Setting.Type.TIME_VALUE, key, lambda s: str(default_value), None, parser, None, properties)

    class Parser:
        def __call__(self, s: str) -> ByteSizeValue:
            return self.bounds_check(ByteSizeValue.parse(s))

        def __init__(self, min_value: ByteSizeValue, max_value: ByteSizeValue, key: str) -> None:
            if min_value.size < -1:
                raise ValueError("min_value must be positive or -1 if undefined")
            if max_value.size < -1:
                raise ValueError("max_value must be positive or -1 if undefined")
            self.min_value = min_value
            self.max_value = max_value
            self.key = key

        def bounds_check(self, value: ByteSizeValue) -> ByteSizeValue:
            if self.min_value.size >= 0 and self.min_value.to_bytes() > value.to_bytes():
                raise ValueError("Value for setting [" + self.key + "], must be above " + str(self.min_value))
            if self.max_value.size >= 0 and self.max_value.to_bytes() < value.to_bytes():
                raise ValueError("Value for setting [" + self.key + "], must be below " + str(self.max_value))
            return value

        def read_from(self, input: StreamInput) -> "ByteSizeValueSetting.Parser":
            self.min_value = ByteSizeValue(0, ByteSizeUnit.BYTES).read_from(input)
            self.max_value = ByteSizeValue(0, ByteSizeUnit.BYTES).read_from(input)
            self.key = input.read_string()
            return self

        def write_to(self, output: StreamOutput) -> "ByteSizeValueSetting.Parser":
            self.min_value.write_to(output)
            self.max_value.write_to(output)
            output.write_string(self.key)
            return self
