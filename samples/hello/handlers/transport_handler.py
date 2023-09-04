
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import (
    OutboundMessageResponse,
)
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TransportHandler():

    # TODO: set up a class to track pending request_ids. For now just hard-coding this.
    register_rest_request_id = 101  # TODO: auto-increment

    @staticmethod
    def send_response(response: OutboundMessageResponse) -> StreamOutput:
        output = StreamOutput()
        response.write_to(output)

        raw_out = output.getvalue()
        print(
            f"\nsent response id {response.get_request_id()}, {len(raw_out)} byte(s):\n\t#{raw_out}\n\t{response.tcp_header}"
        )
        return output

    @staticmethod
    def send_request(request: OutboundMessageRequest) -> StreamOutput:
        output = StreamOutput()
        request.write_to(output)

        raw_out = output.getvalue()
        print(
            f"\nsent request id {request.get_request_id()}, {len(raw_out)} byte(s):\n\t#{raw_out}\n\t{request.tcp_header}"
        )
        return output
