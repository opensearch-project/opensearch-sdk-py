# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/extensions/rest/RestExecuteOnExtensionResponse.java

from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_response import TransportResponse


class RestExecuteOnExtensionResponse(TransportResponse):
    def __init__(
        self,
        status: RestStatus = None,
        content_type: str = "",
        content: bytes = b"",
        headers: dict[str, list[str]] = dict(),
        consumed_params: list[str] = [],
        content_consumed: bool = False,
    ):
        super().__init__()
        self.status = status
        self.content_type = content_type
        self.content = content
        self.headers = headers
        self.consumed_params = consumed_params
        self.content_consumed = content_consumed

    def read_from(self, input: StreamInput):
        super().read_from(input)
        self.status = input.read_enum(RestStatus)
        self.content_type = input.read_string()
        self.content = input.read_bytes(input.read_array_size())
        self.headers = input.read_string_to_string_array_dict()
        self.consumed_params = input.read_string_array()
        self.content_consumed = input.read_boolean()
        return self

    def write_to(self, output: StreamOutput):
        super().write_to(output)
        output.write_enum(self.status)
        output.write_string(self.content_type)
        output.write_v_int(len(self.content))
        output.write(self.content)
        output.write_string_to_string_array_dict(self.headers)
        output.write_string_array(self.consumed_params)
        output.write_boolean(self.content_consumed)
        return self
