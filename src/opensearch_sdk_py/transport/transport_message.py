from typing import Any, Union

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TransportMessage:
    def __init__(self) -> None:
        pass

    def read_from(self, input: StreamInput) -> "TransportMessage":
        return self

    def write_to(self, output: StreamOutput) -> "TransportMessage":
        return self

    def __bytes__(self) -> Union[Any, bytes]:
        output = StreamOutput()
        self.write_to(output)
        return output.getvalue()
