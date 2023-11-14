#!/usr/bin/env python
#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from crud_handler import CRUDRestHandler

from opensearch_sdk_py.api.action_extension import ActionExtension
from opensearch_sdk_py.extension import Extension
from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler


class CRUDExtension(Extension, ActionExtension):
    def __init__(self) -> None:
        Extension.__init__(self, "crud-py")
        ActionExtension.__init__(self)

    @property
    def rest_handlers(self) -> list[ExtensionRestHandler]:
        return [CRUDRestHandler()]
