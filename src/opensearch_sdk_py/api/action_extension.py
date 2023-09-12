#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/opensearch-sdk-java/blob/main/src/main/java/org/opensearch/sdk/api/ActionExtension.java

from abc import abstractmethod

from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler
from opensearch_sdk_py.rest.extension_rest_handlers import ExtensionRestHandlers


class ActionExtension:
    @property
    @abstractmethod
    def rest_handlers(self) -> list[ExtensionRestHandler]:
        pass

    def __init__(self) -> None:
        super().__init__()
        for handler in self.rest_handlers or []:
            ExtensionRestHandlers().register(handler)
