#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/TransportService.java#L706

# this is the request for the internal:transport/handshake action

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_request import TransportRequest


class TransportServiceHandshakeRequest(TransportRequest):
    def __init__(self) -> None:
        super().__init__()

    def read_from(self, input: StreamInput) -> "TransportServiceHandshakeRequest":
        super().read_from(input)
        return self

    def write_to(self, output: StreamOutput) -> "TransportServiceHandshakeRequest":
        super().write_to(output)
        return self
