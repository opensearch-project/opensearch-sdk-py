from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TransportMessage:
    def __init__(self):
        pass

    def read_from(self, input: StreamInput):
        pass  # NO-OP, subclasses implement this

    def write_to(self, output: StreamOutput):
        pass  # NO-OP, subclasses implement this

    def __bytes__(self):
        output = StreamOutput()
        self.write_to(output)
        return output.getvalue()
