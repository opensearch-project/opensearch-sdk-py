#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from typing import Dict, Optional

from opensearch_sdk_py.actions.internal.discovery_extensions_request_handler import DiscoveryExtensionsRequestHandler
from opensearch_sdk_py.actions.internal.extension_rest_request_handler import ExtensionRestRequestHandler
from opensearch_sdk_py.actions.internal.tcp_handshake_request_handler import TcpHandshakeRequestHandler
from opensearch_sdk_py.actions.internal.transport_handshake_request_handler import TransportHandshakeRequestHandler
from opensearch_sdk_py.actions.request_handler import RequestHandler
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput


class RequestHandlers(Dict[str, RequestHandler]):
    _singleton = None

    def __new__(cls):  # type:ignore
        if cls._singleton is None:
            cls._singleton = super(RequestHandlers, cls).__new__(cls)
        return cls._singleton

    def register(self, klass: RequestHandler) -> None:
        instance = klass()
        self[instance.action] = instance

    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> Optional[bytes]:
        handler = self[request.action]
        return handler.handle(request, input) if handler else None


RequestHandlers().register(DiscoveryExtensionsRequestHandler)
RequestHandlers().register(ExtensionRestRequestHandler)
RequestHandlers().register(TcpHandshakeRequestHandler)
RequestHandlers().register(TransportHandshakeRequestHandler)
