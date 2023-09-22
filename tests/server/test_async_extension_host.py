#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import asyncio
import logging
import unittest
from typing import Optional

from opensearch_sdk_py.api.action_extension import ActionExtension
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.rest_execute_on_extension_response import RestExecuteOnExtensionResponse
from opensearch_sdk_py.rest.rest_status import RestStatus
from opensearch_sdk_py.server.async_extension_host import AsyncExtensionHost
from opensearch_sdk_py.transport.acknowledged_response import AcknowledgedResponse
from opensearch_sdk_py.transport.initialize_extension_response import InitializeExtensionResponse
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.outbound_message_response import OutboundMessageResponse
from opensearch_sdk_py.transport.register_rest_actions_request import RegisterRestActionsRequest
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.tcp_header import TcpHeader
from opensearch_sdk_py.transport.version import Version
from tests.transport.data.netty_trace_data import NettyTraceData


class TestAsyncExtensionHost(unittest.TestCase):
    class MyActionExtension(Extension, ActionExtension):
        def __init__(self) -> None:
            Extension.__init__(self, "hello-world")
            ActionExtension.__init__(self)

        @property
        def rest_handlers(self) -> list[ExtensionRestHandler]:
            return []

    class Response:
        header: TcpHeader
        response: OutboundMessageResponse
        remaining_input: StreamInput

    def setUp(self) -> None:
        self.host = AsyncExtensionHost()
        self.extension = TestAsyncExtensionHost.MyActionExtension()
        self.extension.init_response_request_id = 42
        self.host.serve(self.extension)
        self.loop = asyncio.get_event_loop()

    def test_init(self) -> None:
        self.assertEqual(self.host.extension, self.extension)
        self.assertIsNotNone(self.host.request_handlers)
        self.assertEqual(len(self.host.request_handlers), 4)

    async def __client(self, datas: list[Optional[bytes]]) -> list[Optional["TestAsyncExtensionHost.Response"]]:
        logging.info(f"connecting to {self.host.port}")
        reader, writer = await asyncio.open_connection(self.host.address, self.host.port)
        responses: list[Optional[TestAsyncExtensionHost.Response]] = []
        for i in range(len(datas)):
            # signal termination before sending the last message to avoid host blocking on next read
            if i == len(datas) - 1:
                self.host.terminating = True
            data = datas[i]
            if data:
                writer.write(data)
            response = TestAsyncExtensionHost.Response()
            reply = await reader.read(TcpHeader.HEADER_SIZE)
            if len(reply) < TcpHeader.HEADER_SIZE:
                responses.append(None)
            else:
                response.header = TcpHeader().read_from(StreamInput(reply))
                logging.info(f"* {response.header}")
                response.remaining_input = StreamInput(await reader.read(response.header.size))
                logging.info(f"* + {len(response.remaining_input.raw)} byte(s)")
                response.response = OutboundMessageResponse().read_from(response.remaining_input, response.header)
                responses.append(response)
        self.host.terminating = True
        return responses

    async def __server(self) -> None:
        await self.host.async_run()

    async def __both(self, datas: list[Optional[bytes]]) -> list["TestAsyncExtensionHost.Response"]:
        results = await asyncio.gather(*[self.__server(), self.__client(datas)])
        client_result: list[TestAsyncExtensionHost.Response] = results[1]
        return client_result

    def test_assigns_port(self) -> None:
        request = NettyTraceData.load("tests/transport/data/transport_service_handshake_request.txt").data
        self.loop.run_until_complete(self.__both([request]))
        self.assertIsNotNone(self.host.port)
        self.assertGreater(self.host.port, 0)

    def test_discovery_extensions_request(self) -> None:
        request1 = NettyTraceData.load("tests/transport/data/transport_service_handshake_request.txt").data
        request2 = NettyTraceData.load("tests/transport/data/initialize_extension_request.txt").data
        responses = self.loop.run_until_complete(self.__both([request1, request2]))
        self.assertEqual(len(responses), 2)
        reply: TestAsyncExtensionHost.Response = responses[1]
        self.assertEqual(reply.response.thread_context_struct.request_headers, {"_system_index_access_allowed": "false"})
        discovery_extensions_response = RegisterRestActionsRequest().read_from(reply.remaining_input)
        self.assertEqual(discovery_extensions_response.rra.identity.uniqueId, "hello-world")

    def test_run_unhandled_request_error(self) -> None:
        request1 = NettyTraceData.load("tests/transport/data/transport_service_handshake_request.txt").data
        request2 = bytes(OutboundMessageRequest(version=Version(2100099), action="internal:invalid"))
        responses = self.loop.run_until_complete(self.__both([request1, request2]))
        self.assertEqual(len(responses), 2)
        reply: TestAsyncExtensionHost.Response = responses[1]
        self.assertEqual(reply.response.thread_context_struct.request_headers, {})
        extension_initialization_response_error = RestExecuteOnExtensionResponse().read_from(reply.remaining_input)
        self.assertEqual(extension_initialization_response_error.status, RestStatus.NOT_FOUND)
        self.assertEqual(extension_initialization_response_error.content_type, ExtensionRestResponse.JSON_CONTENT_TYPE)
        self.assertEqual(extension_initialization_response_error.headers, {})
        self.assertEqual(extension_initialization_response_error.content, b'{"error": "No handler found for internal:invalid"}')

    def test_acknowledged_response(self) -> None:
        request1 = NettyTraceData.load("tests/transport/data/transport_service_handshake_request.txt").data
        request2 = bytes(OutboundMessageResponse(version=Version(2100099), message=AcknowledgedResponse(True)))
        responses = self.loop.run_until_complete(self.__both([request1, request2]))
        self.assertEqual(len(responses), 2)
        reply: TestAsyncExtensionHost.Response = responses[1]
        self.assertEqual(reply.response.thread_context_struct.request_headers, {})
        init_response = InitializeExtensionResponse().read_from(reply.remaining_input)
        self.assertEqual(init_response.name, "hello-world")

    def test_error_response(self) -> None:
        request1 = NettyTraceData.load("tests/transport/data/transport_service_handshake_request.txt").data
        request2 = OutboundMessageResponse(version=Version(2100099))
        request2.tcp_header.is_error = True
        responses = self.loop.run_until_complete(self.__both([request1, bytes(request2)]))
        self.assertEqual(len(responses), 2)
        self.assertIsNotNone(responses[0])
        self.assertIsNone(responses[1])
