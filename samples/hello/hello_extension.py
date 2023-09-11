#!/usr/bin/env python
#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from hello_rest_handler import HelloRestHandler

from opensearch_sdk_py.api.action_extension import ActionExtension
from opensearch_sdk_py.api.extension import Extension
from opensearch_sdk_py.rest.extension_rest_handler import ExtensionRestHandler


class HelloExtension(Extension, ActionExtension):
    @property
    def implemented_interfaces(self) -> list[tuple]:
        # TODO: This is lazy and temporary.
        # Really we should be using this class to call some SDK class run(),
        # passing an instance of ourself to the SDK and letting it parse out
        # the superclass names with class.__mro__ and calling the appropriate
        # implemented functions from the interfaces.
        return [("Extension", self), ("ActionExtension", self)]

    @property
    def extension_rest_handlers(self) -> list[ExtensionRestHandler]:
        return [HelloRestHandler()]
