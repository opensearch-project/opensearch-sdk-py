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
from typing import Any
from unittest.mock import patch

from opensearch_sdk_py.server.async_host import AsyncHost
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestAsyncHost(unittest.TestCase):
    class MyAsyncHost(AsyncHost):
        def on_input(self, input: StreamInput) -> StreamOutput:
            while True:
                command = input.read_string()
                if command == "PASS":
                    pass
                elif command == "EXCEPTION":
                    self.terminating = True
                    raise Exception(command)
                elif command == "QUIT":
                    self.terminating = True
                    response = StreamOutput()
                    response.write_string("OK")
                    return response

    def setUp(self) -> None:
        self.host = TestAsyncHost.MyAsyncHost()
        self.loop = asyncio.get_event_loop()

    def test_init(self) -> None:
        self.assertEqual(self.host.address, "localhost")
        self.assertIsNone(self.host.port)

    @patch("opensearch_sdk_py.server.async_host.AsyncHost.async_run")
    def test_run_calls_async_run(self, mock_async_run: Any) -> None:
        self.host.run()
        self.assertTrue(mock_async_run.called)

    async def __client(self, commands: list[str]) -> Any:
        reader, writer = await asyncio.open_connection(self.host.address, self.host.port)
        responses = []
        for command in commands:
            output = StreamOutput()
            output.write_string(command)
            logging.info(f"> {command}")
            writer.write(output.getvalue())
        reply = await reader.read()
        if len(reply) > 0:
            response = StreamInput(reply)
            responses.append(response.read_string())
        return responses

    async def __server(self) -> None:
        await self.host.async_run()

    async def __both(self, commands: list[str]) -> Any:
        return await asyncio.gather(*[self.__server(), self.__client(commands)])

    def test_run(self) -> None:
        results = self.loop.run_until_complete(self.__both(["PASS", "QUIT"]))
        self.assertEqual(results[1], ["OK"])

    def test_handle_error(self) -> None:
        results = self.loop.run_until_complete(self.__both(["EXCEPTION"]))
        self.assertEqual(results[1], [])
