#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/OutboundMessage.java#L168

from opensearch_sdk_py.transport.outbound_message import OutboundMessage
from opensearch_sdk_py.transport.thread_context_struct import ThreadContextStruct
from opensearch_sdk_py.transport.transport_message import TransportMessage
from opensearch_sdk_py.transport.version import Version


class OutboundMessageResponse(OutboundMessage):
    def __init__(
        self,
        thread_context: ThreadContextStruct = None,
        features: list[str] = [],
        message: TransportMessage = None,
        version: Version = None,
        request_id: int = 1,
        is_handshake: bool = False,
        is_compress: bool = False,
    ):
        self.features = features
        super().__init__(thread_context, version, 1, request_id, message)
        if is_handshake:
            self.tcp_header.set_handshake()
        if is_compress:
            self.tcp_header.set_compress()
