#!/usr/bin/env python
#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

from hello_extension_action_point import HelloExtensionActionPoint

from opensearch_sdk_py.api.extension import Extension


class HelloExtension(Extension):
    def __init__(self) -> None:
        super().__init__([HelloExtensionActionPoint()])
