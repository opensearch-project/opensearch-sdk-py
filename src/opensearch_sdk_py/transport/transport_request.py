#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.task_id import TaskId
from opensearch_sdk_py.transport.transport_message import TransportMessage


class TransportRequest(TransportMessage):
    def __init__(self, task_id: TaskId = TaskId()) -> None:
        super().__init__()
        self.parent_task_id = task_id

    def read_from(self, input: StreamInput) -> "TransportRequest":
        super().read_from(input)
        self.parent_task_id = TaskId().read_from(input)
        return self

    def write_to(self, output: StreamOutput) -> "TransportRequest":
        super().write_to(output)
        self.parent_task_id.write_to(output)
        return self

    def __str__(self) -> str:
        return f"{self.parent_task_id.__str__()}"
