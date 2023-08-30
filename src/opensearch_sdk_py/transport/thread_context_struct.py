# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/common/util/concurrent/ThreadContext.java#L585

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput

class ThreadContextStruct:
    def __init__(self):
        self.request_headers = dict[str, str]()
        self.response_headers = dict[str, set[str]]()

    def read_from(self, input: StreamInput):
        self.request_headers = input.read_string_to_string_dict()
        self.response_headers = input.read_string_to_string_set_dict()

    def write_to(self, output: StreamOutput):
        output.write_string_to_string_dict(self.request_headers)
        output.write_string_to_string_array_dict(self.response_headers)

    def __str__(self):
        return f"request_headers: {self.request_headers} , response_headers: {self.response_headers}"
