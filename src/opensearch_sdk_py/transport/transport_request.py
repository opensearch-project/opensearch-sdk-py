from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.task_id import TaskId

class TransportRequest:
    def __init__(self, data:bytes):        
        super().__init__()
        # TODO: Implementing this as a temporary way of getting writeable content from subclasses
        # to enable end-to-end testing.  This will probably be replaced by passing the bytes 
        # directly to write_to.  Will write test classes once that's done.
        self.bytes = bytes
        self.parent_task_id = TaskId()

    def read_from(self, input: StreamInput):
        self.parent_task_id = TaskId()
        self.parent_task_id.read_from(input)

    def write_to(self, output: StreamOutput):
        self.parent_task_id.write_to(output)
        output.write(self.bytes)

