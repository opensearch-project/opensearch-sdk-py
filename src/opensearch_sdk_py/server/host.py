#!/usr/bin/env python
#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from abc import ABC, abstractmethod


class Host(ABC):
    def __init__(self, address: str = "localhost", port: int = 1234) -> None:
        self.address = address
        self.port = port

    @abstractmethod
    def run(self) -> None:
        pass  # pragma: no cover
