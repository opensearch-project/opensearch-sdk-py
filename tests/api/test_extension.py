#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import unittest

from opensearch_sdk_py.api.extension import Extension
from opensearch_sdk_py.api.extension_point import ExtensionPoint


class TestExtension(unittest.TestCase):
    class MyExtensionPoint(ExtensionPoint):
        @property
        def implemented_interfaces(self) -> list[str]:
            return ["MyExtensionPointInterface"]

    def test_implemented_interfaces(self) -> None:
        extension = Extension([TestExtension.MyExtensionPoint()])
        self.assertListEqual(extension.implemented_interfaces, ["Extension", "MyExtensionPointInterface"])
