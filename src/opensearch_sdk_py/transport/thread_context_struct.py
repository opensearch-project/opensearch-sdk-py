#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/common/util/concurrent/ThreadContext.java#L585

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class ThreadContextStruct:
    def __init__(self) -> None:
        self.request_headers = dict[str, str]()
        self.response_headers = dict[str, set[str]]()

    def read_from(self, input: StreamInput) -> "ThreadContextStruct":
        self.request_headers = input.read_string_to_string_dict()
        self.response_headers = input.read_string_to_string_set_dict()
        return self

    def write_to(self, output: StreamOutput) -> "ThreadContextStruct":
        output.write_string_to_string_dict(self.request_headers)
        output.write_string_to_string_array_dict(self.response_headers)
        return self

    @property
    def size(self) -> int:
        if len(self.request_headers) == 0 and len(self.response_headers) == 0:
            return 2
        else:
            # TODO: math instead of writing to a stream
            out = StreamOutput()
            self.write_to(out)
            return len(out.getvalue())

    def __str__(self) -> str:
        return f"req={self.request_headers}, res={self.response_headers}"
