# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/extensions/ExtensionDependency.java

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.version import Version


class ExtensionDependency:
    def __init__(self, unique_id: str = "", version: Version = Version()):
        self.unique_id = unique_id
        self.version = version

    def read_from(self, input: StreamInput):
        self.unique_id = input.read_string()
        self.version = input.read_version()
        return self

    def write_to(self, output: StreamOutput):
        output.write_string(self.unique_id)
        output.write_version(self.version)
        return self
