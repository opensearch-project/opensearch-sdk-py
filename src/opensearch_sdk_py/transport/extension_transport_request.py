#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/extensions/ExtensionRequest.java


from opensearch_sdk_py.protobuf.ExtensionRequestProto_pb2 import ExtensionRequest
from opensearch_sdk_py.transport.request_type import RequestType
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_request import TransportRequest


class ExtensionTransportRequest(TransportRequest):
    def __init__(
        self,
        request_type: "RequestType",
        unique_id: str = "",
    ) -> None:
        super().__init__()
        self.er = ExtensionRequest()
        self.er.requestType = request_type.value
        self.er.identity.uniqueId = unique_id

    def read_from(self, input: StreamInput) -> "ExtensionTransportRequest":
        super().read_from(input)
        er_bytes = input.read_bytes(input.read_v_int())
        self.er = ExtensionRequest()
        self.er.ParseFromString(er_bytes)
        return self

    def write_to(self, output: StreamOutput) -> "ExtensionTransportRequest":
        super().write_to(output)
        er_bytes = self.er.SerializeToString()
        output.write_v_int(len(er_bytes))
        output.write(er_bytes)
        return self
