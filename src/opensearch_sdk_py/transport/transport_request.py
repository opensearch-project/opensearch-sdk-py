from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.task_id import TaskId
from opensearch_sdk_py.transport.transport_message import TransportMessage

class TransportRequest(TransportMessage):
    def __init__(self, task_id: TaskId=TaskId()):
        super().__init__()
        self.parent_task_id = task_id

    # subclasses call super.read_from first
    def read_from(self, input: StreamInput):
        self.parent_task_id = TaskId().read_from(input)

    # subclasses pass their writeable bytes as stream
    def write_to(self, output: StreamOutput, request_output: StreamOutput=None):
        self.parent_task_id.write_to(output)
        if request_output:
            output.write(request_output.getvalue())
