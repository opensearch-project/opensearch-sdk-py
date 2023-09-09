#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/opensearch-sdk-java/blob/main/src/main/java/org/opensearch/sdk/rest/ExtensionRestHandler.java

from abc import ABC, abstractmethod

from opensearch_sdk_py.rest.extension_rest_request import ExtensionRestRequest
from opensearch_sdk_py.rest.extension_rest_response import ExtensionRestResponse
from opensearch_sdk_py.rest.named_route import NamedRoute


class ExtensionRestHandler(ABC):
    @abstractmethod
    def handle_request(rest_request: ExtensionRestRequest) -> ExtensionRestResponse:
        pass

    def routes(self) -> list[NamedRoute]:
        return []
