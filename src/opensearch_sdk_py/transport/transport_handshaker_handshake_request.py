#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# this is the request for the internal:tcp/handshake action

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_request import TransportRequest
from opensearch_sdk_py.transport.version import Version


class TransportHandshakerHandshakeRequest(TransportRequest):
    def __init__(self, version: Version = None):
        super().__init__()
        self.version = version

    def read_from(self, input: StreamInput) -> "TransportHandshakerHandshakeRequest":
        super().read_from(input)
        input.read_v_int()
        self.version = input.read_version()
        return self

    def write_to(self, output: StreamOutput) -> "TransportHandshakerHandshakeRequest":
        super().write_to(output)
        StreamOutput()
        if self.version:
            output.write_v_int(StreamOutput.version_size(self.version))
            output.write_version(self.version)
        return self

    def __str__(self) -> str:
        return f"version={self.version.__str__()}"
