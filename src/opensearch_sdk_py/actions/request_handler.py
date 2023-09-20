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

from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.transport.outbound_message import OutboundMessage
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class RequestHandler(ABC):
    def __init__(self, action: str, extension: Extension):
        self.action = action
        self.extension = extension

    @abstractmethod
    def handle(self, request: OutboundMessageRequest, input: StreamInput) -> Optional[bytes]:
        pass  # pragma: no cover

    def send(self, message: OutboundMessage) -> StreamOutput:
        output = StreamOutput()
        message.write_to(output)
        raw_out = output.getvalue()
        logging.info(f"> {message.__str__()}, size={len(raw_out)} byte(s)")
        logging.debug(f"> #{raw_out}")
        return output
