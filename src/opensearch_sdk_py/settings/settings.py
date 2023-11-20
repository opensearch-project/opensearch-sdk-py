#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


import logging
from typing import Any, Dict, Optional, Union

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


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

    @staticmethod
    def read_settings_from_stream(input: StreamInput) -> "Settings":
        settings: dict[str, Union[str, Dict]] = {}
        num_settings: int = input.read_v_int()
        logging.info(f">>>>> Reading {num_settings} settings")
        for i in range(num_settings):
            key: str = input.read_string()
            logging.info(f">>>>> Setting {i}: Reading key {key}")
            value: Any = input.read_generic_value()
            logging.info(f">>>>> Setting {i}: Value is {value}")
            settings[key] = value
        return Settings(settings)

    @staticmethod
    def write_settings_to_stream(settings: "Settings", out: StreamOutput) -> None:
        out.write_v_int(len(settings.settings))
        for key, value in settings.settings.items():
            out.write_string(key)
            out.write_generic_value(value)
        return
