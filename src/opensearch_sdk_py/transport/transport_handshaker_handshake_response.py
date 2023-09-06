#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/TransportHandshaker.java#L229

# this is the response for the internal:tcp/handshake action

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_response import TransportResponse
from opensearch_sdk_py.transport.version import Version


class TransportHandshakerHandshakeResponse(TransportResponse):
    def __init__(self, version: Version = None) -> None:
        super().__init__()
        self.version = version

    def read_from(self, input: StreamInput) -> "TransportHandshakerHandshakeResponse":
        super().read_from(input)
        self.version = input.read_version()
        return self

    def write_to(self, output: StreamOutput) -> "TransportHandshakerHandshakeResponse":
        super().write_to(output)
        output.write_version(self.version)
        return self
