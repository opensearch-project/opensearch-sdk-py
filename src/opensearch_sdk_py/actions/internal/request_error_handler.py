#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from opensearch_sdk_py.actions.request_handler import RequestHandler
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.rest.rest_execute_on_extension_response import RestExecuteOnExtensionResponse
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.version import Version


class RequestErrorHandler(RequestHandler):
    def __init__(
        self,
        extension: Extension,
        status: RestStatus,
        content: bytes,
        content_type: str,
    ):
        self.status = status
        self.content = content
        self.content_type = content_type
        super().__init__("internal:error", extension)

    def handle(self, request: OutboundMessageRequest, input: StreamInput = None) -> StreamOutput:
        self.response = OutboundMessageResponse(
            request.thread_context_struct,
            request.features,
            RestExecuteOnExtensionResponse(
                status=self.status,
                content_type=self.content_type,
                content=self.content,
            ),
            Version(Version.MIN_COMPAT),
            request.request_id,
            request.is_handshake,
            request.is_compress,
        )
        return self.send()
