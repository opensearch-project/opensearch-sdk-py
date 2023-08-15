from stream_input import StreamInput
from stream_output import StreamOutput

class ClusterName:
    def __init__(self, value: str = None):
        self.value = value

    def read_from(self, input: StreamInput):
        pass

    def write_to(self, output: StreamOutput):
        pass


