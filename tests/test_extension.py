#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.api.action_extension import ActionExtension
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler


class TestExtension(unittest.TestCase):
    class MyExtension(Extension, ActionExtension):
        @property
        def rest_handlers(self) -> list[ExtensionRestHandler]:
            return []

    def test_implemented_interfaces(self) -> None:
        extension = TestExtension.MyExtension()
        self.assertListEqual(extension.implemented_interfaces, ["Extension", "ActionExtension"])
        self.assertListEqual(extension.rest_handlers, [])
