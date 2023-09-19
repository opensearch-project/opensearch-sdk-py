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
from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse


class ActionExtension:
    @property
    @abstractmethod
    def rest_handlers(self) -> list[ExtensionRestHandler]:
        pass  # pragma: no cover

    @property
    def named_routes(self) -> list[str]:
        return self.extension_rest_handlers.named_routes or []

    def __init__(self) -> None:
        self.extension_rest_handlers = ExtensionRestHandlers()
        for handler in self.rest_handlers or []:
            self.extension_rest_handlers.register(handler)

    def handle(self, route: str, request: ExtensionRestRequest) -> ExtensionRestResponse:
        return self.extension_rest_handlers.handle(route, request)
