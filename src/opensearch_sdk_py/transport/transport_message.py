from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TransportMessage:
    def __init__(self):
        pass

    def read_from(self, input: StreamInput):
        return self

    def write_to(self, output: StreamOutput):
        return self

    def __bytes__(self):
        output = StreamOutput()
        self.write_to(output)
        return output.getvalue()
