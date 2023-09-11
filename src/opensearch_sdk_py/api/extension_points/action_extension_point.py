#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/opensearch-sdk-java/blob/main/src/main/java/org/opensearch/sdk/api/ActionExtension.java

from typing import Optional

from opensearch_sdk_py.api.extension_point import ExtensionPoint
from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler
from opensearch_sdk_py.rest.extension_rest_handlers import ExtensionRestHandlers


class ActionExtensionPoint(ExtensionPoint):
    @property
    def implemented_interfaces(self) -> list[str]:
        return ["ActionExtension"]

    def __init__(self, rest_handlers: Optional[list[ExtensionRestHandler]] = None) -> None:
        super().__init__()
        if rest_handlers:
            for handler in rest_handlers:
                ExtensionRestHandlers().register(handler)
