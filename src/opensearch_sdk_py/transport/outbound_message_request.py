#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/OutboundMessage.java#L122

from opensearch_sdk_py.transport.outbound_message import OutboundMessage
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.thread_context_struct import ThreadContextStruct
from opensearch_sdk_py.transport.transport_message import TransportMessage
from opensearch_sdk_py.transport.version import Version


class OutboundMessageRequest(OutboundMessage):
    def __init__(
        self,
        thread_context: ThreadContextStruct = None,
        features: list[str] = [],
        message: TransportMessage = None,
        version: Version = None,
        action: str = "",
        request_id: int = 1,
        is_handshake: bool = False,
        is_compress: bool = False,
    ) -> None:
        self.features = features
        self.action = action
        super().__init__(thread_context, version, 0, request_id, message)
        if is_handshake:
            self.tcp_header.set_handshake()
        if is_compress:
            self.tcp_header.set_compress()

    def _read_variable_bytes(self) -> None:
        variable_stream = StreamInput(self.variable_bytes)
        self.features = variable_stream.read_string_array()
        self.action = variable_stream.read_string()

    def _write_variable_bytes(self) -> None:
        output = StreamOutput()
        output.write_string_array(self.features)
        output.write_string(self.action)
        self.variable_bytes = output.getvalue()

    def __str__(self) -> str:
        return f"{super().__str__()}, features={self.features}, action={self.action}"
