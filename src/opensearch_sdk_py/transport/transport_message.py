from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput

class TransportMessage:
    def __init__(self):
        pass

    def read_from(self, input: StreamInput):
        pass

    def write_to(self, output: StreamOutput):
        pass