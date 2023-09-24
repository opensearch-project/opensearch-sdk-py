#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from abc import ABC, abstractmethod

from opensearch_sdk_py.transport.stream_output import StreamOutput


class RequestResponseHandler(ABC):
    @abstractmethod
    def send(self) -> StreamOutput:
        pass  # pragma: no cover
