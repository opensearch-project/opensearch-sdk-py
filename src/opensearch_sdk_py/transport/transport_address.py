#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import ipaddress
from typing import Optional

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TransportAddress(ipaddress.IPv4Address):
    def __init__(self, address: str = "0.0.0.0", port: int = 0, host_name: Optional[str] = None) -> None:
        self.address = ipaddress.IPv4Address(address)
        self.host_name = host_name if host_name else str(self.address)
        self.port = port

    def read_from(self, input: StreamInput) -> "TransportAddress":
        addr_bytes = input.read_byte()
        if addr_bytes != 4:
            raise Exception("Invalid address byte size")
        self.address = ipaddress.IPv4Address(input.read_int())
        self.host_name = input.read_string()
        self.port = input.read_int()
        return self

    def write_to(self, output: StreamOutput) -> "TransportAddress":
        output.write_byte(4)
        output.write_int(int(self.address))
        output.write_string(self.host_name)
        output.write_int(self.port)
        return self
