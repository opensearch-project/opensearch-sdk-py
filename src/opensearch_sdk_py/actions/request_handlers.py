from typing import Dict

from opensearch_sdk_py.actions.internal.discovery_extensions_request_handler import DiscoveryExtensionsRequestHandler
from opensearch_sdk_py.actions.internal.extensions_restexecuteonextensiontaction_handler import ExtensionRestRequestHandler
from opensearch_sdk_py.actions.internal.tcp_handshake_request_handler import TcpHandshakeRequestHandler
from opensearch_sdk_py.actions.internal.transport_handshake_request_handler import TransportHandshakeRequestHandler
from opensearch_sdk_py.actions.request_handler import RequestHandler
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput


class RequestHandlers(Dict[str, RequestHandler]):
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(RequestHandlers, cls).__new__(cls)
        return cls._singleton

    def register(self, klass):
        instance = klass()
        self[instance.action] = instance

    def handle(self, request: OutboundMessageRequest, input: StreamInput):
        handler = self[request.action]
        if handler:
            output = handler.handle(request, input)
        else:
            output = None
        return output


RequestHandlers().register(DiscoveryExtensionsRequestHandler)
RequestHandlers().register(ExtensionRestRequestHandler)
RequestHandlers().register(TcpHandshakeRequestHandler)
RequestHandlers().register(TransportHandshakeRequestHandler)
