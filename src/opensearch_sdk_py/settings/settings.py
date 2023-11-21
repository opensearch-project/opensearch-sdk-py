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

    def read_from(self, input: StreamInput) -> "Settings":
        num_settings: int = input.read_v_int()
        for i in range(num_settings):
            key: str = input.read_string()
            value: Any = input.read_generic_value()
            self.settings[key] = value
        return self

    def write_to(self, out: StreamOutput) -> "Settings":
        out.write_v_int(len(self.settings))
        for key, value in self.settings.items():
            out.write_string(key)
            out.write_generic_value(value)
        return self

    def get(self, setting: str, default: Optional[str] = None) -> Optional[str]:
        s_value = self.settings.get(setting)
        return str(s_value) if s_value else default
