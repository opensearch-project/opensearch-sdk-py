#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/rest/NamedRoute.java

from opensearch_sdk_py.rest.rest_method import RestMethod


class NamedRoute:
    def __init__(
        self,
        method: RestMethod = None,
        path: str = "",
        unique_name: str = "",
    ):
        super().__init__()
        self.method = method
        self.path = path
        self.unique_name = unique_name

    def __str__(self) -> str:
        return f"{self.method.name} {self.path} {self.unique_name}"
