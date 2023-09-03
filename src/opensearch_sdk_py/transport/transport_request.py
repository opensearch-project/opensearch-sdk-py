from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.task_id import TaskId
from opensearch_sdk_py.transport.transport_message import TransportMessage


class TransportRequest(TransportMessage):
    def __init__(self, task_id: TaskId = TaskId()):
        super().__init__()
        self.parent_task_id = task_id

    # subclasses call super.read_from first
    def read_from(self, input: StreamInput):
        super().read_from(input)
        self.parent_task_id = TaskId().read_from(input)

    def write_to(self, output: StreamOutput):
        super().write_to(input)
        self.parent_task_id.write_to(output)
