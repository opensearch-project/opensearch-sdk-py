#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.settings.settings import Settings
from opensearch_sdk_py.transport.environment_settings_response import EnvironmentSettingsResponse
from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput


class TestEnvironmentSettingsResponse(unittest.TestCase):
    def test_environment_settings_response(self) -> None:
        esr = EnvironmentSettingsResponse()
        self.assertIsNone(esr.environment_settings)

        settings = Settings({"foo": "bar"})
        esr = EnvironmentSettingsResponse(settings)
        self.assertEqual(esr.environment_settings.get("foo"), "bar")

        out = StreamOutput()
        esr.write_to(out)
        input = StreamInput(out.getvalue())
        esr = EnvironmentSettingsResponse().read_from(input)

        self.assertEqual(esr.environment_settings.get("foo"), "bar")
