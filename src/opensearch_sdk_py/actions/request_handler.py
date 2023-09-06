#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import logging
from abc import ABC, abstractmethod
from typing import Optional

from opensearch_sdk_py.transport.outbound_message import OutboundMessage
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class RequestHandler(ABC):
    def __init__(self, action: str):
        self.action = action

    @abstractmethod
    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> Optional[bytes]:
        pass

    def send(self, message: OutboundMessage) -> StreamOutput:
        output = StreamOutput()
        message.write_to(output)
        raw_out = output.getvalue()
        logging.info("")
        logging.info(f"sent request id {message.get_request_id()}, {len(raw_out)} byte(s):\n  #{raw_out}\n  {message.tcp_header}")
        return output
