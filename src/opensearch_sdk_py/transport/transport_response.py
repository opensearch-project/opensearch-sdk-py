from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_message import TransportMessage


class TransportResponse(TransportMessage):
    def __init__(self) -> None:
        super().__init__()

    def read_from(self, input: StreamInput) -> "TransportResponse":
        return self

    def write_to(self, output: StreamOutput) -> "TransportResponse":
        return self
