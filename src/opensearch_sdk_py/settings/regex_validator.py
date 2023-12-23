#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import re

from opensearch_sdk_py.settings.validator import Validator
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class RegexValidator(Validator):
    def __init__(self, regex: str = "", is_matching: bool = True) -> None:
        self.regex = regex
        self.is_matching = is_matching

    def validate(self, value: str) -> None:
        if self.is_matching and not re.match(self.regex, value):
            raise ValueError(f"Setting [{value}] does not match regex [{self.regex}]")
        elif re.match(self.regex, value) and not self.is_matching:
            raise ValueError(f"Setting [{value}] must match regex [{self.regex}]")

    def read_from(self, input: StreamInput) -> "RegexValidator":
        self.regex = input.read_string()
        self.is_matching = input.read_boolean()
        return self

    def write_to(self, output: StreamOutput) -> "RegexValidator":
        output.write_string(self.regex)
        output.write_boolean(self.is_matching)
        return self
