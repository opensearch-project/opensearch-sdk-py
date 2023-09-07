#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/NetworkMessage.java


from typing import Optional

from opensearch_sdk_py.transport.tcp_header import TcpHeader
from opensearch_sdk_py.transport.thread_context_struct import ThreadContextStruct
from opensearch_sdk_py.transport.transport_status import TransportStatus
from opensearch_sdk_py.transport.version import Version


class NetworkMessage:
    def __init__(
        self,
        thread_context: ThreadContextStruct = None,
        version: Version = None,
        status: int = TransportStatus.STATUS_REQRES,
        request_id: Optional[int] = None,
    ) -> None:
        self.thread_context_struct = thread_context if thread_context else ThreadContextStruct()
        self.tcp_header = TcpHeader(version=version, status=status, request_id=request_id)
        self.tcp_header.size += self.thread_context_struct.size

    @property
    def version(self) -> Version:
        return self.tcp_header.version

    @property
    def request_id(self) -> int:
        return int(self.tcp_header.request_id)

    @property
    def is_request(self) -> bool:
        return bool(self.tcp_header.is_request)

    @property
    def is_response(self) -> bool:
        return not bool(self.tcp_header.is_request)

    @property
    def is_error(self) -> bool:
        return bool(self.tcp_header.is_error)

    @property
    def is_compress(self) -> bool:
        return bool(self.tcp_header.is_compress)

    @property
    def is_handshake(self) -> bool:
        return bool(self.tcp_header.is_handshake)

    def __str__(self) -> str:
        return f"{self.tcp_header}, ctx={self.thread_context_struct}"
