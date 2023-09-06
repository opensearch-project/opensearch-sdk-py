#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/extensions/rest/RegisterRestActionsRequest.java

from opensearch_sdk_py.protobuf.RegisterRestActionsProto_pb2 import RegisterRestActions
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_request import TransportRequest


class RegisterRestActionsRequest(TransportRequest):
    def __init__(
        self,
        unique_id: str = "",
        rest_actions: list[str] = [],
        deprecated_rest_actions: list[str] = [],
    ) -> None:
        super().__init__()
        self.rra = RegisterRestActions()
        self.rra.identity.uniqueId = unique_id
        self.rra.restActions[:] = rest_actions
        self.rra.deprecatedRestActions[:] = deprecated_rest_actions

    def read_from(self, input: StreamInput) -> "RegisterRestActionsRequest":
        super().read_from(input)
        rra_bytes = input.read_bytes(input.read_v_int())
        self.rra = RegisterRestActions()
        self.rra.ParseFromString(rra_bytes)
        return self

    def write_to(self, output: StreamOutput) -> "RegisterRestActionsRequest":
        super().write_to(output)
        rra_bytes = self.rra.SerializeToString()
        output.write_v_int(len(rra_bytes))
        output.write(rra_bytes)
        return self
