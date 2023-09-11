#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/opensearch-sdk-java/blob/main/src/main/java/org/opensearch/sdk/api/ActionExtension.java

from abc import ABC, abstractmethod

from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler


class ActionExtension(ABC):
    @abstractmethod
    def get_extension_rest_handlers(self) -> list[ExtensionRestHandler]:
        """
        Implementer should return a list of classes implementing ExtensionRestHandler
        """
