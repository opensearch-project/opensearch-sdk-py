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
from unittest.mock import patch

from opensearch_sdk_py.server.async_host import AsyncHost
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestAsyncHost(unittest.TestCase):
    class MyAsyncHost(AsyncHost):
        def on_input(self, input: StreamInput) -> StreamOutput:
            command = input.read_string()
            if command == "QUIT":
                self.terminating = True
            response = StreamOutput()
            response.write_string("OK")
            return response

    def setUp(self) -> None:
        self.host = TestAsyncHost.MyAsyncHost()

    def test_init(self) -> None:
        self.assertEqual(self.host.address, "localhost")
        self.assertEqual(self.host.port, 1234)

    @patch("opensearch_sdk_py.server.async_host.AsyncHost.async_run")
    def test_run_calls_async_run(self, mock_async_run: Any) -> None:
        self.host.run()
        self.assertTrue(mock_async_run.called)

    async def __client(self) -> Any:
        reader, writer = await asyncio.open_connection(self.host.address, self.host.port)
        output = StreamOutput()
        output.write_string("QUIT")
        writer.write(output.getvalue())
        response = StreamInput(await reader.read())
        return response.read_string()

    async def __server(self) -> None:
        await self.host.async_run()

    async def __both(self) -> Any:
        return await asyncio.gather(*[self.__server(), self.__client()])

    def test_run(self) -> None:
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(self.__both())
        self.assertEqual(results[1], "OK")
        loop.close()
