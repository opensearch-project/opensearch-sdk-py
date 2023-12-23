#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from typing import Any

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class Parser:
    def parse(self, s: str) -> Any:
        return s

    def read_from(self, input: StreamInput) -> "Parser":
        return self  # pragma: no cover

    def write_to(self, output: StreamOutput) -> "Parser":
        return self  # pragma: no cover
