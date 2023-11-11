#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from typing import Dict, Optional

from opensearch_sdk_py.actions.response_handler import ResponseHandler
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput


class ResponseHandlers(Dict[int, ResponseHandler]):
    def __init__(self, extension: Extension) -> None:
        self.extension = extension

    def register(self, request_id: int, handler: ResponseHandler) -> None:
        self[request_id] = handler

    def handle(self, response: OutboundMessageResponse, input: StreamInput = None) -> Optional[bytes]:
        if response.request_id in self:
            handler = self[response.request_id]
            del self[response.request_id]
            return handler.handle(response, input) if handler else None
        return None
