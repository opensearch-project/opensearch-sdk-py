from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput

class TransportRequest:
    def __init__(self):
        super().__init__()

    def read_from(self, input: StreamInput):
        # parentTaskId = TaskId.readFromStream(in);
        pass

    def write_to(self, output: StreamOutput):
        # parentTaskId.writeTo(out);
        pass

