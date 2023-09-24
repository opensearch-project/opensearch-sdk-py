#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import logging
from abc import abstractmethod
from typing import Optional

from opensearch_sdk_py.actions.request_response_handler import RequestResponseHandler
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class ResponseHandler(RequestResponseHandler):
    @abstractmethod
    def handle(self, response: OutboundMessageResponse, input: StreamInput = None) -> Optional[bytes]:
        pass  # pragma: no cover

    def send(self, request: OutboundMessageRequest) -> StreamOutput:
        output = StreamOutput()
        request.write_to(output)
        raw_out = output.getvalue()
        logging.info(f"> {request.__str__()}, size={len(raw_out)} byte(s)")
        logging.debug(f"> #{raw_out}")
        return output
