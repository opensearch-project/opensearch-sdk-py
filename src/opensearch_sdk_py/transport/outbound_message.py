#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/OutboundMessage.java

from typing import Optional

from opensearch_sdk_py.transport.network_message import NetworkMessage
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.tcp_header import TcpHeader
from opensearch_sdk_py.transport.thread_context_struct import ThreadContextStruct
from opensearch_sdk_py.transport.transport_message import TransportMessage
from opensearch_sdk_py.transport.transport_status import TransportStatus
from opensearch_sdk_py.transport.version import Version


class OutboundMessage(NetworkMessage):
    def __init__(
        self,
        thread_context: ThreadContextStruct = None,
        version: Version = None,
        status: int = TransportStatus.STATUS_REQRES,
        request_id: int = 1,
        message: TransportMessage = None,
    ):
        self._message_bytes: Optional[bytes]
        self._variable_bytes: Optional[bytes]
        self.message = message
        super().__init__(thread_context, version, status, request_id)
        if message:
            self._message_bytes = bytes(message)
            self.tcp_header.size += len(self._message_bytes)
        else:
            self._message_bytes = None
        self.tcp_header.variable_header_size = self.thread_context_struct.size
        self._variable_bytes = None
        self._write_variable_bytes()

    @property
    def variable_bytes(self) -> Optional[bytes]:
        return self._variable_bytes

    @variable_bytes.setter
    def variable_bytes(self, variable_bytes: bytes) -> None:
        if self._variable_bytes:
            self.tcp_header.size -= len(self._variable_bytes)
            self.tcp_header.variable_header_size -= len(self._variable_bytes)
        self.tcp_header.size += len(variable_bytes)
        self.tcp_header.variable_header_size += len(variable_bytes)
        self._variable_bytes = variable_bytes

    @property
    def message_bytes(self) -> Optional[bytes]:
        return self._message_bytes

    @message_bytes.setter
    def message_bytes(self, message_bytes: bytes) -> None:
        if self._message_bytes:
            self.tcp_header.size -= len(self._message_bytes)
        self.tcp_header.size += len(message_bytes)
        self._message_bytes = message_bytes

    def read_from(self, input: StreamInput, header: TcpHeader = None) -> "OutboundMessage":
        if header:
            self.tcp_header = header
        else:
            self.tcp_header.read_from(input)
        self.thread_context_struct.read_from(input)
        if self.tcp_header.variable_header_size > 0:
            self._variable_bytes = input.read_bytes(self.tcp_header.variable_header_size - self.thread_context_struct.size)
            self._read_variable_bytes()
        # TODO: read message
        return self

    def _read_variable_bytes(self) -> None:
        pass

    def _write_variable_bytes(self) -> None:
        pass

    def write_to(self, output: StreamOutput) -> "OutboundMessage":
        self.tcp_header.write_to(output)
        self.thread_context_struct.write_to(output)
        if self._variable_bytes:
            output.write(self._variable_bytes)
        if self._message_bytes:
            output.write(self._message_bytes)
        return self

    def __str__(self) -> str:
        return f"{super().__str__()}, {self.message.__str__()}"
