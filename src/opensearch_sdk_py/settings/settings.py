#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from typing import Dict, Optional, Union


class Settings:
    def __init__(
        self,
        settings: dict[str, Union[str, Dict]] = {},
        # TODO: Secure Settings
    ) -> None:
        self.settings = settings

    def get(self, setting: str, default: Optional[str] = None) -> str:
        s_value = self.settings.get(setting)
        if s_value is None:
            return default if default else str(None)
        return str(s_value)

    def get_as_int(self, setting: str, default: int) -> int:
        s_value = self.settings.get(setting)
        if s_value is None:
            return default
        if isinstance(s_value, str):
            return int(s_value)
        raise Exception("value is not a string")

    def get_as_float(self, setting: str, default: float) -> float:
        s_value = self.settings.get(setting)
        if s_value is None:
            return default
        if isinstance(s_value, str):
            return float(s_value)
        raise Exception("value is not a string")

    def get_as_boolean(self, setting: str, default: bool) -> bool:
        s_value = self.settings.get(setting)
        if s_value is None:
            return default
        if isinstance(s_value, str):
            return bool(s_value)
        raise Exception("value is not a string")

    def get_as_list(self, setting: str, default: list[str] = []) -> list[str]:
        s_value = self.settings.get(setting)
        if s_value is None:
            return default
        if isinstance(s_value, str):
            return s_value.split(",")
        raise Exception("value is not a string")

    # TODO: get_as_time, get_as_bytes_size
