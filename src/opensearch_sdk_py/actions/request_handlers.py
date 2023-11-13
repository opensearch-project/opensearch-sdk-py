#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from typing import Dict, Optional

from opensearch_sdk_py.actions.request_handler import RequestHandler
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.stream_input import StreamInput


class RequestHandlers(Dict[str, RequestHandler]):
    def __init__(self, extension: Extension) -> None:
        self.extension = extension

    def register(self, handler: RequestHandler) -> None:
        self[handler.action] = handler

    def handle(self, request: OutboundMessageRequest, input: StreamInput = None) -> Optional[bytes]:
        handler = self.get(request.action, None)
        return handler.handle(request, input) if handler else None
