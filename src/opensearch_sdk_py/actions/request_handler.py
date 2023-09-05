import logging
from abc import ABC, abstractmethod

from opensearch_sdk_py.transport.outbound_message import OutboundMessage
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class RequestHandler(ABC):
    def __init__(self, action: str):
        self.action = action

    @abstractmethod
    def handle(self, request: OutboundMessageRequest, input: StreamInput):
        pass

    def send(self, message: OutboundMessage) -> StreamOutput:
        output = StreamOutput()
        message.write_to(output)
        raw_out = output.getvalue()
        logging.info(f"\nsent request id {message.get_request_id()}, {len(raw_out)} byte(s):\n\t#{raw_out}\n\t{message.tcp_header}")
        return output
