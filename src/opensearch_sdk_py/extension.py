#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/opensearch-sdk-java/blob/main/src/main/java/org/opensearch/sdk/Extension.java


class Extension:
    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def implemented_interfaces(self) -> list[str]:
        result = []
        for cls in self.__class__.__bases__:
            result.append(cls.__name__)
        return result
