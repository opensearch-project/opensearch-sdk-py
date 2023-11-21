#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


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

    def get(self, setting: str, default: Optional[str] = None) -> Optional[str]:
        s_value = self.settings.get(setting)
        return str(s_value) if s_value else default

    # TODO change to read_from
    @staticmethod
    def read_settings_from_stream(input: StreamInput) -> "Settings":
        settings: dict[str, Union[str, Dict]] = {}
        num_settings: int = input.read_v_int()
        for i in range(num_settings):
            key: str = input.read_string()
            value: Any = input.read_generic_value()
            settings[key] = value
        return Settings(settings)

    # TODO change to write_to
    @staticmethod
    def write_settings_to_stream(settings: "Settings", out: StreamOutput) -> None:
        out.write_v_int(len(settings.settings))
        for key, value in settings.settings.items():
            out.write_string(key)
            out.write_generic_value(value)
        return
