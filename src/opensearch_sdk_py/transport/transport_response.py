from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_message import TransportMessage


class TransportResponse(TransportMessage):
    def __init__(self):
        super().__init__()

    def read_from(self, input: StreamInput):
        pass  # NO-OP

    def write_to(self, output: StreamOutput, response_output: StreamOutput = None):
        if response_output:
            output.write(response_output.getvalue())
