#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/opensearch-sdk-java/blob/main/src/main/java/org/opensearch/sdk/Extension.java

from abc import ABC, abstractmethod


class Extension(ABC):
    @property
    @abstractmethod
    def implemented_interfaces(self) -> list[tuple]:
        """
        Implementer should return a list of tuples containing the implemented interface (such as
        Extension, ActionExtension, etc.) and the implementing class.
        """
