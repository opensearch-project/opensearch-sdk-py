#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from opensearch_sdk_py.actions.internal.request_error_handler import RequestErrorHandler
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest


class ActionNotFoundRequestErrorHandler(RequestErrorHandler):
    def __init__(self, extension: Extension, request: OutboundMessageRequest) -> None:
        super().__init__(extension, RestStatus.NOT_FOUND, bytes(f'{{"error": "No handler found for {request.action}"}}', "utf-8"), ExtensionRestResponse.JSON_CONTENT_TYPE)
