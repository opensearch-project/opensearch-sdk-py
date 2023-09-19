#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import asyncio
import unittest
from typing import Any

from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.server.async_extension_host import AsyncExtensionHost
from tests.transport.data.netty_trace_data import NettyTraceData


class TestAsyncExtensionHost(unittest.TestCase):
    class MyExtension(Extension):
        def __init__(self) -> None:
            super().__init__("hello-world")

    def setUp(self) -> None:
        self.host = AsyncExtensionHost(port=1235)
        self.extension = TestAsyncExtensionHost.MyExtension()
        self.host.serve(self.extension)

    def test_init(self) -> None:
        self.assertEqual(self.host.extension, self.extension)
        self.assertIsNotNone(self.host.request_handlers)
        self.assertEqual(len(self.host.request_handlers), 4)

    async def __client(self) -> Any:
        _, writer = await asyncio.open_connection(self.host.address, self.host.port)
        writer.write(NettyTraceData.load("tests/transport/data/transport_service_handshake_request.txt").data or b'')
        writer.write(NettyTraceData.load("tests/transport/data/initialize_extension_request.txt").data or b'')
        self.host.terminating = True

    async def __server(self) -> None:
        await self.host.async_run()

    async def __both(self) -> Any:
        return await asyncio.gather(*[self.__server(), self.__client()])

    def test_run(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__both())
