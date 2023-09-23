#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import logging

from opensearch_sdk_py.actions.request_response_handler import RequestResponseHandler
from opensearch_sdk_py.actions.response_handler import ResponseHandler
from opensearch_sdk_py.transport.acknowledged_response import AcknowledgedResponse
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class RegisterRestActionsResponseHandler(ResponseHandler):
    def __init__(self, next_handler: RequestResponseHandler) -> None:
        self.next_handler = next_handler

    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> StreamOutput:
        ack_response = AcknowledgedResponse().read_from(input)
        logging.debug(f"< {ack_response}")
        if ack_response.status:
            self.next_handler.send()
        # TODO error handling
