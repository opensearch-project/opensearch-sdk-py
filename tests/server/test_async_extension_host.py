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
from typing import Any, Optional

from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.server.async_extension_host import AsyncExtensionHost
from opensearch_sdk_py.transport.outbound_message_request import OutboundMessageRequest
from opensearch_sdk_py.transport.version import Version
from tests.transport.data.netty_trace_data import NettyTraceData


class TestAsyncExtensionHost(unittest.TestCase):
    class MyExtension(Extension):
        def __init__(self) -> None:
            super().__init__("hello-world")

    def setUp(self) -> None:
        self.host = AsyncExtensionHost()
        self.extension = TestAsyncExtensionHost.MyExtension()
        self.host.serve(self.extension)
        self.loop = asyncio.get_event_loop()

    def test_init(self) -> None:
        self.assertEqual(self.host.extension, self.extension)
        self.assertIsNotNone(self.host.request_handlers)
        self.assertEqual(len(self.host.request_handlers), 4)

    async def __client(self, datas: list[Optional[bytes]]) -> Any:
        logging.info(f"connecting to {self.host.port}")
        _, writer = await asyncio.open_connection(self.host.address, self.host.port)
        for data in datas:
            if data:
                writer.write(data)
        self.host.terminating = True

    async def __server(self) -> None:
        await self.host.async_run()

    async def __both(self, datas: list[Optional[bytes]]) -> Any:
        return await asyncio.gather(*[self.__server(), self.__client(datas)])

    def test_run(self) -> None:
        self.loop.run_until_complete(self.__both([NettyTraceData.load("tests/transport/data/transport_service_handshake_request.txt").data, NettyTraceData.load("tests/transport/data/initialize_extension_request.txt").data]))
        self.assertIsNotNone(self.host.port)
        self.assertGreater(self.host.port, 0)

    def test_run_error(self) -> None:
        self.loop.run_until_complete(self.__both([NettyTraceData.load("tests/transport/data/transport_service_handshake_request.txt").data, bytes(OutboundMessageRequest(version=Version(2100099), action="internal:invalid"))]))
        self.assertIsNotNone(self.host.port)
        self.assertGreater(self.host.port, 0)
