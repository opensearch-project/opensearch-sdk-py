# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/extensions/rest/ExtensionRestRequest.java


from opensearch_sdk_py.rest.http_version import HttpVersion
from opensearch_sdk_py.rest.rest_method import RestMethod
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_request import TransportRequest


class ExtensionRestRequest(TransportRequest):
    def __init__(
        self,
        method: RestMethod = None,
        uri: str = "",
        path: str = "",
        params: dict[str, str] = dict(),
        headers: dict[str, list[str]] = dict(),
        media_type: str = "",
        content: bytes = b"",
        principal_identifier_token: str = "",
        http_version: HttpVersion = None,
    ) -> None:
        super().__init__()
        self.method = method
        self.uri = uri
        self.path = path
        self.params = params
        self.headers = headers
        self.media_type = media_type
        self.content = content
        self.principal_identifier_token = principal_identifier_token
        self.http_version = http_version

    def read_from(self, input: StreamInput) -> "ExtensionRestRequest":
        super().read_from(input)
        self.method = input.read_enum(RestMethod)
        self.uri = input.read_string()
        self.path = input.read_string()
        self.params = input.read_string_to_string_dict()
        self.headers = input.read_string_to_string_array_dict()
        if input.read_boolean():
            self.media_type = input.read_string()
        self.content = input.read_bytes(input.read_array_size())
        self.principal_identifier_token = input.read_string()
        self.http_version = input.read_enum(HttpVersion)
        return self

    def write_to(self, output: StreamOutput) -> "ExtensionRestRequest":
        super().write_to(output)
        output.write_enum(self.method)
        output.write_string(self.uri)
        output.write_string(self.path)
        output.write_string_to_string_dict(self.params)
        output.write_string_to_string_array_dict(self.headers)
        output.write_boolean(len(self.media_type) > 0)
        if self.media_type:
            output.write_string(self.media_type)
        output.write_v_int(len(self.content))
        output.write(self.content)
        output.write_string(self.principal_identifier_token)
        output.write_enum(self.http_version)
        return self
