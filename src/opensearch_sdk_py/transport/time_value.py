#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


import re

from opensearch_sdk_py.transport.time_unit import TimeUnit


class TimeValue:
    TIME_UNIT_MAPPING = {
        "nanos": TimeUnit.NANOSECONDS,
        "micros": TimeUnit.MICROSECONDS,
        "ms": TimeUnit.MILLISECONDS,
        "s": TimeUnit.SECONDS,
        "m": TimeUnit.MINUTES,
        "h": TimeUnit.HOURS,
        "d": TimeUnit.DAYS,
    }

    def __init__(self, duration: int, time_unit: TimeUnit) -> None:
        self.duration = duration
        self.time_unit = time_unit

    @classmethod
    def parse(cls, value: str) -> "TimeValue":
        match = re.match(r"(?P<duration>\d+)\s*(?P<unit>\w+)", value.lower())
        if match:
            duration: int = int(match.group("duration"))
            unit: str = match.group("unit")
            if unit in TimeValue.TIME_UNIT_MAPPING:
                return TimeValue(duration, TimeValue.TIME_UNIT_MAPPING[unit])
            else:
                raise ValueError(f"Invalid TimeUnit: {unit}")
        else:
            raise ValueError(f"Invalid TimeValue: {value}")

    def __str__(self) -> str:
        unit = {v: k for k, v in self.TIME_UNIT_MAPPING.items()}[self.time_unit]
        return f"{self.duration}{unit}"
