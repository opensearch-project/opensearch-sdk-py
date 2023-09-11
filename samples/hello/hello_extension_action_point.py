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

from opensearch_sdk_py.api.extension_points.action_extension_point import ActionExtensionPoint


class HelloExtensionActionPoint(ActionExtensionPoint):
    def __init__(self) -> None:
        super().__init__([HelloRestHandler()])
