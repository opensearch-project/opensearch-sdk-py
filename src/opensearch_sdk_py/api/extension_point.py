#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from abc import ABC, abstractmethod


class ExtensionPoint(ABC):
    @property
    @abstractmethod
    def implemented_interfaces(self) -> list[str]:
        """
        Return a list of implemented interface (such as Extension, ActionExtension, etc.).
        """
