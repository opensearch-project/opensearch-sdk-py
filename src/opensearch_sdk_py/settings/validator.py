#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#


from abc import abstractmethod

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class Validator:
    @abstractmethod
    def validate(self) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def read_from(self, input: StreamInput) -> "Validator":
        pass  # pragma: no cover

    @abstractmethod
    def write_to(self, output: StreamOutput) -> "Validator":
        pass  # pragma: no cover
