#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/TcpHeader.java

import itertools
from typing import Optional

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_status import TransportStatus
from opensearch_sdk_py.transport.version import Version


class TcpHeader:
    MARKER_BYTES_SIZE = 2
    MESSAGE_LENGTH_SIZE = 4
    REQUEST_ID_SIZE = 8
    STATUS_SIZE = 1
    VERSION_ID_SIZE = 4
    VARIABLE_HEADER_SIZE = 4
    BYTES_REQUIRED_FOR_MESSAGE_SIZE = MARKER_BYTES_SIZE + MESSAGE_LENGTH_SIZE
    VERSION_POSITION = MARKER_BYTES_SIZE + MESSAGE_LENGTH_SIZE + REQUEST_ID_SIZE + STATUS_SIZE
    VARIABLE_HEADER_SIZE_POSITION = VERSION_POSITION + VERSION_ID_SIZE
    PRE_76_HEADER_SIZE = VERSION_POSITION + VERSION_ID_SIZE
    BYTES_REQUIRED_FOR_VERSION = PRE_76_HEADER_SIZE
    HEADER_SIZE = PRE_76_HEADER_SIZE + VARIABLE_HEADER_SIZE
    MESSAGE_SIZE = HEADER_SIZE - BYTES_REQUIRED_FOR_MESSAGE_SIZE

    id_iter = itertools.count()

    def __init__(
        self,
        prefix: bytes = b"ES",
        request_id: Optional[int] = None,
        status: int = 0,
        version: Version = Version.CURRENT,
        size: int = MESSAGE_SIZE,
        variable_header_size: int = 0,
    ) -> None:
        self.prefix = prefix
        self.request_id = request_id if request_id else next(self.id_iter)
        self.status = status
        self.version = version
        self.size = size
        self.variable_header_size = variable_header_size

    def read_from(self, input: StreamInput) -> "TcpHeader":
        self.prefix = input.read_bytes(2)
        self.size = input.read_int()
        self.request_id = input.read_long()
        self.status = input.read_byte()
        self.version = Version()
        self.version.from_bytes(input.read_bytes(4))  # always 4 bytes big-endian
        self.variable_header_size = input.read_int()
        return self

    def write_to(self, output: StreamOutput) -> "TcpHeader":
        output.write(self.prefix)
        output.write_int(self.size)
        output.write_long(self.request_id)
        output.write_byte(self.status)
        output.write(bytes(self.version))  # always 4 bytes big-endian
        output.write_int(self.variable_header_size)
        return self

    def __str__(self) -> str:
        return f"prefix={self.prefix!r}, version={self.version}, type={self.statuses}, message={self.size} byte(s), id={self.request_id}"

    @property
    def is_response(self) -> bool:
        return self.__is_status(TransportStatus.STATUS_REQRES)

    @is_response.setter
    def is_response(self, value: bool) -> None:
        self.__set_status(TransportStatus.STATUS_REQRES, value)

    @property
    def is_request(self) -> bool:
        return not self.is_response

    @is_request.setter
    def is_request(self, value: bool) -> None:
        self.__set_status(TransportStatus.STATUS_REQRES, not value)

    @property
    def is_error(self) -> bool:
        return self.__is_status(TransportStatus.STATUS_ERROR)

    @is_error.setter
    def is_error(self, value: bool) -> None:
        self.__set_status(TransportStatus.STATUS_ERROR, value)

    @property
    def is_compress(self) -> bool:
        return self.__is_status(TransportStatus.STATUS_COMPRESS)

    @is_compress.setter
    def is_compress(self, value: bool) -> None:
        self.__set_status(TransportStatus.STATUS_COMPRESS, value)

    @property
    def is_handshake(self) -> bool:
        return self.__is_status(TransportStatus.STATUS_HANDSHAKE)

    @is_handshake.setter
    def is_handshake(self, value: bool) -> None:
        self.__set_status(TransportStatus.STATUS_HANDSHAKE, value)

    @property
    def statuses(self) -> list[str]:
        result = []
        if self.is_request:
            result.append("request")
        else:
            result.append("response")
        if self.is_error:
            result.append("error")
        if self.is_compress:
            result.append("compressed")
        if self.is_handshake:
            result.append("handshake")
        return result

    def __is_status(self, flag: int) -> bool:
        return bool((self.status & flag) != 0)

    def __set_status(self, flag: int, value: bool) -> None:
        if value:
            self.status |= flag
        else:
            self.status &= ~flag
