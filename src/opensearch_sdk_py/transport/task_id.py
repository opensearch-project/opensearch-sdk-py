#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/libs/core/src/main/java/org/opensearch/core/tasks/TaskId.java

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TaskId:
    def __init__(self, node_id: str = "", id: int = -1) -> None:
        self.node_id = node_id
        self.id = id

    def read_from(self, input: StreamInput) -> "TaskId":
        self.node_id = input.read_string()
        if self.node_id:
            self.id = input.read_long()
        else:
            self.id = -1
        return self

    def write_to(self, output: StreamOutput) -> "TaskId":
        output.write_string(self.node_id)
        if self.node_id:
            output.write_long(self.id)
        return self

    def __str__(self) -> str:
        return f"node={self.node_id}, id={self.id}"
