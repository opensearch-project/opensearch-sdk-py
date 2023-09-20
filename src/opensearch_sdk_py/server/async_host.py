#!/usr/bin/env python
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
import socket
from abc import abstractmethod
from typing import Any

from opensearch_sdk_py.server.host import Host
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class AsyncHost(Host):
    def run(self) -> None:
        asyncio.run(self.async_run())

    async def async_run(self) -> None:
        self.terminating = False
        self.server = self.__listen()
        loop = asyncio.get_event_loop()
        logging.info(f"< server={self.server}")
        while not self.terminating:
            try:
                self.future = asyncio.ensure_future(loop.sock_accept(self.server))
                conn = (await self.future)[0]
                conn.setblocking(False)
                logging.debug(f"< connection={conn}")
                loop.create_task(self.on_connection(conn))
            except asyncio.exceptions.CancelledError:
                pass

    async def on_connection(self, conn: Any) -> None:
        try:
            loop = asyncio.get_event_loop()
            while raw := await loop.sock_recv(conn, 1024 * 10):
                input = StreamInput(raw)
                logging.debug(f"< #{str(raw)}, size={len(raw)} byte(s)")
                output = self.on_input(input)
                if output:
                    data = output.getvalue()
                    logging.debug(f"> #{str(data)}, size={len(data)} byte(s)")
                    await loop.sock_sendall(conn, data)
                if self.terminating:
                    logging.debug("| terminating")
                    self.future.cancel()
                    break
        # except Exception as ex:
        #     logging.exception(ex)
        finally:
            conn.close()

    def __listen(self) -> socket.socket:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.address, self.port))
        server.setblocking(False)
        server.listen()
        return server

    @abstractmethod
    def on_input(self, input: StreamInput) -> StreamOutput:
        pass  # pragma: no cover
