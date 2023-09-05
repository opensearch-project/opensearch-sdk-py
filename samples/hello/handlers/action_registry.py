from handlers.extension_init_handler import ExtensionInitHandler
from handlers.extension_rest_request_handler import ExtensionRestRequestHandler
from handlers.handshake_handler import HandshakeHandler

from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import (
    OutboundMessageResponse,
)
from opensearch_sdk_py.transport.stream_input import StreamInput


class ActionRegistry():

    REQUEST_HANDLERS = {
        "internal:tcp/handshake": (HandshakeHandler, "handle_tcp_handshake"),
        "internal:transport/handshake": (HandshakeHandler, "handle_transport_handshake"),
        "internal:discovery/extensions": (ExtensionInitHandler, "handle_init_request"),
        "internal:extensions/restexecuteonextensiontaction": (ExtensionRestRequestHandler, "handle_rest_request")
    }

    # TODO: This needs to be dynamic, added to when we send a request, and removed from when we get a response
    # The key for this dict needs to be an auto-incrementing long int for request id
    RESPONSE_HANDLERS = {
        ExtensionInitHandler.REGISTER_REST_REQUEST_ID: (ExtensionInitHandler, "handle_register_rest_response"),
    }

    @staticmethod
    def handle_request(request: OutboundMessageRequest, input: StreamInput):
        request_handler = ActionRegistry.REQUEST_HANDLERS[request.action]
        if request_handler:
            output = getattr(request_handler[0], request_handler[1])(request, input)
        else:
            output = None
        return output

    @staticmethod
    def handle_response(response: OutboundMessageResponse, input: StreamInput):
        response_handler = ActionRegistry.RESPONSE_HANDLERS[response.get_request_id()]
        if response_handler:
            output = getattr(response_handler[0], response_handler[1])(response, input)
        else:
            output = None
        return output
