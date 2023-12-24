#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


import re

from opensearch_sdk_py.transport.byte_size_unit import ByteSizeUnit
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class ByteSizeValue:
    BYTE_SIZE_UNIT_MAPPING = {
        "b": ByteSizeUnit.BYTES,
        "kb": ByteSizeUnit.KB,
        "mb": ByteSizeUnit.MB,
        "gb": ByteSizeUnit.GB,
        "tb": ByteSizeUnit.TB,
        "pb": ByteSizeUnit.PB,
    }

    def __init__(self, size: int, unit: ByteSizeUnit) -> None:
        self.size = size
        self.unit = unit

    @classmethod
    def parse(cls, value: str) -> "ByteSizeValue":
        match = re.match(r"(?P<size>\d+)\s*(?P<unit>\w+)", value.lower())
        if match:
            size: int = int(match.group("size"))
            unit: str = match.group("unit")
            if not (unit.endswith("b")):
                unit = unit + "b"
            if unit in ByteSizeValue.BYTE_SIZE_UNIT_MAPPING:
                return ByteSizeValue(size, ByteSizeValue.BYTE_SIZE_UNIT_MAPPING[unit])
            else:
                raise ValueError(f"Invalid TimeUnit: {unit}")
        else:
            raise ValueError(f"Invalid ByteSizeValue: {value}")

    def to_bytes(self) -> int:
        if self.unit == ByteSizeUnit.KB:
            return self.size * 2**10
        if self.unit == ByteSizeUnit.MB:
            return self.size * 2**20
        if self.unit == ByteSizeUnit.GB:
            return self.size * 2**30
        if self.unit == ByteSizeUnit.TB:
            return self.size * 2**40
        if self.unit == ByteSizeUnit.PB:
            return self.size * 2**50
        return self.size

    def read_from(self, input: StreamInput) -> "ByteSizeValue":
        self.size = input.read_z_long()
        self.unit = input.read_enum(ByteSizeUnit)
        return self

    def write_to(self, output: StreamOutput) -> "ByteSizeValue":
        output.write_z_long(self.size)
        output.write_enum(self.unit)
        return self

    def __str__(self) -> str:
        unit = {v: k for k, v in self.BYTE_SIZE_UNIT_MAPPING.items()}[self.unit]
        return f"{self.size}{unit}"
