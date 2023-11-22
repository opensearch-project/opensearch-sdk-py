#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/env/EnvironmentSettingsResponse.java

from opensearch_sdk_py.settings.settings import Settings
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.transport_response import TransportResponse


class EnvironmentSettingsResponse(TransportResponse):
    def __init__(self, environment_settings: Settings = None):
        super().__init__()
        self.environment_settings = environment_settings

    def read_from(self, input: StreamInput) -> "EnvironmentSettingsResponse":
        super().read_from(input)
        self.environment_settings = Settings().read_from(input)
        return self

    def write_to(self, output: StreamOutput) -> "EnvironmentSettingsResponse":
        super().write_to(output)
        self.environment_settings.write_to(output)
        return self
