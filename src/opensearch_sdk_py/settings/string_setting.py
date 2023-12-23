#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from typing import Optional

from opensearch_sdk_py.settings.setting import Setting
from opensearch_sdk_py.settings.validator import Validator


class StringSetting(Setting):
    def __init__(self, key: str, default_value: str, validator: Optional[Validator] = None, *properties: Setting.Property) -> None:
        if validator:
            validator.validate(default_value)
        parser = StringSetting.Parser()
        super().__init__(Setting.Type.STRING, key, lambda s: str(default_value), None, parser, validator, properties)

    class Parser:
        def __call__(self, s: str) -> str:
            return s
