#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/opensearch-sdk-java/blob/main/src/main/java/org/opensearch/sdk/Extension.java

from typing import Optional

from opensearch_sdk_py.api.extension_point import ExtensionPoint


class Extension:
    @property
    def implemented_interfaces(self) -> list[str]:
        """
        Return a list of implemented interface (such as Extension, ActionExtension, etc.).
        """
        result = ["Extension"]
        for extension in self.extension_points:
            result.extend(extension.implemented_interfaces)
        return result

    def __init__(self, extension_points: Optional[list[ExtensionPoint]] = None) -> None:
        self.extension_points = extension_points or []
